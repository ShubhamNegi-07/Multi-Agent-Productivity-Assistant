"""
utils/agent_runtime.py
----------------------
Shared runtime for every agent: one result parser and one guarded invoke.

Each agent module used to carry its own near-identical copy of the response
parser. Centralising it means a change in Gemini's response shape is fixed
once rather than six times, and it gives a single place to turn the SDK's
opaque failures into something the chat thread can actually show a user.

Error contract — app.py renders a failed turn as an error bubble and relies
on exceptions to do it, so nothing here swallows a failure and returns a
string pretending to be an answer:

  * EnvironmentError propagates untouched (app.py has a dedicated branch for
    configuration problems like a missing API key).
  * Everything else is re-raised as RuntimeError carrying a readable,
    non-technical message.
"""

from typing import Any, Callable


# Substrings that identify a failure class in the exception's type name or
# message. Matching on text rather than importing google.api_core keeps this
# module working even if the provider SDK reorganises its exception tree,
# which it has done across major versions.
_ERROR_SIGNATURES: list[tuple[tuple[str, ...], str]] = [
    (
        ("api key not valid", "api_key_invalid", "permissiondenied", "unauthenticated", "401", "403"),
        "The Gemini API key was rejected. Check that GEMINI_API_KEY in your .env "
        "file is current and has the Generative Language API enabled.",
    ),
    (
        ("resourceexhausted", "quota", "rate limit", "429"),
        "Gemini is rate-limiting or the free-tier quota is used up. Wait a minute "
        "and try again.",
    ),
    (
        ("deadlineexceeded", "timeout", "timed out"),
        "The request to Gemini timed out. Check your connection and try again.",
    ),
    (
        ("connection", "network", "dns", "unreachable", "getaddrinfo", "ssl"),
        "Could not reach Gemini. Check your internet connection and try again.",
    ),
    (
        ("notfound", "404", "is not found for api version", "not supported for"),
        "The configured Gemini model is unavailable for this API key. Check the "
        "model name in utils/llm.py.",
    ),
    (
        ("safety", "blocked", "recitation"),
        "Gemini blocked that response under its safety filters. Try rephrasing "
        "the question.",
    ),
]


def describe_error(exc: Exception) -> str:
    """
    Map an exception to a readable, user-facing sentence.

    Falls back to the exception's own text when nothing matches, so an
    unrecognised failure still surfaces something diagnosable rather than a
    generic shrug.
    """
    haystack = f"{type(exc).__name__} {exc}".lower()

    for needles, message in _ERROR_SIGNATURES:
        if any(needle in haystack for needle in needles):
            return message

    detail = str(exc).strip() or type(exc).__name__
    # Long provider tracebacks make the chat bubble unreadable; the full error
    # is still on stderr for anyone running the app from a terminal.
    if len(detail) > 300:
        detail = detail[:297] + "..."
    return f"The agent could not complete that request. ({detail})"


def extract_text(result: Any) -> str:
    """
    Pull the last readable assistant message out of an agent result.

    Gemini returns content either as a plain string or as a list of typed
    parts, and a tool-calling turn can leave trailing messages whose content
    is empty. Walking backwards and skipping the empties lands on the actual
    answer in both shapes.
    """
    if not isinstance(result, dict):
        return "No response generated."

    messages = result.get("messages") or []
    if not messages:
        return "No response generated."

    for msg in reversed(messages):
        content = getattr(msg, "content", None)
        if content is None and isinstance(msg, dict):
            content = msg.get("content")

        if isinstance(content, str) and content.strip():
            return content.strip()

        if isinstance(content, list):
            text_parts: list[str] = []
            for item in content:
                if isinstance(item, dict):
                    if item.get("type") == "text" and item.get("text"):
                        text_parts.append(str(item["text"]))
                elif isinstance(item, str) and item.strip():
                    text_parts.append(item.strip())

            if text_parts:
                joined = "\n".join(text_parts).strip()
                if joined:
                    return joined

    return "No readable response generated."


def run_agent(build_agent: Callable[[], Any], query: str, label: str) -> str:
    """
    Build an agent, run one query through it, and return the answer text.

    Args:
        build_agent: Zero-argument factory returning a configured agent.
        query: The user's message.
        label: Human-readable agent name, used in error messages.

    Returns:
        The agent's reply as plain text.

    Raises:
        EnvironmentError: Configuration is missing (propagated untouched).
        RuntimeError: The agent could not produce a reply, with a readable
            explanation of why.
    """
    if not query or not query.strip():
        return "I did not receive a question. Ask me something and I'll help."

    try:
        agent = build_agent()
    except EnvironmentError:
        # Missing/blank API key — app.py reports configuration errors itself.
        raise
    except Exception as exc:
        raise RuntimeError(
            f"{label} could not start. {describe_error(exc)}"
        ) from exc

    try:
        result = agent.invoke({"messages": [{"role": "user", "content": query}]})
    except EnvironmentError:
        raise
    except Exception as exc:
        raise RuntimeError(f"{label} failed. {describe_error(exc)}") from exc

    return extract_text(result)

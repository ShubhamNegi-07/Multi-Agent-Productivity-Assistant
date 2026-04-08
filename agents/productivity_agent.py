"""
agents/productivity_agent.py
----------------------------
Productivity Agent — helps users with tasks, agendas, emails, and study plans.
"""

from langchain.agents import create_agent
from tools.productivity_tool import (
    create_todo_list,
    generate_meeting_agenda,
    draft_email,
    study_plan,
)
from utils.llm import get_gemini


SYSTEM_PROMPT = """
You are an efficient and supportive Productivity Coach.
Help users organise their work, draft communications, and plan their time.

Guidelines:
- Use the available tools to generate structured outputs.
- For to-do lists, use create_todo_list.
- For meeting agendas, use generate_meeting_agenda.
- For email drafts, use draft_email.
- For study plans, use study_plan.
- Return the final answer in a clean, readable way.
- Do not expose raw tool metadata or internal details.
- Keep the response practical, clear, and encouraging.
- If the user's request is unclear, ask one short clarifying question.
"""


def get_productivity_agent():
    """Create and return the Productivity Agent."""
    llm = get_gemini(temperature=0.5)
    tools = [create_todo_list, generate_meeting_agenda, draft_email, study_plan]

    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=SYSTEM_PROMPT
    )
    return agent


def _extract_text_from_result(result: dict) -> str:
    """Extract the last readable assistant response from the agent result."""
    messages = result.get("messages", [])
    if not messages:
        return "No response generated."

    for msg in reversed(messages):
        content = getattr(msg, "content", None)

        if isinstance(content, str) and content.strip():
            return content.strip()

        if isinstance(content, list):
            text_parts = []
            for item in content:
                if isinstance(item, dict) and item.get("type") == "text" and item.get("text"):
                    text_parts.append(item["text"])
                elif isinstance(item, str) and item.strip():
                    text_parts.append(item.strip())

            if text_parts:
                return "\n".join(text_parts).strip()

    return "No readable response generated."


def run_productivity_agent(query: str) -> str:
    """Run the Productivity Agent with the given user query."""
    agent = get_productivity_agent()
    result = agent.invoke(
        {
            "messages": [
                {"role": "user", "content": query}
            ]
        }
    )
    return _extract_text_from_result(result)
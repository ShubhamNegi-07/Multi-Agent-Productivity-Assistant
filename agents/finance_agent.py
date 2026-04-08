"""
agents/finance_agent.py
-----------------------
Finance Agent — handles EMI, interest, budgeting, and basic finance term explanations.
"""

from langchain.agents import create_agent
from tools.finance_tool import (
    calculate_emi,
    simple_interest,
    compound_interest,
    monthly_budget_split,
    explain_finance_term,
)
from utils.llm import get_gemini


SYSTEM_PROMPT = """
You are a helpful and friendly Financial Assistant.

Your job:
- Help users with EMI, simple interest, compound interest, budget split, and basic finance term explanations.

Rules:
- Always use the available tools for calculations and finance term explanations.
- Never do manual calculations on your own.
- Never show raw tool output exactly as it is.
- Convert tool results into a clean final response.

Output style:
- Write in a natural, easy-to-understand way.
- Start with a short paragraph that directly answers the user.
- Then give key values in bullet points where useful.
- Keep the answer neat and not too long.
- Avoid emoji-heavy formatting.
- For finance term explanations, give a short paragraph and, if useful, one simple real-world line.
- Never give investment or stock market advice.
"""


def get_finance_agent():
    """Create and return the Finance Agent."""
    llm = get_gemini(temperature=0.1)
    tools = [
        calculate_emi,
        simple_interest,
        compound_interest,
        monthly_budget_split,
        explain_finance_term,
    ]

    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=SYSTEM_PROMPT,
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
                if isinstance(item, dict):
                    if item.get("type") == "text" and item.get("text"):
                        text_parts.append(item["text"])
                elif isinstance(item, str) and item.strip():
                    text_parts.append(item.strip())

            if text_parts:
                return "\n".join(text_parts).strip()

    return "No readable response generated."


def run_finance_agent(query: str) -> str:
    """Run the Finance Agent with the given user query."""
    agent = get_finance_agent()
    result = agent.invoke(
        {
            "messages": [
                {"role": "user", "content": query}
            ]
        }
    )
    return _extract_text_from_result(result)
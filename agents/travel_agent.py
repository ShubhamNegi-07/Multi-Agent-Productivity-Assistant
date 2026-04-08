"""
agents/travel_agent.py
----------------------
Travel Agent — helps users plan trips, estimate budgets, and get travel advice.
"""

from langchain.agents import create_agent
from tools.travel_tool import (
    estimate_trip_budget,
    suggest_transport,
    travel_checklist,
    best_time_to_visit,
)
from utils.llm import get_gemini


SYSTEM_PROMPT = """
You are an expert Travel Planner for Indian destinations.
Help users plan enjoyable and budget-friendly trips.

Guidelines:
- Use the available tools to answer trip planning questions.
- Be warm, enthusiastic, and practical in your responses.
- When asked about budget, call the budget tool.
- When asked about transport, call the transport tool.
- When asked for a checklist, call the checklist tool.
- When asked about the best time to visit, call the seasonal advice tool.
- Never expose raw tool output, internal metadata, signatures, or extras.
- Always give a clean final answer in normal readable text.
- If needed, combine tool results into a well-structured response.
- Always encourage safe and responsible travel.
"""


def get_travel_agent():
    """Create and return the Travel Agent."""
    llm = get_gemini(temperature=0.4)
    tools = [
        estimate_trip_budget,
        suggest_transport,
        travel_checklist,
        best_time_to_visit,
    ]

    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=SYSTEM_PROMPT,
    )
    return agent


def _extract_text_from_result(result: dict) -> str:
    """Extract the last clean readable text response from agent result."""
    messages = result.get("messages", [])
    if not messages:
        return "⚠️ No response generated."

    for msg in reversed(messages):
        content = getattr(msg, "content", None)

        if isinstance(content, str) and content.strip():
            return content

        if isinstance(content, list):
            text_parts = []
            for item in content:
                if isinstance(item, dict):
                    if item.get("type") == "text" and item.get("text"):
                        text_parts.append(item["text"])
                elif isinstance(item, str) and item.strip():
                    text_parts.append(item)

            if text_parts:
                return "\n".join(text_parts).strip()

    return "⚠️ No readable response generated."


def run_travel_agent(query: str) -> str:
    """Run the Travel Agent with the given user query."""
    agent = get_travel_agent()
    result = agent.invoke(
        {
            "messages": [
                {"role": "user", "content": query}
            ]
        }
    )
    return _extract_text_from_result(result)
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
from utils.agent_runtime import run_agent
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


def run_travel_agent(query: str) -> str:
    """Run the Travel Agent with the given user query."""
    return run_agent(get_travel_agent, query, "Travel Agent")

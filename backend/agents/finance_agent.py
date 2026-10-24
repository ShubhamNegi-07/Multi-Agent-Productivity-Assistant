from langchain.agents import create_agent

from backend.tools.finance_tool import (
    calculate_emi,
    compound_interest,
    explain_finance_term,
    monthly_budget_split,
    simple_interest,
)
from backend.utils.agent_runtime import run_agent
from backend.utils.llm import get_gemini


SYSTEM_PROMPT = """
You are a careful personal finance assistant. Use the available tools for
calculations, show assumptions, and explain results plainly. Do not present
your guidance as regulated financial advice.
"""


def get_finance_agent():
    return create_agent(
        model=get_gemini(temperature=0.3),
        tools=[
            calculate_emi,
            simple_interest,
            compound_interest,
            monthly_budget_split,
            explain_finance_term,
        ],
        system_prompt=SYSTEM_PROMPT,
    )


def run_finance_agent(query: str) -> str:
    return run_agent(get_finance_agent, query, "Finance Agent")

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
from utils.agent_runtime import run_agent
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


def run_productivity_agent(query: str) -> str:
    """Run the Productivity Agent with the given user query."""
    return run_agent(get_productivity_agent, query, "Productivity Agent")

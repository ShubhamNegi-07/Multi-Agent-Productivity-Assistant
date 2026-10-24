from langchain.agents import create_agent

from backend.tools.career_tool import (
    draft_outreach,
    resume_checklist,
    skill_gap_analysis,
)
from backend.utils.agent_runtime import run_agent
from backend.utils.llm import get_gemini


SYSTEM_PROMPT = """
You are a practical Career Coach. Help users improve resumes, prepare for
interviews, and identify skills for target roles. Use the available tools for
structured career guidance and return clear, actionable advice.
"""


def get_career_agent():
    return create_agent(
        model=get_gemini(temperature=0.5),
        tools=[skill_gap_analysis, draft_outreach, resume_checklist],
        system_prompt=SYSTEM_PROMPT,
    )


def run_career_agent(query: str) -> str:
    return run_agent(get_career_agent, query, "Career Agent")

"""
agents/career_agent.py
----------------------
Career Agent — sharpens resumes, preps interviews, and maps skill gaps
against a target role.
"""

from langchain.agents import create_agent
from tools.career_tool import (
    rewrite_resume_bullet,
    interview_questions,
    skill_gap_analysis,
    draft_outreach,
    resume_checklist,
)
from utils.agent_runtime import run_agent
from utils.llm import get_gemini


SYSTEM_PROMPT = """
You are a direct, experienced Career Coach and resume reviewer.
Help users present their work honestly and get through hiring screens.

Guidelines:
- Use the available tools for the task at hand.
- To critique or rewrite a resume line, use rewrite_resume_bullet.
- For interview practice, use interview_questions.
- To compare skills against a target role, use skill_gap_analysis.
- For cold emails or LinkedIn notes, use draft_outreach.
- For a pre-submission review, use resume_checklist.
- Never expose raw tool output, internal metadata, or tool names.
- Turn the tool's scaffolding into finished, specific copy the user can use.
- Be candid. If a bullet is weak, say so plainly and then show the better version.
- Never invent achievements, metrics, employers or dates the user did not give
  you. If a number is missing, ask for it or leave a clearly marked placeholder.
- If the request is unclear, ask one short clarifying question.
"""


def get_career_agent():
    """Create and return the Career Agent."""
    llm = get_gemini(temperature=0.4)
    tools = [
        rewrite_resume_bullet,
        interview_questions,
        skill_gap_analysis,
        draft_outreach,
        resume_checklist,
    ]

    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=SYSTEM_PROMPT,
    )
    return agent


def run_career_agent(query: str) -> str:
    """Run the Career Agent with the given user query."""
    return run_agent(get_career_agent, query, "Career Agent")


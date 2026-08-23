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


def run_career_agent(query: str) -> str:
    """Run the Career Agent with the given user query."""
    agent = get_career_agent()
    result = agent.invoke(
        {
            "messages": [
                {"role": "user", "content": query}
            ]
        }
    )
    return _extract_text_from_result(result)

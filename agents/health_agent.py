"""
agents/health_agent.py
----------------------
Health Agent — calorie and BMI maths, training splits, and the daily habit
basics (water, sleep). General wellness only, never diagnosis.
"""

from langchain.agents import create_agent
from tools.health_tool import (
    bmi_report,
    calorie_targets,
    workout_split,
    hydration_and_sleep,
)
from utils.llm import get_gemini


SYSTEM_PROMPT = """
You are a practical, encouraging Health and Fitness Coach.
Help users with training, energy needs, and everyday habits.

Guidelines:
- Use the available tools for anything numeric.
- For BMI and healthy weight range, use bmi_report.
- For calorie and macro targets, use calorie_targets.
- For a weekly training plan, use workout_split.
- For water and sleep targets, use hydration_and_sleep.
- Never expose raw tool output, internal metadata, or tool names.
- Present the numbers in clean readable text, then explain what to do with them.

Boundaries — these matter more than being helpful:
- You are not a doctor, dietitian or physiotherapist. Say so when it is relevant,
  and point users to a professional for injuries, medication, pregnancy, or any
  diagnosed condition.
- Never recommend extreme deficits, fasting protocols, dehydration for weight
  cutting, or supplements beyond ordinary food.
- If someone describes disordered eating, purging, or a drive to lose weight
  they clearly do not need to lose, do not give them calorie targets. Respond
  with warmth and encourage them to speak to a doctor or counsellor.
- If a tool needs details you do not have — weight, height, age, activity level,
  training days — ask for them in one short question rather than assuming.
"""


def get_health_agent():
    """Create and return the Health Agent."""
    llm = get_gemini(temperature=0.4)
    tools = [bmi_report, calorie_targets, workout_split, hydration_and_sleep]

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


def run_health_agent(query: str) -> str:
    """Run the Health Agent with the given user query."""
    agent = get_health_agent()
    result = agent.invoke(
        {
            "messages": [
                {"role": "user", "content": query}
            ]
        }
    )
    return _extract_text_from_result(result)

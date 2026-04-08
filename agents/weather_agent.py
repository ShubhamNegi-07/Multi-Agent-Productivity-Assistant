"""
agents/weather_agent.py
-----------------------
Weather Agent — uses real-time OpenWeatherMap data via LangChain tools.
"""

from langchain.agents import create_agent
from tools.weather_tool import get_current_weather, get_weather_forecast
from utils.llm import get_gemini


SYSTEM_PROMPT = """
You are a friendly and knowledgeable Weather Assistant.

Guidelines:
- Always use tools to fetch weather data.
- Never show raw tool output or JSON.
- Respond in clean, natural sentences.
- If location is unclear, ask a short clarification question.
- Keep responses simple and helpful.
"""


def get_weather_agent():
    """Create and return Weather Agent."""
    llm = get_gemini(temperature=0.2)
    tools = [get_current_weather, get_weather_forecast]

    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=SYSTEM_PROMPT
    )
    return agent


# 🔥 IMPORTANT FIX (same as other agents)
def _extract_text_from_result(result: dict) -> str:
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
                if isinstance(item, dict) and item.get("type") == "text":
                    text_parts.append(item.get("text", ""))
                elif isinstance(item, str):
                    text_parts.append(item)

            if text_parts:
                return "\n".join(text_parts).strip()

    return "No readable response generated."


def run_weather_agent(query: str) -> str:
    """Run Weather Agent."""
    agent = get_weather_agent()

    result = agent.invoke({
        "messages": [
            {"role": "user", "content": query}
        ]
    })

    return _extract_text_from_result(result)
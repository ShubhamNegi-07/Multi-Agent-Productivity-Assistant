"""
agents/weather_agent.py
-----------------------
Weather Agent — uses real-time OpenWeatherMap data via LangChain tools.
"""

from langchain.agents import create_agent
from tools.weather_tool import get_current_weather, get_weather_forecast
from utils.agent_runtime import run_agent
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


def run_weather_agent(query: str) -> str:
    """Run Weather Agent."""
    return run_agent(get_weather_agent, query, "Weather Agent")

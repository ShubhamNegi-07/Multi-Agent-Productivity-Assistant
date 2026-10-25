"""
tools/weather_tool.py
---------------------
Real-time weather tool using the OpenWeatherMap API.
Decorated with @tool so LangChain agents can invoke it automatically.
"""

import os
from pathlib import Path

import requests
from dotenv import load_dotenv
from langchain.tools import tool

load_dotenv(Path(__file__).resolve().parents[2] / ".env")
BASE_URL = "https://api.openweathermap.org/data/2.5"
WEATHER_TIMEOUT_SECONDS = 10


def _weather_api_key() -> str | None:
    return os.getenv("OPENWEATHER_API_KEY")


def _weather_network_error() -> str:
    return "Weather data is temporarily unavailable. Please try again later."


@tool
def get_current_weather(city: str) -> str:
    """
    Fetch real-time weather for the given city.
    Returns temperature, feels-like, humidity, wind speed, and condition.

    Args:
        city: Name of the city (e.g., 'Dehradun', 'Mumbai').
    """
    api_key = _weather_api_key()
    if not api_key:
        return "âŒ OPENWEATHER_API_KEY is missing in .env file."

    try:
        response = requests.get(
            f"{BASE_URL}/weather",
            params={"q": city, "appid": api_key, "units": "metric"},
            timeout=WEATHER_TIMEOUT_SECONDS,
        )

        if response.status_code != 200:
            return "Weather data could not be found for that location."

        data = response.json()

        weather_desc  = data["weather"][0]["description"].capitalize()
        temp          = data["main"]["temp"]
        feels_like    = data["main"]["feels_like"]
        humidity      = data["main"]["humidity"]
        wind_speed    = data["wind"]["speed"]
        country       = data["sys"]["country"]

        return (
            f"ðŸŒ¤ï¸  **Weather in {city.title()}, {country}**\n"
            f"â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”\n"
            f"ðŸŒ¡ï¸  Temperature  : {temp}Â°C\n"
            f"ðŸ¤”  Feels Like   : {feels_like}Â°C\n"
            f"ðŸ’§  Humidity     : {humidity}%\n"
            f"ðŸ’¨  Wind Speed   : {wind_speed} m/s\n"
            f"ðŸŒˆ  Condition    : {weather_desc}"
        )

    except requests.exceptions.RequestException:
        return _weather_network_error()
    except (AttributeError, KeyError, IndexError, TypeError, ValueError):
        return "Weather data was incomplete. Please try again later."


@tool
def get_weather_forecast(city: str) -> str:
    """
    Fetch a 3-day weather forecast (every 24 hours) for the given city.

    Args:
        city: Name of the city (e.g., 'Delhi', 'Mumbai').
    """
    api_key = _weather_api_key()
    if not api_key:
        return "âŒ OPENWEATHER_API_KEY is missing in .env file."

    try:
        response = requests.get(
            f"{BASE_URL}/forecast",
            params={
                "q": city,
                "appid": api_key,
                "units": "metric",
                "cnt": 24,
            },
            timeout=WEATHER_TIMEOUT_SECONDS,
        )

        if response.status_code != 200:
            return "Forecast data could not be found for that location."

        data = response.json()

        lines = [f"ðŸ“…  **3-Day Forecast for {city.title()}**\n{'â”'*34}"]
        for item in data["list"][::8][:3]:
            dt_txt    = item["dt_txt"]
            temp      = item["main"]["temp"]
            condition = item["weather"][0]["description"].capitalize()
            lines.append(f"ðŸ•  {dt_txt}  |  {temp}Â°C  |  {condition}")

        return "\n".join(lines)

    except requests.exceptions.RequestException:
        return _weather_network_error()
    except (AttributeError, KeyError, IndexError, TypeError, ValueError):
        return "Forecast data was incomplete. Please try again later."

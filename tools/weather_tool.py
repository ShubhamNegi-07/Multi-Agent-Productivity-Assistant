"""
tools/weather_tool.py
---------------------
Real-time weather tool using the OpenWeatherMap API.
Decorated with @tool so LangChain agents can invoke it automatically.
"""

import os
import requests
from langchain.tools import tool
from dotenv import load_dotenv

load_dotenv()

WEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5"


@tool
def get_current_weather(city: str) -> str:
    """
    Fetch real-time weather for the given city.
    Returns temperature, feels-like, humidity, wind speed, and condition.

    Args:
        city: Name of the city (e.g., 'Hyderabad', 'Chennai').
    """
    if not WEATHER_API_KEY:
        return "❌ OPENWEATHER_API_KEY is missing in .env file."

    try:
        url = f"{BASE_URL}/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
        response = requests.get(url, timeout=10)
        data = response.json()

        if response.status_code != 200:
            return f"❌ Could not fetch weather for '{city}'. Reason: {data.get('message', 'Unknown error')}."

        weather_desc  = data["weather"][0]["description"].capitalize()
        temp          = data["main"]["temp"]
        feels_like    = data["main"]["feels_like"]
        humidity      = data["main"]["humidity"]
        wind_speed    = data["wind"]["speed"]
        country       = data["sys"]["country"]

        return (
            f"🌤️  **Weather in {city.title()}, {country}**\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🌡️  Temperature  : {temp}°C\n"
            f"🤔  Feels Like   : {feels_like}°C\n"
            f"💧  Humidity     : {humidity}%\n"
            f"💨  Wind Speed   : {wind_speed} m/s\n"
            f"🌈  Condition    : {weather_desc}"
        )

    except requests.exceptions.ConnectionError:
        return "❌ Network error. Please check your internet connection."
    except Exception as exc:
        return f"❌ Unexpected error: {str(exc)}"


@tool
def get_weather_forecast(city: str) -> str:
    """
    Fetch a 3-day weather forecast (every 24 hours) for the given city.

    Args:
        city: Name of the city (e.g., 'Delhi', 'Mumbai').
    """
    if not WEATHER_API_KEY:
        return "❌ OPENWEATHER_API_KEY is missing in .env file."

    try:
        url = f"{BASE_URL}/forecast?q={city}&appid={WEATHER_API_KEY}&units=metric&cnt=3"
        response = requests.get(url, timeout=10)
        data = response.json()

        if response.status_code != 200:
            return f"❌ Could not fetch forecast for '{city}'. Reason: {data.get('message', 'Unknown error')}."

        lines = [f"📅  **3-Day Forecast for {city.title()}**\n{'━'*34}"]
        for item in data["list"]:
            dt_txt    = item["dt_txt"]
            temp      = item["main"]["temp"]
            condition = item["weather"][0]["description"].capitalize()
            lines.append(f"🕐  {dt_txt}  |  {temp}°C  |  {condition}")

        return "\n".join(lines)

    except Exception as exc:
        return f"❌ Error fetching forecast: {str(exc)}"

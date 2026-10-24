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
        city: Name of the city (e.g., 'Dehradun', 'Mumbai').
    """
    if not WEATHER_API_KEY:
        return "âŒ OPENWEATHER_API_KEY is missing in .env file."

    try:
        url = f"{BASE_URL}/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
        response = requests.get(url, timeout=10)
        data = response.json()

        if response.status_code != 200:
            return f"âŒ Could not fetch weather for '{city}'. Reason: {data.get('message', 'Unknown error')}."

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

    except requests.exceptions.ConnectionError:
        return "âŒ Network error. Please check your internet connection."
    except Exception as exc:
        return f"âŒ Unexpected error: {str(exc)}"


@tool
def get_weather_forecast(city: str) -> str:
    """
    Fetch a 3-day weather forecast (every 24 hours) for the given city.

    Args:
        city: Name of the city (e.g., 'Delhi', 'Mumbai').
    """
    if not WEATHER_API_KEY:
        return "âŒ OPENWEATHER_API_KEY is missing in .env file."

    try:
        url = f"{BASE_URL}/forecast?q={city}&appid={WEATHER_API_KEY}&units=metric&cnt=24"
        response = requests.get(url, timeout=10)
        data = response.json()

        if response.status_code != 200:
            return f"âŒ Could not fetch forecast for '{city}'. Reason: {data.get('message', 'Unknown error')}."

        lines = [f"ðŸ“…  **3-Day Forecast for {city.title()}**\n{'â”'*34}"]
        for item in data["list"][::8][:3]:
            dt_txt    = item["dt_txt"]
            temp      = item["main"]["temp"]
            condition = item["weather"][0]["description"].capitalize()
            lines.append(f"ðŸ•  {dt_txt}  |  {temp}Â°C  |  {condition}")

        return "\n".join(lines)

    except Exception as exc:
        return f"âŒ Error fetching forecast: {str(exc)}"

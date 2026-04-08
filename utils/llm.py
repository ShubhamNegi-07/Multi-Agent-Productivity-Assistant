"""
utils/llm.py
------------
Centralized LLM initialization for the Multi-Agent Assistant.
Loads the Gemini model once and returns it to any agent that needs it.
"""

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()


def get_gemini(temperature: float = 0.3) -> ChatGoogleGenerativeAI:
    """
    Initialize and return a Gemini LLM instance.

    Args:
        temperature: Controls response creativity (0 = deterministic, 1 = creative).

    Returns:
        A configured ChatGoogleGenerativeAI instance.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "GEMINI_API_KEY is not set. Please add it to your .env file."
        )

    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=api_key,
        temperature=temperature,
        convert_system_message_to_human=True,
    )

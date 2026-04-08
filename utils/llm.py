import os
import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# Load .env only if it exists (for local development)
load_dotenv()

def get_gemini(temperature: float = 0.3) -> ChatGoogleGenerativeAI:
    """
    Initialize and return a Gemini LLM instance using Streamlit secrets 
    or environment variables.
    """
    # 1. Try to get the key from Streamlit Secrets (Cloud)
    # 2. Fallback to os.getenv (Local .env)
    api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise EnvironmentError(
            "GEMINI_API_KEY is not set. If running locally, check your .env file. "
            "If deployed, add it to the Streamlit Cloud Secrets dashboard."
        )

    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash", # Note: Ensure this model name is correct for your region
        google_api_key=api_key,
        temperature=temperature,
        convert_system_message_to_human=True,
    )
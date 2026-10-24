from langchain.agents import create_agent

from backend.tools.recipe_tool import (
    convert_kitchen_measure,
    cooking_times,
    meal_ideas_from_ingredients,
    scale_recipe,
    shopping_list,
)
from backend.utils.agent_runtime import run_agent
from backend.utils.llm import get_gemini


SYSTEM_PROMPT = """
You are a helpful cooking assistant. Help users scale recipes, convert
kitchen measurements, plan meals, and estimate cooking times. Ask for missing
ingredients or serving information rather than inventing quantities.
"""


def get_recipe_agent():
    return create_agent(
        model=get_gemini(temperature=0.5),
        tools=[
            scale_recipe,
            convert_kitchen_measure,
            meal_ideas_from_ingredients,
            cooking_times,
            shopping_list,
        ],
        system_prompt=SYSTEM_PROMPT,
    )


def run_recipe_agent(query: str) -> str:
    return run_agent(get_recipe_agent, query, "Recipe Agent")

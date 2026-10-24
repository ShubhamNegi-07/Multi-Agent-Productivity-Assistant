import re

from langchain.tools import tool


def _parse_quantity(value: str) -> tuple[float | None, str]:
    match = re.match(r"^\s*(\d+(?:\.\d+)?)\s*(.*)$", value)
    if not match:
        return None, value.strip()
    return float(match.group(1)), match.group(2).strip()


@tool
def scale_recipe(ingredients: str, original_servings: int, target_servings: int) -> str:
    """Scale newline-separated recipe ingredients to a new serving count."""
    if original_servings <= 0 or target_servings <= 0:
        return "Serving counts must be greater than zero."
    factor = target_servings / original_servings
    scaled: list[str] = []
    for line in ingredients.splitlines():
        quantity, remainder = _parse_quantity(line)
        if quantity is None:
            scaled.append(line.strip())
        else:
            scaled.append(f"{quantity * factor:g} {remainder}".strip())
    return "\n".join(scaled) or "Please provide ingredients."


@tool
def convert_kitchen_measure(amount: float, unit: str, target_unit: str) -> str:
    """Convert common cup, tablespoon, teaspoon, and millilitre measures."""
    units = {"tsp": 1, "tbsp": 3, "cup": 48, "ml": 0.202884}
    source = unit.strip().lower()
    target = target_unit.strip().lower()
    if source not in units or target not in units:
        return "Supported units: tsp, tbsp, cup, and ml."
    result = amount * units[source] / units[target]
    return f"{amount:g} {source} is approximately {result:g} {target}."


@tool
def meal_ideas_from_ingredients(ingredients: str) -> str:
    """Suggest simple meal formats from a comma-separated ingredient list."""
    items = [item.strip() for item in ingredients.split(",") if item.strip()]
    return f"Try a stir-fry, grain bowl, or soup using: {', '.join(items)}." if items else "Please provide ingredients."


@tool
def cooking_times(ingredient: str, method: str) -> str:
    """Give a conservative starting point for common cooking methods."""
    return f"Cook {ingredient.strip()} by {method.strip()} and check for tenderness before serving."


@tool
def shopping_list(recipe: str) -> str:
    """Turn newline-separated recipe items into a shopping checklist."""
    items = [item.strip("- *\t") for item in recipe.splitlines() if item.strip()]
    return "\n".join(f"- {item}" for item in items) or "Please provide recipe ingredients."

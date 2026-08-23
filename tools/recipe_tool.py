"""
tools/recipe_tool.py
--------------------
Kitchen tools for the Recipe Agent.

Everything here is offline arithmetic and lookup tables: ingredient scaling,
volume-to-weight conversion (which is ingredient-specific, so it needs a
density table rather than a single factor), cooking-time references and
shopping-list aggregation.
"""

import re
from fractions import Fraction

from langchain.tools import tool


BAR = "━" * 46

# Grams per US cup. Volume→weight is *not* a single conversion: a cup of flour
# and a cup of sugar differ by ~80 g, which is the difference between a cake
# and a brick. Anything not listed falls back to water and says so.
CUP_GRAMS = {
    "water": 240, "milk": 240, "buttermilk": 240, "yogurt": 245, "curd": 245,
    "oil": 218, "ghee": 205, "butter": 227, "honey": 340, "maple syrup": 322,
    "flour": 120, "maida": 120, "wheat flour": 120, "atta": 120,
    "bread flour": 127, "almond flour": 96, "cornstarch": 128, "cornflour": 128,
    "besan": 92, "gram flour": 92, "semolina": 167, "suji": 167, "rava": 167,
    "sugar": 200, "brown sugar": 213, "powdered sugar": 120, "jaggery": 200,
    "rice": 185, "basmati rice": 185, "cooked rice": 158,
    "oats": 90, "rolled oats": 90, "poha": 60,
    "lentils": 192, "dal": 192, "toor dal": 192, "moong dal": 196,
    "chana dal": 200, "chickpeas": 200, "kidney beans": 184, "rajma": 184,
    "cocoa powder": 85, "coconut": 80, "desiccated coconut": 80,
    "cheese": 113, "grated cheese": 113, "paneer": 226,
    "breadcrumbs": 108, "nuts": 140, "almonds": 143, "cashews": 137,
    "peanuts": 146, "raisins": 165, "chocolate chips": 170,
    "salt": 288, "table salt": 288,
}

# Teaspoon-based units, in millilitres.
VOLUME_ML = {
    "tsp": 4.93, "teaspoon": 4.93,
    "tbsp": 14.79, "tablespoon": 14.79,
    "cup": 236.59, "cups": 236.59,
    "ml": 1.0, "millilitre": 1.0, "milliliter": 1.0,
    "l": 1000.0, "litre": 1000.0, "liter": 1000.0,
    "fl oz": 29.57, "floz": 29.57,
    "pint": 473.18, "quart": 946.35,
}

WEIGHT_G = {
    "g": 1.0, "gram": 1.0, "grams": 1.0,
    "kg": 1000.0, "kilogram": 1000.0,
    "oz": 28.35, "ounce": 28.35,
    "lb": 453.59, "pound": 453.59,
}

# Fractions cooks actually use. Scaled quantities snap to the nearest one so
# the output reads like a recipe instead of "0.5833 cups".
NICE_FRACTIONS = [
    Fraction(1, 8), Fraction(1, 4), Fraction(1, 3), Fraction(1, 2),
    Fraction(2, 3), Fraction(3, 4),
]

# Curated dish catalogue: dish → (cuisine, meal types, ingredient set, minutes).
# Matching is by ingredient overlap, so the sets are the important part.
DISHES = {
    "Masala omelette": ("Indian", {"breakfast"}, {"egg", "onion", "tomato", "chilli", "oil"}, 10),
    "Scrambled eggs on toast": ("Global", {"breakfast"}, {"egg", "butter", "bread", "milk"}, 10),
    "Poha": ("Indian", {"breakfast"}, {"poha", "onion", "potato", "peanut", "mustard seed"}, 20),
    "Upma": ("Indian", {"breakfast"}, {"semolina", "onion", "chilli", "mustard seed", "oil"}, 20),
    "Vegetable pulao": ("Indian", {"lunch", "dinner"}, {"rice", "onion", "carrot", "peas", "spices"}, 35),
    "Jeera rice": ("Indian", {"lunch", "dinner"}, {"rice", "cumin", "ghee"}, 25),
    "Dal tadka": ("Indian", {"lunch", "dinner"}, {"dal", "onion", "tomato", "garlic", "ghee"}, 35),
    "Rajma masala": ("Indian", {"lunch", "dinner"}, {"rajma", "onion", "tomato", "ginger", "garlic"}, 45),
    "Chana masala": ("Indian", {"lunch", "dinner"}, {"chickpeas", "onion", "tomato", "spices"}, 40),
    "Paneer bhurji": ("Indian", {"lunch", "dinner"}, {"paneer", "onion", "tomato", "chilli"}, 20),
    "Palak paneer": ("Indian", {"lunch", "dinner"}, {"paneer", "spinach", "onion", "garlic", "cream"}, 35),
    "Aloo gobi": ("Indian", {"lunch", "dinner"}, {"potato", "cauliflower", "onion", "turmeric"}, 30),
    "Chicken curry": ("Indian", {"lunch", "dinner"}, {"chicken", "onion", "tomato", "ginger", "garlic", "spices"}, 45),
    "Egg curry": ("Indian", {"lunch", "dinner"}, {"egg", "onion", "tomato", "spices"}, 30),
    "Veg fried rice": ("Asian", {"lunch", "dinner"}, {"rice", "carrot", "cabbage", "soy sauce", "spring onion"}, 20),
    "Hakka noodles": ("Asian", {"lunch", "dinner"}, {"noodles", "cabbage", "carrot", "soy sauce", "capsicum"}, 25),
    "Fried rice with egg": ("Asian", {"lunch", "dinner"}, {"rice", "egg", "soy sauce", "spring onion", "oil"}, 20),
    "Pasta in tomato sauce": ("Italian", {"lunch", "dinner"}, {"pasta", "tomato", "garlic", "olive oil", "basil"}, 25),
    "Pasta aglio e olio": ("Italian", {"lunch", "dinner"}, {"pasta", "garlic", "olive oil", "chilli"}, 15),
    "Mac and cheese": ("Global", {"lunch", "dinner"}, {"pasta", "cheese", "milk", "butter", "flour"}, 30),
    "Grilled cheese sandwich": ("Global", {"snack", "lunch"}, {"bread", "cheese", "butter"}, 10),
    "Veg sandwich": ("Global", {"snack", "breakfast"}, {"bread", "tomato", "cucumber", "butter", "onion"}, 10),
    "Besan chilla": ("Indian", {"breakfast", "snack"}, {"besan", "onion", "tomato", "chilli"}, 15),
    "Pakora": ("Indian", {"snack"}, {"besan", "onion", "potato", "oil", "chilli"}, 25),
    "Maggi upgrade": ("Indian", {"snack"}, {"noodles", "onion", "tomato", "egg", "peas"}, 12),
    "Tomato soup": ("Global", {"snack", "dinner"}, {"tomato", "onion", "garlic", "butter", "cream"}, 30),
    "Kadhi": ("Indian", {"lunch", "dinner"}, {"besan", "curd", "turmeric", "mustard seed"}, 35),
    "Curd rice": ("Indian", {"lunch"}, {"rice", "curd", "mustard seed", "curry leaves"}, 15),
    "Khichdi": ("Indian", {"lunch", "dinner"}, {"rice", "dal", "turmeric", "ghee", "cumin"}, 30),
    "Banana pancakes": ("Global", {"breakfast"}, {"banana", "egg", "flour", "milk", "butter"}, 20),
    "Fruit and yogurt bowl": ("Global", {"breakfast", "snack"}, {"yogurt", "banana", "honey", "oats", "nuts"}, 5),
    "Overnight oats": ("Global", {"breakfast"}, {"oats", "milk", "honey", "banana"}, 5),
    "Chicken fried rice": ("Asian", {"lunch", "dinner"}, {"rice", "chicken", "soy sauce", "carrot", "egg"}, 30),
    "Grilled chicken salad": ("Global", {"lunch", "dinner"}, {"chicken", "lettuce", "cucumber", "tomato", "olive oil"}, 25),
    "Tandoori paneer tikka": ("Indian", {"snack", "dinner"}, {"paneer", "curd", "capsicum", "onion", "spices"}, 40),
}

# Cooking-time reference. item → (method, time, doneness cue).
COOK_TIMES = {
    "rice": [("Stovetop, 1:2 rice to water", "12–15 min simmer + 10 min rest", "Grains separate, no bite in the centre"),
             ("Pressure cooker", "2 whistles, then rest off heat", "Steam released naturally, grains fluffy")],
    "basmati rice": [("Soak 20 min, 1:1.5 water", "10–12 min simmer + 10 min rest", "Long separate grains, fully elongated")],
    "toor dal": [("Pressure cooker, 1:3 dal to water", "3–4 whistles (~12 min)", "Mashes with light pressure from a spoon")],
    "moong dal": [("Pressure cooker, 1:2.5", "2 whistles (~8 min)", "Soft and creamy, holds no shape")],
    "rajma": [("Soak 8 h, pressure cooker", "6–8 whistles (~25 min)", "Skin slips off, centre creamy not chalky")],
    "chickpeas": [("Soak 8 h, pressure cooker", "5–6 whistles (~20 min)", "Squashes flat between two fingers")],
    "pasta": [("Boiling salted water", "8–11 min (check the box, then taste 1 min early)", "Al dente: firm centre, no white core")],
    "eggs": [("Boiling water, soft", "6 min", "Runny yolk, set white"),
             ("Boiling water, jammy", "8 min", "Fudgy centre"),
             ("Boiling water, hard", "10–12 min", "Fully set, no grey ring if cooled fast")],
    "potatoes": [("Boiling, whole medium", "18–22 min", "Knife slides in with no resistance"),
                 ("Oven roast at 200°C", "35–45 min", "Crisp outside, fluffy inside")],
    "chicken breast": [("Pan, medium heat", "6–7 min per side", "74°C internal, juices run clear")],
    "chicken thigh": [("Pan or oven at 200°C", "25–30 min", "75°C internal, meat pulls from bone")],
    "chicken curry": [("Simmer after searing", "25–35 min", "Meat shreds under a fork, oil separates at the edge")],
    "paneer": [("Pan-fry", "2 min per side", "Golden edges — longer turns it rubbery")],
    "roti": [("Dry tawa, high heat", "45–60 s per side, then puff on flame", "Brown speckles, fully puffed")],
    "vegetables": [("Stir-fry, high heat", "4–6 min", "Bright colour, still snaps when bent")],
    "cauliflower": [("Roast at 220°C", "22–28 min", "Charred edges, tender stem")],
    "spinach": [("Wilt in a hot pan", "2–3 min", "Collapsed and dark, no raw squeak")],
    "onion": [("Sauté for a curry base", "8–10 min", "Deep golden — pale onion means a raw-tasting gravy")],
}


def _parse_qty(text: str) -> tuple[float, str]:
    """
    Pull a leading quantity off an ingredient line.

    Handles '2', '0.5', '1/2' and mixed numbers like '1 1/2', because recipes
    are written all three ways and a plain float() chokes on the last two.
    Returns (quantity, remainder). Quantity is 0.0 when the line has no
    number at all ('salt to taste'), which callers treat as unscalable.
    """
    s = text.strip()
    m = re.match(r"^(\d+)\s+(\d+)\s*/\s*(\d+)\s*(.*)$", s)
    if m:  # mixed number: 1 1/2
        whole, num, den, rest = m.groups()
        if int(den) != 0:
            return int(whole) + int(num) / int(den), rest.strip()
    m = re.match(r"^(\d+)\s*/\s*(\d+)\s*(.*)$", s)
    if m:  # bare fraction: 1/2
        num, den, rest = m.groups()
        if int(den) != 0:
            return int(num) / int(den), rest.strip()
    m = re.match(r"^(\d+(?:\.\d+)?)\s*(.*)$", s)
    if m:
        return float(m.group(1)), m.group(2).strip()
    return 0.0, s


def _fmt_qty(value: float) -> str:
    """
    Render a scaled quantity the way a recipe would write it.

    Below 10 it snaps to the nearest cook-friendly fraction (⅛ through ¾)
    because '0.583 cup' is not an instruction anyone can follow. Above 10 the
    fractions stop being useful, so it rounds to whole numbers.
    """
    if value <= 0:
        return ""
    if value >= 10:
        return f"{value:.0f}"

    whole = int(value)
    frac = value - whole
    if frac < 0.06:
        return f"{whole}" if whole else "0"

    best = min(NICE_FRACTIONS, key=lambda f: abs(float(f) - frac))
    if abs(float(best) - frac) > 0.07:
        # Not close to anything cooks measure — one decimal is more honest.
        return f"{value:.1f}"
    if float(best) == 1.0:
        return f"{whole + 1}"
    return f"{whole} {best.numerator}/{best.denominator}" if whole else f"{best.numerator}/{best.denominator}"


def _cup_grams(ingredient: str) -> tuple[float, bool]:
    """Grams per cup for an ingredient. Second value is False when guessed."""
    ing = ingredient.strip().lower()
    if not ing:
        return CUP_GRAMS["water"], False
    # Longest key first so 'brown sugar' beats 'sugar' and 'wheat flour'
    # beats 'flour'.
    for key in sorted(CUP_GRAMS, key=len, reverse=True):
        if key in ing:
            return CUP_GRAMS[key], True
    return CUP_GRAMS["water"], False


@tool
def scale_recipe(ingredients: str, from_servings: int, to_servings: int) -> str:
    """
    Rescale a list of ingredients from one serving count to another.

    Args:
        ingredients: Ingredient lines, newline or comma separated
            (e.g. '200 g flour, 2 eggs, 1/2 tsp salt').
        from_servings: Servings the original recipe makes (e.g., 4).
        to_servings: Servings you want (e.g., 6).
    """
    if from_servings <= 0 or to_servings <= 0:
        return "⚠️  Both serving counts must be positive whole numbers."
    if not ingredients.strip():
        return "⚠️  Give me the ingredient list to scale."

    factor = to_servings / from_servings
    raw = [p.strip() for p in re.split(r"[\n,;]+", ingredients) if p.strip()]

    scaled, unscalable = [], []
    for line in raw:
        qty, rest = _parse_qty(line)
        if qty == 0.0:
            unscalable.append(rest or line)
        else:
            scaled.append(f"{_fmt_qty(qty * factor)} {rest}".strip())

    lines = [
        f"🍳  **Recipe Scaled — {from_servings} → {to_servings} servings**",
        BAR,
        f"Multiplier : ×{factor:.3g}",
        BAR,
    ]
    for item in scaled:
        lines.append(f"     • {item}")
    if unscalable:
        lines.append(BAR)
        lines.append("Left as written (no measurable quantity):")
        for item in unscalable:
            lines.append(f"     • {item}")

    lines += [BAR]
    if factor > 1:
        lines.append(
            "💡  Scaling up: keep the pan size proportional or the food steams "
            "instead of browning. Cook in two batches rather than crowding one pan."
        )
        lines.append(
            "💡  Salt, chilli and strong spices scale sub-linearly — add about "
            "three-quarters of the scaled amount, taste, then adjust."
        )
    elif factor < 1:
        lines.append(
            "💡  Scaling down: the pan gets too big, so liquids reduce faster. "
            "Drop the heat slightly and check earlier than the original timing."
        )
    lines.append(
        "💡  Baking is the exception — eggs don't halve cleanly. For cakes and "
        "breads, prefer weighing (beat the egg and use half by weight)."
    )
    return "\n".join(lines)


@tool
def convert_kitchen_measure(amount: float, from_unit: str, to_unit: str, ingredient: str) -> str:
    """
    Convert between kitchen measures, including cups to grams for an ingredient.

    Args:
        amount: How much to convert (e.g., 1.5).
        from_unit: Starting unit — cup, tbsp, tsp, ml, l, g, kg, oz, lb.
        to_unit: Target unit, same list.
        ingredient: What is being measured (e.g., 'flour'). Required for any
            volume-to-weight conversion, since density varies by ingredient.
    """
    if amount <= 0:
        return "⚠️  Amount must be a positive number."

    f, t = from_unit.strip().lower(), to_unit.strip().lower()
    f_vol, t_vol = f in VOLUME_ML, t in VOLUME_ML
    f_wt, t_wt = f in WEIGHT_G, t in WEIGHT_G

    if not (f_vol or f_wt):
        return f"⚠️  I don't know the unit '{from_unit}'. Try cup, tbsp, tsp, ml, l, g, kg, oz or lb."
    if not (t_vol or t_wt):
        return f"⚠️  I don't know the unit '{to_unit}'. Try cup, tbsp, tsp, ml, l, g, kg, oz or lb."

    gpc, known = _cup_grams(ingredient)
    notes = []

    if f_vol and t_vol:
        result = amount * VOLUME_ML[f] / VOLUME_ML[t]
    elif f_wt and t_wt:
        result = amount * WEIGHT_G[f] / WEIGHT_G[t]
    elif f_vol and t_wt:
        grams = (amount * VOLUME_ML[f] / VOLUME_ML["cup"]) * gpc
        result = grams / WEIGHT_G[t]
        notes.append(f"Density used : {gpc:g} g per cup of {ingredient.strip() or 'water'}")
    else:  # weight → volume
        grams = amount * WEIGHT_G[f]
        result = (grams / gpc) * VOLUME_ML["cup"] / VOLUME_ML[t]
        notes.append(f"Density used : {gpc:g} g per cup of {ingredient.strip() or 'water'}")

    if notes and not known:
        notes.append(
            f"⚠️   '{ingredient.strip() or '(blank)'}' isn't in my density table, so "
            f"this assumes water. For flour, sugar, rice or fats the real answer "
            f"differs by up to 60% — name the ingredient for an accurate figure."
        )

    lines = [
        f"📐  **Measure Conversion**",
        BAR,
        f"{amount:g} {f}  →  **{result:.3g} {t}**",
    ]
    if ingredient.strip():
        lines.append(f"Ingredient : {ingredient.strip()}")
    lines.append(BAR)
    lines += notes
    if f_vol and t_wt or f_wt and t_vol:
        lines.append(
            "💡  Cups measure volume, not mass, so how hard you pack the cup "
            "changes the result. Weighing is the fix — scales are why bakery "
            "output is consistent and home baking isn't."
        )
    lines += [
        BAR,
        "🥄  **Handy equivalents**",
        "     1 cup = 16 tbsp = 48 tsp ≈ 237 ml",
        "     1 tbsp = 3 tsp ≈ 14.8 ml",
        "     1 stick butter = 8 tbsp = 113 g",
    ]
    return "\n".join(lines)


@tool
def meal_ideas_from_ingredients(ingredients: str, meal_type: str) -> str:
    """
    Suggest dishes you can make from ingredients you already have.

    Args:
        ingredients: What's in the kitchen, comma separated
            (e.g., 'rice, onion, tomato, egg').
        meal_type: 'breakfast', 'lunch', 'dinner', 'snack', or 'any'.
    """
    if not ingredients.strip():
        return "⚠️  Tell me what you have and I'll match it against dishes."

    have = {i.strip().lower() for i in re.split(r"[\n,;]+", ingredients) if i.strip()}
    want = meal_type.strip().lower()
    if want in ("any", "", "anything"):
        want = None

    scored = []
    for dish, (cuisine, meals, needs, minutes) in DISHES.items():
        if want and want not in meals:
            continue
        # Substring both ways so 'tomatoes' matches 'tomato' and 'onion'
        # matches 'red onion'.
        matched = {n for n in needs if any(n in h or h in n for h in have)}
        missing = needs - matched
        if not matched:
            continue
        scored.append((len(matched) / len(needs), len(missing), dish, cuisine, minutes, sorted(missing)))

    if not scored:
        return (
            f"🤔  Nothing in my catalogue matches those ingredients"
            f"{f' for {meal_type}' if want else ''}.\n"
            f"{BAR}\n"
            f"I matched against {len(DISHES)} dishes. Try listing a staple or "
            f"two as well — rice, pasta, bread, eggs, dal or paneer unlock most "
            f"of the list."
        )

    scored.sort(key=lambda r: (-r[0], r[1], r[2]))
    ready = [r for r in scored if r[0] == 1.0]
    close = [r for r in scored if r[0] < 1.0][:6]

    lines = [
        f"🍽️   **Cook From What You Have**",
        BAR,
        f"You have : {', '.join(sorted(have))}",
        f"Matched  : {len(scored)} of {len(DISHES)} dishes"
        + (f"   ·   filtered to {meal_type}" if want else ""),
        BAR,
    ]
    if ready:
        lines.append("✅  **Everything needed — make these now**")
        for _, _, dish, cuisine, minutes, _ in ready[:6]:
            lines.append(f"     • {dish}  ·  {cuisine}  ·  ~{minutes} min")
        lines.append(BAR)
    if close:
        lines.append("🛒  **One or two items short**")
        for pct, _, dish, cuisine, minutes, missing in close:
            lines.append(
                f"     • {dish}  ·  ~{minutes} min  —  need: {', '.join(missing)}"
            )
        lines.append(BAR)
    lines.append(
        "💡  Salt, oil, and basic spices are assumed to be in the kitchen — "
        "they're not counted as missing."
    )
    return "\n".join(lines)


@tool
def cooking_times(item: str) -> str:
    """
    Look up cooking time and a doneness cue for a common ingredient or dish.

    Args:
        item: What's being cooked (e.g., 'rice', 'eggs', 'rajma', 'pasta').
    """
    q = item.strip().lower()
    if not q:
        return "⚠️  Name something for me to look up."

    # Longest key first so 'basmati rice' wins over 'rice'.
    hit = None
    for key in sorted(COOK_TIMES, key=len, reverse=True):
        if key in q or q in key:
            hit = key
            break

    if not hit:
        return (
            f"🤔  '{item.strip()}' isn't in my timing table.\n"
            f"{BAR}\n"
            f"I have: {', '.join(sorted(COOK_TIMES))}.\n"
            f"{BAR}\n"
            f"💡  For anything unlisted, cook to a cue rather than a clock — "
            f"meat to internal temperature, vegetables to colour and bite, "
            f"pulses to whether they crush between two fingers."
        )

    lines = [f"⏱️   **Cooking Time — {hit.title()}**", BAR]
    for method, time, cue in COOK_TIMES[hit]:
        lines += [
            f"**{method}**",
            f"     Time     : {time}",
            f"     Ready when : {cue}",
            "",
        ]
    lines += [
        BAR,
        "💡  Times assume a medium flame and a pan that isn't crowded. Both "
        "double if you overload the pan — the food steams in its own moisture "
        "instead of searing.",
        "💡  Trust the cue over the clock. Stove power, altitude and pot "
        "thickness all move these numbers.",
    ]
    return "\n".join(lines)


@tool
def shopping_list(dishes: str, servings: int) -> str:
    """
    Build a consolidated shopping list for one or more dishes.

    Args:
        dishes: Dish names, comma separated (e.g., 'dal tadka, jeera rice').
        servings: How many people you're cooking for (e.g., 4).
    """
    if servings <= 0:
        return "⚠️  Servings must be a positive whole number."
    if not dishes.strip():
        return "⚠️  Name the dishes and I'll build the list."

    wanted = [d.strip() for d in re.split(r"[\n,;]+", dishes) if d.strip()]
    matched, unknown = [], []
    for name in wanted:
        low = name.lower()
        hit = next(
            (d for d in sorted(DISHES, key=len, reverse=True) if low in d.lower() or d.lower() in low),
            None,
        )
        if hit:
            matched.append(hit)
        else:
            unknown.append(name)

    if not matched:
        return (
            f"🤔  None of those are in my catalogue.\n{BAR}\n"
            f"I know {len(DISHES)} dishes, including: "
            f"{', '.join(sorted(DISHES)[:12])}…"
        )

    # Aggregate: which dishes need each ingredient.
    basket: dict[str, list[str]] = {}
    total_minutes = 0
    for dish in matched:
        _, _, needs, minutes = DISHES[dish]
        total_minutes += minutes
        for n in needs:
            basket.setdefault(n, []).append(dish)

    shared = {k: v for k, v in basket.items() if len(v) > 1}
    single = {k: v for k, v in basket.items() if len(v) == 1}

    lines = [
        f"🛒  **Shopping List — {servings} serving{'' if servings == 1 else 's'}**",
        BAR,
        f"Dishes   : {', '.join(matched)}",
        f"Hands-on : ~{total_minutes} min total if cooked back to back",
        BAR,
    ]
    if shared:
        lines.append("🔁  **Used in more than one dish — buy these first**")
        for item in sorted(shared):
            lines.append(f"     • {item}   ({len(shared[item])} dishes)")
        lines.append(BAR)
    if single:
        lines.append("📋  **Everything else**")
        for item in sorted(single):
            lines.append(f"     • {item}   ({single[item][0]})")
        lines.append(BAR)
    if unknown:
        lines.append(f"⚠️   Not in my catalogue, so not costed in: {', '.join(unknown)}")
        lines.append(BAR)
    lines += [
        "💡  Quantities are deliberately absent — they depend on the recipe you "
        "follow. Use the scaling tool once you've picked one.",
        "💡  Shop the shared list first. Overlapping ingredients are where "
        "cooking two dishes gets cheaper than cooking one twice.",
    ]
    return "\n".join(lines)

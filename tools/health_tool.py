"""
tools/health_tool.py
--------------------
Fitness and daily-habit tools for the Health Agent.

Everything here is general wellness maths — BMI, Mifflin-St Jeor energy
expenditure, training splits, hydration and sleep ranges. None of it is
medical advice, and the calorie tool refuses to go below the standard
safety floors even if asked for an aggressive deficit.
"""

from langchain.tools import tool


BAR = "━" * 46

# Activity descriptor → TDEE multiplier over BMR.
ACTIVITY = {
    "sedentary": (1.20, "desk-bound, little deliberate movement"),
    "light": (1.375, "light exercise 1–3 days a week"),
    "moderate": (1.55, "moderate exercise 3–5 days a week"),
    "active": (1.725, "hard exercise 6–7 days a week"),
    "very active": (1.90, "physical job, or two sessions a day"),
}

# Lowest intake to recommend without supervision, by Mifflin sex input.
CALORIE_FLOOR = {"male": 1500, "female": 1200, "unspecified": 1350}

DISCLAIMER = (
    "⚕️   General wellness estimates from population formulas — not medical "
    "advice. Check with a doctor before changing your diet or training if you "
    "have a health condition, take medication, are pregnant, or are under 18."
)


def _normalise_sex(sex: str) -> str:
    """
    Map free text onto the two variants Mifflin-St Jeor actually has.

    The equation only offers a male and a female constant. Rather than
    guessing, anything outside those maps to 'unspecified', which averages
    the two — a mid-point estimate with the uncertainty stated, instead of a
    false-precision number.
    """
    s = sex.strip().lower()
    if s in ("m", "male", "man", "boy"):
        return "male"
    if s in ("f", "female", "woman", "girl"):
        return "female"
    return "unspecified"


def _normalise_activity(activity_level: str) -> str:
    a = activity_level.strip().lower()
    for key in ("very active", "sedentary", "light", "moderate", "active"):
        if key in a:
            return key
    return "moderate"


@tool
def bmi_report(weight_kg: float, height_cm: float) -> str:
    """
    Calculate BMI, its category, and the corresponding healthy weight range.

    Args:
        weight_kg: Body weight in kilograms (e.g., 72).
        height_cm: Height in centimetres (e.g., 178).
    """
    if weight_kg <= 0 or height_cm <= 0:
        return "⚠️  Weight and height must both be positive numbers."

    m = height_cm / 100
    bmi = weight_kg / (m * m)

    # WHO international cut-offs.
    if bmi < 18.5:
        who = "Underweight"
    elif bmi < 25:
        who = "Normal"
    elif bmi < 30:
        who = "Overweight"
    else:
        who = "Obese"

    # WHO Asia-Pacific cut-offs, which ICMR uses for Indian populations —
    # cardiometabolic risk rises at a lower BMI, so the same number lands in
    # a different band. Both are shown rather than silently picking one.
    if bmi < 18.5:
        asia = "Underweight"
    elif bmi < 23:
        asia = "Normal"
    elif bmi < 25:
        asia = "Overweight"
    else:
        asia = "Obese"

    return (
        f"⚖️   **BMI Report**\n"
        f"{BAR}\n"
        f"Input      : {weight_kg:g} kg at {height_cm:g} cm\n"
        f"**BMI        : {bmi:.1f}**\n"
        f"{BAR}\n"
        f"WHO (international) : {who}   — normal band 18.5–24.9\n"
        f"WHO Asia-Pacific    : {asia}   — normal band 18.5–22.9\n"
        f"                      (the band ICMR applies for Indian populations)\n"
        f"{BAR}\n"
        f"Healthy weight range at your height\n"
        f"     • International : {18.5 * m * m:.1f} – {24.9 * m * m:.1f} kg\n"
        f"     • Asia-Pacific  : {18.5 * m * m:.1f} – {22.9 * m * m:.1f} kg\n"
        f"{BAR}\n"
        f"💡  BMI ignores muscle mass and fat distribution. If you lift "
        f"regularly it will overstate your risk — waist circumference and "
        f"waist-to-height ratio track health better.\n"
        f"{DISCLAIMER}"
    )


@tool
def calorie_targets(
    weight_kg: float,
    height_cm: float,
    age: int,
    sex: str,
    activity_level: str,
    goal: str,
) -> str:
    """
    Estimate daily calorie and macronutrient targets for a goal.

    Args:
        weight_kg: Body weight in kilograms (e.g., 72).
        height_cm: Height in centimetres (e.g., 178).
        age: Age in years (e.g., 21).
        sex: 'male', 'female', or anything else for a mid-point estimate.
        activity_level: 'sedentary', 'light', 'moderate', 'active' or 'very active'.
        goal: 'lose', 'maintain' or 'gain'.
    """
    if weight_kg <= 0 or height_cm <= 0 or age <= 0:
        return "⚠️  Weight, height and age must all be positive numbers."

    s = _normalise_sex(sex)
    act = _normalise_activity(activity_level)
    mult, act_desc = ACTIVITY[act]

    # Mifflin-St Jeor.
    base = 10 * weight_kg + 6.25 * height_cm - 5 * age
    offsets = {"male": 5, "female": -161, "unspecified": -78}
    bmr = base + offsets[s]
    tdee = bmr * mult

    g = goal.strip().lower()
    if any(k in g for k in ("lose", "cut", "fat loss", "lean", "deficit", "slim")):
        goal_name, target, protein_per_kg = "Fat loss", tdee * 0.80, 2.0
        note = "A 20% deficit — roughly 0.5–0.7 kg a week. Faster than that costs muscle."
    elif any(k in g for k in ("gain", "bulk", "muscle", "mass", "surplus", "build")):
        goal_name, target, protein_per_kg = "Muscle gain", tdee + 300, 1.8
        note = "A ~300 kcal surplus — about 0.25–0.4 kg a week, mostly lean if you train."
    else:
        goal_name, target, protein_per_kg = "Maintenance", tdee, 1.6
        note = "Hold steady. Weigh yourself weekly and adjust by ±150 kcal if it drifts."

    floor = CALORIE_FLOOR[s]
    floored = target < floor
    if floored:
        target = floor

    protein_g = protein_per_kg * weight_kg
    fat_g = (target * 0.25) / 9
    carb_g = max(0, (target - protein_g * 4 - fat_g * 9) / 4)

    lines = [
        f"🔥  **Daily Energy Targets — {goal_name}**",
        BAR,
        f"Profile  : {weight_kg:g} kg · {height_cm:g} cm · {age} yrs · {s}",
        f"Activity : {act} ({act_desc}) ×{mult}",
        BAR,
        f"BMR (at rest)          : {bmr:,.0f} kcal",
        f"TDEE (with activity)   : {tdee:,.0f} kcal",
        f"**Target for {goal_name.lower():<14}: {target:,.0f} kcal**",
        BAR,
        f"🍽️   **Macro split**",
        f"     Protein : {protein_g:,.0f} g   ({protein_per_kg:g} g/kg — keep this one honest)",
        f"     Fat     : {fat_g:,.0f} g   (25% of calories)",
        f"     Carbs   : {carb_g:,.0f} g   (the remainder — your training fuel)",
        BAR,
        f"💡  {note}",
    ]
    if floored:
        lines.append(
            f"⚠️   The formula returned less than {floor} kcal, so it's been held "
            f"at that floor. Going below it without supervision risks muscle "
            f"loss and nutrient gaps — reduce calories less and move more instead."
        )
    lines += [
        "💡  These are population averages with roughly ±10% spread. Track two "
        "weeks of real weight change and trust that over the formula.",
        DISCLAIMER,
    ]
    return "\n".join(lines)


@tool
def workout_split(days_per_week: int, goal: str) -> str:
    """
    Build a weekly training split for the number of days available.

    Args:
        days_per_week: Realistic training days per week (1–7).
        goal: 'strength', 'muscle', 'fat loss' or 'general fitness'.
    """
    days = max(1, min(7, int(days_per_week)))
    g = goal.strip().lower()

    if "strength" in g:
        goal_name = "Strength"
        scheme = "3–5 sets of 3–6 reps on main lifts, 2–4 min rest"
        cardio = "Optional — keep it light so it doesn't eat recovery"
    elif any(k in g for k in ("muscle", "hypertrophy", "size", "bulk")):
        goal_name = "Muscle"
        scheme = "3–4 sets of 8–12 reps, 60–90 s rest, last 2 reps genuinely hard"
        cardio = "10–15 min easy work post-session, 2–3× a week"
    elif any(k in g for k in ("fat", "lose", "cut", "lean")):
        goal_name = "Fat loss"
        scheme = "3 sets of 8–12 reps on compounds — lifting protects muscle in a deficit"
        cardio = "150–200 min of easy cardio a week, plus a daily step target"
    else:
        goal_name = "General fitness"
        scheme = "2–3 sets of 10–15 reps, full range, controlled tempo"
        cardio = "20–30 min of something you enjoy, 3× a week"

    plans = {
        1: ["Full body — squat, hinge, push, pull, carry"],
        2: ["Full body A — squat focus, horizontal push/pull",
            "Full body B — hinge focus, vertical push/pull"],
        3: ["Full body A — squat, bench, row",
            "Full body B — deadlift, overhead press, pull-up",
            "Full body C — lunge, incline press, cable row + core"],
        4: ["Upper A — horizontal push/pull priority",
            "Lower A — squat priority",
            "Upper B — vertical push/pull priority",
            "Lower B — hinge priority"],
        5: ["Push — chest, shoulders, triceps",
            "Pull — back, biceps, rear delts",
            "Legs — quads, hamstrings, calves",
            "Upper — weak points, arms, shoulders",
            "Lower + core — hinge priority, loaded carries"],
        6: ["Push A — heavy", "Pull A — heavy", "Legs A — heavy",
            "Push B — volume", "Pull B — volume", "Legs B — volume"],
        7: ["Push", "Pull", "Legs", "Rest-day mobility + walk",
            "Upper", "Lower", "Conditioning + core"],
    }

    lines = [
        f"🏋️   **{days}-Day Split — {goal_name}**",
        BAR,
        f"Rep scheme : {scheme}",
        f"Cardio     : {cardio}",
        BAR,
    ]
    for i, session in enumerate(plans[days], 1):
        lines.append(f"     Day {i}  ·  {session}")
    if days < 7:
        lines.append(f"     {'Rest'}   ·  {7 - days} day(s) off — walk, stretch, sleep")

    lines += [
        BAR,
        "📈  **Progression** — add a little each week, in this order:",
        "     1.  One more rep per set, until you hit the top of the range",
        "     2.  Then add weight and drop back to the bottom of the range",
        "     3.  Only then consider adding a set",
        BAR,
        "💡  Consistency beats the split. Four sessions you actually attend "
        "outperform six you skip half of.",
        "💡  Warm up 5–10 min and leave 48 h before training the same muscle hard again.",
        DISCLAIMER,
    ]
    return "\n".join(lines)


@tool
def hydration_and_sleep(weight_kg: float, age: int) -> str:
    """
    Give daily water and sleep targets for a body weight and age.

    Args:
        weight_kg: Body weight in kilograms (e.g., 72).
        age: Age in years (e.g., 21).
    """
    if weight_kg <= 0 or age <= 0:
        return "⚠️  Weight and age must both be positive numbers."

    water_l = weight_kg * 0.035
    glasses = round(water_l * 1000 / 250)

    if age < 14:
        sleep = "9–11 hours"
    elif age < 18:
        sleep = "8–10 hours"
    elif age < 65:
        sleep = "7–9 hours"
    else:
        sleep = "7–8 hours"

    return (
        f"💧  **Hydration & Sleep**\n"
        f"{BAR}\n"
        f"**Water : {water_l:.1f} L a day**  (~{glasses} glasses of 250 ml)\n"
        f"     Baseline is ~35 ml per kg of body weight.\n"
        f"     Add 500–750 ml for every hour of hard training or heat.\n"
        f"     Add ~250 ml per caffeinated drink.\n"
        f"{BAR}\n"
        f"**Sleep : {sleep} a night**  (age {age})\n"
        f"     Regular timing matters as much as total hours — same wake time "
        f"daily, including weekends.\n"
        f"     No caffeine within 8 h of bed; it has a ~5 h half-life.\n"
        f"     Screens off 30–60 min before, room cool and dark.\n"
        f"{BAR}\n"
        f"🔎  **Quick self-checks**\n"
        f"     • Pale-straw urine means hydration is fine. Dark yellow means catch up.\n"
        f"     • Needing an alarm to wake up every single day means you're short on sleep.\n"
        f"{BAR}\n"
        f"💡  Sleep is the highest-leverage thing on this list. Under-sleeping "
        f"raises appetite, lowers training quality, and blunts recovery — it "
        f"undoes the diet and the gym at the same time.\n"
        f"{DISCLAIMER}"
    )

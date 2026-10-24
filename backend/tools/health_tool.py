from langchain.tools import tool


@tool
def bmi_report(weight_kg: float, height_cm: float) -> str:
    """Calculate a basic BMI estimate."""
    if weight_kg <= 0 or height_cm <= 0:
        return "Weight and height must be positive."
    bmi = weight_kg / (height_cm / 100) ** 2
    return f"BMI: {bmi:.1f}"


@tool
def calorie_targets(weight_kg: float, height_cm: float, age: int, activity_level: str) -> str:
    """Estimate baseline calorie needs."""
    if min(weight_kg, height_cm, age) <= 0:
        return "Weight, height, and age must be positive."
    bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    return f"Estimated maintenance calories: {bmr:.0f} kcal before activity adjustment."


@tool
def workout_split(days_per_week: int, goal: str) -> str:
    """Build a simple weekly training split."""
    if not 1 <= days_per_week <= 7:
        return "Training days must be between 1 and 7."
    return f"{days_per_week}-day {goal.strip() or 'general fitness'} training split."


@tool
def hydration_and_sleep(weight_kg: float, age: int) -> str:
    """Give basic hydration and sleep targets."""
    if weight_kg <= 0 or age <= 0:
        return "Weight and age must both be positive numbers."
    return f"Water target: {weight_kg * 0.035:.1f} L; sleep target: 7–9 hours."

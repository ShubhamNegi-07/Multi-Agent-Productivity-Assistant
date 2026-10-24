from langchain.tools import tool


@tool
def grade_needed(
    current_percent: float,
    completed_weight: float,
    final_weight: float,
    target_percent: float,
) -> str:
    """Calculate the score needed on a final assessment."""
    if not 0 <= completed_weight <= 100 or not 0 <= final_weight <= 100:
        return "Weights should be between 0 and 100."
    if not 0 <= current_percent <= 100 or not 0 <= target_percent <= 100:
        return "Percentages should be between 0 and 100."
    if final_weight <= 0:
        return "Final weight must be greater than 0."
    needed = (target_percent - current_percent * completed_weight / 100) * 100 / final_weight
    return f"Required score: {max(0, needed):.1f}%"


@tool
def pomodoro_plan(total_minutes: int, focus_minutes: int) -> str:
    """Create a simple focus-session plan."""
    if total_minutes <= 0 or focus_minutes <= 0:
        return "Study time must be positive."
    return f"{total_minutes} minutes available in {focus_minutes}-minute focus blocks."


@tool
def flashcards_from_notes(notes: str) -> str:
    """Turn notes into basic flashcards."""
    return notes.strip() or "Please provide notes."


@tool
def spaced_repetition_schedule(topic: str, days: int) -> str:
    """Create a spaced-repetition schedule."""
    return f"Review {topic} on days 1, 3, 7, and {max(days, 7)}."


@tool
def exam_revision_plan(subjects: str, hours_per_day: float, days_until_exam: int) -> str:
    """Create a basic exam revision plan."""
    return f"Allocate {hours_per_day:g} hours per day across {subjects} for {days_until_exam} days."

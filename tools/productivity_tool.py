"""
tools/productivity_tool.py
--------------------------
Text-generation and planning tools for the Productivity Agent.
Returns structured, ready-to-use content for common productivity tasks.
"""

from langchain.tools import tool
from datetime import datetime, timedelta


@tool
def create_todo_list(task_text: str) -> str:
    """
    Convert a comma-separated list of tasks into a formatted to-do list.

    Args:
        task_text: Comma-separated tasks (e.g., 'Buy groceries, Call doctor, Review report').
    """
    tasks = [t.strip() for t in task_text.split(",") if t.strip()]
    if not tasks:
        return "⚠️  No tasks provided. Please enter tasks separated by commas."

    lines = [f"📝  **To-Do List** — {datetime.now().strftime('%d %b %Y')}", "━" * 36]
    for i, task in enumerate(tasks, 1):
        lines.append(f"  {i:02d}.  ☐  {task}")
    lines.append("━" * 36)
    lines.append(f"📌  Total Tasks: {len(tasks)}")

    return "\n".join(lines)


@tool
def generate_meeting_agenda(topic: str) -> str:
    """
    Generate a professional meeting agenda for a given topic.

    Args:
        topic: The main topic or purpose of the meeting (e.g., 'Q2 Project Review').
    """
    return (
        f"📋  **Meeting Agenda — {topic.title()}**\n"
        f"{'━'*44}\n"
        f"📅  Date      : {datetime.now().strftime('%d %B %Y')}\n"
        f"⏰  Duration  : 60 minutes\n"
        f"{'━'*44}\n"
        f"1️⃣   [00:00 – 00:05]  Welcome & Roll Call\n"
        f"2️⃣   [00:05 – 00:15]  Previous Action Items Review\n"
        f"3️⃣   [00:15 – 00:40]  Main Discussion: {topic.title()}\n"
        f"4️⃣   [00:40 – 00:50]  Open Questions & Concerns\n"
        f"5️⃣   [00:50 – 00:60]  Action Items & Next Steps\n"
        f"{'━'*44}\n"
        f"📌  Please come prepared with updates on your tasks."
    )


@tool
def draft_email(purpose: str) -> str:
    """
    Draft a professional email for a given purpose.

    Args:
        purpose: The reason for the email (e.g., 'sick leave', 'project update',
                 'meeting request', 'resignation', 'apology').
    """
    purpose_lower = purpose.lower()

    templates = {
        "sick leave": (
            "Request for Sick Leave",
            "Dear [Manager's Name],\n\n"
            "I hope this message finds you well. I am writing to inform you that I am "
            "feeling unwell today and am unable to attend work. I will be taking a sick "
            "leave for [number of days] days, from [start date] to [end date].\n\n"
            "I will ensure that all pending tasks are managed and, if required, I can "
            "be reached via email for any urgent matters.\n\n"
            "Thank you for your understanding.\n\nBest regards,\n[Your Name]"
        ),
        "leave": (
            "Leave Application",
            "Dear [Manager's Name],\n\n"
            "I would like to request a leave of absence for [number of days] days from "
            "[start date] to [end date] due to [reason].\n\n"
            "I will ensure a smooth handover of my responsibilities before leaving and "
            "will remain reachable for critical issues.\n\n"
            "Kindly approve my leave request.\n\nThank you,\n[Your Name]"
        ),
        "project update": (
            "Project Status Update",
            "Dear [Recipient's Name],\n\n"
            "I am writing to provide you with a quick update on the [Project Name].\n\n"
            "✅  Completed: [List completed tasks]\n"
            "🔄  In Progress: [List ongoing tasks]\n"
            "⏳  Upcoming: [List next steps]\n\n"
            "Please feel free to reach out if you have any questions or concerns.\n\n"
            "Best regards,\n[Your Name]"
        ),
        "meeting request": (
            "Meeting Request — [Topic]",
            "Dear [Recipient's Name],\n\n"
            "I hope you are doing well. I would like to schedule a meeting to discuss "
            "[topic]. Could you please let me know your availability for a 30-minute "
            "call this week?\n\n"
            "Suggested slots:\n"
            "  • [Day 1], [Time]\n"
            "  • [Day 2], [Time]\n\n"
            "Looking forward to your response.\n\nBest regards,\n[Your Name]"
        ),
    }

    for key, (subject, body) in templates.items():
        if key in purpose_lower:
            return (
                f"📧  **Draft Email**\n"
                f"{'━'*44}\n"
                f"📌  Subject : {subject}\n"
                f"{'━'*44}\n"
                f"{body}\n"
                f"{'━'*44}\n"
                f"💡  Tip: Replace all [ ] placeholders before sending."
            )

    # Generic fallback
    return (
        f"📧  **Draft Email — {purpose.title()}**\n"
        f"{'━'*44}\n"
        f"📌  Subject : Regarding {purpose.title()}\n"
        f"{'━'*44}\n"
        f"Dear [Recipient's Name],\n\n"
        f"I am writing to you regarding {purpose}. [Provide context and details here.]\n\n"
        f"[Add your main message, request, or information.]\n\n"
        f"Please feel free to reach out if you have any questions.\n\n"
        f"Best regards,\n[Your Name]\n"
        f"{'━'*44}\n"
        f"💡  Tip: Customize the placeholders before sending."
    )


@tool
def study_plan(subject: str, hours_per_day: float) -> str:
    """
    Create a structured 7-day study plan for a given subject.

    Args:
        subject: The subject or topic to study (e.g., 'Python', 'Machine Learning').
        hours_per_day: Daily study hours available (e.g., 2.0, 3.5).
    """
    total_hours = hours_per_day * 7
    start_date  = datetime.now()

    topics = [
        f"Introduction & Fundamentals of {subject}",
        f"Core Concepts — Part 1",
        f"Core Concepts — Part 2",
        f"Hands-on Practice & Exercises",
        f"Advanced Topics & Real-world Use Cases",
        f"Project / Case Study Work",
        f"Revision, Quiz & Review",
    ]

    lines = [
        f"📚  **7-Day Study Plan — {subject.title()}**",
        f"{'━'*44}",
        f"⏱️  {hours_per_day} hrs/day  |  Total: {total_hours:.1f} hrs",
        f"{'━'*44}",
    ]

    for i, topic in enumerate(topics):
        day    = start_date + timedelta(days=i)
        day_str = day.strftime("%a, %d %b")
        lines.append(f"📅  Day {i+1} ({day_str}): {topic}")

    lines += [
        f"{'━'*44}",
        f"💡  Tips:",
        f"  • Use Pomodoro: 25 min study + 5 min break",
        f"  • Take notes and summarize each session",
        f"  • Practice with small projects daily",
    ]

    return "\n".join(lines)

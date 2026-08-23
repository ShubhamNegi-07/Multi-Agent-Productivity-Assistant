"""
tools/study_tool.py
-------------------
Study-planning tools for the Study Agent.

All offline: spaced-repetition dates from the calendar, revision-time
allocation, the algebra behind "what do I need on the final", Pomodoro
blocking, and turning notes into flashcards.
"""

import re
from datetime import date, datetime, timedelta

from langchain.tools import tool


BAR = "━" * 46

# Expanding intervals, in days after first study. The gaps widen because
# recall gets more durable each time you successfully retrieve it — reviewing
# on a fixed daily cadence wastes the same effort on material already solid.
INTERVALS = [1, 3, 7, 14, 30, 60]

# Rough minutes of focused work most people sustain before quality drops.
SESSION_CAP_MINUTES = 90


def _parse_date(text: str, fallback: date) -> tuple[date, str]:
    """
    Parse a date written any of the common ways. Returns (date, error).

    Empty input means 'today', which is the sensible default for a start date
    and never right for a deadline — callers check for that themselves.
    """
    s = text.strip()
    if not s:
        return fallback, ""
    for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y", "%Y/%m/%d", "%d %b %Y", "%d %B %Y"):
        try:
            return datetime.strptime(s, fmt).date(), ""
        except ValueError:
            continue
    return fallback, f"couldn't read the date '{s}' — use YYYY-MM-DD"


@tool
def spaced_repetition_schedule(topic: str, exam_date: str, start_date: str) -> str:
    """
    Build a spaced-repetition review calendar for a topic, with real dates.

    Args:
        topic: What you're learning (e.g., 'Operating Systems — deadlocks').
        exam_date: When you're tested, as YYYY-MM-DD. Leave blank if there
            is no fixed exam.
        start_date: When you first study it, as YYYY-MM-DD. Blank means today.
    """
    if not topic.strip():
        return "⚠️  Tell me the topic you're scheduling."

    today = date.today()
    start, err1 = _parse_date(start_date, today)
    exam, err2 = _parse_date(exam_date, date.max)
    problems = [e for e in (err1, err2) if e]
    if problems:
        return "⚠️  " + "; ".join(problems)

    has_exam = exam != date.max
    if has_exam and exam < start:
        return (
            f"⚠️  The exam ({exam.isoformat()}) is before the start date "
            f"({start.isoformat()}). Check the dates."
        )

    rows = [("Learn", start, "First pass — read, understand, write your own summary")]
    for i, gap in enumerate(INTERVALS, 1):
        when = start + timedelta(days=gap)
        if has_exam and when >= exam:
            break
        rows.append((
            f"Review {i}",
            when,
            "Recall from a blank page first, then check. Reading notes again is not review.",
        ))

    if has_exam:
        eve = exam - timedelta(days=1)
        if eve > start:
            rows.append(("Final pass", eve, "Only your own summary and the questions you got wrong"))

    lines = [
        f"📚  **Revision Schedule — {topic.strip()}**",
        BAR,
        f"Start : {start.strftime('%a %d %b %Y')}",
    ]
    if has_exam:
        days_left = (exam - today).days
        lines.append(f"Exam  : {exam.strftime('%a %d %b %Y')}   ({days_left} day(s) from today)")
    else:
        lines.append("Exam  : none set — the schedule runs the full 60-day curve")
    lines.append(BAR)

    for label, when, what in rows:
        rel = (when - today).days
        if rel == 0:
            tag = "today"
        elif rel == 1:
            tag = "tomorrow"
        elif rel < 0:
            tag = f"{-rel} day(s) ago"
        else:
            tag = f"in {rel} days"
        lines.append(f"**{label:<11}** {when.strftime('%a %d %b')}   ({tag})")
        lines.append(f"              {what}")

    lines += [BAR]
    if has_exam and len(rows) <= 2:
        lines.append(
            "⚠️   There isn't much runway here — the exam is close enough that "
            "only one or two passes fit. Spacing beats cramming, but with this "
            "little time, prioritise past-paper questions over re-reading."
        )
    lines += [
        "💡  **How to actually review**: close the notes, write down everything "
        "you remember, *then* check. The struggle to retrieve is what builds "
        "the memory — recognition while re-reading feels productive and isn't.",
        "💡  Got something wrong? Reset it to the start of the schedule. Got it "
        "instantly? Skip the next review and stretch the gap.",
    ]
    return "\n".join(lines)


@tool
def study_plan(subjects: str, days_until_exam: int, hours_per_day: float) -> str:
    """
    Split available study time across subjects, day by day.

    Args:
        subjects: Subjects to cover, comma separated. Add ':weight' to give
            one more time (e.g., 'Maths:3, Physics:2, English:1').
        days_until_exam: Days you have to prepare (e.g., 14).
        hours_per_day: Realistic study hours per day (e.g., 4).
    """
    if days_until_exam <= 0:
        return "⚠️  Days until the exam must be a positive whole number."
    if hours_per_day <= 0:
        return "⚠️  Hours per day must be a positive number."
    if hours_per_day > 14:
        return (
            "⚠️  More than 14 hours a day isn't a plan, it's a way to lose a "
            "week to burnout. Give me a number you can repeat daily."
        )
    if not subjects.strip():
        return "⚠️  List the subjects you need to cover."

    parsed = []
    for chunk in re.split(r"[\n,;]+", subjects):
        chunk = chunk.strip()
        if not chunk:
            continue
        if ":" in chunk:
            name, _, w = chunk.rpartition(":")
            try:
                weight = max(0.1, float(w.strip()))
            except ValueError:
                name, weight = chunk, 1.0
        else:
            name, weight = chunk, 1.0
        parsed.append((name.strip(), weight))

    if not parsed:
        return "⚠️  I couldn't read any subject names out of that."

    total_hours = days_until_exam * hours_per_day
    total_weight = sum(w for _, w in parsed)

    lines = [
        f"🗂️   **Study Plan — {days_until_exam} day(s), {hours_per_day:g} h/day**",
        BAR,
        f"Total study time : {total_hours:g} hours",
        f"Subjects         : {len(parsed)}",
        BAR,
        "**Time allocation**",
    ]
    for name, weight in parsed:
        share = weight / total_weight
        hrs = total_hours * share
        lines.append(
            f"     {name:<22} {hrs:5.1f} h   ({share * 100:.0f}%)"
            + (f"   ·  weight {weight:g}" if weight != 1.0 else "")
        )
    lines.append(BAR)

    # Rotate subjects across days rather than blocking one subject per day —
    # interleaving beats blocking for retention, and it means no subject goes
    # untouched for a week.
    sessions_per_day = max(1, min(3, round(hours_per_day / 1.5)))
    block = hours_per_day / sessions_per_day
    lines.append(
        f"**Daily shape** — {sessions_per_day} block(s) of {block:.1f} h, "
        f"subjects rotating"
    )
    order = [name for name, _ in sorted(parsed, key=lambda p: -p[1])]
    slot = 0
    preview_days = min(days_until_exam, 7)
    for d in range(1, preview_days + 1):
        todays = []
        for _ in range(sessions_per_day):
            todays.append(order[slot % len(order)])
            slot += 1
        lines.append(f"     Day {d:<3} {'  →  '.join(todays)}")
    if days_until_exam > preview_days:
        lines.append(f"     …then keep rotating for the remaining {days_until_exam - preview_days} day(s)")

    lines += [
        BAR,
        "💡  Interleaving (switching subjects) feels harder than blocking one "
        "subject per day, and tests better weeks later. The difficulty is the "
        "mechanism, not a sign you're doing it wrong.",
        "💡  Reserve the last 20% of your total hours for past papers under "
        "timed conditions. Knowing the material and being able to produce it "
        "in three hours are different skills.",
    ]
    if block > 1.5:
        lines.append(
            f"⚠️   {block:.1f}-hour blocks are longer than most people hold "
            f"focus. Break each one with 5 minutes off-screen every 25–50 min."
        )
    return "\n".join(lines)


@tool
def grade_needed(
    current_percent: float,
    completed_weight: float,
    final_weight: float,
    target_percent: float,
) -> str:
    """
    Work out the score needed on a final assessment to hit a target grade.

    Args:
        current_percent: Your average so far on completed work (e.g., 72).
        completed_weight: What that work is worth of the final grade, as a
            percentage (e.g., 60).
        final_weight: What the remaining assessment is worth (e.g., 40).
        target_percent: The overall grade you want (e.g., 75).
    """
    if completed_weight < 0 or final_weight <= 0:
        return "⚠️  Completed weight can't be negative and the final must be worth more than 0%."
    if not (0 <= current_percent <= 100) or not (0 <= target_percent <= 100):
        return "⚠️  Percentages should be between 0 and 100."

    total_weight = completed_weight + final_weight
    banked = current_percent * completed_weight / 100
    needed = (target_percent - banked) * 100 / final_weight

    lines = [
        f"🎯  **Score Needed on the Final**",
        BAR,
        f"So far        : {current_percent:g}% on work worth {completed_weight:g}% of the grade",
        f"Still to come : an assessment worth {final_weight:g}%",
        f"Target        : {target_percent:g}% overall",
        BAR,
        f"Banked so far : {banked:.1f} of the {target_percent:g} points you need",
    ]

    if abs(total_weight - 100) > 0.5:
        lines.append(
            f"⚠️   Your weights add up to {total_weight:g}%, not 100%. The maths "
            f"below assumes they're the whole grade — if something's missing, "
            f"add it in and re-run."
        )
    lines.append(BAR)

    if needed <= 0:
        lines += [
            f"✅  **You've already secured it.** Even a zero on the final leaves "
            f"you at {banked * 100 / total_weight:.1f}%.",
            f"Required score : **0%** (mathematically already done)",
        ]
    elif needed > 100:
        best = (banked + final_weight) * 100 / total_weight
        lines += [
            f"❌  **Not reachable.** You'd need **{needed:.1f}%**, and the paper "
            f"only goes to 100.",
            f"Best possible now : {best:.1f}% overall (a perfect final)",
            BAR,
            f"💡  Aim at the highest grade that *is* reachable, and check whether "
            f"your institution allows a resit, a dropped-lowest rule, or "
            f"scaling — those change the arithmetic, and this tool doesn't "
            f"know your regulations.",
        ]
    else:
        lines.append(f"📄  Required score : **{needed:.1f}%** on the final")
        if needed > current_percent + 15:
            lines.append(
                f"⚠️   That's {needed - current_percent:.0f} points above your "
                f"current average — a real jump, not a rounding error. Plan for "
                f"it properly rather than hoping."
            )
        elif needed < current_percent - 10:
            lines.append(
                "💡  Comfortably below your current average. Hold steady rather "
                "than coasting — the margin is smaller than it looks if one "
                "question goes badly."
            )
        lines.append(BAR)
        lines.append("**What each outcome gives you overall**")
        for score in (50, 60, 70, 80, 90, 100):
            overall = (banked + score * final_weight / 100) * 100 / total_weight
            mark = "  ← target met" if overall >= target_percent else ""
            lines.append(f"     {score:>3}% on the final  →  {overall:5.1f}% overall{mark}")

    lines += [
        BAR,
        "💡  This assumes a straight weighted average with no scaling, no "
        "dropped components and no minimum-component rules. Check your course "
        "handbook — those exceptions are common and they move the number.",
    ]
    return "\n".join(lines)


@tool
def pomodoro_plan(total_minutes: int, focus_minutes: int) -> str:
    """
    Split a study session into focus blocks with breaks, timed end to end.

    Args:
        total_minutes: How long you have in total (e.g., 180).
        focus_minutes: Length of one focus block, 10–90 (e.g., 25).
    """
    if total_minutes <= 0:
        return "⚠️  Total time must be a positive number of minutes."
    focus = max(10, min(SESSION_CAP_MINUTES, int(focus_minutes)))
    short_break = 5 if focus <= 30 else 10
    long_break = 15 if focus <= 30 else 25

    lines = [
        f"⏳  **Focus Session — {total_minutes} min available**",
        BAR,
        f"Block length : {focus} min focus / {short_break} min break",
        f"Long break   : {long_break} min after every 4th block",
        BAR,
    ]
    if int(focus_minutes) != focus:
        lines.insert(3, f"(adjusted from {int(focus_minutes)} — kept within 10–{SESSION_CAP_MINUTES} min)")

    elapsed, block_no, timeline = 0, 0, []
    while elapsed + focus <= total_minutes:
        block_no += 1
        timeline.append((elapsed, elapsed + focus, f"Focus block {block_no}"))
        elapsed += focus
        if elapsed >= total_minutes:
            break
        brk = long_break if block_no % 4 == 0 else short_break
        if elapsed + brk > total_minutes:
            break
        timeline.append((elapsed, elapsed + brk, "Long break" if brk == long_break else "Break"))
        elapsed += brk

    if not timeline:
        return (
            f"⚠️  {total_minutes} min isn't long enough for a {focus}-min block.\n"
            f"{BAR}\n"
            f"Use the time as one short unbroken push instead — set a timer for "
            f"{total_minutes} min, pick one specific task, and stop when it rings."
        )

    for start, end, label in timeline:
        bar = "█" if label.startswith("Focus") else "░"
        lines.append(f"     {start:>3}–{end:<3} min  {bar * 3}  {label}")

    focus_total = sum(e - s for s, e, l in timeline if l.startswith("Focus"))
    leftover = total_minutes - elapsed
    lines += [
        BAR,
        f"Focus time   : {focus_total} min across {block_no} block(s)",
        f"Break time   : {elapsed - focus_total} min",
    ]
    if leftover > 0:
        lines.append(f"Unallocated  : {leftover} min — use it to review what you just did")
    lines += [
        BAR,
        "💡  Decide the *one* task before the timer starts. Blocks fail from "
        "vague intent far more often than from short attention.",
        "💡  Breaks mean off-screen. Scrolling isn't a break — it uses the same "
        "attention you're trying to rest.",
        "💡  If the timer rings mid-flow, keep going. The clock serves the work.",
    ]
    return "\n".join(lines)


@tool
def flashcards_from_notes(notes: str) -> str:
    """
    Turn notes into question-and-answer flashcards.

    Args:
        notes: Notes with one item per line, using 'term - definition',
            'term: definition', or 'term = definition'.
    """
    if not notes.strip():
        return "⚠️  Paste the notes you want turned into cards."

    cards, skipped = [], []
    for raw in notes.splitlines():
        line = raw.strip().lstrip("-•*+ \t")
        if not line:
            continue
        # Try the separators in order of how unambiguous they are. An en/em
        # dash or ' - ' with spaces is checked before a bare hyphen so
        # hyphenated terms ('time-complexity: …') survive intact.
        m = re.split(r"\s+[—–]\s+|\s+-\s+|\s*:\s+|\s*=\s*", line, maxsplit=1)
        if len(m) == 2 and m[0].strip() and m[1].strip():
            cards.append((m[0].strip(), m[1].strip()))
        else:
            skipped.append(line)

    if not cards:
        return (
            f"⚠️  I couldn't find any term/definition pairs in that.\n{BAR}\n"
            f"Put one item per line with a separator, like:\n"
            f"     Deadlock - four conditions must hold at once\n"
            f"     Mutex: lock allowing one thread in a critical section\n"
            f"     Big-O = worst-case growth rate of an algorithm"
        )

    lines = [f"🗃️   **{len(cards)} Flashcard(s)**", BAR]
    for i, (front, back) in enumerate(cards, 1):
        lines += [f"**Card {i}**", f"     Q: {front}", f"     A: {back}", ""]

    lines += [BAR]
    if skipped:
        lines.append(f"⚠️   {len(skipped)} line(s) had no separator, so they're not cards:")
        for s in skipped[:5]:
            lines.append(f"     • {s[:70]}")
        if len(skipped) > 5:
            lines.append(f"     …and {len(skipped) - 5} more")
        lines.append(BAR)

    lines += [
        "💡  Test yourself **front to back and back to front**. Recognising a "
        "definition is easier than producing the term, and exams ask for both.",
        "💡  One idea per card. If an answer has three parts, it's three cards — "
        "otherwise you'll learn the first part and bluff the rest.",
        "💡  Cards you get right go to the back of the pile. Cards you get "
        "wrong come back within the same session.",
    ]
    return "\n".join(lines)

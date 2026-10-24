        lines.append("")
    lines += [
        BAR,
        "ðŸ’¡  Answer behavioural questions with STAR: Situation, Task, Action, Result.",
        "     End on the Result â€” with a number if you have one.",
        "ðŸ’¡  Prepare two questions to ask them. Not having any reads as disinterest.",
    ]
    return "\n".join(lines)


@tool
def skill_gap_analysis(target_role: str, current_skills: str) -> str:
    """
    Compare a person's current skills against a target role and list the gaps.

    Args:
        target_role: The job title being aimed at (e.g., 'data analyst').
        current_skills: Comma-separated skills they already have
                        (e.g., 'Python, SQL, Excel').
    """
    matched, required = _match_role(target_role)
    if not required:
        return (
            f"ðŸ”  I don't have a screened-skill list for '{target_role}'.\n"
            f"{BAR}\n"
            f"Roles I have mapped: {', '.join(sorted(ROLE_SKILLS))}.\n"
            f"Pick the closest one, or tell me the job description and I'll "
            f"work from that instead."
        )

    owned = [s.strip().lower() for s in current_skills.split(",") if s.strip()]
    have, missing = [], []
    for skill in required:
        blob = skill.lower()
        if any(_owns(blob, o) for o in owned):
            have.append(skill)
        else:
            missing.append(skill)

    pct = round(100 * len(have) / len(required))
    filled = "â–ˆ" * round(pct / 10) + "â–‘" * (10 - round(pct / 10))

    lines = [
        f"ðŸ”  **Skill Gap â€” {matched.title()}**",
        BAR,
        f"Readiness: {filled}  {pct}%   ({len(have)} of {len(required)} covered)",
        BAR,
    ]
    if have:
        lines.append("âœ…  **Already covered**")
        lines += [f"     â€¢ {s}" for s in have]
        lines.append("")
    if missing:
        lines.append("ðŸŽ¯  **Gaps to close**")
        lines += [f"     â€¢ {s}" for s in missing]
        lines.append("")
        lines += [
            BAR,
            "ðŸ“…  **Suggested order** â€” depth on one gap beats a shallow pass at all:",
        ]
        for i, s in enumerate(missing[:3], 1):
            head = s.split("â€”")[0].strip()
            lines.append(f"     Week {i * 2 - 1}â€“{i * 2}:  {head}  â†’  finish with one small artefact")
    else:
        lines.append("ðŸŽ‰  Every screened skill is covered. Shift your effort to "
                     "portfolio proof and interview practice.")

    lines += [
        BAR,
        "ðŸ’¡  A gap only counts as closed when you have something to show for it â€” "
        "a repo, a dashboard, a case study. Listing the skill isn't evidence.",
    ]
    return "\n".join(lines)


@tool
def draft_outreach(target_role: str, company: str) -> str:
    """
    Draft a cold email and a short LinkedIn connection note for a target job.

    Args:
        target_role: Role being applied for (e.g., 'junior data analyst').
        company: Company or team being contacted (e.g., 'Zomato').
    """
    role = target_role.strip().title()
    org = company.strip() or "[Company]"

    return (
        f"âœ‰ï¸   **Outreach Pack â€” {role} @ {org}**\n"
        f"{BAR}\n"
        f"ðŸ“§  **Cold email**\n"
        f"Subject: {role} â€” [one concrete thing you built]\n\n"
        f"Hi [Name],\n\n"
        f"I'm [Your Name], [one line: what you are and the single most relevant "
        f"thing you've done]. I'm reaching out about the {role} role at {org}.\n\n"
        f"Two things that seem relevant:\n"
        f"  â€¢ [Achievement with a number â€” what changed because of you]\n"
        f"  â€¢ [Skill or project that maps directly to their job description]\n\n"
        f"[One sentence showing you actually looked at {org} â€” a product "
        f"decision, a launch, something specific. Generic praise is worse than "
        f"none.]\n\n"
        f"I've attached my resume. Happy to send a short walkthrough of "
        f"[project] if useful.\n\n"
        f"Thanks for your time,\n"
        f"[Your Name] Â· [phone] Â· [portfolio link]\n"
        f"{BAR}\n"
        f"ðŸ”—  **LinkedIn note** (300-character limit â€” this is ~250)\n\n"
        f"Hi [Name] â€” I'm applying for the {role} opening at {org}. I've "
        f"[one-line proof: built X / analysed Y / shipped Z]. Would you be open "
        f"to a short chat about what the team is prioritising this quarter?\n"
        f"{BAR}\n"
        f"ðŸ’¡  Send to a person, not a careers inbox â€” the hiring manager or "
        f"someone already in the role.\n"
        f"ðŸ’¡  Follow up once after 5â€“7 working days, then stop.\n"
        f"ðŸ’¡  Replace every [ ] placeholder. An unedited template is obvious."
    )


@tool
def resume_checklist(experience_level: str) -> str:
    """
    Return a pre-submission resume checklist for a given experience level.

    Args:
        experience_level: 'fresher', 'mid' or 'senior' (also accepts
                          'student', 'entry', 'experienced', 'lead').
    """
    level = experience_level.strip().lower()
    if any(k in level for k in ("fresh", "student", "entry", "intern", "grad")):
        tier, specific = "Fresher / Entry-level", [
            "One page. No exceptions at this stage.",
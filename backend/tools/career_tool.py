from langchain.tools import tool


ROLE_SKILLS = {
    "data analyst": ["Python", "SQL", "Excel", "data visualization", "statistics"],
    "software engineer": ["Python", "Git", "testing", "APIs", "data structures"],
    "product manager": ["roadmaps", "user research", "analytics", "communication"],
}


def _role_skills(target_role: str) -> tuple[str, list[str]]:
    role = target_role.strip().lower()
    for name, skills in ROLE_SKILLS.items():
        if name in role or role in name:
            return name, skills
    return target_role.strip() or "target role", []


@tool
def skill_gap_analysis(target_role: str, current_skills: str) -> str:
    """Compare current skills with a small screened role profile."""
    role, required = _role_skills(target_role)
    if not required:
        return f"No screened profile is available for '{role}'. Provide a job description instead."
    owned = {skill.strip().lower() for skill in current_skills.split(",") if skill.strip()}
    covered = [skill for skill in required if skill.lower() in owned]
    missing = [skill for skill in required if skill.lower() not in owned]
    return (
        f"Skill gap for {role.title()}\n"
        f"Covered: {', '.join(covered) or 'none'}\n"
        f"Priority gaps: {', '.join(missing) or 'none'}"
    )


@tool
def draft_outreach(target_role: str, company: str) -> str:
    """Draft a concise outreach message for a target role."""
    role = target_role.strip() or "the open role"
    organisation = company.strip() or "your company"
    return (
        f"Subject: Interest in {role} at {organisation}\n\n"
        f"Hi [Name],\n\nI am reaching out about {role} at {organisation}. "
        "I would value the chance to share relevant work and learn more about "
        "the team's priorities.\n\nBest,\n[Your Name]"
    )


@tool
def resume_checklist(experience_level: str) -> str:
    """Return a practical resume review checklist."""
    level = experience_level.strip() or "your experience level"
    return (
        f"Resume checklist for {level}:\n"
        "- Lead with measurable outcomes.\n"
        "- Tailor keywords to the job description.\n"
        "- Keep formatting consistent and scannable.\n"
        "- Remove unsupported claims and stale technologies."
    )

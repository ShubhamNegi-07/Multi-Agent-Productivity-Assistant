"""
tools/career_tool.py
--------------------
Resume, interview-prep and job-search tools for the Career Agent.

These return deterministic scaffolding — diagnostics, checklists, question
banks — and leave the final wording to the agent. That split keeps the advice
consistent between runs while the prose stays natural.
"""

from langchain.tools import tool
import re


# ─── Reference data ───────────────────────────────────────────────────────────
# Target role → the skills that actually get screened for. Keys are lowercase
# and matched by longest substring, so "senior data analyst" resolves to
# "data analyst" instead of falling through to the generic branch.
ROLE_SKILLS = {
    "data analyst": [
        "SQL — joins, aggregations, window functions, CTEs",
        "Python (pandas, numpy) or R for cleaning and analysis",
        "Advanced spreadsheets — Excel or Google Sheets: pivots, lookups, models",
        "A BI tool — Power BI, Tableau or Looker Studio",
        "Statistics — distributions, hypothesis testing, A/B basics",
        "Stakeholder communication — turning a chart into a decision",
    ],
    "data scientist": [
        "Python (pandas, scikit-learn) and solid SQL",
        "Statistics and experiment design — power, p-values, confounders",
        "Feature engineering and model validation (cross-validation, leakage)",
        "One deep-learning framework — PyTorch or TensorFlow",
        "Communicating model limits to non-technical stakeholders",
        "Git and reproducible notebooks or pipelines",
    ],
    "machine learning engineer": [
        "Python plus strong software-engineering fundamentals",
        "PyTorch or TensorFlow, and model serving (FastAPI, TorchServe)",
        "MLOps — experiment tracking, model registry, CI for models",
        "Docker and at least one cloud (AWS / GCP / Azure)",
        "Data pipelines — Airflow, Spark or dbt",
        "Latency, cost and drift monitoring in production",
    ],
    "backend developer": [
        "One backend language deeply — Python, Java, Go or Node.js",
        "REST and/or gRPC API design, plus authentication patterns",
        "Databases — schema design, indexing, query tuning, transactions",
        "Caching and queues — Redis, Kafka or RabbitMQ",
        "Testing — unit, integration, and a CI pipeline",
        "Docker, and basic cloud deployment",
    ],
    "frontend developer": [
        "JavaScript/TypeScript fundamentals — async, closures, modules",
        "React (hooks, state management) or an equivalent framework",
        "HTML and CSS layout — flexbox, grid, responsive breakpoints",
        "Accessibility basics — semantics, keyboard nav, contrast",
        "Performance — bundle size, lazy loading, Core Web Vitals",
        "Testing — Jest / Vitest plus Playwright or Cypress",
    ],
    "full stack developer": [
        "One frontend framework and one backend language, both shipped",
        "Database design and an ORM, plus raw SQL when it matters",
        "API design and authentication/authorisation flows",
        "Git workflow, code review, and CI/CD",
        "Deployment — Docker, a cloud host, environment config",
        "Enough system design to justify your architecture in an interview",
    ],
    "software engineer": [
        "Data structures and algorithms — arrays, maps, trees, graphs, DP",
        "One language to real depth rather than five superficially",
        "System design fundamentals — caching, load balancing, sharding",
        "Git, code review etiquette, and writing tests",
        "Debugging and reading unfamiliar codebases",
        "Two or three portfolio projects you can defend in detail",
    ],
    "devops engineer": [
        "Linux administration and shell scripting",
        "Docker and Kubernetes",
        "Infrastructure as code — Terraform or Pulumi",
        "CI/CD pipelines — GitHub Actions, GitLab CI or Jenkins",
        "Observability — Prometheus, Grafana, centralised logging",
        "Cloud networking, IAM and cost awareness",
    ],
    "product manager": [
        "Problem framing and writing crisp product requirements",
        "User research — interviews, surveys, usability tests",
        "Metrics — funnels, retention, north-star definition",
        "Prioritisation frameworks and roadmap trade-offs",
        "Working fluently with engineering and design",
        "SQL or dashboard literacy so you aren't blocked on data requests",
    ],
    "ui ux designer": [
        "Figma to a professional standard — components, auto-layout, variants",
        "Interaction and visual design fundamentals — hierarchy, spacing, type",
        "User research and usability testing",
        "Design systems and handoff to engineers",
        "Accessibility — contrast, focus states, touch targets",
        "A portfolio with case studies showing process, not just screens",
    ],
    "business analyst": [
        "Requirements gathering and documentation (BRD / FRD, user stories)",
        "SQL and advanced spreadsheets",
        "Process mapping — BPMN or simple flowcharts",
        "Stakeholder management and workshop facilitation",
        "A BI tool for reporting",
        "Basic understanding of the domain you're applying into",
    ],
    "qa engineer": [
        "Manual test design — boundary, equivalence, negative cases",
        "Automation — Selenium, Playwright or Cypress",
        "API testing — Postman plus a code-driven client",
        "Bug reporting that a developer can act on without asking questions",
        "CI integration so tests run on every pull request",
        "Basic SQL for verifying data-layer behaviour",
    ],
}

# Openers that signal a job description rather than an achievement.
WEAK_OPENERS = (
    "responsible for", "worked on", "helped with", "involved in",
    "was tasked with", "duties included", "assisted in", "participated in",
    "took part in", "in charge of", "handled", "did ",
)

# Substrings that suggest the bullet actually states an outcome.
IMPACT_MARKERS = (
    "%", "increas", "decreas", "reduc", "improv", "sav", "grew", "growth",
    "cut ", "boost", "resulting in", "led to", "faster", "quicker", "revenue",
    "conversion", "retention", "accuracy", "uptime",
)

STRONG_VERBS = [
    "Built", "Shipped", "Led", "Designed", "Automated", "Streamlined",
    "Migrated", "Optimised", "Launched", "Rebuilt", "Scaled", "Cut",
    "Negotiated", "Mentored", "Owned", "Delivered",
]

BAR = "━" * 46


def _owns(skill_blob: str, owned_token: str) -> bool:
    """
    Does `owned_token` appear in `skill_blob` as a whole term?

    A plain substring test credits the wrong things: someone who knows **Go**
    matches "**Go**ogle Sheets", and "R" matches every "o**r**". The lookarounds
    demand a non-alphanumeric neighbour on each side, which keeps single-letter
    skills like R and C working while still allowing "c++" and "node.js", whose
    trailing characters aren't word characters at all.
    """
    token = owned_token.strip()
    if not token:
        return False
    return bool(
        re.search(rf"(?<![a-z0-9]){re.escape(token)}(?![a-z0-9])", skill_blob)
    )


def _match_role(target_role: str) -> tuple[str, list[str]]:
    """
    Resolve free text to a known role, longest key first.

    Longest-first matters: "machine learning engineer" contains neither
    "data scientist" nor "software engineer", but "senior backend developer"
    must not match on a shorter, wronger key.
    """
    needle = target_role.lower().replace("/", " ").replace("-", " ")
    for key in sorted(ROLE_SKILLS, key=len, reverse=True):
        if key in needle:
            return key, ROLE_SKILLS[key]
    # Loose second pass: any single distinctive word ("analyst", "devops").
    for key in sorted(ROLE_SKILLS, key=len, reverse=True):
        head = key.split()[-1]
        if head in needle:
            return key, ROLE_SKILLS[key]
    return "", []


@tool
def rewrite_resume_bullet(bullet: str) -> str:
    """
    Diagnose a weak resume bullet and return a rewrite scaffold.

    Args:
        bullet: The bullet point as currently written (e.g., 'Responsible for
                handling the college tech fest social media').
    """
    text = bullet.strip().strip("•-–— ")
    if not text:
        return "⚠️  No bullet provided. Paste the line you want rewritten."

    lower = text.lower()
    findings = []

    opener = next((w for w in WEAK_OPENERS if lower.startswith(w)), None)
    if opener:
        findings.append(
            f'⚠️   Opens with "{opener.strip()}" — that describes a duty, not '
            f"an achievement. Lead with a verb that shows you caused something."
        )
    else:
        findings.append("✅   Opens with an action rather than a job description.")

    if any(ch.isdigit() for ch in text):
        findings.append("✅   Contains a number a recruiter can anchor on.")
    else:
        findings.append(
            "⚠️   No number anywhere. Scope or scale it — people reached, hours "
            "saved, items handled, percent changed. An estimate beats nothing."
        )

    if any(m in lower for m in IMPACT_MARKERS):
        findings.append("✅   States an outcome, not just an activity.")
    else:
        findings.append(
            "⚠️   Stops at what you did and never says what changed as a result."
        )

    words = len(text.split())
    if words > 32:
        findings.append(
            f"⚠️   {words} words — long enough to get skimmed past. Aim for 12–24."
        )
    elif words < 6:
        findings.append(f"⚠️   Only {words} words — too thin to carry evidence.")
    else:
        findings.append(f"✅   {words} words — a readable length.")

    return (
        f"🧾  **Bullet Diagnostic**\n"
        f"{BAR}\n"
        f'Original: "{text}"\n'
        f"{BAR}\n"
        + "\n".join(findings)
        + f"\n{BAR}\n"
        f"🔁  **Rewrite formula (X–Y–Z)**\n"
        f"     [Strong verb] + [what you did] + [how / with what] + [measurable result]\n\n"
        f'     Skeleton:  "<verb> <the thing>, <method or tool>, '
        f'resulting in <number + unit>"\n'
        f"{BAR}\n"
        f"🎯  Verbs to choose from: {', '.join(STRONG_VERBS[:8])}\n"
        f"💡  If you genuinely have no metric, quantify the *scope* instead — "
        f"team size, audience, frequency, budget."
    )


@tool
def interview_questions(role: str, round_type: str) -> str:
    """
    Return likely interview questions for a role and interview round.

    Args:
        role: Target job title (e.g., 'backend developer', 'data analyst').
        round_type: Which round — 'technical', 'behavioral', 'hr', or 'all'.
    """
    matched, skills = _match_role(role)
    label = (matched or role).title()
    want = round_type.strip().lower() or "all"

    technical = [
        f"Walk me through a project on your resume that used {skills[0].split('—')[0].strip() if skills else 'your main skill'}.",
        "What part of that project would you build differently now, and why?",
        "Here's a problem with an obvious brute-force answer — find it, then improve it.",
        "How do you know your work is correct? Talk me through how you test it.",
        "Explain something from your field to me as if I'm not technical.",
        "What's a tool or concept you learned recently, entirely on your own?",
    ]
    behavioral = [
        "Tell me about a time you disagreed with a teammate. What happened?",
        "Describe a deadline you missed. What did you change afterwards?",
        "Tell me about the hardest bug or blocker you've worked through.",
        "When have you had to learn something quickly under pressure?",
        "Give me an example of feedback that stung but turned out to be right.",
        "Tell me about a time you took ownership of something nobody asked you to.",
    ]
    hr = [
        f"Why this role, and why {label} specifically rather than an adjacent one?",
        "Where do you want to be in three years?",
        "What are your salary expectations?",
        "Why are you leaving your current role / looking right now?",
        "What's your biggest weakness — and what are you doing about it?",
        "Do you have any questions for us?",
    ]

    blocks = []
    if want in ("technical", "tech", "all"):
        blocks.append(("🛠️   TECHNICAL", technical))
    if want in ("behavioral", "behavioural", "hr+behavioral", "all"):
        blocks.append(("🧠  BEHAVIOURAL", behavioral))
    if want in ("hr", "all"):
        blocks.append(("💬  HR / CLOSING", hr))
    if not blocks:
        blocks = [("🛠️   TECHNICAL", technical), ("🧠  BEHAVIOURAL", behavioral)]

    lines = [f"🎤  **Interview Prep — {label}**", BAR]
    for title, questions in blocks:
        lines.append(f"{title}")
        for i, q in enumerate(questions, 1):
            lines.append(f"  {i}.  {q}")
        lines.append("")
    lines += [
        BAR,
        "💡  Answer behavioural questions with STAR: Situation, Task, Action, Result.",
        "     End on the Result — with a number if you have one.",
        "💡  Prepare two questions to ask them. Not having any reads as disinterest.",
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
            f"🔍  I don't have a screened-skill list for '{target_role}'.\n"
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
    filled = "█" * round(pct / 10) + "░" * (10 - round(pct / 10))

    lines = [
        f"🔍  **Skill Gap — {matched.title()}**",
        BAR,
        f"Readiness: {filled}  {pct}%   ({len(have)} of {len(required)} covered)",
        BAR,
    ]
    if have:
        lines.append("✅  **Already covered**")
        lines += [f"     • {s}" for s in have]
        lines.append("")
    if missing:
        lines.append("🎯  **Gaps to close**")
        lines += [f"     • {s}" for s in missing]
        lines.append("")
        lines += [
            BAR,
            "📅  **Suggested order** — depth on one gap beats a shallow pass at all:",
        ]
        for i, s in enumerate(missing[:3], 1):
            head = s.split("—")[0].strip()
            lines.append(f"     Week {i * 2 - 1}–{i * 2}:  {head}  →  finish with one small artefact")
    else:
        lines.append("🎉  Every screened skill is covered. Shift your effort to "
                     "portfolio proof and interview practice.")

    lines += [
        BAR,
        "💡  A gap only counts as closed when you have something to show for it — "
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
        f"✉️   **Outreach Pack — {role} @ {org}**\n"
        f"{BAR}\n"
        f"📧  **Cold email**\n"
        f"Subject: {role} — [one concrete thing you built]\n\n"
        f"Hi [Name],\n\n"
        f"I'm [Your Name], [one line: what you are and the single most relevant "
        f"thing you've done]. I'm reaching out about the {role} role at {org}.\n\n"
        f"Two things that seem relevant:\n"
        f"  • [Achievement with a number — what changed because of you]\n"
        f"  • [Skill or project that maps directly to their job description]\n\n"
        f"[One sentence showing you actually looked at {org} — a product "
        f"decision, a launch, something specific. Generic praise is worse than "
        f"none.]\n\n"
        f"I've attached my resume. Happy to send a short walkthrough of "
        f"[project] if useful.\n\n"
        f"Thanks for your time,\n"
        f"[Your Name] · [phone] · [portfolio link]\n"
        f"{BAR}\n"
        f"🔗  **LinkedIn note** (300-character limit — this is ~250)\n\n"
        f"Hi [Name] — I'm applying for the {role} opening at {org}. I've "
        f"[one-line proof: built X / analysed Y / shipped Z]. Would you be open "
        f"to a short chat about what the team is prioritising this quarter?\n"
        f"{BAR}\n"
        f"💡  Send to a person, not a careers inbox — the hiring manager or "
        f"someone already in the role.\n"
        f"💡  Follow up once after 5–7 working days, then stop.\n"
        f"💡  Replace every [ ] placeholder. An unedited template is obvious."
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
            "Projects section sits *above* work experience — it's your evidence.",
            "3–4 projects, each with what it does, the stack, and an outcome.",
            "Include internships, freelance work, college fests, club roles — "
            "anything where you owned a result.",
            "Drop the objective statement. Use the space for a project instead.",
            "Keep education (degree, institute, year). CGPA only if it's strong.",
        ]
    elif any(k in level for k in ("senior", "lead", "manager", "principal", "8", "9", "10")):
        tier, specific = "Senior / Lead", [
            "Two pages is fine. Three is not.",
            "Lead with scope: team size, systems owned, budget, blast radius.",
            "Show decisions and trade-offs, not task lists.",
            "Include mentoring, hiring and cross-team influence.",
            "Push work older than ~10 years into a one-line 'Earlier' section.",
            "Education drops to the bottom — your track record outranks it.",
        ]
    else:
        tier, specific = "Mid-level", [
            "One page if you can, two at most.",
            "Work experience first; projects become a supporting section.",
            "3–5 bullets per role, ordered most impressive first.",
            "Show progression — scope or ownership growing across roles.",
            "Cut college-era projects unless they're still your best work.",
            "Name the tools you'd be hired for, in the words the job ad uses.",
        ]

    universal = [
        "Every bullet starts with a past-tense action verb — no 'Responsible for'.",
        "At least half your bullets carry a number.",
        "No pronouns, no full stops at the end of bullets (be consistent either way).",
        "One font, one accent colour, consistent date format throughout.",
        "No photo, no age, no marital status, no 'References available on request'.",
        "Filename: FirstName_LastName_Role.pdf — not resume_final_v3.pdf.",
        "Exported as PDF, with selectable text (screenshots break ATS parsing).",
        "Skills match the job description's vocabulary — ATS matches on strings.",
        "Read it aloud once. Anything you stumble over, a recruiter will too.",
    ]

    lines = [f"📄  **Resume Checklist — {tier}**", BAR, f"🎯  **For your level**"]
    lines += [f"     ☐  {item}" for item in specific]
    lines += ["", f"✅  **Applies to everyone**"]
    lines += [f"     ☐  {item}" for item in universal]
    lines += [
        BAR,
        "💡  Tailor per application. One generic resume sent to 50 companies "
        "loses to five tailored ones.",
    ]
    return "\n".join(lines)

"""
app.py
------
Streamlit frontend for the Multi-Agent Productivity Assistant.

Chat-first rework:
  * Conversation reads top-to-bottom, newest at the bottom.
  * Composer is `st.chat_input`, pinned to the bottom of the viewport.
  * User turns are right-aligned ink bubbles; agent turns are left-aligned
    cards badged with the agent's avatar, name and response time.
  * Agents are picked from the sidebar; every turn stays in one shared
    thread so you can see which agent answered what.

Note on memory: the `run_*_agent` functions are stateless — they take a
single query string and return a string. The "Conversation memory" toggle
stitches recent turns into the prompt so follow-ups ("what should I pack?")
resolve against the earlier answer. Turn it off for one-shot questions.
"""

import html
import time

import streamlit as st

# ─── Page Configuration ───────────────────────────────────────────────────────
st.set_page_config(
    page_title="Assistant Hub",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Agent Configuration ──────────────────────────────────────────────────────
# Keyed by agent id so the sidebar nav, session state and history entries all
# refer to agents by the same stable token.
AGENTS = {
    "weather": {
        "id": "weather",
        "name": "Weather Agent",
        "icon": "🌤️",
        "color": "#0369A1",
        "greeting": "Good day, Creator",
        "tagline": "Watching the skies so your plans don't get rained on.",
        "examples": [
            "Will there be any extreme weather alerts this week?",
            "Is it safe to travel tomorrow based on weather conditions?",
            "Tell me the best time of day to go out today based on heat and sunlight.",
        ],
    },
    "travel": {
        "id": "travel",
        "name": "Travel Agent",
        "icon": "✈️",
        "color": "#15803D",
        "greeting": "Ready for the next trip, Creator",
        "tagline": "Here to turn 'someday' into an itinerary.",
        "examples": [
            "Create a detailed itinerary for Kedarnath with time, cost, and difficulty level.",
            "Suggest a solo trip plan for a beginner traveler from Dehradun.",
            "Give me a packing checklist based on destination, weather, and trip duration.",
        ],
    },
    "finance": {
        "id": "finance",
        "name": "Finance Agent",
        "icon": "💰",
        "color": "#B45309",
        "greeting": "Let's talk money, Creator",
        "tagline": "On your side, one smart rupee at a time.",
        "examples": [
            "Help me plan an emergency fund step-by-step.",
            "How can I save ₹1 lakh in 12 months with my current spending habits?",
            "Suggest how I can reduce unnecessary spending without affecting my lifestyle.",
        ],
    },
    "productivity": {
        "id": "productivity",
        "name": "Productivity Agent",
        "icon": "📋",
        "color": "#7E22CE",
        "greeting": "Let's get things done, Creator",
        "tagline": "Turns your chaos into a clean checklist.",
        "examples": [
            "Plan my entire week with time-blocking for college, coding practice, and gym.",
            "Draft a professional sick leave email to my manager.",
            "Turn my messy notes into a clean, actionable to-do list with priorities.",
        ],
    },
    "career": {
        "id": "career",
        "name": "Career Agent",
        "icon": "💼",
        "color": "#4338CA",
        "greeting": "Let's build the next step, Creator",
        "tagline": "Sharpening your resume, one bullet at a time.",
        "examples": [
            "Rewrite this bullet: 'Responsible for handling the college tech fest social media.'",
            "I know Python, SQL and Excel — what am I missing for a data analyst role?",
            "Give me the questions I'll actually be asked for a fresher backend interview.",
        ],
    },
    "health": {
        "id": "health",
        "name": "Health Agent",
        "icon": "🏃",
        "color": "#0F766E",
        "greeting": "Let's look after you, Creator",
        "tagline": "Small daily habits, tracked properly.",
        "examples": [
            "I'm 21, 72 kg, 178 cm and moderately active — what should my daily calories be?",
            "Build me a 4-day gym split for strength that fits around college hours.",
            "How much water and sleep should I be getting at my weight?",
        ],
    },
}

# How much prior conversation to hand back to a (stateless) agent.
MEMORY_TURNS = 6
MEMORY_CHARS = 700

# ─── Session State ────────────────────────────────────────────────────────────
# Initialised before the stylesheet on purpose: the active agent's accent is
# baked straight into the nav CSS below, so `active` has to be known first.
_DEFAULTS = {
    "history": [],        # list of message dicts, oldest first
    "active": "weather",  # currently selected agent id
    "pending": None,      # query awaiting an agent run
    "pending_agent": None,
    "remember": True,     # stitch prior turns into the prompt
}
for _key, _val in _DEFAULTS.items():
    if _key not in st.session_state:
        st.session_state[_key] = _val

processing = st.session_state.pending is not None

# ─── Design System ────────────────────────────────────────────────────────────
BASE_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Instrument+Serif:ital@0;1&display=swap');

:root {
    --canvas:    #F7F6F3;
    --surface:   #FFFFFF;
    --line:      #E4E0D7;
    --line-soft: #EDEAE3;
    --ink:       #191817;
    --ink-2:     #5B574F;
    --ink-3:     #918C82;
    --user-bg:   #1F1E1C;
    --user-ink:  #FAF9F6;
    --danger:    #B42318;
    --radius:    18px;
    --shadow:    0 1px 2px rgba(25, 24, 23, .04), 0 10px 28px rgba(25, 24, 23, .05);
    --col:       860px;
}

/* ── Streamlit chrome ────────────────────────────────────────────────────────
   Do NOT blanket-hide `header`: [data-testid="stHeader"] is where Streamlit
   mounts the *expand sidebar* button once the sidebar is collapsed, and
   visibility:hidden inherits — the button stays in the DOM and still works,
   but is invisible and unclickable, so a closed sidebar can never be
   reopened. Hide the individual toolbar bits instead and keep the header as a
   slim solid band holding the sidebar toggle. */
[data-testid="stToolbarActions"],
[data-testid="stAppDeployButton"],
[data-testid="stMainMenu"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"],
#MainMenu,
footer {
    display: none !important;
}

/* Header is position:absolute, so it reserves no space — .block-container's
   top padding below is what keeps content clear of it. Opaque canvas fill so
   the transcript scrolls *behind* it rather than showing through. 3.75rem is
   Streamlit's own header height; matching it beats overriding it. */
[data-testid="stHeader"] {
    background: var(--canvas);
}

/* Sidebar open/close controls: quiet by default, ink on hover.
   Both forms are listed on purpose — Streamlit puts the testid directly on the
   <button> for the expand control but on a *wrapper* for the collapse control,
   so a single descendant selector would silently miss one of them. */
button[data-testid="stExpandSidebarButton"],
[data-testid="stExpandSidebarButton"] button,
button[data-testid="stSidebarCollapseButton"],
[data-testid="stSidebarCollapseButton"] button {
    color: var(--ink-2) !important;
    border-radius: 9px !important;
}
button[data-testid="stExpandSidebarButton"]:hover,
[data-testid="stExpandSidebarButton"] button:hover,
button[data-testid="stSidebarCollapseButton"]:hover,
[data-testid="stSidebarCollapseButton"] button:hover {
    color: var(--ink) !important;
    background: var(--line-soft) !important;
}

.block-container {
    max-width: var(--col);
    padding: 4rem 1.5rem 8rem 1.5rem;
}

/* ── Sticky agent header ─────────────────────────────────────────────────── */
.topbar {
    position: sticky;
    top: 3.75rem;           /* flush under Streamlit's 60px header band */
    z-index: 5;
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px 2px 14px 2px;
    margin-bottom: 6px;
    background: linear-gradient(to bottom, var(--canvas) 68%, rgba(247, 246, 243, 0));
    backdrop-filter: blur(6px);
}
.topbar-name {
    font-size: 1.02rem;
    font-weight: 650;
    letter-spacing: -0.01em;
    color: var(--ink);
    line-height: 1.2;
}
.topbar-tag {
    font-size: 0.82rem;
    color: var(--ink-2);
    line-height: 1.3;
    margin-top: 2px;
}

/* ── Avatars ─────────────────────────────────────────────────────────────── */
.avatar {
    flex-shrink: 0;
    width: 30px;
    height: 30px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.95rem;
    background: #F0EEE8;
    background: color-mix(in srgb, var(--accent, #918C82) 13%, #FFFFFF);
    border: 1px solid var(--line);
    border-color: color-mix(in srgb, var(--accent, #918C82) 26%, #FFFFFF);
}
.avatar-lg { width: 38px; height: 38px; border-radius: 12px; font-size: 1.15rem; }

/* ── Message rows ────────────────────────────────────────────────────────── */
.row { display: flex; gap: 10px; margin: 0 0 14px 0; animation: rise .22s ease-out; }
.row-user { justify-content: flex-end; }
.row-agent { justify-content: flex-start; align-items: flex-start; }

@keyframes rise {
    from { opacity: 0; transform: translateY(6px); }
    to   { opacity: 1; transform: none; }
}

.bubble {
    max-width: 78%;
    padding: 11px 15px;
    font-size: 0.945rem;
    line-height: 1.62;
    overflow-wrap: break-word;
    word-break: break-word;
}

.bubble-user {
    background: var(--user-bg);
    color: var(--user-ink);
    border-radius: var(--radius) var(--radius) 5px var(--radius);
    font-weight: 450;
}

.bubble-agent {
    max-width: calc(100% - 40px);
    background: var(--surface);
    color: var(--ink);
    border: 1px solid var(--line);
    border-radius: var(--radius) var(--radius) var(--radius) 5px;
    box-shadow: var(--shadow);
    padding: 12px 16px 13px 16px;
}
.bubble-agent.is-error {
    border-color: color-mix(in srgb, var(--danger) 35%, #FFFFFF);
    background: color-mix(in srgb, var(--danger) 4%, #FFFFFF);
}

/* Agent name / timing strip above the answer */
.meta {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 7px;
    padding-bottom: 7px;
    border-bottom: 1px solid var(--line-soft);
}
.meta-who {
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.07em;
    text-transform: uppercase;
    color: var(--accent, var(--ink-2));
}
.meta-time {
    margin-left: auto;
    font-size: 0.7rem;
    font-weight: 600;
    color: var(--ink-3);
    font-variant-numeric: tabular-nums;
}

/* Tame markdown that Streamlit renders *inside* a bubble */
.bubble > :first-child { margin-top: 0; }
.bubble > :last-child  { margin-bottom: 0; }
.bubble p { margin: 0 0 0.7em 0; }
.bubble p:last-child { margin-bottom: 0; }
.bubble ul, .bubble ol { margin: 0.4em 0 0.7em 0; padding-left: 1.35em; }
.bubble li { margin-bottom: 0.28em; }
.bubble li::marker { color: var(--ink-3); }
.bubble h1, .bubble h2, .bubble h3, .bubble h4 {
    font-size: 0.95rem;
    font-weight: 680;
    letter-spacing: -0.005em;
    margin: 0.9em 0 0.35em 0;
    padding: 0;
    color: var(--ink);
}
.bubble strong { font-weight: 660; }
.bubble code {
    font-size: 0.86em;
    background: #F4F2EC;
    padding: 0.1em 0.35em;
    border-radius: 5px;
}
.bubble table { font-size: 0.88rem; border-collapse: collapse; margin: 0.5em 0; }
.bubble th, .bubble td { border: 1px solid var(--line); padding: 5px 9px; text-align: left; }
.bubble th { background: #F7F6F3; font-weight: 650; }
.bubble hr { border: 0; border-top: 1px solid var(--line-soft); margin: 0.9em 0; }

/* ── Typing indicator ───────────────────────────────────────────────────── */
.typing { display: inline-flex; align-items: center; gap: 5px; height: 20px; }
.typing i {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--ink-3);
    animation: pulse 1.15s infinite ease-in-out;
}
.typing i:nth-child(2) { animation-delay: 0.15s; }
.typing i:nth-child(3) { animation-delay: 0.30s; }
@keyframes pulse {
    0%, 75%, 100% { opacity: 0.22; transform: translateY(0); }
    35%           { opacity: 1;    transform: translateY(-3px); }
}

/* ── Empty state ────────────────────────────────────────────────────────── */
.hero {
    padding: 4.5rem 0 1.6rem 0;
    text-align: center;
}
/* Deliberately a div, not an <h1>: Streamlit wraps real headings in
   stHeadingWithActionElements and styles them with the theme font at a
   specificity that beats a plain class, which silently killed the serif. */
.hero-title {
    font-family: 'Instrument Serif', Georgia, 'Times New Roman', serif;
    font-size: 2.7rem;
    font-weight: 400;
    line-height: 1.14;
    letter-spacing: -0.015em;
    color: var(--ink);
    margin: 0;
}
.eyebrow {
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--ink-3);
    margin: 1.6rem 0 0.7rem 2px;
}

/* Example prompts: left-aligned, quiet until hovered */
.st-key-examples button {
    justify-content: flex-start !important;
    text-align: left !important;
    width: 100%;
    background: var(--surface) !important;
    border: 1px solid var(--line) !important;
    color: var(--ink-2) !important;
    font-size: 0.885rem !important;
    font-weight: 450 !important;
    line-height: 1.45 !important;
    padding: 11px 14px !important;
    margin-bottom: 8px;
    box-shadow: 0 1px 2px rgba(25, 24, 23, .03);
    transition: border-color .15s, color .15s, transform .15s;
}
.st-key-examples button:hover {
    color: var(--ink) !important;
    border-color: var(--ink-3) !important;
    transform: translateX(2px);
}
.st-key-examples button p { text-align: left !important; }

/* ── Sidebar ────────────────────────────────────────────────────────────── */
[data-testid="stSidebar"] { padding-top: 1.05rem; }

/* Streamlit's default 1rem gap between elements made a six-agent list scroll
   for no reason. Tighten it once here and let each label's own margin do the
   grouping, so spacing is set in one place instead of fought per widget. */
[data-testid="stSidebar"] [data-testid="stVerticalBlock"] { gap: 0.3rem; }
[data-testid="stSidebarUserContent"] { padding-bottom: 1.6rem; }

.brand {
    display: flex;
    align-items: center;
    gap: 9px;
    margin: 0 0 0.25rem 2px;
}
.brand-mark {
    flex-shrink: 0;
    width: 27px;
    height: 27px;
    border-radius: 9px;
    background: var(--user-bg);
    color: var(--user-ink);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.82rem;
}
.brand-name {
    font-size: 0.98rem;
    font-weight: 680;
    letter-spacing: -0.01em;
    color: var(--ink);
}
.brand-sub {
    font-size: 0.745rem;
    color: var(--ink-3);
    line-height: 1.45;
    margin: 0 0 0.95rem 2px;
}

/* "New chat" is the only filled action in the sidebar — a card, so it reads as
   a control rather than another nav row. */
[data-testid="stSidebar"] .st-key-new_chat button {
    justify-content: flex-start !important;
    text-align: left !important;
    background: var(--surface) !important;
    border: 1px solid var(--line) !important;
    color: var(--ink) !important;
    font-size: 0.875rem !important;
    font-weight: 550 !important;
    padding: 9px 11px !important;
    box-shadow: 0 1px 2px rgba(25, 24, 23, .04);
    transition: border-color .14s, transform .14s;
}
[data-testid="stSidebar"] .st-key-new_chat button:hover:not(:disabled) {
    border-color: var(--ink-3) !important;
}
[data-testid="stSidebar"] .st-key-new_chat button:disabled {
    opacity: 0.42;
    box-shadow: none;
}

/* Section label with a trailing hairline, which visually brackets the list
   under it without needing a container or a divider element. */
.side-label {
    display: flex;
    align-items: center;
    gap: 7px;
    font-size: 0.655rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--ink-3);
    margin: 1.2rem 0 0.5rem 2px;
}
.side-label::after {
    content: "";
    flex: 1;
    height: 1px;
    background: var(--line);
}
.side-count {
    font-size: 0.615rem;
    font-weight: 700;
    letter-spacing: 0;
    color: var(--ink-3);
    background: var(--line-soft);
    border: 1px solid var(--line);
    border-radius: 5px;
    padding: 0 5px;
}

/* ── Agent nav ────────────────────────────────────────────────────────────
   Every row is the same shape — the accent alone carries selection, so the
   list stays a list instead of one heavy slab among five ghosts.

   The transparent 1px border is load-bearing: the per-agent rules below set
   only `border-color`, and on a Streamlit `tertiary` button (border: none)
   a bare border-color paints nothing, so the hover accent never appeared. */
[data-testid="stSidebar"] [class*="st-key-nav_"] button {
    justify-content: flex-start !important;
    text-align: left !important;
    font-size: 0.885rem !important;
    font-weight: 500 !important;
    padding: 9px 11px !important;
    border: 1px solid transparent !important;
    background: transparent !important;
    color: var(--ink-2) !important;
    box-shadow: none !important;
    transition: background .14s, border-color .14s, color .14s;
}
[data-testid="stSidebar"] [class*="st-key-nav_"] button p {
    text-align: left !important;
    font-weight: inherit !important;
}
[data-testid="stSidebar"] [class*="st-key-nav_"] button:disabled {
    opacity: 0.4;
}

/* Widget labels (the memory toggle) — match the nav's text weight */
[data-testid="stSidebar"] label p {
    font-size: 0.845rem !important;
    color: var(--ink-2) !important;
}

.side-foot {
    display: flex;
    align-items: center;
    gap: 6px;
    margin-top: 0.7rem;
    font-size: 0.735rem;
    color: var(--ink-3);
    line-height: 1.5;
    padding-left: 2px;
}
.side-foot::before {
    content: "";
    width: 5px;
    height: 5px;
    border-radius: 50%;
    background: var(--line);
    flex-shrink: 0;
}
.side-foot.is-live::before { background: #15803D; }

/* ── Composer (pinned chat input) ───────────────────────────────────────── */
[data-testid="stBottomBlockContainer"] {
    max-width: calc(var(--col) + 3rem);
    padding-bottom: 1.1rem;
}
[data-testid="stChatInput"] {
    border: 1px solid var(--line) !important;
    border-radius: 15px !important;
    background: var(--surface) !important;
    box-shadow: var(--shadow);
}
[data-testid="stChatInput"]:focus-within {
    border-color: var(--ink-3) !important;
}
[data-testid="stChatInput"] textarea { font-size: 0.945rem !important; }
[data-testid="stChatInput"] textarea::placeholder { color: var(--ink-3) !important; opacity: 1; }

/* ── Accessibility ──────────────────────────────────────────────────────── */
button:focus-visible,
textarea:focus-visible,
input:focus-visible {
    outline: 2px solid #0F766E !important;
    outline-offset: 2px;
}

@media (prefers-reduced-motion: reduce) {
    .row { animation: none; }
    .typing i { animation: none; opacity: 0.5; }
    .st-key-examples button:hover { transform: none; }
}

@media (max-width: 640px) {
    .block-container { padding: 4rem 0.9rem 7rem 0.9rem; }
    .bubble { max-width: 88%; font-size: 0.92rem; }
    .bubble-agent { max-width: calc(100% - 40px); }
    .hero { padding: 2.5rem 0 1.2rem 0; }
    .hero-title { font-size: 2rem; }
}
</style>
"""

st.markdown(BASE_CSS, unsafe_allow_html=True)

# Per-agent accent on the sidebar nav buttons. Streamlit stamps a
# `st-key-<key>` class on each keyed widget's container, so each agent's button
# carries its own colour without any fragile nth-child selectors.
#
# The *selected* agent is styled here too rather than through Streamlit's
# `type="primary"`, which paints a flat black slab from theme.primaryColor and
# ignores the agent's own colour entirely. Emitting the rule for whichever id is
# active keeps all six rows one shape and lets the accent carry the state.
_nav_css = ["<style>"]
for _a in AGENTS.values():
    _sel = f'[data-testid="stSidebar"] .st-key-nav_{_a["id"]} button'
    if _a["id"] == st.session_state.active:
        # `transition: none` is deliberate. Streamlit's own primary styling paints
        # the dark slab first, so with the base rule's 0.14s colour transition
        # still in force the selected row visibly fades black → accent on every
        # load and rerun. The active row never changes state without a rerun
        # anyway, so it has nothing to animate — only the hover rows below do.
        _nav_css.append(
            f"{_sel}, {_sel}:hover {{"
            f"  background: color-mix(in srgb, {_a['color']} 11%, #FFFFFF) !important;"
            f"  border-color: color-mix(in srgb, {_a['color']} 30%, #FFFFFF) !important;"
            f"  color: {_a['color']} !important;"
            f"  font-weight: 620 !important;"
            f"  box-shadow: inset 3px 0 0 0 {_a['color']} !important;"
            f"  transition: none !important;"
            f"}}"
        )
    else:
        _nav_css.append(
            f"{_sel}:hover:not(:disabled) {{"
            f"  background: color-mix(in srgb, {_a['color']} 6%, #FFFFFF) !important;"
            f"  border-color: color-mix(in srgb, {_a['color']} 34%, #FFFFFF) !important;"
            f"  color: {_a['color']} !important;"
            f"}}"
        )
_nav_css.append("</style>")
st.markdown("".join(_nav_css), unsafe_allow_html=True)


# ─── Lazy import helpers ──────────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_agent(agent_key: str):
    """Import and return an agent's run function on first use."""
    if agent_key == "weather":
        from agents.weather_agent import run_weather_agent
        return run_weather_agent
    elif agent_key == "travel":
        from agents.travel_agent import run_travel_agent
        return run_travel_agent
    elif agent_key == "finance":
        from agents.finance_agent import run_finance_agent
        return run_finance_agent
    elif agent_key == "productivity":
        from agents.productivity_agent import run_productivity_agent
        return run_productivity_agent
    elif agent_key == "career":
        from agents.career_agent import run_career_agent
        return run_career_agent
    elif agent_key == "health":
        from agents.health_agent import run_health_agent
        return run_health_agent
    else:
        raise ValueError(f"Unknown agent key: {agent_key}")


# ─── Rendering Helpers ────────────────────────────────────────────────────────
def user_bubble(text: str) -> str:
    """Right-aligned ink bubble. Text is escaped — user input is never markdown."""
    safe = html.escape(text).replace("\n", "<br>")
    return f'<div class="row row-user"><div class="bubble bubble-user">{safe}</div></div>'


def agent_bubble_open(agent: dict, elapsed: str, is_error: bool = False) -> str:
    """
    Opening half of an agent bubble, up to (and including) the meta strip.

    The response itself is markdown, so it has to sit between blank lines in
    the *same* st.markdown call: a blank line closes the raw-HTML block, the
    markdown gets parsed, then the closing tags reopen as HTML. Splitting this
    across calls is what used to leave responses rendering outside their card.
    """
    err = " is-error" if is_error else ""
    return (
        f'<div class="row row-agent" style="--accent: {agent["color"]};">'
        f'<div class="avatar">{agent["icon"]}</div>'
        f'<div class="bubble bubble-agent{err}">'
        f'<div class="meta">'
        f'<span class="meta-who">{html.escape(agent["name"])}</span>'
        f'<span class="meta-time">{html.escape(elapsed)}</span>'
        f"</div>"
    )


AGENT_BUBBLE_CLOSE = "</div></div>"


def render_agent_message(agent: dict, body: str, elapsed: str, is_error: bool = False) -> str:
    return f"{agent_bubble_open(agent, elapsed, is_error)}\n\n{body}\n\n{AGENT_BUBBLE_CLOSE}"


def build_agent_input(query: str, prior: list) -> str:
    """
    Fold recent turns into the prompt.

    The `run_*_agent` functions take one string and keep no state, so a bare
    follow-up like "what should I pack?" would otherwise arrive with no
    referent. This prepends a trimmed transcript instead.
    """
    if not st.session_state.remember:
        return query

    usable = [m for m in prior if not m.get("error")]
    if not usable:
        return query

    lines = []
    for msg in usable[-MEMORY_TURNS:]:
        body = msg["content"].strip()
        if len(body) > MEMORY_CHARS:
            body = body[:MEMORY_CHARS].rstrip() + "…"
        who = "User" if msg["role"] == "user" else f"Assistant ({msg.get('agent', 'Assistant')})"
        lines.append(f"{who}: {body}")

    transcript = "\n".join(lines)
    return (
        "[Earlier conversation, for context only — do not repeat it back]\n"
        f"{transcript}\n\n"
        "[Current message]\n"
        f"{query}"
    )


def submit(query: str, agent_id: str) -> None:
    """Queue a turn and rerun so the user's bubble paints before the agent runs."""
    st.session_state.history.append({"role": "user", "content": query})
    st.session_state.pending = query
    st.session_state.pending_agent = agent_id
    st.rerun()


# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        '<div class="brand">'
        '<div class="brand-mark" aria-hidden="true">✨</div>'
        '<span class="brand-name">Assistant Hub</span>'
        "</div>"
        f'<div class="brand-sub">{len(AGENTS)} specialists, one shared thread</div>',
        unsafe_allow_html=True,
    )

    if st.button(
        "New chat",
        icon=":material/add:",
        width="stretch",
        disabled=processing or not st.session_state.history,
        key="new_chat",
    ):
        st.session_state.history = []
        st.rerun()

    st.markdown(
        f'<div class="side-label">Agents'
        f'<span class="side-count">{len(AGENTS)}</span></div>',
        unsafe_allow_html=True,
    )

    for agent_id, agent in AGENTS.items():
        is_active = agent_id == st.session_state.active
        # `primary` on the active row is kept purely as a DOM signal — it gives
        # assistive tech a real attribute difference (kind="primary") rather
        # than colour alone. The nav CSS above overrides how it looks.
        if st.button(
            f"{agent['icon']}  {agent['name']}",
            key=f"nav_{agent_id}",
            type="primary" if is_active else "tertiary",
            width="stretch",
            disabled=processing,
            help=agent["tagline"],
        ):
            st.session_state.active = agent_id
            st.rerun()

    st.markdown('<div class="side-label">Thread</div>', unsafe_allow_html=True)

    st.toggle(
        "Conversation memory",
        key="remember",
        disabled=processing,
        help=(
            "Sends recent turns along with your message so follow-up questions "
            "keep their context. Turn off for independent one-shot questions."
        ),
    )

    turns = sum(1 for m in st.session_state.history if m["role"] == "user")
    st.markdown(
        f'<div class="side-foot{" is-live" if turns else ""}">'
        f'{turns if turns else "No"} message{"" if turns == 1 else "s"} in this thread'
        f"</div>",
        unsafe_allow_html=True,
    )

active = AGENTS[st.session_state.active]

# ─── Agent Header ─────────────────────────────────────────────────────────────
# One aria-live region so switching agents is announced to screen readers —
# Streamlit reruns the whole script on the nav click, so this updates at once.
st.markdown(
    f'<div class="topbar" role="status" aria-live="polite" aria-atomic="true" '
    f'style="--accent: {active["color"]};">'
    f'<div class="avatar avatar-lg" aria-hidden="true">{active["icon"]}</div>'
    f"<div>"
    f'<div class="topbar-name">{html.escape(active["name"])}</div>'
    f'<div class="topbar-tag">{html.escape(active["tagline"])}</div>'
    f"</div>"
    f"</div>",
    unsafe_allow_html=True,
)

# ─── Transcript ───────────────────────────────────────────────────────────────
for msg in st.session_state.history:
    if msg["role"] == "user":
        st.markdown(user_bubble(msg["content"]), unsafe_allow_html=True)
    else:
        st.markdown(
            render_agent_message(
                AGENTS.get(msg["agent_id"], active),
                msg["content"],
                msg.get("elapsed", ""),
                msg.get("error", False),
            ),
            unsafe_allow_html=True,
        )

# ─── Empty State ──────────────────────────────────────────────────────────────
if not st.session_state.history:
    st.markdown(
        f'<div class="hero">'
        f'<div class="hero-title" role="heading" aria-level="1">'
        f'{html.escape(active["greeting"])}</div>'
        f"</div>"
        f'<div class="eyebrow">Try one of these</div>',
        unsafe_allow_html=True,
    )

    with st.container(key="examples"):
        for i, example in enumerate(active["examples"]):
            if st.button(example, key=f"ex_{st.session_state.active}_{i}", width="stretch"):
                submit(example, st.session_state.active)

# ─── Composer ─────────────────────────────────────────────────────────────────
# `st.chat_input` pins itself to the bottom of the viewport regardless of where
# it is declared, so it goes *before* the agent call below: the run block ends
# in st.rerun(), and anything declared after it would never render on a
# processing pass — leaving an enabled composer on screen mid-answer, where a
# second submit would discard the in-flight response.
prompt = st.chat_input(
    f"Message {active['name']}…",
    disabled=processing,
    key="composer",
)

if prompt and prompt.strip():
    submit(prompt.strip(), st.session_state.active)

# ─── Run the queued turn ──────────────────────────────────────────────────────
# The user's bubble is already on screen from submit()'s rerun, so the typing
# placeholder lands directly beneath it while the (blocking) agent call runs.
if processing:
    pending_agent = AGENTS[st.session_state.pending_agent]
    query = st.session_state.pending

    slot = st.empty()
    slot.markdown(
        f'<div class="row row-agent" style="--accent: {pending_agent["color"]};">'
        f'<div class="avatar">{pending_agent["icon"]}</div>'
        f'<div class="bubble bubble-agent">'
        f'<div class="typing" role="status" aria-label="{pending_agent["name"]} is thinking">'
        f"<i></i><i></i><i></i></div>"
        f"</div></div>",
        unsafe_allow_html=True,
    )

    # history[-1] is the user turn we just queued; everything before it is context.
    prior = st.session_state.history[:-1]
    entry = {
        "role": "assistant",
        "agent": pending_agent["name"],
        "agent_id": pending_agent["id"],
    }

    try:
        started = time.time()
        run_fn = load_agent(pending_agent["id"])
        answer = run_fn(build_agent_input(query, prior))
        entry["content"] = answer
        entry["elapsed"] = f"{time.time() - started:.2f}s"
    except EnvironmentError as env_err:
        entry["content"] = f"**Configuration error** — {env_err}"
        entry["error"] = True
    except Exception as exc:  # surfaced in-thread so the conversation stays readable
        entry["content"] = f"**Something went wrong** — {exc}"
        entry["error"] = True

    st.session_state.history.append(entry)
    st.session_state.pending = None
    st.session_state.pending_agent = None
    slot.empty()
    st.rerun()

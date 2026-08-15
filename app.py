"""
app.py
------
Streamlit Frontend for the Multi-Agent Productivity Assistant.
Fixed: stray empty div at top, response rendering outside its card,
gap between chat box and response, added animated loading circle on Ask button.
"""

import streamlit as st
import time

# ─── Page Configuration ───────────────────────────────────────────────────────
st.set_page_config(
    page_title="Multi-Agent Productivity Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #fdfbf7 0%, #f4ebd0 100%);
        color: #1a1a1a;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    .block-container { padding: 2rem 3rem; max-width: 1300px; }

    [data-testid="stSidebar"] {
        background-color: #faf8f5;
        border-right: 1px solid #eae5de;
        padding-top: 1.5rem;
    }
    [data-testid="stSidebar"] h3, [data-testid="stSidebar"] label {
        color: #2d2d2d !important; font-weight: 600 !important;
    }
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label p {
        color: #1a1a1a !important;
        font-weight: 600 !important;
    }
    [data-testid="stSidebar"] .stRadio label {
        background: transparent !important;
        border-radius: 8px;
        padding: 8px 12px !important;
        transition: background 0.2s;
    }
    [data-testid="stSidebar"] .stRadio label:hover {
        background: #f0ece4 !important;
    }

    .main-heading {
        font-size: 2.8rem;
        font-weight: 700;
        color: #111111;
        text-align: center;
        margin-top: 1rem;
        margin-bottom: 1.5rem;
        letter-spacing: -0.03em;
    }

    /* Native bordered container used for the chat box — replaces manual div hack */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: #ffffff;
        border: 1px solid #dcd6cd !important;
        border-radius: 16px !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.06);
        width: min(1100px, 94%);
        margin: 0 auto 1rem auto;
        padding: 8px;
    }

    .stTextArea textarea {
        background-color: #ffffff !important;
        border: none !important;
        color: #111111 !important;
        font-size: 1.05rem !important;
        font-weight: 500 !important;
        padding: 4px !important;
        box-shadow: none !important;
    }
    .stTextArea textarea::placeholder {
        color: #666666 !important;
        opacity: 1 !important;
    }
    .stTextArea textarea:focus {
        box-shadow: none !important;
    }

    .quick-card {
        background: #ffffff;
        border: 1px solid #e2ddd5;
        border-radius: 14px;
        padding: 1.2rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03);
    }
    .quick-card-title {
        font-weight: 700;
        color: #111111;
        font-size: 0.95rem;
        margin-bottom: 4px;
    }
    .quick-card-desc {
        color: #444444;
        font-size: 0.85rem;
        line-height: 1.4;
    }

    .stButton > button {
        background: #111111 !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 10px;
        padding: 0.5rem 1.2rem;
        font-weight: 600;
        font-size: 0.9rem;
    }
    .stButton > button:hover {
        background: #333333 !important;
        color: #ffffff !important;
    }

    /* Response card — fluid width, fills the main content area */
    .response-card {
        background: #ffffff;
        border: 1px solid #dcd6cd;
        border-radius: 12px;
        padding: 1.2rem;
        margin: 0.4rem auto 1.4rem auto;
        width: min(1100px, 94%);
        color: #111111;
        line-height: 1.6;
        font-size: 0.95rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03);
        overflow-wrap: break-word;
        word-break: break-word;
    }

    /* Follow-up "Continue" affordance under the latest agent response */
    .followup-hint {
        width: min(1100px, 94%);
        margin: 0.6rem auto 0.8rem auto;
        font-size: 0.85rem;
        color: #555555;
        line-height: 1.4;
    }
    div[data-testid="stForm"] {
        width: min(1100px, 94%);
        margin: 0 auto 1.5rem auto;
        border: 1px dashed #dcd6cd;
        border-radius: 12px;
        padding: 10px 14px;
        background: #fffdf9;
    }

    /* Continue button (form submit) — explicit hover/active/focus so state
       never inverts to an unreadable combo (e.g. dark-on-dark on click) */
    div[data-testid="stForm"] .stButton > button,
    div[data-testid="stFormSubmitButton"] > button {
        background: #111111 !important;
        color: #ffffff !important;
        border: 1px solid #111111 !important;
    }
    div[data-testid="stForm"] .stButton > button:hover,
    div[data-testid="stFormSubmitButton"] > button:hover {
        background: #333333 !important;
        color: #ffffff !important;
        border-color: #333333 !important;
    }
    div[data-testid="stForm"] .stButton > button:active,
    div[data-testid="stFormSubmitButton"] > button:active {
        background: #000000 !important;
        color: #ffffff !important;
        border-color: #000000 !important;
    }
    div[data-testid="stForm"] .stButton > button:focus-visible,
    div[data-testid="stFormSubmitButton"] > button:focus-visible {
        background: #111111 !important;
        color: #ffffff !important;
        outline: 3px solid #0284c7 !important;
        outline-offset: 2px;
    }

    /* Sidebar header avatar */
    .sidebar-avatar {
        width: 34px;
        height: 34px;
        border-radius: 50%;
        background: #111111;
        color: #ffffff;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1rem;
        flex-shrink: 0;
    }

    /* Top agent-name label above the greeting */
    .agent-name {
        text-align: center;
        font-size: 1.05rem;
        font-weight: 800;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        margin-top: 0.5rem;
    }

    /* Visible focus states for keyboard navigation (a11y) */
    .stButton > button:focus-visible,
    .stTextArea textarea:focus-visible,
    .stTextInput input:focus-visible,
    [data-testid="stSidebar"] .stRadio label:focus-within {
        outline: 3px solid #0284c7 !important;
        outline-offset: 2px;
    }

    /* Responsive breakpoints */
    @media (max-width: 640px) {
        .block-container { padding: 1rem 1rem; }
        .main-heading { font-size: 1.9rem; }
        .agent-name { font-size: 0.9rem; }
        div[data-testid="stVerticalBlockBorderWrapper"],
        .response-card,
        .followup-hint,
        div[data-testid="stForm"] { width: 100%; }
    }

    /* Animated loading circle for the Ask button */
    .circle-loader-wrap {
        display: flex;
        align-items: center;
        justify-content: center;
        height: 42px;
    }
    .circle-loader {
        width: 22px;
        height: 22px;
        border: 3px solid #dcd6cd;
        border-top: 3px solid #111111;
        border-radius: 50%;
        animation: spin 0.7s linear infinite;
    }
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    hr { border-color: #dcd6cd; margin: 1.2rem 0; }
</style>
""", unsafe_allow_html=True)

# ─── Agent Configuration ──────────────────────────────────────────────────────
AGENTS = {
    "🌤️  Weather Agent": {
        "id": "weather",
        "full_name": "Weather Agent",
        "key": "weather",
        "color": "#0284c7",
        "description": "Get real-time weather insights, forecasts, and practical daily recommendations.",
        "greeting_template": "Good day, Creator ☁️",
        "tagline": "{name} is watching the skies so your plans don't get rained on.",
        "examples": [
            "Will there be any extreme weather alerts this week?",
            "Is it safe to travel tomorrow based on weather conditions?",
            "Tell me the best time of day to go out today based on heat and sunlight.",
        ],
        "icon": "🌤️",
    },
    "✈️  Travel Agent": {
        "id": "travel",
        "full_name": "Travel Agent",
        "key": "travel",
        "color": "#16a34a",
        "description": "Plan trips, estimate budgets, get packing checklists & travel tips.",
        "greeting_template": "Ready for the next trip, Creator ✈️",
        "tagline": "{name} is here to turn 'someday' into an itinerary.",
        "examples": [
            "Create a detailed itinerary for Kedarnath with time, cost, and difficulty level.",
            "Suggest a solo trip plan for a beginner traveler from Dehradun.",
            "Give me a packing checklist based on destination, weather, and trip duration.",
        ],
        "icon": "✈️",
    },
    "💰  Finance Agent": {
        "id": "finance",
        "full_name": "Finance Agent",
        "key": "finance",
        "color": "#d97706",
        "description": "Calculate EMI, interest, and split your monthly budget smartly.",
        "greeting_template": "Let's talk money, Creator 💰",
        "tagline": "{name} is on your side, one smart rupee at a time.",
        "examples": [
            "Help me plan an emergency fund step-by-step.",
            "How can I save ₹1 lakh in 12 months with my current spending habits?",
            "Suggest how I can reduce unnecessary spending without affecting my lifestyle.",
        ],
        "icon": "💰",
    },
    "📋  Productivity Agent": {
        "id": "productivity",
        "full_name": "Productivity Agent",
        "key": "productivity",
        "color": "#9333ea",
        "description": "Create to-do lists, meeting agendas, emails & study plans.",
        "greeting_template": "Let's get things done, Creator 📋",
        "tagline": "{name} turns your chaos into a clean checklist.",
        "examples": [
            "Plan my entire week with time-blocking for college, coding practice, and gym.",
            "Draft a professional sick leave email to my manager.",
            "Turn my messy notes into a clean, actionable to-do list with priorities.",
        ],
        "icon": "📋",
    },
}

# ─── Lazy import helpers ──────────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_agent(agent_key: str):
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
    else:
        raise ValueError(f"Unknown agent key: {agent_key}")

# ─── Session State ────────────────────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []
if "processing" not in st.session_state:
    st.session_state.processing = False
if "pending_query" not in st.session_state:
    st.session_state.pending_query = None
if "pending_agent" not in st.session_state:
    st.session_state.pending_agent = None

# ─── Sidebar Navigation ───────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 1.5rem;">
            <div class="sidebar-avatar" aria-hidden="true">✨</div>
            <span style="font-size: 1.1rem; font-weight: 700; color: #111111;">Assistant Hub</span>
        </div>
    """, unsafe_allow_html=True)

    if st.button("➕ New Chat", use_container_width=True, disabled=st.session_state.processing):
        st.session_state.history = []
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### Agents")

    selected_agent_label = st.radio(
        "Select Agent",
        list(AGENTS.keys()),
        index=0,
        label_visibility="collapsed",
        disabled=st.session_state.processing,
        help="Choose which specialist agent handles your next question.",
    )

    agent_info = AGENTS[selected_agent_label]
    agent_color = agent_info["color"]

    st.markdown("---")
    st.markdown(
        f"<div style='font-size:0.8rem; color:#555555; font-weight:600;'>ACTIVE AGENT</div>"
        f"<div style='font-size:0.95rem; font-weight:700; color:{agent_color}; margin-top:2px;'>{selected_agent_label}</div>",
        unsafe_allow_html=True,
    )

# ─── Main Interface Layout ───────────────────────────────────────────────────
# Requirement 1+2: agent name up top + personalized greeting. Both live inside
# one aria-live region so screen readers announce the change as soon as the
# user switches agents in the sidebar — Streamlit reruns the whole script on
# radio change, so this updates immediately with no page reload.
tagline_text = agent_info["tagline"].format(name=agent_info["full_name"])
st.markdown(
    f"""
    <div role="status" aria-live="polite" aria-atomic="true">
        <div class="agent-name" style="color:{agent_color};">
            {agent_info['icon']} {agent_info['full_name']}
        </div>
        <h1 class="main-heading">{agent_info['greeting_template']}</h1>
        <p style="text-align:center; color:#444444; font-size:0.95rem; margin-top:-1rem; margin-bottom:1.5rem;">
            {tagline_text}
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Chat box — native bordered container, no manual div open/close split across calls
chat_box = st.container(border=True)
with chat_box:
    user_query = st.text_area(
        "Query Input",
        placeholder=f"How can {agent_info['full_name']} help you today?",
        height=75,
        label_visibility="collapsed",
        disabled=st.session_state.processing,
    )

    col_sub1, col_sub2 = st.columns([5, 1])
    with col_sub2:
        if st.session_state.processing:
            st.markdown(
                '<div class="circle-loader-wrap"><div class="circle-loader"></div></div>',
                unsafe_allow_html=True,
            )
            submit = False
        else:
            submit = st.button("Ask ➔", use_container_width=True)

# Quick Start Cards
if not st.session_state.history and not st.session_state.processing:
    st.markdown(
        "<p style='text-align: center; color: #444444; font-size: 0.85rem; font-weight: 700; "
        "text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 1.2rem;'>Quick Start Examples</p>",
        unsafe_allow_html=True,
    )

    qc1, qc2 = st.columns(2)
    examples_subset = agent_info["examples"][:2]
    for i, ex_query in enumerate(examples_subset):
        with [qc1, qc2][i]:
            st.markdown(
                f"""
                <div class="quick-card">
                    <div class="quick-card-title">{agent_info['icon']} Sample Query {i+1}</div>
                    <div class="quick-card-desc">{ex_query}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

# ─── Step 1: click Ask -> set processing state, rerun so spinner shows immediately ─────
if submit:
    query = user_query.strip()
    if not query:
        st.warning("⚠️ Please enter a query before submitting.")
    else:
        st.session_state.processing = True
        st.session_state.pending_query = query
        st.session_state.pending_agent = agent_info
        st.rerun()

# ─── Step 2: actually run the agent (spinner is already visible from step 1's rerun) ───
if st.session_state.processing:
    pending_agent = st.session_state.pending_agent
    pending_query = st.session_state.pending_query
    try:
        start_time = time.time()
        run_fn = load_agent(pending_agent["key"])
        response = run_fn(pending_query)
        elapsed = time.time() - start_time

        st.session_state.history.append({
            "agent": pending_agent["full_name"],
            "color": pending_agent["color"],
            "query": pending_query,
            "response": response,
            "time": f"{elapsed:.2f}s",
        })
    except EnvironmentError as env_err:
        st.error(f"🔑 Configuration Error: {env_err}")
    except Exception as exc:
        st.error(f"❌ Execution error: {str(exc)}")
    finally:
        st.session_state.processing = False
        st.session_state.pending_query = None
        st.session_state.pending_agent = None
        st.rerun()

# ─── Conversation History Stream ──────────────────────────────────────────────
if st.session_state.history:
    st.markdown("---")
    st.markdown("<h3 style='color: #111111; font-weight: 700;'>Conversation History</h3>", unsafe_allow_html=True)

    history_list = list(reversed(st.session_state.history))

    for idx, item in enumerate(history_list):
        st.markdown(
            f"<div style='background:#ffffff; border: 1px solid #dcd6cd; border-radius:10px; "
            f"padding:12px 16px; margin-bottom:8px; width: min(1100px, 94%); margin-left: auto; margin-right: auto; "
            f"box-shadow: 0 4px 12px rgba(0,0,0,0.03); overflow-wrap: break-word;'>"
            f"<span style='color:#555555; font-size:0.75rem; font-weight: 700;'>YOU</span><br>"
            f"<span style='color:#111111; font-size:0.95rem; font-weight: 500;'>{item['query']}</span>"
            f"</div>",
            unsafe_allow_html=True,
        )

        st.markdown(
            f"<div style='width: min(1100px, 94%); margin-left: auto; margin-right: auto; display: flex; "
            f"justify-content: space-between; align-items: center; margin-top: 6px; padding: 0 4px;'>"
            f"<span style='color:{item['color']}; font-size:0.8rem; font-weight:700;'>{item['agent'].upper()}</span>"
            f"<span style='color:#555555; font-size:0.75rem; font-weight: 600;'>⏱ {item['time']}</span>"
            f"</div>",
            unsafe_allow_html=True,
        )

        # Response rendered INSIDE the card in a single st.markdown call.
        # (Splitting open-div / content / close-div across separate st.markdown
        # calls was the bug — each call gets sanitized independently, so the
        # div never actually wraps the content.)
        st.markdown(
            f'<div class="response-card">\n\n{item["response"]}\n\n</div>',
            unsafe_allow_html=True,
        )

        # ── Follow-up flow ──────────────────────────────────────────────────
        # Only offer this on the most recent exchange (idx == 0 after reversal)
        # and only when the agent's reply reads like a follow-up question.
        is_latest = idx == 0
        looks_like_question = item["response"].rstrip().endswith("?")
        if is_latest and looks_like_question and not st.session_state.processing:
            st.markdown(
                '<p class="followup-hint">This looks like a follow-up question — '
                'reply below and press Enter, or hit Continue.</p>',
                unsafe_allow_html=True,
            )
            # st.form gives us the Enter-to-submit fallback for free: pressing
            # Enter inside a form's text_input submits the form, same as
            # clicking the button does.
            with st.form(key=f"followup_form_{len(st.session_state.history)}", clear_on_submit=True):
                followup_text = st.text_input(
                    "Follow-up reply",
                    label_visibility="collapsed",
                    placeholder="Type your answer…",
                )
                followup_submitted = st.form_submit_button("Continue ➔", use_container_width=False)

            if followup_submitted and followup_text.strip():
                st.session_state.processing = True
                st.session_state.pending_query = followup_text.strip()
                st.session_state.pending_agent = AGENTS[selected_agent_label]
                st.rerun()
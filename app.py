"""
app.py
------
Streamlit Frontend for the Multi-Agent Productivity Assistant.
Provides an interactive UI to select and query any of the four specialized agents.
"""

import streamlit as st
import time

# ─── Page Configuration ───────────────────────────────────────────────────────
st.set_page_config(
    page_title="Multi-Agent Productivity Assistant",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Main background */
    .stApp { background-color: #0f1117; }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1d2e 0%, #16213e 100%);
        border-right: 1px solid #2d3561;
    }

    /* Card styling for responses */
    .response-card {
        background: linear-gradient(135deg, #1a1d2e, #16213e);
        border: 1px solid #2d3561;
        border-radius: 12px;
        padding: 1rem 1.2rem;
        margin-top: 0.5rem;
        color: #e0e0e0;
        line-height: 1.7;
        font-size: 1rem;
        white-space: normal;
        word-break: break-word;
        overflow-x: hidden;
    }

    /* Agent badge */
    .agent-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }

    /* Title gradient */
    .main-title {
        background: linear-gradient(90deg, #667eea, #764ba2, #f64f59);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.4rem;
        font-weight: 800;
        text-align: center;
    }

    /* Info box */
    .info-box {
        background: rgba(102, 126, 234, 0.1);
        border-left: 4px solid #667eea;
        border-radius: 4px;
        padding: 0.8rem 1rem;
        margin: 0.5rem 0;
        color: #a0aec0;
        font-size: 0.9rem;
    }

    /* Metric cards */
    .metric-row {
        display: flex;
        gap: 1rem;
        margin: 1rem 0;
    }

    /* Query input area */
    .stTextArea textarea {
        background-color: #1a1d2e !important;
        border: 1px solid #2d3561 !important;
        border-radius: 8px !important;
        color: #e0e0e0 !important;
        font-size: 1rem !important;
    }

    /* Submit button */
    .stButton > button {
        background: linear-gradient(90deg, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        width: 100%;
        transition: opacity 0.2s;
    }

    .stButton > button:hover {
        opacity: 0.85;
    }

    /* Divider */
    hr { border-color: #2d3561; }
</style>
""", unsafe_allow_html=True)


# ─── Agent Configuration ──────────────────────────────────────────────────────
AGENTS = {
    "🌤️  Weather Agent": {
        "key": "weather",
        "color": "#4fc3f7",
        "description": "Get real-time weather insights, forecasts, and practical daily recommendations.",
        "examples": [
            "Will it rain today in Dehradun and should I carry an umbrella?",
            "Give me a 5-day forecast with travel or outdoor activity suggestions.",
            "Will there be any extreme weather alerts this week?",
            "Is it safe to travel tomorrow based on weather conditions?",
            "Tell me the best time of day to go out today based on heat and sunlight."
        ],
    },
    "✈️  Travel Agent": {
        "key": "travel",
        "color": "#81c784",
        "description": "Plan trips, estimate budgets, get packing checklists & travel tips.",
        "examples": [
            "Create a detailed itinerary for Kedarnath with time, cost, and difficulty level.",
            "Suggest a solo trip plan for a beginner traveler from Dehradun.",
            "Give me a packing checklist based on destination, weather, and trip duration.",
            "Compare train vs bus vs flight for my trip with cost and time analysis.",
            "What are common travel mistakes I should avoid for my destination?"
        ],
    },
    "💰  Finance Agent": {
        "key": "finance",
        "color": "#ffb74d",
        "description": "Calculate EMI, interest, and split your monthly budget smartly.",
        "examples": [
            "Break down my ₹25,000 monthly income into rent, savings, and expenses realistically.",
            "Help me plan an emergency fund step-by-step.",
            "How can I save ₹1 lakh in 12 months with my current spending habits?",
        ],
    },
    "📋  Productivity Agent": {
        "key": "productivity",
        "color": "#ce93d8",
        "description": "Create to-do lists, meeting agendas, emails & study plans.",
        "examples": [
            "Plan my entire week with time-blocking for college, coding practice, and gym.",
            "Draft a professional sick leave email to my manager.",
            "Create a daily routine to improve focus and avoid procrastination.",
            "Help me organize my day when I feel overwhelmed and unproductive.",
        ],
    },
}


# ─── Lazy import helpers ──────────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_agent(agent_key: str):
    """Load and cache each agent to avoid re-initialisation on every query."""
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


# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🤖 Agent Selector")
    st.markdown("---")

    selected_agent_label = st.radio(
        "Choose an agent:",
        list(AGENTS.keys()),
        index=0,
        label_visibility="collapsed",
    )

    agent_info = AGENTS[selected_agent_label]
    agent_color = agent_info["color"]

    st.markdown(f"""
    <div style='background:rgba(255,255,255,0.05); border-radius:10px;
                padding:12px; margin-top:12px; border-left:4px solid {agent_color};'>
        <p style='color:{agent_color}; font-weight:700; margin:0 0 6px;'>About this Agent</p>
        <p style='color:#a0aec0; font-size:0.88rem; margin:0;'>{agent_info['description']}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### 💡 Example Queries")
    for ex in agent_info["examples"]:
        st.markdown(f"<div class='info-box'>→ {ex}</div>", unsafe_allow_html=True)

    st.markdown("---")
    if st.button("🗑️  Clear History"):
        st.session_state.history = []
        st.rerun()

    st.markdown(
        "<p style='color:#4a5568; font-size:0.78rem; text-align:center; margin-top:20px;'>"
        "Built with LangChain · Gemini · Streamlit</p>",
        unsafe_allow_html=True,
    )


# ─── Main UI ──────────────────────────────────────────────────────────────────
st.markdown("<h1 class='main-title'>Multi-Agent Productivity Assistant</h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:center; color:#718096; margin-top:-10px;'>"
    "Powered by LangChain · Google Gemini · Specialized AI Agents</p>",
    unsafe_allow_html=True,
)
st.markdown("---")

# Active agent indicator
st.markdown(
    f"<p style='color:{agent_color}; font-weight:600; font-size:1.05rem;'>"
    f"Active Agent: {selected_agent_label}</p>",
    unsafe_allow_html=True,
)

# Query input
user_query = st.text_area(
    "Enter your query:",
    placeholder=f"e.g. {agent_info['examples'][0]}",
    height=110,
    label_visibility="collapsed",
)

col1, col2 = st.columns([3, 1])
with col1:
    submit = st.button("🚀  Ask Agent", use_container_width=True)
with col2:
    st.markdown("")

# ─── Agent Execution ──────────────────────────────────────────────────────────
if submit:
    query = user_query.strip()
    if not query:
        st.warning("⚠️  Please enter a query before submitting.")
    else:
        with st.spinner(f"🔄  {selected_agent_label.strip()} is thinking..."):
            try:
                start_time = time.time()
                run_fn = load_agent(agent_info["key"])
                response = run_fn(query)
                elapsed = time.time() - start_time

                st.session_state.history.append({
                    "agent": selected_agent_label,
                    "color": agent_color,
                    "query": query,
                    "response": response,
                    "time": f"{elapsed:.2f}s",
                })

            except EnvironmentError as env_err:
                st.error(f"🔑 Configuration Error: {env_err}")
                st.info("Make sure your `.env` file contains valid API keys.")
            except Exception as exc:
                st.error(f"❌ Agent error: {str(exc)}")

# ─── Response History ─────────────────────────────────────────────────────────
if st.session_state.history:
    st.markdown("---")
    st.markdown("### 💬 Conversation")

    for idx, item in enumerate(reversed(st.session_state.history)):
        with st.container():
            # User query
            st.markdown(
                f"<div style='background:#1e2130; border-radius:8px; padding:10px 14px;"
                f"margin-bottom:6px; border-left:3px solid #4a5568;'>"
                f"<span style='color:#718096; font-size:0.78rem;'>YOU</span><br>"
                f"<span style='color:#e2e8f0;'>{item['query']}</span>"
                f"</div>",
                unsafe_allow_html=True,
            )

            # Agent response header
            st.markdown(
                f"<div style='background:#1a1d2e; border-radius:8px; padding:12px 16px;"
                f"margin-bottom:4px; border-left:3px solid {item['color']};'>"
                f"<span style='color:{item['color']}; font-size:0.78rem; font-weight:700;'>"
                f"{item['agent'].strip().upper()}</span>"
                f"<span style='color:#4a5568; font-size:0.75rem; float:right;'>⏱ {item['time']}</span>"
                f"</div>",
                unsafe_allow_html=True,
            )

            # Agent response body
            st.markdown('<div class="response-card">', unsafe_allow_html=True)
            st.markdown(item["response"])
            st.markdown('</div>', unsafe_allow_html=True)

            if idx < len(st.session_state.history) - 1:
                st.markdown("---")
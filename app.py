PY
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
<div align="center">

# 🤖 Multi-Agent Productivity Assistant

**A modular, tool-enabled multi-agent AI system built with LangChain, Google Gemini, and Streamlit.**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://multi-agent-appuctivity-assistant-jopdwch8jkayamkqsl2gqn.streamlit.app/)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![LangChain](https://img.shields.io/badge/LangChain-1.x%20tool--calling-1C3C3C)
![Gemini](https://img.shields.io/badge/LLM-Gemini%202.5%20Flash-8E75B2)
![License](https://img.shields.io/badge/license-unspecified-lightgrey)

[Live Demo](https://multi-agent-appuctivity-assistant-jopdwch8jkayamkqsl2gqn.streamlit.app/) · [Setup](#-setup) · [Usage](#-usage) · [Architecture](#-architecture)

</div>

<br>

---

## ✨ Overview

Eight specialized agents, each scoped to its own tool set via LangChain tool calling:

<div align="center">

| | Agent | Domain | Tools |
|:---:|---|---|---|
| 🌤️ | **Weather** | Real-time weather | `get_current_weather` · `get_weather_forecast` |
| ✈️ | **Travel** | Trip planning | `estimate_trip_budget` · `suggest_transport` · `travel_checklist` · `best_time_to_visit` |
| 💰 | **Finance** | Financial calculations | `calculate_emi` · `simple_interest` · `compound_interest` · `monthly_budget_split` · `explain_finance_term` |
| 📋 | **Productivity** | Work & planning | `create_todo_list` · `generate_meeting_agenda` · `draft_email` · `study_plan` |
| 💼 | **Career** | Resumes & interviews | `rewrite_resume_bullet` · `interview_questions` · `skill_gap_analysis` · `draft_outreach` · `resume_checklist` |
| 🏃 | **Health** | Fitness & habits | `bmi_report` · `calorie_targets` · `workout_split` · `hydration_and_sleep` |
| 🍳 | **Recipe** | Cooking & kitchen maths | `scale_recipe` · `convert_kitchen_measure` · `meal_ideas_from_ingredients` · `cooking_times` · `shopping_list` |
| 📚 | **Study** | Revision & exams | `spaced_repetition_schedule` · `exam_revision_plan` · `grade_needed` · `pomodoro_plan` · `flashcards_from_notes` |

</div>

> **Note on `study_plan` vs `exam_revision_plan`** — the Productivity Agent's `study_plan` builds a simple 7-day plan for one subject. The Study Agent's `exam_revision_plan` splits hours across several subjects against an exam deadline. They are deliberately separate tools with distinct names.

## 🚀 Features

- 🧩 Modular agents, each with an isolated, domain-specific toolset
- 🌐 Real-time data via OpenWeatherMap
- 🧠 LLM reasoning and response generation via Gemini
- 💬 Streamlit chat interface with per-agent theming and a shared thread
- 🛡️ Centralized error handling — provider failures surface as readable messages, not stack traces

## 📂 Project Structure

```
Main-multi-agent/
│
├── agents/
│   ├── weather_agent.py        # Weather agent
│   ├── travel_agent.py         # Travel planning agent
│   ├── finance_agent.py        # Financial calculation agent
│   ├── productivity_agent.py   # Productivity tools agent
│   ├── career_agent.py         # Resume, interview and skill-gap agent
│   ├── health_agent.py         # Fitness and daily habits agent
│   ├── recipe_agent.py         # Cooking and kitchen-maths agent
│   └── study_agent.py          # Revision and exam-planning agent
│
├── tools/
│   ├── weather_tool.py         # OpenWeatherMap API integration
│   ├── travel_tool.py          # Travel calculation tools
│   ├── finance_tool.py         # EMI and interest formula tools
│   ├── productivity_tool.py    # Planning and drafting tools
│   ├── career_tool.py          # Resume and interview tools
│   ├── health_tool.py          # BMI, calorie and training tools
│   ├── recipe_tool.py          # Scaling, conversion and shopping tools
│   └── study_tool.py           # Spaced repetition and grade tools
│
├── utils/
│   ├── llm.py                  # Gemini LLM initialization
│   └── agent_runtime.py        # Shared invoke guard + response parser
│
├── app.py                      # Streamlit UI
├── .env                        # API keys (not committed)
├── .env.example                # Template for .env
├── requirements.txt            # Python dependencies
└── README.md
```

Every agent follows the same shape: a system prompt, a tool list, and a `run_*_agent(query)` entry point that delegates to `utils/agent_runtime.run_agent`. Adding a ninth agent means writing those two files and adding one entry to the `AGENTS` dict in `app.py` — the sidebar, theming and routing are all driven off that registry.

## 🛠 Setup

<details>
<summary><strong>1. Clone the repository</strong></summary>

```bash
git clone <repository-url>
cd Main-multi-agent
```
</details>

<details>
<summary><strong>2. Create a virtual environment</strong></summary>

Python 3.10 or newer. Developed and verified on 3.14.3.

```bash
python -m venv venv
```

```bash
# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```
</details>

<details>
<summary><strong>3. Install dependencies</strong></summary>

```bash
pip install -r requirements.txt
```
</details>

<details>
<summary><strong>4. Configure API keys</strong></summary>

```bash
cp .env.example .env
```

```env
GEMINI_API_KEY=your_actual_gemini_key_here
OPENWEATHER_API_KEY=your_actual_openweather_key_here
```

| Key | Source |
|---|---|
| `GEMINI_API_KEY` | [Google AI Studio](https://aistudio.google.com/app/apikey) |
| `OPENWEATHER_API_KEY` | [OpenWeatherMap](https://openweathermap.org/api) (free tier) |

Only `GEMINI_API_KEY` is required. Without `OPENWEATHER_API_KEY` the Weather Agent cannot fetch live data; the other seven agents are unaffected.
</details>

<details>
<summary><strong>5. Run the app</strong></summary>

```bash
streamlit run app.py
```

Streamlit's default is `http://localhost:8501`. If that port is taken, it auto-selects the next one and prints the actual URL — check the terminal rather than assuming a fixed port.
</details>

## 💬 Usage

Pick an agent from the sidebar, type a question in plain language, and the agent routes it through its tools to Gemini for a formatted response.

## 🧭 Example Queries

<table>
<tr><td>

**🌤️ Weather**
- "What is the weather in Hyderabad?"
- "Give me a 3-day forecast for Mumbai."

</td><td>

**✈️ Travel**
- "Plan a 3-day trip to Goa for 2 people."
- "Suggest transport for 650 km travel."

</td></tr>
<tr><td>

**📋 Productivity**
- "Draft a sick leave email."
- "Turn my messy notes into a to-do list."

</td><td>

**💼 Career**
- "Rewrite: 'Responsible for handling social media.'"
- "What am I missing for a data analyst role?"

</td></tr>
<tr><td>

**🏃 Health**
- "I'm 21, 72 kg, 178 cm — daily calories?"
- "Build me a 4-day strength split."

</td><td>

**🍳 Recipe**
- "Scale this for 6: 2 cups flour, 1/2 tsp salt."
- "How many grams is 2 cups of besan?"

</td></tr>
<tr><td>

**📚 Study**
- "Split 3 hrs/day across Maths, Physics, Chemistry — exam in 14 days."
- "I'm at 72% with 60% done. What do I need on the final to hit 80%?"

</td><td>

**💰 Finance**
- "Calculate EMI for 5 lakhs at 9% for 5 years."
- "Split my ₹60,000 salary using the 50/30/20 rule."

</td></tr>
</table>

## 🏗 Architecture

```
User input
    │
    ▼
Streamlit UI (app.py)  ── AGENTS registry drives routing, nav and theming
    │
    ▼
Selected agent (agents/)  ── system prompt + scoped tool list
    │
    ▼
utils/agent_runtime.run_agent  ── guarded invoke, readable error translation
    │
    ▼
LangChain tool calling (create_agent)
    │
    ▼
Tool execution (tools/) ── external APIs / calculation logic
    │
    ▼
Gemini formats the response
    │
    ▼
Response displayed in UI
```

Failures raise rather than return a fake answer: `agent_runtime` turns provider errors into plain sentences ("the Gemini API key was rejected", "quota is used up") and `app.py` renders them as an error bubble in the thread.

## 🧰 Technologies

| | Technology | Purpose |
|:---:|---|---|
| 🦜 | LangChain 1.x | Agent creation, tool binding |
| 🕸 | LangGraph | Agent execution graph behind `create_agent` |
| ✨ | Gemini 2.5 Flash | LLM reasoning & generation |
| 🌦 | OpenWeatherMap | Real-time weather data |
| 🎈 | Streamlit | Web frontend |
| 🔐 | python-dotenv | Environment variable management |

## 🤝 Contributing

<!-- PLACEHOLDER: no process existed in the original README. -->

1. Fork the repo
2. `git checkout -b feature/your-feature`
3. Commit with a clear message
4. Open a pull request describing the change

## 📜 Changelog

| Version | Date | Changes |
|---|---|---|
| Unreleased | 2026-09-12 | Wired the Recipe and Study agents (their tools existed but had no agent or UI entry). Renamed `study_tool.study_plan` → `exam_revision_plan` to remove a name clash with the Productivity Agent's tool. Added `utils/agent_runtime.py`, replacing six near-identical response parsers and adding guarded invocation with readable provider errors. Added input validation to the finance, travel and productivity tools. Pinned `requirements.txt` to the tested majors and declared the missing `langgraph`. Added `.env.example`. |
| — | — | Initial documented release |

## 📄 License

> ⚠️ **Not actually specified yet.** "Feel free to extend" isn't a license — it says nothing about attribution, liability, or redistribution. Pick one (MIT is the common default for projects like this) and add a `LICENSE` file before calling this production-ready.

## 📬 Contact

<!-- PLACEHOLDER: maintainer name / email / issue tracker link -->

---

<div align="center">

Built with LangChain, Gemini, and Streamlit.

</div>
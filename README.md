<div align="center">

# 🤖 Multi-Agent Productivity Assistant

**A modular, tool-enabled multi-agent AI system built with LangChain, Google Gemini, and Streamlit.**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://multi-agent-appuctivity-assistant-jopdwch8jkayamkqsl2gqn.streamlit.app/)
![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue)
![LangChain](https://img.shields.io/badge/LangChain-tool--calling-1C3C3C)
![Gemini](https://img.shields.io/badge/LLM-Gemini%201.5%20Flash-8E75B2)
![License](https://img.shields.io/badge/license-unspecified-lightgrey)

[Live Demo](https://multi-agent-appuctivity-assistant-jopdwch8jkayamkqsl2gqn.streamlit.app/) · [Setup](#-setup) · [Usage](#-usage) · [Architecture](#-architecture)

</div>

<br>

---

## ✨ Overview

Four specialized agents, each scoped to its own tool set via LangChain tool calling:

<div align="center">

| | Agent | Domain | Tools |
|:---:|---|---|---|
| 🌤️ | **Weather** | Real-time weather | `get_current_weather` · `get_weather_forecast` |
| ✈️ | **Travel** | Trip planning | `estimate_trip_budget` · `suggest_transport` · `travel_checklist` · `best_time_to_visit` |
| 💰 | **Finance** | Financial calculations | `calculate_emi` · `simple_interest` · `compound_interest` · `monthly_budget_split` |
| 📋 | **Productivity** | Work & planning | `create_todo_list` · `generate_meeting_agenda` · `draft_email` · `study_plan` |

</div>

## 🚀 Features

- 🧩 Modular agents, each with an isolated, domain-specific toolset
- 🌐 Real-time data via OpenWeatherMap
- 🧠 LLM reasoning and response generation via Gemini
- 💬 Streamlit chat interface

## 📂 Project Structure

```
Main-multi-agent/
│
├── agents/
│   ├── weather_agent.py        # Weather agent
│   ├── travel_agent.py         # Travel planning agent
│   ├── finance_agent.py        # Financial calculation agent
│   └── productivity_agent.py   # Productivity tools agent
│
├── tools/
│   ├── weather_tool.py         # OpenWeatherMap API integration
│   ├── travel_tool.py          # Travel calculation tools
│   ├── finance_tool.py         # EMI and interest formula tools
│   └── productivity_tool.py    # Planning and drafting tools
│
├── utils/
│   └── llm.py                  # Gemini LLM initialization
│
├── app.py                      # Streamlit UI
├── .env                        # API keys (not committed)
├── .env.example                # Template for .env
├── requirements.txt            # Python dependencies
└── README.md
```

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
| `GEMINI_API_KEY` | [Google AI Studio](https://makersuite.google.com/app/apikey) |
| `OPENWEATHER_API_KEY` | [OpenWeatherMap](https://openweathermap.org/api) (free tier) |
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

**💰 Finance**
- "Calculate EMI for 5 lakhs at 9% for 5 years."
- "Split my ₹60,000 salary using the 50/30/20 rule."

</td><td>

**📋 Productivity**
- "Draft a sick leave email."
- "Make a 7-day study plan for ML, 2 hrs/day."

</td></tr>
</table>

## 🏗 Architecture

```
User input
    │
    ▼
Streamlit UI (app.py)
    │
    ▼
Selected agent (agents/)
    │
    ▼
LangChain tool calling
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

## 🧰 Technologies

| | Technology | Purpose |
|:---:|---|---|
| 🦜 | LangChain | Agent creation, tool binding |
| ✨ | Gemini 1.5 Flash | LLM reasoning & generation |
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

<!-- PLACEHOLDER -->

| Version | Date | Changes |
|---|---|---|
| Unreleased | — | Initial documented release |

## 📄 License

> ⚠️ **Not actually specified yet.** "Feel free to extend" isn't a license — it says nothing about attribution, liability, or redistribution. Pick one (MIT is the common default for projects like this) and add a `LICENSE` file before calling this production-ready.

## 📬 Contact

<!-- PLACEHOLDER: maintainer name / email / issue tracker link -->

---

<div align="center">

Built with LangChain, Gemini, and Streamlit.

</div>
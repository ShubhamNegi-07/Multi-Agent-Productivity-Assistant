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

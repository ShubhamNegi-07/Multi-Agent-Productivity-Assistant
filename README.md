# 🤖 Multi-Agent Productivity Assistant

A modular, tool-enabled multi-agent AI application built with **LangChain**, **Google Gemini**, **OpenWeatherMap API**, and **Streamlit**.

# Try it out: https://multi-agent-assistant-2mszfia7nwedzgbfdjkn4g.streamlit.app/
---

## 📌 Project Overview

This system consists of **four specialized AI agents**, each equipped with its own set of tools to handle domain-specific tasks:

| Agent | Domain | Key Tools |
|---|---|---|
| 🌤️ Weather Agent | Real-time weather | `get_current_weather`, `get_weather_forecast` |
| ✈️ Travel Agent | Trip planning | `estimate_trip_budget`, `suggest_transport`, `travel_checklist`, `best_time_to_visit` |
| 💰 Finance Agent | Financial calculations | `calculate_emi`, `simple_interest`, `compound_interest`, `monthly_budget_split` |
| 📋 Productivity Agent | Work & planning | `create_todo_list`, `generate_meeting_agenda`, `draft_email`, `study_plan` |

---

## 🗂️ Project Structure

```
Main-multi-agent/
│
├── agents/
│   ├── weather_agent.py        # Weather Agent (uses real API)
│   ├── travel_agent.py         # Travel planning agent
│   ├── finance_agent.py        # Financial calculation agent
│   └── productivity_agent.py   # Productivity tools agent
│
├── tools/
│   ├── weather_tool.py         # OpenWeatherMap API integration
│   ├── travel_tool.py          # Custom travel tools
│   ├── finance_tool.py         # EMI & interest formula tools
│   └── productivity_tool.py    # Planning & writing tools
│
├── utils/
│   └── llm.py                  # Gemini LLM initialisation
│
├── app.py                      # Streamlit UI
├── .env                        # API keys (not committed)
├── .env.example                # Template for .env
├── requirements.txt            # Python dependencies
└── README.md
```

---

## ⚙️ Setup Instructions

### 1. Clone / Download the Project

```bash
cd Main-multi-agent
```

### 2. Create a Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API Keys

Copy `.env.example` to `.env` and fill in your keys:

```bash
cp .env.example .env
```

Edit `.env`:

```
GEMINI_API_KEY=your_actual_gemini_key_here
OPENWEATHER_API_KEY=your_actual_openweather_key_here
```

#### Getting API Keys

- **Gemini API Key** → [Google AI Studio](https://makersuite.google.com/app/apikey)
- **OpenWeatherMap Key** → [openweathermap.org/api](https://openweathermap.org/api) *(free tier)*

### 5. Run the Application

```bash
streamlit run app.py
```

Open your browser at **http://localhost:8502**

---

## 🧠 How It Works

```
User Input
    ↓
Streamlit UI (app.py)
    ↓
Selected Agent (agents/)
    ↓
LangChain Tool Calling
    ↓
Tool Execution (tools/)  ←── External APIs / Python Logic
    ↓
Gemini LLM formats response
    ↓
Answer displayed in UI
```

---

## 💡 Example Queries

### 🌤️ Weather Agent
- *"What is the weather in Hyderabad?"*
- *"Give me a 3-day forecast for Mumbai."*

### ✈️ Travel Agent
- *"Plan a 3-day trip to Goa for 2 people."*
- *"Suggest transport for 650 km travel."*
- *"Give me a packing checklist for Ladakh."*

### 💰 Finance Agent
- *"Calculate EMI for 5 lakhs at 9% for 5 years."*
- *"Find compound interest for ₹10,000 at 8% for 3 years, compounded monthly."*
- *"Split my ₹60,000 salary using 50/30/20 rule."*

### 📋 Productivity Agent
- *"Draft a sick leave email."*
- *"Create a meeting agenda for the Q3 Product Review."*
- *"Make a 7-day study plan for Machine Learning with 2 hours per day."*

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| **LangChain** | Agent creation, tool binding, tool calling |
| **Google Gemini 1.5 Flash** | LLM reasoning and response generation |
| **OpenWeatherMap API** | Real-time weather data |
| **Streamlit** | Interactive web frontend |
| **Python-dotenv** | Secure API key management |

---

## 📄 License

This project is for educational purposes. Feel free to extend and build upon it.

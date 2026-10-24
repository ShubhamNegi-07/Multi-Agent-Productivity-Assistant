# Multi-Agent Productivity Assistant

An AI productivity workspace with eight specialist agents for weather,
travel, finance, productivity, careers, health, recipes, and study planning.
The project is organized as a decoupled full-stack monorepo: a Python
FastAPI service provides the agent API, while a React/Vite application provides
the interactive Assistant Hub.

## Project overview

The assistant routes each request to a domain-specific LangChain agent. Each
agent has a focused system prompt and an isolated set of tools. Gemini
generates the final natural-language response, while deterministic tools handle
calculations, structured planning, and external data access.

The current web workflow is:

```text
React/Vite Assistant Hub
        |
        | HTTP: /api/agents, /api/chat
        v
FastAPI backend
        |
        v
Selected LangChain agent
        |
        +--> Domain tools and OpenWeatherMap
        |
        v
Gemini response
```

## Decoupled architecture

### Backend: FastAPI and LangChain

The backend exposes:

- `GET /api/agents` — returns the eight available agent summaries.
- `POST /api/chat` — routes a message to the selected agent and accepts
  conversation history and a memory preference.

The API validates request payloads with Pydantic, applies CORS for local Vite
and Next.js development servers, and translates agent failures into explicit
HTTP errors.

### Frontend: React, Vite, and shadcn-style components

The frontend contains the Assistant Hub shell:

- Specialist navigation sidebar
- Agent header and status indicator
- Empty state with prompt suggestions
- User and assistant message transcript
- Copy-response action
- Auto-resizing chat composer
- Conversation memory toggle

The UI uses TypeScript, Tailwind CSS 3, Lucide icons, and local
shadcn-compatible primitives. The API client reads `VITE_API_BASE_URL` and
defaults to `http://localhost:8001`.

## Specialist agents

| Agent | Focus | Example capabilities |
| --- | --- | --- |
| Weather | Live weather | Current conditions and forecasts |
| Travel | Trip planning | Budgets, transport, checklists, timing |
| Finance | Personal finance maths | EMI, interest, budgeting, terminology |
| Productivity | Work organization | To-do lists, agendas, emails, study plans |
| Career | Career development | Skill gaps, outreach, resume checklists |
| Health | General wellness | BMI, calorie estimates, training, hydration |
| Recipe | Cooking assistance | Recipe scaling, conversions, meal ideas |
| Study | Revision planning | Grades, Pomodoro sessions, flashcards, revision |

Health and finance features provide general informational guidance, not
medical or regulated financial advice.

## Tech stack

### Backend

- Python 3.10+
- FastAPI and Uvicorn
- LangChain 1.x and LangGraph 1.x
- Gemini through `langchain-google-genai`
- Pydantic request and response models
- `python-dotenv` for local environment configuration
- `requests` for OpenWeatherMap access

### Frontend

- React 18
- TypeScript
- Vite
- Tailwind CSS 3
- shadcn-style UI primitives
- Radix UI packages
- Lucide React icons

## Directory layout

```text
Multi-Agent-Productivity-Assistant/
├── backend/
│   ├── agents/              # Eight specialist LangChain agents
│   ├── tools/               # Domain tools used by agents
│   ├── utils/
│   │   ├── agent_runtime.py # Shared invocation and error handling
│   │   └── llm.py           # Gemini initialization
│   ├── main.py              # FastAPI app and API routes
│   ├── rendering.py         # Safe response rendering helper
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/      # Assistant, chat, navigation, and UI components
│   │   ├── lib/api.ts       # Typed backend API client
│   │   ├── pages/           # AssistantPage
│   │   └── styles.css       # Tailwind entrypoint and theme tokens
│   ├── package.json
│   ├── tailwind.config.cjs
│   ├── tsconfig.json
│   └── vite.config.ts
├── tests/
│   └── test_regressions.py
├── .env.example
├── .gitignore
└── README.md
```

The root `.env` is intentionally ignored and must never be committed.

## Setup and installation

### 1. Clone and enter the repository

```powershell
git clone https://github.com/ShubhamNegi-07/Multi-Agent-Productivity-Assistant.git
cd Multi-Agent-Productivity-Assistant
```

### 2. Configure backend environment variables

Copy the template:

```powershell
Copy-Item .env.example .env
```

Edit `.env` and set:

```dotenv
GEMINI_API_KEY="your_gemini_api_key"
OPENWEATHER_API_KEY="your_openweathermap_key"
```

`GEMINI_API_KEY` is required for agent responses. The weather agent also
requires `OPENWEATHER_API_KEY` for live weather data.

### 3. Install backend dependencies

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r backend\requirements.txt
```

Start the backend on the configured development port:

```powershell
python -m uvicorn backend.main:app --reload --port 8001
```

The API is available at `http://localhost:8001`.

### 4. Install and run the frontend

Open a second terminal:

```powershell
cd frontend
npm install
npm run dev
```

The Vite application is normally available at
`http://localhost:5173`. The frontend defaults to the backend at port 8001.
To override it:

```powershell
$env:VITE_API_BASE_URL = "http://localhost:8001"
npm run dev
```

## Testing and verification

Run the backend regression suite from the repository root:

```powershell
python -m unittest discover -s tests -v
```

Compile the key Python modules:

```powershell
python -m py_compile backend\main.py tests\test_regressions.py
```

Build the frontend:

```powershell
cd frontend
npm run build
```

Useful smoke checks:

```powershell
Invoke-WebRequest http://localhost:8001/api/agents
Invoke-WebRequest http://localhost:5173
```

## Development notes

- Keep secrets in `.env`; never commit them.
- Keep backend imports package-qualified with `backend.*`.
- Add new agent tools under `backend/tools/` and register them in the
  corresponding agent module.
- Preserve regression coverage when changing validation or rendering behavior.
- The frontend uses the `@/*` TypeScript alias for `frontend/src/*`.

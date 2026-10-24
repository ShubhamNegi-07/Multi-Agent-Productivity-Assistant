from __future__ import annotations

import time
from collections.abc import Callable
from typing import Annotated, Literal

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict, Field, field_validator

MEMORY_TURNS = 6
MEMORY_CHARS = 700
AgentRunner = Callable[[str], str]

AGENTS = {
    "weather": {"id": "weather", "name": "Weather Agent", "icon": "🌤️", "tagline": "Watching the skies so your plans don't get rained on."},
    "travel": {"id": "travel", "name": "Travel Agent", "icon": "✈️", "tagline": "Here to turn 'someday' into an itinerary."},
    "finance": {"id": "finance", "name": "Finance Agent", "icon": "💰", "tagline": "On your side, one smart rupee at a time."},
    "productivity": {"id": "productivity", "name": "Productivity Agent", "icon": "📋", "tagline": "Turns your chaos into a clean checklist."},
    "career": {"id": "career", "name": "Career Agent", "icon": "💼", "tagline": "Sharpening your resume, one bullet at a time."},
    "health": {"id": "health", "name": "Health Agent", "icon": "🏃", "tagline": "Small daily habits, tracked properly."},
    "recipe": {"id": "recipe", "name": "Recipe Agent", "icon": "🍳", "tagline": "Scales the recipe so dinner still works."},
    "study": {"id": "study", "name": "Study Agent", "icon": "📚", "tagline": "Revision timed so it actually sticks."},
}


class HistoryMessage(BaseModel):
    model_config = ConfigDict(extra="forbid")
    role: Literal["user", "assistant"]
    content: Annotated[str, Field(min_length=1, max_length=10_000)]
    agent: str | None = Field(default=None, max_length=100)

    @field_validator("content")
    @classmethod
    def content_must_not_be_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("content must not be blank")
        return value


class ChatRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    agent_id: str = Field(min_length=1, max_length=40)
    message: Annotated[str, Field(min_length=1, max_length=10_000)]
    history: list[HistoryMessage] = Field(default_factory=list, max_length=50)
    remember: bool = True

    @field_validator("agent_id", "message")
    @classmethod
    def strings_must_not_be_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("value must not be blank")
        return value.strip()


class AgentSummary(BaseModel):
    id: str
    name: str
    icon: str
    tagline: str


class ChatResponse(BaseModel):
    agent: AgentSummary
    message: str
    elapsed_ms: int


def load_agent(agent_id: str) -> AgentRunner:
    modules = {
        "weather": ("weather_agent", "run_weather_agent"),
        "travel": ("travel_agent", "run_travel_agent"),
        "finance": ("finance_agent", "run_finance_agent"),
        "productivity": ("productivity_agent", "run_productivity_agent"),
        "career": ("career_agent", "run_career_agent"),
        "health": ("health_agent", "run_health_agent"),
        "recipe": ("recipe_agent", "run_recipe_agent"),
        "study": ("study_agent", "run_study_agent"),
    }
    if agent_id not in modules:
        raise HTTPException(status_code=404, detail=f"Unknown agent: {agent_id}")
    module_name, function_name = modules[agent_id]
    module = __import__(f"backend.agents.{module_name}", fromlist=[function_name])
    return getattr(module, function_name)


def build_prompt(request: ChatRequest) -> str:
    if not request.remember or not request.history:
        return request.message
    history = request.history[-MEMORY_TURNS:]
    context = "\n".join(
        f"{item.role.title()}: {item.content[-MEMORY_CHARS:]}" for item in history
    )
    return f"Conversation context:\n{context}\n\nUser: {request.message}"


app = FastAPI(title="Multi-Agent Productivity Assistant API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/agents", response_model=list[AgentSummary])
def list_agents() -> list[AgentSummary]:
    return [AgentSummary(**agent) for agent in AGENTS.values()]


@app.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    agent = AGENTS.get(request.agent_id)
    if agent is None:
        raise HTTPException(status_code=404, detail=f"Unknown agent: {request.agent_id}")
    runner = load_agent(request.agent_id)
    started = time.perf_counter()
    try:
        response = runner(build_prompt(request))
    except EnvironmentError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Agent request failed.") from exc
    return ChatResponse(
        agent=AgentSummary(**agent),
        message=response,
        elapsed_ms=round((time.perf_counter() - started) * 1000),
    )

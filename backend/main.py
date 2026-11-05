from __future__ import annotations

import time
from collections.abc import Callable
from collections import deque
import logging
from threading import Lock
from typing import Annotated, Literal

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field, field_validator

MEMORY_TURNS = 6
MEMORY_CHARS = 700
MAX_RESPONSE_CHARS = 4_000
RATE_LIMIT_WINDOW_SECONDS = 60
RATE_LIMIT_REQUESTS = 30
AgentRunner = Callable[[str], str]
logger = logging.getLogger(__name__)
rate_limit_lock = Lock()
rate_limit_buckets: dict[str, deque[float]] = {}

AGENTS = {
    "weather": {"id": "weather", "name": "Weather Desk", "icon": "cloud-sun", "tagline": "Conditions and forecasts for the day ahead."},
    "travel": {"id": "travel", "name": "Travel Desk", "icon": "map", "tagline": "Turn a destination into a workable plan."},
    "finance": {"id": "finance", "name": "Finance Desk", "icon": "calculator", "tagline": "Clear numbers for the decisions in front of you."},
    "productivity": {"id": "productivity", "name": "Planning Desk", "icon": "notebook", "tagline": "Make the next steps visible and manageable."},
    "career": {"id": "career", "name": "Career Desk", "icon": "briefcase", "tagline": "Sharper applications, conversations, and next moves."},
    "health": {"id": "health", "name": "Health Desk", "icon": "dumbbell", "tagline": ""},
    "recipe": {"id": "recipe", "name": "Kitchen Desk", "icon": "chef", "tagline": "Reliable quantities, timings, and shopping lists."},
    "study": {"id": "study", "name": "Study Desk", "icon": "graduation", "tagline": "A focused route from notes to recall."},
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
    message: str = Field(max_length=MAX_RESPONSE_CHARS)
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


app = FastAPI(title="OmniDesk API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def limit_chat_requests(request: Request, call_next):
    if request.url.path == "/api/chat":
        client_id = request.client.host if request.client else "unknown"
        now = time.monotonic()
        cutoff = now - RATE_LIMIT_WINDOW_SECONDS

        with rate_limit_lock:
            bucket = rate_limit_buckets.setdefault(client_id, deque())
            while bucket and bucket[0] <= cutoff:
                bucket.popleft()
            if len(bucket) >= RATE_LIMIT_REQUESTS:
                retry_after = max(1, round(bucket[0] + RATE_LIMIT_WINDOW_SECONDS - now))
                return JSONResponse(
                    status_code=429,
                    content={"detail": "Too many assistant requests. Please try again later."},
                    headers={"Retry-After": str(retry_after)},
                )
            bucket.append(now)

    return await call_next(request)


@app.get("/api/agents", response_model=list[AgentSummary])
def list_agents() -> list[AgentSummary]:
    return [AgentSummary(**agent) for agent in AGENTS.values()]


@app.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    agent = AGENTS.get(request.agent_id)
    if agent is None:
        raise HTTPException(status_code=404, detail=f"Unknown agent: {request.agent_id}")
    started = time.perf_counter()
    try:
        runner = load_agent(request.agent_id)
        response = runner(build_prompt(request))
    except EnvironmentError as exc:
        logger.warning("Agent configuration unavailable: %s", exc)
        raise HTTPException(
            status_code=503,
            detail="The assistant is temporarily unavailable. Please try again later.",
        ) from exc
    except RuntimeError as exc:
        logger.warning("Agent provider request failed: %s", exc)
        raise HTTPException(
            status_code=503,
            detail="The assistant could not complete that request. Please try again.",
        ) from exc
    except Exception as exc:
        logger.exception("Unexpected agent request failure")
        raise HTTPException(
            status_code=500,
            detail="An unexpected assistant error occurred. Please try again.",
        ) from exc
    response = response[:MAX_RESPONSE_CHARS]
    return ChatResponse(
        agent=AgentSummary(**agent),
        message=response,
        elapsed_ms=round((time.perf_counter() - started) * 1000),
    )

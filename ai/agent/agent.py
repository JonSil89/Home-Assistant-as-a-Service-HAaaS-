"""
HAaaS AI Agent — FastAPI entrypoint.

Exposes a minimal REST API that accepts natural-language commands,
delegates all business logic to the orchestrator, and returns
structured, typed responses.

Run locally (from the repo root):
    uvicorn ai.agent.agent:app --reload --port 8100

Interactive API docs available at:
    http://localhost:8100/docs   (Swagger UI)
    http://localhost:8100/redoc  (ReDoc)
"""
from __future__ import annotations

import uuid
from typing import Any, Optional

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

from ai.orchestrator.orchestrator import process


# ---------------------------------------------------------------------------
# Application
# ---------------------------------------------------------------------------

app = FastAPI(
    title="HAaaS AI Agent",
    description=(
        "AI control layer for Home Assistant as a Service. "
        "Accepts natural-language commands and routes them to the appropriate "
        "Home Assistant action via the orchestrator."
    ),
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)


# ---------------------------------------------------------------------------
# Request / response schemas
# ---------------------------------------------------------------------------

class CommandRequest(BaseModel):
    """Incoming command payload."""

    input: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="Natural-language command from the user.",
        examples=["Turn on the kitchen light", "Show me the current status"],
    )
    session_id: Optional[str] = Field(
        default=None,
        description=(
            "Session identifier used to maintain Short-Term Memory across turns. "
            "A new UUID is generated automatically if omitted."
        ),
    )


class CommandResponse(BaseModel):
    """Structured response returned by the agent."""

    session_id: str = Field(description="Session identifier (auto-generated if not provided).")
    response: str = Field(description="Human-readable reply from the agent.")
    action: Optional[str] = Field(default=None, description="Intent that was executed, if any.")
    data: Optional[dict[str, Any]] = Field(default=None, description="Raw tool output data.")


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check",
    tags=["ops"],
)
def health_check() -> HealthResponse:
    """Lightweight liveness probe — used by Docker and load balancers."""
    return HealthResponse(
        status="ok",
        service="haas-ai-agent",
        version=app.version,
    )


@app.post(
    "/command",
    response_model=CommandResponse,
    status_code=status.HTTP_200_OK,
    summary="Send a natural-language command",
    tags=["agent"],
)
def command(body: CommandRequest) -> CommandResponse:
    """
    Accept a natural-language command and return the agent's response.

    - Maintains per-session Short-Term Memory (STM) across multiple turns.
    - Delegates intent detection, tool dispatch, and memory updates to
      the orchestrator.
    - Returns a structured response including the raw tool output when applicable.

    **Example request:**
    ```json
    {
      "input": "Turn on the bedroom light",
      "session_id": "optional-uuid-for-continuity"
    }
    ```
    """
    stripped = body.input.strip()
    if not stripped:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Field 'input' must not be blank or whitespace-only.",
        )

    session_id = body.session_id or str(uuid.uuid4())

    result = process(session_id=session_id, user_input=stripped)

    return CommandResponse(
        session_id=session_id,
        response=result["response"],
        action=result.get("action"),
        data=result.get("data"),
    )

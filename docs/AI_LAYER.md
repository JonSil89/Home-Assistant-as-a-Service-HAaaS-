# AI Layer – Architecture & Design

## What is the AI Layer?

The AI layer is an **isolated, additive module** that sits alongside the existing
HAaaS infrastructure without modifying it.  It exposes a REST API that accepts
natural-language commands and routes them to the appropriate Home Assistant action.

All code lives exclusively under `/ai`.  No existing file has been modified.

---

## Position in the HAaaS Architecture

```
User / Voice / Frontend
        │
        ▼
┌───────────────────────┐
│  HAaaS AI Agent       │  ← POST /command  (port 8100)
│  ai/agent/agent.py    │
└──────────┬────────────┘
           │ delegates to
           ▼
┌───────────────────────┐
│  Orchestrator         │  ← rule-based intent detection + tool dispatch
│  ai/orchestrator/     │
└────┬──────────┬───────┘
     │          │
     ▼          ▼
┌─────────┐  ┌────────────────────────┐
│  STM    │  │  Tools                 │
│ memory/ │  │  tools/home_assistant  │
└─────────┘  └────────────────────────┘
                      │
                      ▼
            Home Assistant REST API
            (simulated — no real calls yet)
```

This maps directly onto the existing `docs/roadmap_llm.md` diagram:

| LLM Roadmap Layer     | AI Layer Component              |
|-----------------------|---------------------------------|
| AI Engine (B–D)       | Orchestrator                    |
| HA API Layer (E)      | tools/home_assistant.py         |
| Functional Tools (F)  | TOOL_REGISTRY in orchestrator   |
| Context / Memory      | memory/stm.py                   |

---

## Module Breakdown

### `ai/agent/agent.py`
FastAPI application.  Entrypoint for all external traffic.

- `GET  /health` — liveness probe for Docker and load balancers.
- `POST /command` — accepts `{ "input": "...", "session_id": "..." }` and returns
  `{ "session_id", "response", "action", "data" }`.

### `ai/orchestrator/orchestrator.py`
Stateless coordination layer.  Receives input, reads STM, classifies intent,
calls the appropriate tool, writes back to STM.  The `_detect_intent` function
is the single replacement point for an LLM classifier.

### `ai/memory/stm.py`
Short-Term Memory.  Stores the last N turns of each conversation session.

- `InMemorySTM` — default, zero-dependency, process-local.
- `RedisSTM` — commented-out stub; swap in by changing one line.
- TTL: sessions expire after 1 hour by default.

### `ai/tools/home_assistant.py`
Tool abstraction.  All functions currently return **simulated** responses.
Signatures are fixed; only the function bodies need to change when wiring
up real HA API calls.

---

## STM vs LTM Concept

| Dimension        | Short-Term Memory (STM)              | Long-Term Memory (LTM)               |
|------------------|--------------------------------------|--------------------------------------|
| Scope            | Single conversation session          | Cross-session / user-level           |
| Storage          | In-process dict → Redis              | Vector DB (Pinecone, pgvector, FAISS)|
| Lifetime         | Minutes → hours (TTL)                | Indefinite                           |
| Content          | Last intent, turn count, recent input| User preferences, automation history |
| Current status   | **Implemented** (InMemorySTM)        | Planned (see roadmap)                |

LTM is referenced in `docs/roadmap_pinecone.md` and `.env.example`
(`VECTOR_DB_TYPE`, `PINECONE_API_KEY`).  The AI layer is designed to accept
an LTM backend without structural changes — the orchestrator will call
`ltm.recall(session_id)` and `ltm.store(...)` in the same way it currently
calls STM.

---

## Running Locally

```bash
# From the repo root
pip install -r ai/requirements.txt
uvicorn ai.agent.agent:app --reload --port 8100
```

Example command:

```bash
curl -X POST http://localhost:8100/command \
     -H "Content-Type: application/json" \
     -d '{"input": "Turn on the kitchen light"}'
```

Expected response:

```json
{
  "session_id": "e3b0c...",
  "response": "Turning on the lights in the kitchen.",
  "action": "turn_on_light",
  "data": {
    "status": "success",
    "action": "turn_on",
    "entity_id": "light.kitchen",
    "simulated": true
  }
}
```

Interactive API docs: `http://localhost:8100/docs`

---

## Running with Docker

```bash
# From the repo root
docker compose -f ai/docker-compose.ai.yml up --build
```

The agent is exposed on `http://localhost:8100`.

---

## Future Roadmap

### Phase 1 – LLM Integration
Replace `_detect_intent` in `orchestrator.py` with an OpenAI / Azure OpenAI
function-calling request.  The orchestrator contract (input → intent + params)
does not change.

```
OPENAI_API_KEY=...  # already in .env.example
```

### Phase 2 – Real HA Integration
Set `HA_BASE_URL` and `HA_TOKEN` environment variables and replace the
simulated function bodies in `tools/home_assistant.py` with `httpx` calls
to the HA REST API.  Function signatures are frozen — no orchestrator changes.

### Phase 3 – Long-Term Memory (Vector DB)
Add `ai/memory/ltm.py` backed by Pinecone or FAISS (both already referenced
in `.env.example` and `docs/roadmap_pinecone.md`).  Store user preferences,
device history, and automation patterns for personalised responses.

### Phase 4 – Additional Tools
Extend `TOOL_REGISTRY` in `orchestrator.py` with new tool modules:

- `ai/tools/climate.py` — thermostat and HVAC control
- `ai/tools/notifications.py` — push alerts
- `ai/tools/calendar.py` — scheduling and time-based automations
- `ai/tools/energy.py` — smart energy monitoring

### Phase 5 – Multi-Tenancy
The `session_id` already isolates memory per conversation.  For SaaS
multi-tenancy, prefix all STM keys with `tenant_id:session_id` and enforce
RBAC at the agent layer.

---

## Safety & Compliance Notes

- No real HA calls are made in the current implementation (`simulated: true`).
- No secrets are hard-coded; all credentials use environment variables.
- The agent runs as a non-root user inside the Docker container.
- STM data does not leave the process (or Redis instance) — GDPR-safe by default.
- All new code is isolated in `/ai`; existing IaC, CI/CD, and docs are untouched.

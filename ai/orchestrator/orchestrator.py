"""
Orchestrator — the coordination brain of the AI control layer.

Responsibilities
----------------
1. Receive raw user input and a session identifier.
2. Load the session's Short-Term Memory (STM) context.
3. Detect the user's intent via a rule-based classifier.
4. Dispatch to the appropriate Home Assistant tool.
5. Persist the interaction back to STM.
6. Return a structured response to the caller (the agent).

Design notes
------------
- Intent detection is intentionally rule-based for now; the ``_detect_intent``
  function is the single replacement point for an LLM classifier later.
- All tool calls go through the ``TOOL_REGISTRY`` dict, making it trivial to
  add new tools (MQTT, climate, notifications, …) without touching dispatch logic.
- The orchestrator is stateless itself; state lives exclusively in the STM backend.
"""
from __future__ import annotations

from typing import Any, Callable

from ai.memory.stm import memory
from ai.tools import home_assistant as ha


# ---------------------------------------------------------------------------
# Tool registry
# ---------------------------------------------------------------------------
# Maps intent name → callable.  Each callable accepts **params and returns
# a dict[str, Any].  Add new tools here; nothing else changes.

TOOL_REGISTRY: dict[str, Callable[..., dict[str, Any]]] = {
    "turn_on_light": lambda room, **_: ha.turn_on_light(room),
    "turn_off_light": lambda room, **_: ha.turn_off_light(room),
    "get_status": lambda **_: ha.get_status(),
}

# Rooms the classifier recognises; extend as HA entities grow.
_KNOWN_ROOMS: list[str] = [
    "living room",
    "bedroom",
    "kitchen",
    "bathroom",
    "office",
    "hallway",
    "garage",
]

_FALLBACK_ROOM = "living_room"


# ---------------------------------------------------------------------------
# Intent detection
# ---------------------------------------------------------------------------

def _detect_intent(text: str) -> tuple[str, dict[str, Any]]:
    """
    Keyword-based intent classifier.

    Returns:
        (intent_name, params_dict)

    Replacement point: swap this function body for an LLM/NLU call
    (e.g. OpenAI function-calling, Rasa NLU) without changing the rest of
    the orchestrator.
    """
    lower = text.lower()

    if any(kw in lower for kw in ("turn on", "switch on", "put on", "enable")):
        return "turn_on_light", {"room": _extract_room(lower)}

    if any(kw in lower for kw in ("turn off", "switch off", "disable", "shut off")):
        return "turn_off_light", {"room": _extract_room(lower)}

    if any(kw in lower for kw in ("status", "what is", "show me", "what's on", "list")):
        return "get_status", {}

    return "unknown", {}


def _extract_room(text: str) -> str:
    """
    Extract the first recognised room name from *text*.
    Falls back to ``_FALLBACK_ROOM`` if none is found.
    """
    for room in _KNOWN_ROOMS:
        if room in text:
            return room
    return _FALLBACK_ROOM


# ---------------------------------------------------------------------------
# Human-readable response templates
# ---------------------------------------------------------------------------

_RESPONSES: dict[str, str] = {
    "turn_on_light": "Turning on the lights in the {room}.",
    "turn_off_light": "Turning off the lights in the {room}.",
    "get_status": "Here is the current device status.",
    "unknown": (
        "I didn't understand that command. "
        "Try: 'turn on the kitchen light', 'turn off bedroom light', or 'show status'."
    ),
}


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def process(session_id: str, user_input: str) -> dict[str, Any]:
    """
    Orchestrate a single user interaction.

    Args:
        session_id:  Unique identifier for the conversation session.
        user_input:  Raw natural-language string from the user.

    Returns:
        dict with:
          - ``response`` (str)   — human-readable reply
          - ``action``   (str|None) — intent that was executed, or None
          - ``data``     (Any)   — raw tool output, or None
    """
    # 1. Load existing session context
    context: dict[str, Any] = memory.get_context(session_id)

    # 2. Classify intent
    intent, params = _detect_intent(user_input)

    # 3. Dispatch to tool
    tool_result: dict[str, Any] | None = None
    if intent in TOOL_REGISTRY:
        tool_result = TOOL_REGISTRY[intent](**params)

    # 4. Build human-readable response
    template = _RESPONSES.get(intent, _RESPONSES["unknown"])
    response = template.format(**params) if params else template

    # 5. Persist to STM
    memory.update_context(session_id, {
        "last_input": user_input,
        "last_intent": intent,
        "last_response": response,
        "turn_count": int(context.get("turn_count", 0)) + 1,
    })

    return {
        "response": response,
        "action": intent if intent != "unknown" else None,
        "data": tool_result,
    }

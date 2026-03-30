"""
Home Assistant tool abstraction layer.

Current state: all functions return **simulated** responses.
No network calls are made.

Migration path to real HA
--------------------------
When real integration is ready:
1. Set HA_BASE_URL and HA_TOKEN via environment variables.
2. Replace each function body with an httpx (async-ready) call to the
   HA REST API.  The function signatures MUST NOT change so the
   orchestrator needs zero updates.

HA REST API reference:
  https://developers.home-assistant.io/docs/api/rest/
"""
from __future__ import annotations

import os
from typing import Any

# Reserved — not used until real integration is enabled.
HA_BASE_URL: str = os.getenv("HA_BASE_URL", "http://homeassistant.local:8123")
HA_TOKEN: str = os.getenv("HA_TOKEN", "")

_SIMULATED = True  # Flip to False once real HA calls are wired up


# ---------------------------------------------------------------------------
# Light controls
# ---------------------------------------------------------------------------

def turn_on_light(room: str) -> dict[str, Any]:
    """
    Turn on the light entity for *room*.

    Args:
        room: Human-readable room name, e.g. ``"living room"``.

    Returns:
        Action result dict with status, entity_id, and simulation flag.
    """
    entity_id = _room_to_entity(room)
    return {
        "status": "success",
        "action": "turn_on",
        "entity_id": entity_id,
        "simulated": _SIMULATED,
    }


def turn_off_light(room: str) -> dict[str, Any]:
    """
    Turn off the light entity for *room*.

    Args:
        room: Human-readable room name, e.g. ``"bedroom"``.

    Returns:
        Action result dict with status, entity_id, and simulation flag.
    """
    entity_id = _room_to_entity(room)
    return {
        "status": "success",
        "action": "turn_off",
        "entity_id": entity_id,
        "simulated": _SIMULATED,
    }


# ---------------------------------------------------------------------------
# Status snapshot
# ---------------------------------------------------------------------------

def get_status() -> dict[str, Any]:
    """
    Return a snapshot of all known device states.

    In the real implementation this will call:
      GET /api/states
    and return the parsed JSON.
    """
    return {
        "status": "ok",
        "simulated": _SIMULATED,
        "entities": {
            "light.living_room": {"state": "on", "brightness": 200},
            "light.bedroom": {"state": "off"},
            "light.kitchen": {"state": "on", "brightness": 128},
            "sensor.temperature_living_room": {"state": "21.5", "unit": "°C"},
            "sensor.temperature_bedroom": {"state": "19.8", "unit": "°C"},
            "binary_sensor.front_door": {"state": "closed"},
            "binary_sensor.back_door": {"state": "closed"},
            "switch.heating": {"state": "on"},
        },
    }


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _room_to_entity(room: str) -> str:
    """Convert a free-text room name to a HA entity_id slug."""
    return f"light.{room.lower().strip().replace(' ', '_')}"

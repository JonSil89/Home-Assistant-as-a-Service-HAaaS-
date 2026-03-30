"""
Short-Term Memory (STM) module.

Architecture decisions
-----------------------
- A backend-agnostic ``STMBackend`` ABC defines the contract.
- ``InMemorySTM`` is the default implementation (single-process, zero deps).
- A ``RedisSTM`` stub is included as a comment to show exactly what must be
  implemented when scaling to multi-instance deployments.
- Callers import only the ``memory`` singleton; swapping backends requires
  changing a single line in this file.

TTL
---
Each session entry carries a ``_ts`` timestamp.  ``get_context`` evicts
entries that have exceeded the TTL so memory does not grow unbounded.
"""
from __future__ import annotations

import time
from abc import ABC, abstractmethod
from typing import Any


# ---------------------------------------------------------------------------
# Abstract interface
# ---------------------------------------------------------------------------

class STMBackend(ABC):
    """Common interface for all STM storage backends."""

    @abstractmethod
    def get_context(self, session_id: str) -> dict[str, Any]:
        """Return the current context dict for *session_id*, or {} if absent/expired."""
        ...

    @abstractmethod
    def update_context(self, session_id: str, data: dict[str, Any]) -> None:
        """Merge *data* into the existing context for *session_id*."""
        ...

    @abstractmethod
    def clear_context(self, session_id: str) -> None:
        """Delete all context for *session_id* (e.g. on logout or session end)."""
        ...


# ---------------------------------------------------------------------------
# In-memory implementation
# ---------------------------------------------------------------------------

class InMemorySTM(STMBackend):
    """
    Process-local dictionary-based STM.

    Suitable for:
      - Local development
      - Single-container deployments

    Not suitable for:
      - Horizontally scaled deployments (use RedisSTM instead)
      - Persistence across restarts
    """

    def __init__(self, ttl_seconds: int = 3600) -> None:
        self._store: dict[str, dict[str, Any]] = {}
        self._ttl = ttl_seconds

    def get_context(self, session_id: str) -> dict[str, Any]:
        entry = self._store.get(session_id)
        if entry is None:
            return {}
        if time.time() - entry.get("_ts", 0) > self._ttl:
            del self._store[session_id]
            return {}
        return {k: v for k, v in entry.items() if k != "_ts"}

    def update_context(self, session_id: str, data: dict[str, Any]) -> None:
        existing = self._store.get(session_id, {})
        existing.update(data)
        existing["_ts"] = time.time()
        self._store[session_id] = existing

    def clear_context(self, session_id: str) -> None:
        self._store.pop(session_id, None)

    # Convenience — not part of the public ABC
    def session_count(self) -> int:
        """Return the number of active (non-expired) sessions."""
        now = time.time()
        return sum(
            1 for v in self._store.values()
            if now - v.get("_ts", 0) <= self._ttl
        )


# ---------------------------------------------------------------------------
# RedisSTM — plug-in replacement (uncomment and configure to enable)
# ---------------------------------------------------------------------------
# import json
# class RedisSTM(STMBackend):
#     """
#     Redis-backed STM for multi-instance / persistent deployments.
#     Requires: pip install redis
#     """
#     def __init__(self, redis_client: Any, ttl_seconds: int = 3600) -> None:
#         self._r = redis_client
#         self._ttl = ttl_seconds
#
#     def _key(self, session_id: str) -> str:
#         return f"haas:stm:{session_id}"
#
#     def get_context(self, session_id: str) -> dict[str, Any]:
#         raw = self._r.get(self._key(session_id))
#         return json.loads(raw) if raw else {}
#
#     def update_context(self, session_id: str, data: dict[str, Any]) -> None:
#         key = self._key(session_id)
#         existing = json.loads(self._r.get(key) or "{}")
#         existing.update(data)
#         self._r.setex(key, self._ttl, json.dumps(existing))
#
#     def clear_context(self, session_id: str) -> None:
#         self._r.delete(self._key(session_id))


# ---------------------------------------------------------------------------
# Module-level singleton
# ---------------------------------------------------------------------------
# To switch backends, replace InMemorySTM() with RedisSTM(redis_client).
# No other file needs to change.

memory: STMBackend = InMemorySTM()

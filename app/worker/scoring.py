"""Pure scoring rules — no Kafka, no DB, just the weights."""
from __future__ import annotations

_WEIGHTS = {
    "view": 1.0,
    "click": 3.0,
    "purchase": 10.0,
}


def score_for(event_type: str) -> float:
    """Return the score contribution for an event type (0 if unknown)."""
    return _WEIGHTS.get(event_type, 0.0)

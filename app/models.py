"""Domain models — plain dataclasses, free of any database concern."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Event:
    event_id: str
    user_id: str
    item_id: str
    event_type: str
    created_at: datetime


@dataclass(frozen=True)
class Recommendation:
    user_id: str
    item_id: str
    score: float
    updated_at: datetime

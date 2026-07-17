"""Pydantic request/response models — the API's runtime contract."""
from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field


class EventType(str, Enum):
    view = "view"
    click = "click"
    purchase = "purchase"


class EventIn(BaseModel):
    user_id: str = Field(min_length=1, max_length=128)
    item_id: str = Field(min_length=1, max_length=128)
    event_type: EventType


class EventAccepted(BaseModel):
    event_id: str
    status: str = "accepted"


class RecommendationOut(BaseModel):
    item_id: str
    score: float


class RecommendationsResponse(BaseModel):
    user_id: str
    count: int
    items: list[RecommendationOut]

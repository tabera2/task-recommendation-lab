"""Recommendation read endpoint: top-N items for a user (cached)."""
from __future__ import annotations

from fastapi import APIRouter, Query

from app.schemas import RecommendationOut, RecommendationsResponse
from app.services import recommendation_service

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


@router.get("/{user_id}", response_model=RecommendationsResponse)
def get_recommendations(
    user_id: str,
    limit: int = Query(default=20, ge=1, le=100),
) -> RecommendationsResponse:
    items = recommendation_service.get_top_n(user_id, limit)
    out = [RecommendationOut(**item) for item in items]
    return RecommendationsResponse(user_id=user_id, count=len(out), items=out)

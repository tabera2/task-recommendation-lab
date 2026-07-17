"""Service layer: cache-aside over the recommendation repository."""
from __future__ import annotations

from app.cache import redis_client
from app.repositories import recommendation_repo


def _cache_key(user_id: str, limit: int) -> str:
    version = redis_client.get_version(user_id)
    return f"recs:{user_id}:v{version}:limit:{limit}"


def get_top_n(user_id: str, limit: int) -> list[dict]:
    key = _cache_key(user_id, limit)

    cached = redis_client.get_json(key)
    if cached is not None:
        return cached  # cache hit

    rows = recommendation_repo.top_n(user_id, limit)
    items = [{"item_id": r.item_id, "score": r.score} for r in rows]
    redis_client.set_json(key, items)  # populate on miss
    return items

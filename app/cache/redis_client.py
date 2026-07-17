"""Redis access with TTL writes — failures are swallowed and logged."""
from __future__ import annotations

import json
import logging

import redis

from app.config import settings

log = logging.getLogger(__name__)
_client = redis.Redis.from_url(settings.redis_url, socket_timeout=0.25)


def get_json(key: str) -> object | None:
    try:
        raw = _client.get(key)
        return json.loads(raw) if raw else None
    except redis.RedisError as exc:
        log.warning("redis get failed key=%s err=%s", key, exc)
        return None


def set_json(key: str, value: object, ttl: int | None = None) -> None:
    try:
        _client.set(key, json.dumps(value), ex=ttl or settings.cache_ttl_seconds)
    except redis.RedisError as exc:
        log.warning("redis set failed key=%s err=%s", key, exc)


def get_version(user_id: str) -> int:
    """Current cache version for a user (0 if never bumped or on failure)."""
    try:
        raw = _client.get(f"recs_version:{user_id}")
        return int(raw) if raw else 0
    except redis.RedisError as exc:
        log.warning("redis version read failed user=%s err=%s", user_id, exc)
        return 0


def bump_version(user_id: str) -> None:
    """Invalidate a user's cached recs by incrementing their version (best-effort)."""
    try:
        _client.incr(f"recs_version:{user_id}")
    except redis.RedisError as exc:
        log.warning("redis version bump failed user=%s err=%s", user_id, exc)


def is_ready() -> bool:
    try:
        return bool(_client.ping())
    except redis.RedisError:
        return False

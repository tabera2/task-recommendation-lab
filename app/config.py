"""Environment-driven configuration (12-factor)."""
from __future__ import annotations

import logging
import os
from dataclasses import dataclass

log = logging.getLogger("config")


@dataclass(frozen=True)
class Settings:
    database_url: str = os.environ.get(
        "DATABASE_URL", "postgresql://localhost:5432/recs"
    )
    kafka_brokers: str = os.environ.get("KAFKA_BROKERS", "localhost:9092")
    events_topic: str = os.environ.get("EVENTS_TOPIC", "user-events")
    consumer_group: str = os.environ.get("CONSUMER_GROUP", "scoring-worker")
    redis_url: str = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
    cache_ttl_seconds: int = int(os.environ.get("CACHE_TTL_SECONDS", "30"))
    s3_bucket: str = os.environ.get("S3_BUCKET", "recs-exports")
    export_max_users: int = int(os.environ.get("EXPORT_MAX_USERS", "10000"))


settings = Settings()


def validate() -> None:
    """Fail fast on missing required config; warn on optional degradation."""
    required = {"DATABASE_URL": settings.database_url, "KAFKA_BROKERS": settings.kafka_brokers}
    missing = [name for name, value in required.items() if not value]
    if missing:
        raise RuntimeError(f"missing required config: {', '.join(missing)}")
    if not settings.redis_url:
        log.warning("REDIS_URL unset — running without cache (degraded)")
    # Log effective config at startup, redacting nothing sensitive here.
    log.info(
        "config loaded brokers=%s topic=%s bucket=%s",
        settings.kafka_brokers,
        settings.events_topic,
        settings.s3_bucket,
    )

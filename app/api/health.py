"""Liveness and readiness probes for load balancers and orchestrators."""
from __future__ import annotations

from fastapi import APIRouter, Response, status

from app.cache import redis_client
from app.db import session
from app.kafka import producer

router = APIRouter(tags=["health"])


@router.get("/health")
def health() -> dict:
    """Liveness: the process is up and serving. No dependency checks."""
    return {"status": "ok"}


@router.get("/ready")
def ready(response: Response) -> dict:
    """Readiness: can we actually serve traffic? Probe each dependency."""
    checks = {
        "postgres": _safe(session.healthcheck),
        "redis": _safe(redis_client.is_ready),
        "kafka": _safe(producer.is_ready),
    }
    # Postgres is required; Redis and Kafka are reported but non-fatal here.
    if not checks["postgres"]:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    return {"ready": checks["postgres"], "checks": checks}


def _safe(probe) -> bool:
    try:
        return bool(probe())
    except Exception:  # noqa: BLE001 - a probe must never raise
        return False

"""Ingestion endpoint: validate, enrich, publish to Kafka."""
from __future__ import annotations

import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, status
from kafka.errors import KafkaError

from app.kafka.producer import publish_event
from app.logging import configure
from app.schemas import EventAccepted, EventIn

router = APIRouter(prefix="/events", tags=["events"])
log = configure("api")


@router.post("", response_model=EventAccepted, status_code=status.HTTP_202_ACCEPTED)
def ingest_event(event: EventIn) -> EventAccepted:
    event_id = str(uuid.uuid4())
    payload = {
        "event_id": event_id,
        "correlation_id": event_id,
        "user_id": event.user_id,
        "item_id": event.item_id,
        "event_type": event.event_type.value,
        "ts": datetime.now(timezone.utc).isoformat(),
    }
    try:
        publish_event(payload)
    except KafkaError as exc:
        log.error(
            "publish failed", extra={"correlation_id": event_id, "user_id": event.user_id}
        )
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"event bus unavailable: {exc}",
        )
    log.info(
        "event accepted",
        extra={
            "correlation_id": event_id,
            "user_id": event.user_id,
            "item_id": event.item_id,
            "event_type": event.event_type.value,
        },
    )
    return EventAccepted(event_id=event_id)

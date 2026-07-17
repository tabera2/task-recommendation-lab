"""Worker loop: consume events, score them, upsert, invalidate cache."""
from __future__ import annotations

from app.cache import redis_client
from app.kafka.consumer import build_consumer
from app.logging import configure
from app.repositories import recommendation_repo
from app.worker.scoring import score_for

log = configure("worker")


def process_message(payload: dict) -> None:
    correlation_id = payload.get("correlation_id")
    delta = score_for(payload["event_type"])
    if delta <= 0:
        log.warning("unknown event type", extra={"correlation_id": correlation_id})
        return
    user_id = payload["user_id"]
    recommendation_repo.add_score(user_id, payload["item_id"], delta)
    redis_client.bump_version(user_id)
    log.info(
        "score updated",
        extra={
            "correlation_id": correlation_id,
            "user_id": user_id,
            "item_id": payload["item_id"],
        },
    )


def run() -> None:
    consumer = build_consumer()
    try:
        for message in consumer:
            process_message(message.value)
            consumer.commit()
    finally:
        consumer.close()


if __name__ == "__main__":
    run()

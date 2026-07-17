"""Thin wrapper around a Kafka producer with JSON serialization."""
from __future__ import annotations

import json

from kafka import KafkaProducer
from kafka.errors import KafkaError

from app.config import settings

_producer = KafkaProducer(
    bootstrap_servers=settings.kafka_brokers.split(","),
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    acks="all",
    retries=3,
)


def publish_event(payload: dict) -> None:
    """Publish synchronously; raise KafkaError if delivery fails."""
    future = _producer.send(settings.events_topic, value=payload)
    future.get(timeout=10)  # block so the caller learns about failures


def is_ready() -> bool:
    try:
        return bool(_producer.bootstrap_connected())
    except KafkaError:
        return False

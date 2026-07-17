"""A configured Kafka consumer for the events topic."""
from __future__ import annotations

import json

from kafka import KafkaConsumer

from app.config import settings


def build_consumer() -> KafkaConsumer:
    return KafkaConsumer(
        settings.events_topic,
        bootstrap_servers=settings.kafka_brokers.split(","),
        group_id=settings.consumer_group,
        enable_auto_commit=False,  # we commit manually after the DB write
        auto_offset_reset="earliest",
        value_deserializer=lambda b: json.loads(b.decode("utf-8")),
    )

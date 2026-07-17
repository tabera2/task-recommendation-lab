"""Structured JSON logging shared by the API and the worker."""
from __future__ import annotations

import json
import logging
import sys


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "level": record.levelname,
            "service": getattr(record, "service", "unknown"),
            "msg": record.getMessage(),
        }
        for field in ("correlation_id", "user_id", "item_id", "event_type"):
            value = getattr(record, field, None)
            if value is not None:
                payload[field] = value
        return json.dumps(payload)


def configure(service: str) -> logging.Logger:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())
    root = logging.getLogger()
    root.handlers = [handler]
    root.setLevel(logging.INFO)
    logger = logging.getLogger(service)
    return logging.LoggerAdapter(logger, {"service": service})  # type: ignore[return-value]

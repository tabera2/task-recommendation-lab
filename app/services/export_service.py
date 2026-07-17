"""Snapshot top-N recommendations per user to S3 as JSON Lines."""
from __future__ import annotations

import io
import json
import uuid
from datetime import datetime, timezone

from app.aws import s3_client
from app.config import settings
from app.repositories import recommendation_repo


def export_snapshot(top_n: int = 20) -> dict:
    export_id = str(uuid.uuid4())
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    key = f"snapshots/{stamp}/{export_id}.jsonl"

    buffer = io.StringIO()
    user_count = 0
    for user_id, rows in recommendation_repo.iter_top_per_user(
        top_n, settings.export_max_users
    ):
        record = {
            "user_id": user_id,
            "items": [{"item_id": r.item_id, "score": r.score} for r in rows],
        }
        buffer.write(json.dumps(record) + "\n")  # one JSON object per line
        user_count += 1

    uri = s3_client.put_text(key, buffer.getvalue())
    return {"export_id": export_id, "s3_uri": uri, "users": user_count}

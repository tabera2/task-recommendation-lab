"""Minimal S3 upload wrapper."""
from __future__ import annotations

import boto3

from app.config import settings

_s3 = boto3.client("s3")


def put_text(key: str, body: str) -> str:
    """Upload a UTF-8 text body to the configured bucket; return the s3:// uri."""
    _s3.put_object(
        Bucket=settings.s3_bucket,
        Key=key,
        Body=body.encode("utf-8"),
        ContentType="application/x-ndjson",
    )
    return f"s3://{settings.s3_bucket}/{key}"

"""Operational endpoint to snapshot recommendations to S3."""
from __future__ import annotations

from fastapi import APIRouter, Query, status

from app.services import export_service

router = APIRouter(prefix="/exports", tags=["exports"])


@router.post("", status_code=status.HTTP_201_CREATED)
def create_export(top_n: int = Query(default=20, ge=1, le=100)) -> dict:
    return export_service.export_snapshot(top_n=top_n)

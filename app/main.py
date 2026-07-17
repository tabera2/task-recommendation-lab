"""FastAPI application factory."""
from __future__ import annotations

from fastapi import FastAPI

from app.api import events, health, recommendations


def create_app() -> FastAPI:
    app = FastAPI(title="Recommendation System")
    app.include_router(health.router)
    app.include_router(events.router)
    app.include_router(recommendations.router)
    return app


app = create_app()

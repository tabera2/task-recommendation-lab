"""Web process entrypoint: start the FastAPI server."""
from __future__ import annotations

import uvicorn

from app.config import validate
from app.logging import configure


def main() -> None:
    configure("api")
    validate()  # fail fast before binding the port
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, workers=2)


if __name__ == "__main__":
    main()

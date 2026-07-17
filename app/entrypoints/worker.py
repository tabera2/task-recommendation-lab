"""Worker process entrypoint: start the Kafka scoring loop."""
from __future__ import annotations

from app.config import validate
from app.logging import configure
from app.worker.main import run


def main() -> None:
    configure("worker")
    validate()  # fail fast before consuming
    run()


if __name__ == "__main__":
    main()

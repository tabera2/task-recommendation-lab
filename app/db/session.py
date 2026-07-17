"""Database connection pool and a context-managed cursor."""
from __future__ import annotations

from contextlib import contextmanager
from typing import Iterator

import psycopg
from psycopg_pool import ConnectionPool

from app.config import settings

_pool = ConnectionPool(settings.database_url, min_size=1, max_size=10, open=True)


@contextmanager
def cursor(commit: bool = False) -> Iterator[psycopg.Cursor]:
    """Yield a cursor from a pooled connection, committing on success."""
    with _pool.connection() as conn:
        with conn.cursor() as cur:
            yield cur
        if commit:
            conn.commit()


def healthcheck() -> bool:
    """Return True if a trivial query succeeds against the pool."""
    with cursor() as cur:
        cur.execute("SELECT 1")
        return cur.fetchone() == (1,)

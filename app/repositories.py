"""Data access — all SQL lives here, behind intent-named methods."""
from __future__ import annotations

from app.db.session import cursor
from app.models import Event, Recommendation


class EventRepository:
    def insert(self, event: Event) -> None:
        with cursor(commit=True) as cur:
            cur.execute(
                """
                INSERT INTO events (event_id, user_id, item_id, event_type)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (event_id) DO NOTHING
                """,
                (event.event_id, event.user_id, event.item_id, event.event_type),
            )


class RecommendationRepository:
    def add_score(self, user_id: str, item_id: str, delta: float) -> None:
        """Increment a user's score for an item, inserting the row if absent."""
        with cursor(commit=True) as cur:
            cur.execute(
                """
                INSERT INTO recommendations (user_id, item_id, score, updated_at)
                VALUES (%s, %s, %s, now())
                ON CONFLICT (user_id, item_id)
                DO UPDATE SET score = recommendations.score + EXCLUDED.score,
                              updated_at = now()
                """,
                (user_id, item_id, delta),
            )

    def top_n(self, user_id: str, limit: int) -> list[Recommendation]:
        with cursor() as cur:
            cur.execute(
                """
                SELECT user_id, item_id, score, updated_at
                FROM recommendations
                WHERE user_id = %s
                ORDER BY score DESC
                LIMIT %s
                """,
                (user_id, limit),
            )
            return [Recommendation(*row) for row in cur.fetchall()]

    def iter_top_per_user(self, top_n: int, max_users: int):
        """Yield (user_id, [Recommendation, ...]) for each user, bounded by max_users."""
        with cursor() as cur:
            cur.execute(
                "SELECT DISTINCT user_id FROM recommendations ORDER BY user_id LIMIT %s",
                (max_users,),
            )
            user_ids = [row[0] for row in cur.fetchall()]
        for user_id in user_ids:
            yield user_id, self.top_n(user_id, top_n)


event_repo = EventRepository()
recommendation_repo = RecommendationRepository()

-- Core domain tables for the recommendation MVP.
CREATE TABLE IF NOT EXISTS users (
    id          BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    external_id TEXT UNIQUE NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS items (
    id          BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    external_id TEXT UNIQUE NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Raw events: kept minimal, mostly for debugging and replay.
CREATE TABLE IF NOT EXISTS events (
    id         BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    event_id   UUID UNIQUE NOT NULL,
    user_id    TEXT NOT NULL,
    item_id    TEXT NOT NULL,
    event_type TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Precomputed per-user item scores: the read path for recommendations.
CREATE TABLE IF NOT EXISTS recommendations (
    user_id    TEXT NOT NULL,
    item_id    TEXT NOT NULL,
    score      DOUBLE PRECISION NOT NULL DEFAULT 0,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (user_id, item_id)
);

-- Supports fast top-N retrieval: WHERE user_id = ? ORDER BY score DESC.
CREATE INDEX IF NOT EXISTS idx_recs_user_score
    ON recommendations (user_id, score DESC);

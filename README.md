# Google | Scalable Distributed Task & Recommendation System

An intermediate capstone that grows a real recommendation backend the way Google-scale systems are actually shaped — model the domain in Postgres, ingest user events through a streaming-first FastAPI, consume them in a Kafka worker that maintains per-user item scores, serve top-N recommendations behind a cache-aside Redis layer with best-effort invalidation, then make it operable with structured logs, health/readiness probes, an S3 snapshot export, and a clean web/worker process split ready for EC2.

Built step-by-step with [KhwajaLabs Build](https://khwajalabs.com).

## Stack
- Python
- FastAPI
- Postgres
- Redis
- Kafka
- Docker
- AWS

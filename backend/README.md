# Insurance Claim Optimizer API (MVP)

FastAPI backend per AGENT.md: Google Sign-In via Supabase (JWT validation), presigned uploads, claims, async jobs for drafting/PDF/email, SSE progress, and a simple worker. This MVP uses in-memory repositories so it runs without a database; replace repos with Postgres/Supabase in production.

## Run

- Copy `.env.example` to `.env` and edit if needed
- Dev server: `make dev` then open http://localhost:8080/docs
- Worker: `make worker` (MVP worker is a no-op loop)

## Notes

- Auth: send `Authorization: Bearer <token>`. Without JWKS configured, tokens are decoded unverified for local use only.
- Storage: upload URLs are placeholders; `POST /v1/files/{id}/complete` marks file as scanned+ready.
- Drafting/PDF/Email: jobs complete immediately with stubbed results.
- SSE: `GET /v1/stream/jobs/{job_id}` streams `progress` and `done` events.

## Project Structure

- `app/main.py`: FastAPI app, middleware, routers
- `app/auth`: JWT validator and user dependency
- `app/domain`: Pydantic DTOs and pure domain models
- `app/repositories`: In-memory repos (swap for Postgres/asyncpg)
- `app/services`: Business logic (storage, AI, PDF, email, idempotency)
- `app/api/v1`: Routers for health, users, files, providers, claims, jobs, stream, webhooks
- `app/workers/runner.py`: Worker loop scaffold

## Make Targets

- `make dev` — run API
- `make worker` — run worker
- `make fmt` / `make lint` — code quality
- `make test` — placeholder

## OpenAPI

FastAPI mounts `/docs` and `/openapi.json`. DTOs mirror AGENT.md examples.

## Next Steps

- Replace in-memory repos with asyncpg/Supabase tables and RLS.
- Implement real presigned URLs, virus scan, OCR, PDF, and email providers.
- Add tests with pytest + httpx.AsyncClient.


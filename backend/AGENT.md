
# AGENT.md — Backend API Generator Spec (Python + FastAPI + Supabase)

> **Purpose:** This document instructs an AI code agent (Cursor, Copilot, etc.) to generate a production-ready, object‑oriented backend for the **AI‑assisted Insurance Claim Optimizer** MVP. The stack is **Python + FastAPI + Supabase (Postgres + Storage + Auth)**, with **Google Sign‑In** via Supabase. Follow this spec exactly.

---

## 0) High‑Level Overview

### What the application is
A web backend that lets users:
1. **Sign in with Google** (Supabase Auth) to create a secure session (JWT).
2. **Upload evidence** (images, PDFs) to Supabase Storage; the backend manages file metadata, virus scan status, and OCR text.
3. **Create and edit claims** (incident details, provider metadata, attachments).
4. **Generate AI drafts** of claims (async jobs), receive progress via **SSE** or polling, refine the draft, and **finalize**.
5. **Export to PDF**, **email** the PDF to themselves, and optionally **submit** to an insurer (stretch goal).
6. **Track status** of the claim over time (timeline).

### Tech stack
- **Language:** Python 3.11+
- **Framework:** FastAPI (pydantic v2 models)
- **Database:** Supabase (Postgres) with RLS policies; connect via `asyncpg` or `supabase-py`
- **Auth:** Supabase Auth with **Google provider** (front‑end handles OAuth; backend validates JWT via Supabase JWKS)
- **Storage:** Supabase Storage (presigned URLs for direct uploads)
- **Queue/Jobs:** Database‑backed **Jobs** table (async workers) + FastAPI background tasks (MVP)
- **LLM calls:** Service class abstraction (DI) so the model provider is pluggable
- **PDF generation:** WeasyPrint or ReportLab (service class)
- **Email:** Postmark/Sendgrid (service class); abstract with interface
- **Observability:** `X-Request-Id`, structured logging, error middleware
- **Schema:** See “Database Schema” (matches API & Supabase schema provided)

### Architectural style
- **Object-Oriented**, **Hexagonal/Clean Architecture** flavor:
  - **Routers** (FastAPI) → **Controllers** → **Services** → **Repositories** → **DB**
  - **Domain models** (pydantic) separate from **DB DTOs**
  - **Dependency Injection** via FastAPI `Depends()`
  - **Idempotency** for POST actions (header `Idempotency-Key`)
  - **Problem+JSON** errors (RFC 7807)

---

**Note:** For the hackathon, keep workers simple: use a single background runner started with the app, or a separate `uvicorn` process with `runner.py` that polls the `jobs` table.

---

## 2) Environment Variables

Create `.env` and `.env.example` with:

```
APP_ENV=local
APP_PORT=8080
APP_HOST=0.0.0.0

SUPABASE_URL=
SUPABASE_ANON_KEY=
SUPABASE_SERVICE_ROLE_KEY=
SUPABASE_JWKS_URL=https://<project-id>.supabase.co/auth/v1/jwks

SUPABASE_STORAGE_BUCKET=claims

# Email (one provider for MVP)
EMAIL_PROVIDER=postmark
POSTMARK_API_TOKEN=

# PDF
PDF_ENGINE=weasyprint

# AI (drafting)
AI_PROVIDER=openai
OPENAI_API_KEY=

# CORS
CORS_ORIGINS=http://localhost:3000,https://staging.frontend.app,https://frontend.app
```

---

## 3) Auth Model (Google Sign‑In via Supabase)

- Frontend performs OAuth **Google Sign‑In** using Supabase JS.
- Frontend sends `Authorization: Bearer <access_token>` with each request.
- Backend validates JWT against Supabase **JWKS** (cache keys). Extract `sub` as `user_id`.
- RLS in Postgres ensures row‑level ownership.

Implement:
- `auth/jwt_validator.py` to fetch & cache JWKS, verify signature, check exp/iss/aud.
- `auth/dependencies.py` exposes `get_current_user()` returning a `UserPrincipal` (id, email).

Routes impacted:
- All `/v1/*` except `/v1/health` and `/v1/webhooks/incoming/*` require bearer token.

---

## 4) API Routes to Implement (v1)

Mirror the OpenAPI design (abbreviated here for routing & responsibilities). Implement handlers in **controllers** inside `api/v1/*.py`, calling **services** and **repositories**. All responses should conform to pydantic response models in `domain/dto/responses.py`.

### 4.1 Health
- `GET /v1/health` → `{ "status": "ok" }`

### 4.2 Auth (utility)
- `GET /v1/users/me` → Return decoded user profile (from DB `profiles` or on‑the‑fly).

### 4.3 Files (Presigned Uploads → Complete → Metadata)
- `POST /v1/files` → Create file metadata (purpose, content_type, filename, size), generate **presigned URL** (Supabase Storage) and return `{file_id, upload_url, headers}`.
- `POST /v1/files/{file_id}/complete` → Mark uploaded; queue virus scan + OCR job; set status `uploaded` → `scanning`.
- `GET /v1/files/{file_id}` → Return metadata (status, ocr_text, virus_scan).

### 4.4 Providers
- `GET /v1/providers?q=&limit=&cursor=` → Search providers (trgm index). Return cursor pagination.
- `POST /v1/providers/validate-policy` → Best‑effort regex/mask check based on provider & claim_type.

### 4.5 Claims
- `POST /v1/claims` (Idempotency‑Key supported) → Create draft claim with incident & attachments.- `GET /v1/claims?status=&limit=&cursor=` → List user claims.- `GET /v1/claims/{claim_id}` → Full claim (draft, attachments, validation, confidence).\ 
- `PATCH /v1/claims/{claim_id}` → Update editable fields (incident, draft, provider/policy).

### 4.6 Draft Generation (Async Jobs + SSE)
- `POST /v1/claims/{claim_id}/drafts` → Create `jobs` row type `draft_generation`; background worker processes:
  - Gather inputs (OCR, incident, provider metadata).
  - AI model produces structured draft (sections + notes).
  - Compute validation issues + confidence.
  - Upsert `claim_drafts`, update `claims` summary.
- `GET /v1/jobs/{job_id}` → Poll job status.
- `GET /v1/stream/jobs/{job_id}` → **SSE** progress stream.

### 4.7 Finalize / PDF / Email / Submit
- `POST /v1/claims/{claim_id}/finalize` → Locks content, recompute confidence.- `POST /v1/claims/{claim_id}/pdf` → `jobs` row type `pdf_generation`; worker writes PDF to Storage; return signed URL via `GET /v1/claims/{claim_id}/pdf`.- `GET /v1/claims/{claim_id}/pdf` → If ready, return signed URL.- `POST /v1/claims/{claim_id}/email` → `jobs` row type `email_delivery` (to user, with optional `cc`).- `POST /v1/claims/{claim_id}/submit` (stretch) → `jobs` row type `submission` (or return 501).- `GET /v1/claims/{claim_id}/status` → Return `claims` status & timeline (history table).

### 4.8 Webhooks
- `POST /v1/webhooks/outgoing` → Register user webhook (job events, claim status changes).- `POST /v1/webhooks/incoming/insurer` → Public endpoint (verifies provider signature if available).

---

## 5) Domain Models (Pydantic v2)

Create `domain/models/*.py` with classes for: `User`, `File`, `Provider`, `Claim`, `ClaimDraft`, `ValidationIssue`, `Confidence`, `Job`, `Webhook`. Keep domain models free of persistence concerns. Use **DTOs** in `domain/dto` for request/response schemas that match the API.

**Key DTOs (non‑exhaustive):**
- `CreateFileRequest`, `CreateFileResponse`, `FileResponse`
- `CreateClaimRequest`, `UpdateClaimRequest`, `ClaimResponse`
- `StartDraftRequest`, `JobResponse`
- `PolicyValidationRequest`, `PolicyValidationResult`
- `PDFResponse { url }`
- `Problem` per RFC 7807

---

## 6) Repositories (Database Layer)

Use async Postgres access. Options:
- `supabase-py` for Storage/Auth helpers, but **prefer direct SQL** (asyncpg) for performance and clarity.
- Implement repository classes:
  - `UsersRepo`, `FilesRepo`, `ProvidersRepo`, `ClaimsRepo`, `JobsRepo`, `WebhooksRepo`.
- Each repo provides CRUD methods with **parameterized SQL** mapped to DTOs.

Respect **RLS**: backend service uses **service role** for workers, normal bearer for user requests. In API request handlers, queries run under the user token (enforced by PostgREST equivalence) or use row filters on `user_id` to double‑check ownership.

---

## 7) Services (Business Logic)

Create stateless, testable service classes. Inject repos and other services in constructors.

- `StorageService`: presigned upload URL, signed download URL, bucket management.
- `VirusScanService`: MVP can stub to `clean`; interface allows later integration.
- `OCRService`: read images/PDFs and populate `files.ocr_text` (Tesseract or cloud API).
- `AIDraftingService`: orchestrates model prompt, parses response into structured draft; computes validation + confidence.
- `PDFService`: renders draft to PDF (template + WeasyPrint).
- `EmailService`: sends email with link/attachment; records in `emails` table.
- `SubmissionService`: placeholder; returns 501 if unsupported.
- `IdempotencyService`: deduplicate POST operations based on `Idempotency-Key` header.

---

## 8) Jobs & Workers

- A **Jobs** table holds `queued|running|succeeded|failed` states, `progress`, `result`, `error`.- `workers/runner.py` loop:  1. Claim a `queued` job using `FOR UPDATE SKIP LOCKED`.  2. Set `running`, periodically update `progress`.  3. On success, set `succeeded` and write `result`.  4. On error, set `failed` with message.- For **SSE**, stream `progress` updates read from DB poll (small interval) or a `LISTEN/NOTIFY` channel.

---

## 9) Middleware & Error Handling

- **Request ID**: generate `X-Request-Id` if absent; include in logs & responses.
- **CORS**: from `.env` `CORS_ORIGINS`.
- **Auth**: bearer token parsing; attach `current_user` to request state.
- **Problem+JSON**: on exceptions, return RFC 7807 payloads with helpful `detail` and `errors` map.
- **Rate limit headers** (static for MVP) and `X-Next-Cursor` for list endpoints.

---

## 10) OpenAPI & Docs

- Mount `/docs` and `/openapi.json` (FastAPI default). Ensure schemas mirror DTOs.
- Add examples for each DTO for quick frontend wiring.

---

## 11) Testing

- Use `pytest` + `httpx.AsyncClient`.- Fixtures for test DB (or a Supabase test project) and signed test JWT.- Unit tests for services (AI mocked), integration tests for routes.

---

## 12) Makefile / Commands

```
.PHONY: dev worker fmt lint test

dev:
	uvicorn app.main:app --reload --port $${APP_PORT:-8080}

worker:
	python -m app.workers.runner

fmt:
	ruff check --fix .

lint:
	ruff check .
	pylint app || true

test:
	pytest -q
```

---

## 13) Implementation Tasks (Cursor — do these in order)

- [ ] Scaffold **project structure** exactly as specified.
- [ ] Implement **config** loader (`pydantic-settings`) and DI `container.py` wiring.
- [ ] Add **middleware**: request id, CORS, auth, problem+json.- [ ] Implement **JWT validation** against **Supabase JWKS**; cache keys.
- [ ] Implement **domain models** & **DTOs** for all endpoints.
- [ ] Implement **repositories** with async SQL (parameterized) following the Supabase schema.- [ ] Implement **services** listed above (stubbing virus scan & submission is fine).
- [ ] Implement **routes** in `api/v1/*` as per section 4 with complete validation and examples.
- [ ] Implement **SSE** for job progress (poll DB; send `event: progress`).
- [ ] Implement **worker** loop to process jobs.- [ ] Add **OpenAPI** metadata (title/version/servers) and tag routes.- [ ] Add **tests** for health/auth/files/claims/jobs.- [ ] Provide **Dockerfile** and `README.md` run steps.

---

## 14) Example Snippets (show style)

### 14.1 DTO (pydantic v2)
```python
# app/domain/dto/requests.py
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Literal

ClaimType = Literal['auto','home','health','travel','other']

class CreateFileRequest(BaseModel):
    purpose: Literal['incident_image','policy_pdf','other']
    content_type: str
    filename: Optional[str] = None
    bytes: Optional[int] = None

class CreateClaimRequest(BaseModel):
    claim_type: ClaimType
    provider_id: Optional[str] = None
    provider_name: Optional[str] = None
    policy_number: Optional[str] = None
    incident_description: Optional[str] = None
    incident_occurred_at: Optional[str] = None
    incident_location: Optional[str] = None
    incident_metadata: dict = Field(default_factory=dict)
    attachments: List[str] = Field(default_factory=list)
```

### 14.2 Router (files)
```python
# app/api/v1/routes_files.py
from fastapi import APIRouter, Depends, Header
from app.domain.dto.requests import CreateFileRequest
from app.domain.dto.responses import CreateFileResponse, FileResponse
from app.auth.dependencies import get_current_user
from app.services.storage_service import StorageService

router = APIRouter(prefix="/v1/files", tags=["files"])

@router.post("", response_model=CreateFileResponse, status_code=201)
async def create_file_slot(
    payload: CreateFileRequest,
    storage: StorageService = Depends(),
    user = Depends(get_current_user),
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
):
    return await storage.create_upload_slot(user.id, payload, idempotency_key)

@router.post("/{file_id}/complete", response_model=FileResponse, status_code=202)
async def complete_upload(file_id: str, storage: StorageService = Depends(), user=Depends(get_current_user)):
    return await storage.mark_complete_and_queue_scan(user.id, file_id)

@router.get("/{file_id}", response_model=FileResponse)
async def get_file(file_id: str, storage: StorageService = Depends(), user=Depends(get_current_user)):
    return await storage.get_file(user.id, file_id)
```

### 14.3 Worker Claim
```python
# app/workers/runner.py
import asyncio
from app.repositories.jobs_repo import JobsRepo
from app.services.ai_drafting_service import AIDraftingService

async def run_once(jobs: JobsRepo, ai: AIDraftingService):
    job = await jobs.claim_next(queue_type="draft_generation")
    if not job:
        return False
    try:
        await jobs.start(job.id)
        await ai.process_draft_job(job)  # updates progress & claim_drafts
        await jobs.succeed(job.id, result={"ok": True})
    except Exception as e:
        await jobs.fail(job.id, str(e))
    return True

async def main():
    jobs = JobsRepo()
    ai = AIDraftingService()
    while True:
        did = await run_once(jobs, ai)
        await asyncio.sleep(0 if did else 1)

if __name__ == "__main__":
    asyncio.run(main())
```

---

## 15) Database Schema Reference

Use the **Supabase SQL** already prepared (tables: `profiles`, `providers`, `provider_claim_types`, `files`, `claims`, `claim_drafts`, `claim_attachments`, `claim_validation_issues`, `claim_status_history`, `jobs`, `webhooks`, `emails` + enums, triggers, RLS). Ensure repository queries align with those names and columns.

---

## 16) Run Instructions (README excerpt)

1. Copy `.env.example` → `.env` and fill values (Supabase keys, bucket, OpenAI, email).
2. `pip install -e .` (use `pyproject.toml` with FastAPI, uvicorn, asyncpg, httpx, pydantic‑settings, python‑jose, jwcrypto, weasyprint, sendgrid/postmark, pillow, pytesseract, tenacity, orjson, sse-starlette).
3. Start API: `make dev` → `http://localhost:8080/docs`.
4. Start Worker: `make worker`.
5. Frontend authenticates via **Supabase Google Sign‑In** and sends bearer to API.

---

## 17) Quality Bar

- 100% typed code, docstrings, and clear separation of concerns.
- No business logic in routers. Services/repositories test‑covered.
- Problem+JSON everywhere for errors.
- Idempotency for create/submit/email routes.
- SSE works on Chrome/Firefox; keep events small and frequent.

---

## 18) Deliverables

- Fully running FastAPI backend with all **routes**, **services**, **repos**, **worker**, **docs**, **tests**, and **Dockerfile** following this AGENT.md.
- Matches the OpenAPI described by the product spec; any drift must be documented.

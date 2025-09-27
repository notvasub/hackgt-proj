from __future__ import annotations

from fastapi import APIRouter, Depends, Header, Query

from app.auth.dependencies import get_current_user
from app.container import (
    get_ai_drafting_service,
    get_claims_repo,
    get_email_service,
    get_idempotency_service,
    get_pdf_service,
    get_submission_service,
)
from app.domain.dto.requests import CreateClaimRequest, StartDraftRequest, UpdateClaimRequest
from app.domain.dto.responses import ClaimResponse, JobResponse, PDFResponse
from app.repositories.claims_repo import ClaimsRepo
from app.services.ai_drafting_service import AIDraftingService
from app.services.email_service import EmailService
from app.services.idempotency_service import IdempotencyService
from app.services.pdf_service import PDFService
from app.services.submission_service import SubmissionService

router = APIRouter(prefix="/v1/claims", tags=["claims"])


@router.post("", response_model=ClaimResponse, status_code=201)
async def create_claim(
    payload: CreateClaimRequest,
    claims: ClaimsRepo = Depends(get_claims_repo),
    idempo: IdempotencyService = Depends(get_idempotency_service),
    user=Depends(get_current_user),
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
):
    cached = idempo.get(user.id, idempotency_key)
    if cached:
        return cached
    claim = await claims.create(user.id, payload)
    resp = await claims.to_response(claim)
    idempo.set(user.id, idempotency_key, resp)
    return resp


@router.get("")
async def list_claims(
    status: str | None = Query(default=None),
    limit: int = Query(default=20, ge=1, le=100),
    cursor: str | None = Query(default=None),
    claims: ClaimsRepo = Depends(get_claims_repo),
    user=Depends(get_current_user),
):
    items, next_cursor = await claims.list(user.id, status=status, limit=limit, cursor=cursor)
    return {"items": [await claims.to_response(c) for c in items], "next_cursor": next_cursor}


@router.get("/{claim_id}", response_model=ClaimResponse)
async def get_claim(claim_id: str, claims: ClaimsRepo = Depends(get_claims_repo), user=Depends(get_current_user)):
    claim = await claims.get(user.id, claim_id)
    return await claims.to_response(claim)


@router.patch("/{claim_id}", response_model=ClaimResponse)
async def update_claim(
    claim_id: str,
    payload: UpdateClaimRequest,
    claims: ClaimsRepo = Depends(get_claims_repo),
    user=Depends(get_current_user),
):
    updated = await claims.update(user.id, claim_id, payload)
    return await claims.to_response(updated)


@router.post("/{claim_id}/drafts", response_model=JobResponse, status_code=202)
async def start_draft(
    claim_id: str,
    payload: StartDraftRequest,
    ai: AIDraftingService = Depends(get_ai_drafting_service),
    user=Depends(get_current_user),
):
    job = await ai.enqueue_draft_job(user.id, claim_id, payload)
    return job


@router.post("/{claim_id}/finalize", response_model=ClaimResponse)
async def finalize_claim(
    claim_id: str,
    claims: ClaimsRepo = Depends(get_claims_repo),
    user=Depends(get_current_user),
):
    await claims.finalize(user.id, claim_id)
    claim = await claims.get(user.id, claim_id)
    return await claims.to_response(claim)


@router.post("/{claim_id}/pdf", response_model=JobResponse)
async def generate_pdf(
    claim_id: str,
    pdf: PDFService = Depends(get_pdf_service),
    user=Depends(get_current_user),
):
    return await pdf.enqueue_pdf_job(user.id, claim_id)


@router.get("/{claim_id}/pdf", response_model=PDFResponse)
async def get_pdf(
    claim_id: str,
    pdf: PDFService = Depends(get_pdf_service),
    user=Depends(get_current_user),
):
    return await pdf.get_pdf(user.id, claim_id)


@router.post("/{claim_id}/email", response_model=JobResponse)
async def send_email(
    claim_id: str,
    email: EmailService = Depends(get_email_service),
    idempo: IdempotencyService = Depends(get_idempotency_service),
    user=Depends(get_current_user),
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
):
    cached = idempo.get(user.id, idempotency_key)
    if cached:
        return cached
    job = await email.enqueue_email_job(user.id, claim_id)
    idempo.set(user.id, idempotency_key, job)
    return job


@router.post("/{claim_id}/submit")
async def submit_claim(
    claim_id: str,
    submission: SubmissionService = Depends(get_submission_service),
    user=Depends(get_current_user),
):
    return await submission.submit(user.id, claim_id)


@router.get("/{claim_id}/status")
async def claim_status(claim_id: str, claims: ClaimsRepo = Depends(get_claims_repo), user=Depends(get_current_user)):
    return await claims.status(user.id, claim_id)


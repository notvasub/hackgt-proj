from __future__ import annotations

from typing import Optional

from app.config import Settings
from app.repositories.claims_repo import ClaimsRepo
from app.repositories.jobs_repo import JobsRepo


# Simple in-memory map claim_id -> url
_PDF_URLS: dict[str, str] = {}


class PDFService:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._jobs: Optional[JobsRepo] = None
        self._claims: Optional[ClaimsRepo] = None

    def attach(self, jobs: JobsRepo, claims: ClaimsRepo) -> None:
        self._jobs = jobs
        self._claims = claims

    async def enqueue_pdf_job(self, user_id: str, claim_id: str) -> dict:
        if not self._jobs:
            self._jobs = JobsRepo()
        job = await self._jobs.enqueue(user_id, "pdf_generation", {"claim_id": claim_id})
        # Generate a fake URL immediately for MVP
        _PDF_URLS[claim_id] = f"https://storage.fake/pdfs/{claim_id}.pdf"
        await self._jobs.succeed(job["id"], {"url": _PDF_URLS[claim_id]})
        return job

    async def get_pdf(self, user_id: str, claim_id: str) -> dict:
        url = _PDF_URLS.get(claim_id)
        return {"url": url}


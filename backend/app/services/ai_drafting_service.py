from __future__ import annotations

from typing import Any, Dict, List

from app.config import Settings
from app.domain.dto.requests import StartDraftRequest
from app.repositories.claims_repo import ClaimsRepo
from app.repositories.files_repo import FilesRepo
from app.repositories.jobs_repo import JobsRepo
from app.repositories.providers_repo import ProvidersRepo


class AIDraftingService:
    def __init__(
        self,
        settings: Settings,
        claims_repo: ClaimsRepo,
        files_repo: FilesRepo,
        providers_repo: ProvidersRepo,
        jobs_repo: JobsRepo,
    ) -> None:
        self._settings = settings
        self._claims = claims_repo
        self._files = files_repo
        self._providers = providers_repo
        self._jobs = jobs_repo

    async def enqueue_draft_job(self, user_id: str, claim_id: str, payload: StartDraftRequest) -> dict:
        # Enqueue and return job object
        job = await self._jobs.enqueue(user_id, "draft_generation", {"claim_id": claim_id})
        # For MVP, instantly produce a draft
        await self.process_draft_job(job["id"], user_id=user_id, claim_id=claim_id)
        return await self._jobs.get(user_id, job["id"])

    async def process_draft_job(self, job_id: str, user_id: str, claim_id: str) -> None:
        await self._jobs.start(job_id)
        claim = await self._claims.get(user_id, claim_id)
        await self._jobs.progress(job_id, 20)
        draft = self._simple_draft(claim.incident_description or "")
        await self._jobs.progress(job_id, 70)
        issues = self._simple_issues(claim)
        confidence = 0.8 if not issues else 0.6
        await self._claims.save_draft(claim_id, draft, confidence, issues)
        await self._jobs.succeed(job_id, {"claim_id": claim_id, "draft_ready": True})

    def _simple_draft(self, description: str) -> Dict[str, Any]:
        return {
            "summary": description[:200] or "No incident description provided.",
            "sections": [
                {"title": "Incident", "text": description or "TBD"},
                {"title": "Damages", "text": "TBD"},
                {"title": "Requested Action", "text": "Please process this claim promptly."},
            ],
            "notes": [],
        }

    def _simple_issues(self, claim) -> List[str]:
        issues: List[str] = []
        if not claim.policy_number:
            issues.append("Policy number missing")
        if not claim.provider_id and not claim.provider_name:
            issues.append("Provider not selected")
        if not claim.incident_description:
            issues.append("Incident description missing")
        return issues


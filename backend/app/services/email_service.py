from __future__ import annotations

from app.config import Settings
from app.repositories.jobs_repo import JobsRepo


class EmailService:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._jobs = JobsRepo()

    async def enqueue_email_job(self, user_id: str, claim_id: str) -> dict:
        job = await self._jobs.enqueue(user_id, "email_delivery", {"claim_id": claim_id})
        # Pretend to send immediately in MVP
        await self._jobs.succeed(job["id"], {"sent": True})
        return job


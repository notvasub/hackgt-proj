from __future__ import annotations

from typing import Dict, Optional

from app.domain.models.core import Job
from app.utils.ids import new_id


_JOBS: Dict[str, Job] = {}


class JobsRepo:
    async def enqueue(self, user_id: str, type_: str, payload: dict | None = None) -> dict:
        job_id = new_id("job")
        job = Job(id=job_id, user_id=user_id, type=type_)
        _JOBS[job_id] = job
        return await self.to_response(job)

    async def get(self, user_id: str, job_id: str) -> dict:
        job = _JOBS.get(job_id)
        if not job or job.user_id != user_id:
            raise KeyError("job_not_found")
        return await self.to_response(job)

    async def claim_next(self, queue_type: str) -> Optional[Job]:
        for job in _JOBS.values():
            if job.type == queue_type and job.status == "queued":
                job.status = "running"
                return job
        return None

    async def start(self, job_id: str) -> None:
        _JOBS[job_id].status = "running"

    async def progress(self, job_id: str, progress: int) -> None:
        _JOBS[job_id].progress = progress

    async def succeed(self, job_id: str, result: dict | None = None) -> None:
        job = _JOBS[job_id]
        job.status = "succeeded"
        job.progress = 100
        if result is not None:
            job.result = result

    async def fail(self, job_id: str, error: str) -> None:
        job = _JOBS[job_id]
        job.status = "failed"
        job.error = error

    async def to_response(self, job: Job) -> dict:
        return {
            "id": job.id,
            "type": job.type,
            "status": job.status,
            "progress": job.progress,
            "result": job.result,
            "error": job.error,
        }


from __future__ import annotations

import asyncio

from fastapi import APIRouter, Depends
from starlette.responses import EventSourceResponse

from app.auth.dependencies import get_current_user
from app.container import get_jobs_repo
from app.repositories.jobs_repo import JobsRepo

router = APIRouter(prefix="/v1/stream", tags=["stream"])


@router.get("/jobs/{job_id}")
async def stream_job(job_id: str, jobs: JobsRepo = Depends(get_jobs_repo), user=Depends(get_current_user)):
    async def event_gen():
        last_progress = -1
        while True:
            job = await jobs.get(user.id, job_id)
            if job["progress"] != last_progress:
                last_progress = job["progress"]
                yield f"event: progress\ndata: {job['progress']}\n\n"
            if job["status"] in ("succeeded", "failed"):
                yield f"event: done\ndata: {job['status']}\n\n"
                break
            await asyncio.sleep(0.5)

    return EventSourceResponse(event_gen())


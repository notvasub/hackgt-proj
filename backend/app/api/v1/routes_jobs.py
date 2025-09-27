from __future__ import annotations

from fastapi import APIRouter, Depends

from app.auth.dependencies import get_current_user
from app.container import get_jobs_repo
from app.domain.dto.responses import JobResponse
from app.repositories.jobs_repo import JobsRepo

router = APIRouter(prefix="/v1/jobs", tags=["jobs"])


@router.get("/{job_id}", response_model=JobResponse)
async def get_job(job_id: str, jobs: JobsRepo = Depends(get_jobs_repo), user=Depends(get_current_user)):
    return await jobs.get(user.id, job_id)


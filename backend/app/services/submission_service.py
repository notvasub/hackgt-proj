from __future__ import annotations

from fastapi import HTTPException, status


class SubmissionService:
    async def submit(self, user_id: str, claim_id: str):
        raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Submission not supported in MVP")


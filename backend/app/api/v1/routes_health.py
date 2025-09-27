from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(prefix="/v1/health", tags=["health"])


@router.get("")
async def health():
    return {"status": "ok"}


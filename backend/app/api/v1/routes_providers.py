from __future__ import annotations

from fastapi import APIRouter, Depends, Query

from app.auth.dependencies import get_current_user
from app.container import get_providers_repo
from app.domain.dto.requests import PolicyValidationRequest
from app.domain.dto.responses import PolicyValidationResult
from app.repositories.providers_repo import ProvidersRepo

router = APIRouter(prefix="/v1/providers", tags=["providers"])


@router.get("")
async def search_providers(
    q: str = Query(default=""),
    limit: int = Query(default=20, ge=1, le=100),
    cursor: str | None = Query(default=None),
    providers: ProvidersRepo = Depends(get_providers_repo),
    user=Depends(get_current_user),
):
    items, next_cursor = await providers.search(q=q, limit=limit, cursor=cursor)
    headers = {"X-Next-Cursor": next_cursor or ""}
    return {"items": items, "next_cursor": next_cursor}


@router.post("/validate-policy", response_model=PolicyValidationResult)
async def validate_policy(
    payload: PolicyValidationRequest,
    providers: ProvidersRepo = Depends(get_providers_repo),
    user=Depends(get_current_user),
):
    return await providers.validate_policy(payload)


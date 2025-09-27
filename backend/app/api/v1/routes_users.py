from __future__ import annotations

from fastapi import APIRouter, Depends

from app.auth.dependencies import UserPrincipal, get_current_user

router = APIRouter(prefix="/v1/users", tags=["auth"])


@router.get("/me")
async def get_me(user: UserPrincipal = Depends(get_current_user)):
    return {"id": user.id, "email": user.email}


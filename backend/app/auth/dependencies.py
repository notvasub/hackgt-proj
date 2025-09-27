from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from fastapi import Depends, Header, HTTPException, Request, status

from app.auth.jwt_validator import DecodedToken, validate_jwt


@dataclass
class UserPrincipal:
    id: str
    email: Optional[str]
    token: DecodedToken


async def get_current_user(
    request: Request,
    authorization: str | None = Header(default=None, alias="Authorization"),
) -> UserPrincipal:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing bearer token")
    token = authorization.split(" ", 1)[1]
    try:
        decoded = await validate_jwt(token)
        return UserPrincipal(id=decoded.sub, email=decoded.email, token=decoded)
    except Exception as exc:  # noqa: BLE001 - bubble as 401
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc))


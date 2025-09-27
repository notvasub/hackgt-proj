from __future__ import annotations

import asyncio
import json
import time
from dataclasses import dataclass
from typing import Any, Dict, Optional

import httpx
from jose import jwk, jwt
from jose.utils import base64url_decode

from app.config import get_settings


@dataclass
class DecodedToken:
    sub: str
    email: Optional[str]
    raw: Dict[str, Any]


class JWKSCache:
    def __init__(self, ttl_seconds: int = 300) -> None:
        self._keys: Dict[str, Any] = {}
        self._expires_at = 0
        self._ttl = ttl_seconds
        self._lock = asyncio.Lock()

    async def get_keys(self) -> Dict[str, Any]:
        async with self._lock:
            now = time.time()
            if now < self._expires_at and self._keys:
                return self._keys
            url = get_settings().supabase_jwks_url
            if not url:
                # No JWKS URL configured; return empty to allow local dev bypass
                self._keys = {}
                self._expires_at = now + self._ttl
                return self._keys
            async with httpx.AsyncClient(timeout=5) as client:
                resp = await client.get(url)
                resp.raise_for_status()
                data = resp.json()
                keys = {k["kid"]: k for k in data.get("keys", [])}
                self._keys = keys
                self._expires_at = now + self._ttl
                return self._keys


_jwks_cache = JWKSCache()


async def validate_jwt(token: str, audience: Optional[str] = None) -> DecodedToken:
    """Validate a JWT against Supabase JWKS.

    For local development without JWKS configured, this function will decode
    the token without verification to extract minimal claims. DO NOT USE in prod.
    """
    settings = get_settings()
    headers = jwt.get_unverified_header(token)
    kid = headers.get("kid")

    keys = await _jwks_cache.get_keys()
    if keys and kid in keys:
        key = keys[kid]
        public_key = jwk.construct(key)
        message, encoded_sig = token.rsplit(".", 1)
        decoded_sig = base64url_decode(encoded_sig.encode())
        if not public_key.verify(message.encode(), decoded_sig):
            raise ValueError("Invalid JWT signature")
        claims = jwt.get_unverified_claims(token)
        now = int(time.time())
        if claims.get("exp") and now > int(claims["exp"]):
            raise ValueError("JWT expired")
        if audience and claims.get("aud") and audience not in claims["aud"]:
            raise ValueError("Invalid audience")
    else:
        # Fallback for local testing: unverified decode
        claims = jwt.get_unverified_claims(token)

    return DecodedToken(sub=str(claims.get("sub")), email=claims.get("email"), raw=claims)  # type: ignore[arg-type]


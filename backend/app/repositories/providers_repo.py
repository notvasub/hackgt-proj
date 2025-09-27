from __future__ import annotations

from typing import List, Optional, Tuple

from app.domain.dto.requests import PolicyValidationRequest
from app.domain.dto.responses import PolicyValidationResult


_PROVIDERS = [
    {"id": "prov_abc", "name": "Acme Insurance", "claim_types": ["auto", "home", "health"]},
    {"id": "prov_xyz", "name": "Zen Assurance", "claim_types": ["travel", "other"]},
]


class ProvidersRepo:
    async def search(self, q: str, limit: int, cursor: Optional[str]) -> Tuple[List[dict], Optional[str]]:
        ql = q.lower()
        results = [p for p in _PROVIDERS if ql in p["name"].lower() or ql in p["id"]]
        return results[:limit], None

    async def validate_policy(self, payload: PolicyValidationRequest) -> PolicyValidationResult:
        policy = payload.policy_number.strip()
        digits = "".join(ch for ch in policy if ch.isdigit())
        valid = len(digits) >= 6
        normalized = f"****{digits[-4:]}" if digits else None
        hints = [] if valid else ["Policy number too short"]
        return PolicyValidationResult(valid=valid, normalized=normalized, hints=hints)


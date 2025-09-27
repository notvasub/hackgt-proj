from __future__ import annotations

from typing import Dict, List, Optional, Tuple

from app.domain.dto.requests import CreateClaimRequest, UpdateClaimRequest
from app.domain.models.core import Claim, ClaimDraft
from app.domain.dto.responses import ClaimResponse
from app.utils.ids import new_id


_CLAIMS: Dict[str, Claim] = {}
_CLAIM_DRAFTS: Dict[str, ClaimDraft] = {}


class ClaimsRepo:
    async def create(self, user_id: str, payload: CreateClaimRequest) -> Claim:
        claim_id = new_id("clm")
        claim = Claim(
            id=claim_id,
            user_id=user_id,
            claim_type=payload.claim_type,
            provider_id=payload.provider_id,
            provider_name=payload.provider_name,
            policy_number=payload.policy_number,
            incident_description=payload.incident_description,
            incident_occurred_at=payload.incident_occurred_at,
            incident_location=payload.incident_location,
            incident_metadata=payload.incident_metadata,
            attachments=payload.attachments,
        )
        _CLAIMS[claim_id] = claim
        return claim

    async def get(self, user_id: str, claim_id: str) -> Claim:
        claim = _CLAIMS.get(claim_id)
        if not claim or claim.user_id != user_id:
            raise KeyError("claim_not_found")
        return claim

    async def list(self, user_id: str, status: Optional[str], limit: int, cursor: Optional[str]) -> Tuple[List[Claim], Optional[str]]:
        items = [c for c in _CLAIMS.values() if c.user_id == user_id and (not status or c.status == status)]
        items.sort(key=lambda c: c.created_at, reverse=True)
        return items[:limit], None

    async def update(self, user_id: str, claim_id: str, payload: UpdateClaimRequest) -> Claim:
        claim = await self.get(user_id, claim_id)
        data = payload.model_dump(exclude_unset=True)
        for k, v in data.items():
            if v is not None:
                setattr(claim, k, v)
        return claim

    async def finalize(self, user_id: str, claim_id: str) -> None:
        claim = await self.get(user_id, claim_id)
        claim.status = "finalized"

    async def save_draft(self, claim_id: str, content: dict, confidence: float, issues: List[str]) -> None:
        _CLAIM_DRAFTS[claim_id] = ClaimDraft(claim_id=claim_id, content=content, confidence=confidence, issues=issues)

    async def to_response(self, claim: Claim) -> ClaimResponse:
        draft = _CLAIM_DRAFTS.get(claim.id)
        return ClaimResponse(
            id=claim.id,
            status=claim.status,
            claim_type=claim.claim_type,
            provider_id=claim.provider_id,
            provider_name=claim.provider_name,
            policy_number=claim.policy_number,
            incident_description=claim.incident_description,
            incident_occurred_at=claim.incident_occurred_at,
            incident_location=claim.incident_location,
            incident_metadata=claim.incident_metadata,
            attachments=claim.attachments,
            draft=draft.content if draft else None,
            confidence=draft.confidence if draft else None,
            issues=draft.issues if draft else [],
        )

    async def status(self, user_id: str, claim_id: str) -> dict:
        claim = await self.get(user_id, claim_id)
        return {"id": claim.id, "status": claim.status}


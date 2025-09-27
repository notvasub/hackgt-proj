from __future__ import annotations

from typing import List, Literal, Optional
from pydantic import BaseModel, Field, EmailStr


ClaimType = Literal["auto", "home", "health", "travel", "other"]


class CreateFileRequest(BaseModel):
    purpose: Literal["incident_image", "policy_pdf", "other"]
    content_type: str
    filename: Optional[str] = None
    bytes: Optional[int] = None


class CreateClaimRequest(BaseModel):
    claim_type: ClaimType
    provider_id: Optional[str] = None
    provider_name: Optional[str] = None
    policy_number: Optional[str] = None
    incident_description: Optional[str] = None
    incident_occurred_at: Optional[str] = None
    incident_location: Optional[str] = None
    incident_metadata: dict = Field(default_factory=dict)
    attachments: List[str] = Field(default_factory=list)


class UpdateClaimRequest(BaseModel):
    provider_id: Optional[str] = None
    provider_name: Optional[str] = None
    policy_number: Optional[str] = None
    incident_description: Optional[str] = None
    incident_occurred_at: Optional[str] = None
    incident_location: Optional[str] = None
    incident_metadata: dict | None = None
    attachments: List[str] | None = None


class StartDraftRequest(BaseModel):
    notes: Optional[str] = None


class PolicyValidationRequest(BaseModel):
    provider_id: Optional[str] = None
    claim_type: ClaimType
    policy_number: str
    email: Optional[EmailStr] = None


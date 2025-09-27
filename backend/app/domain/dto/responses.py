from __future__ import annotations

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class CreateFileResponse(BaseModel):
    file_id: str
    upload_url: str
    headers: Dict[str, str] = Field(default_factory=dict)


class FileResponse(BaseModel):
    id: str
    purpose: str
    content_type: str
    filename: Optional[str]
    size: Optional[int]
    status: str
    virus_scan: str
    ocr_text: Optional[str]


class ClaimResponse(BaseModel):
    id: str
    status: str
    claim_type: str
    provider_id: Optional[str] = None
    provider_name: Optional[str] = None
    policy_number: Optional[str] = None
    incident_description: Optional[str] = None
    incident_occurred_at: Optional[str] = None
    incident_location: Optional[str] = None
    incident_metadata: Dict[str, Any] = Field(default_factory=dict)
    attachments: List[str] = Field(default_factory=list)
    draft: Optional[Dict[str, Any]] = None
    confidence: Optional[float] = None
    issues: List[str] = Field(default_factory=list)


class JobResponse(BaseModel):
    id: str
    type: str
    status: str
    progress: int
    result: Dict[str, Any] = Field(default_factory=dict)
    error: Optional[str] = None


class PolicyValidationResult(BaseModel):
    valid: bool
    normalized: Optional[str] = None
    hints: List[str] = Field(default_factory=list)


class PDFResponse(BaseModel):
    url: Optional[str]


from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class User:
    id: str
    email: Optional[str] = None


@dataclass
class File:
    id: str
    user_id: str
    purpose: str
    content_type: str
    filename: Optional[str] = None
    size: Optional[int] = None
    status: str = "pending"  # pending|uploaded|scanning|ready|failed
    virus_scan: str = "unknown"  # clean|infected|unknown
    ocr_text: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class Provider:
    id: str
    name: str
    claim_types: List[str] = field(default_factory=list)


@dataclass
class Claim:
    id: str
    user_id: str
    claim_type: str
    provider_id: Optional[str] = None
    provider_name: Optional[str] = None
    policy_number: Optional[str] = None
    incident_description: Optional[str] = None
    incident_occurred_at: Optional[str] = None
    incident_location: Optional[str] = None
    incident_metadata: Dict[str, Any] = field(default_factory=dict)
    attachments: List[str] = field(default_factory=list)
    status: str = "draft"
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class ClaimDraft:
    claim_id: str
    content: Dict[str, Any] = field(default_factory=dict)
    confidence: float = 0.5
    issues: List[str] = field(default_factory=list)


@dataclass
class Job:
    id: str
    user_id: str
    type: str
    status: str = "queued"  # queued|running|succeeded|failed
    progress: int = 0
    result: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None


@dataclass
class Webhook:
    id: str
    user_id: str
    url: str


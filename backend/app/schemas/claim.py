"""Claim-related Pydantic schemas."""

import uuid
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from app.models.claim import ClaimType, ClaimStatus, ProcessingStatus


class ClaimFileResponse(BaseModel):
    """Schema for claim file response."""
    id: uuid.UUID
    filename: str
    original_filename: str
    file_size: int
    content_type: str
    s3_url: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class ClaimProcessingJobResponse(BaseModel):
    """Schema for processing job response."""
    id: uuid.UUID
    status: ProcessingStatus
    error_message: Optional[str] = None
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class ClaimCreate(BaseModel):
    """Schema for claim creation."""
    incident_description: str = Field(..., min_length=10, max_length=5000)
    incident_date: Optional[datetime] = None
    incident_location: Optional[str] = Field(None, max_length=500)
    insurance_provider: str = Field(..., min_length=2, max_length=255)
    policy_number: str = Field(..., min_length=3, max_length=100)
    claim_type: ClaimType


class ClaimUpdate(BaseModel):
    """Schema for claim updates."""
    optimized_description: Optional[str] = None
    damage_assessment: Optional[str] = None
    claim_justification: Optional[str] = None
    requested_amount: Optional[float] = Field(None, ge=0)
    strength_score: Optional[int] = Field(None, ge=0, le=100)


class ClaimResponse(BaseModel):
    """Schema for claim response."""
    id: uuid.UUID
    user_id: uuid.UUID
    
    # Incident details
    incident_description: str
    incident_date: Optional[datetime] = None
    incident_location: Optional[str] = None
    
    # Insurance information
    insurance_provider: str
    policy_number: str
    claim_type: ClaimType
    
    # AI-generated content
    optimized_description: Optional[str] = None
    damage_assessment: Optional[str] = None
    claim_justification: Optional[str] = None
    requested_amount: Optional[float] = None
    strength_score: Optional[int] = None
    
    # Status and metadata
    status: ClaimStatus
    created_at: datetime
    updated_at: datetime
    
    # Related data
    files: List[ClaimFileResponse] = []
    processing_jobs: List[ClaimProcessingJobResponse] = []
    
    class Config:
        from_attributes = True


class ClaimListResponse(BaseModel):
    """Schema for claim list response."""
    claims: List[ClaimResponse]
    total: int
    page: int
    size: int
    pages: int


class FileUploadResponse(BaseModel):
    """Schema for file upload response."""
    id: uuid.UUID
    filename: str
    original_filename: str
    file_size: int
    content_type: str
    s3_url: str
    created_at: datetime
    
    class Config:
        from_attributes = True

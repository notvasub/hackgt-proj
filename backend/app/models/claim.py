"""Claim-related models."""

import uuid
from datetime import datetime
from typing import Optional, List
from enum import Enum
from sqlalchemy import String, Text, DateTime, ForeignKey, Integer, Float, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class ClaimType(str, Enum):
    """Claim type enumeration."""
    AUTO = "auto"
    HOME = "home"
    HEALTH = "health"
    RENTERS = "renters"
    OTHER = "other"


class ClaimStatus(str, Enum):
    """Claim status enumeration."""
    DRAFT = "draft"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class ProcessingStatus(str, Enum):
    """Processing job status enumeration."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class Claim(Base):
    """Main claim model."""
    
    __tablename__ = "claims"
    
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        ForeignKey("users.id", ondelete="CASCADE")
    )
    
    # Incident details
    incident_description: Mapped[str] = mapped_column(Text)
    incident_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    incident_location: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    
    # Insurance information
    insurance_provider: Mapped[str] = mapped_column(String(255))
    policy_number: Mapped[str] = mapped_column(String(100))
    claim_type: Mapped[ClaimType] = mapped_column(SQLEnum(ClaimType))
    
    # AI-generated content
    optimized_description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    damage_assessment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    claim_justification: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    requested_amount: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    strength_score: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    # Status and metadata
    status: Mapped[ClaimStatus] = mapped_column(
        SQLEnum(ClaimStatus), 
        default=ClaimStatus.DRAFT
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, 
        default=datetime.utcnow, 
        onupdate=datetime.utcnow
    )
    
    # Relationships
    files: Mapped[List["ClaimFile"]] = relationship(
        "ClaimFile", 
        back_populates="claim", 
        cascade="all, delete-orphan"
    )
    processing_jobs: Mapped[List["ClaimProcessingJob"]] = relationship(
        "ClaimProcessingJob", 
        back_populates="claim", 
        cascade="all, delete-orphan"
    )


class ClaimFile(Base):
    """File attachments for claims."""
    
    __tablename__ = "claim_files"
    
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4
    )
    claim_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        ForeignKey("claims.id", ondelete="CASCADE")
    )
    
    filename: Mapped[str] = mapped_column(String(255))
    original_filename: Mapped[str] = mapped_column(String(255))
    file_size: Mapped[int] = mapped_column(Integer)
    content_type: Mapped[str] = mapped_column(String(100))
    s3_key: Mapped[str] = mapped_column(String(500))
    s3_url: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Relationships
    claim: Mapped["Claim"] = relationship("Claim", back_populates="files")


class ClaimProcessingJob(Base):
    """Background processing jobs for claims."""
    
    __tablename__ = "claim_processing_jobs"
    
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4
    )
    claim_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        ForeignKey("claims.id", ondelete="CASCADE")
    )
    
    celery_task_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    status: Mapped[ProcessingStatus] = mapped_column(
        SQLEnum(ProcessingStatus), 
        default=ProcessingStatus.PENDING
    )
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    # Relationships
    claim: Mapped["Claim"] = relationship("Claim", back_populates="processing_jobs")

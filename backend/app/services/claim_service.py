"""Claim service for business logic."""

import uuid
from datetime import datetime
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from sqlalchemy.orm import selectinload
from app.models.claim import Claim, ClaimStatus, ProcessingStatus
from app.models.user import User
from app.schemas.claim import ClaimCreate, ClaimUpdate, ClaimListResponse
from app.services.ai_service import AIService


class ClaimService:
    """Service for claim-related operations."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.ai_service = AIService()
    
    async def create_claim(self, user_id: uuid.UUID, claim_data: ClaimCreate) -> Claim:
        """Create a new claim."""
        claim = Claim(
            user_id=user_id,
            incident_description=claim_data.incident_description,
            incident_date=claim_data.incident_date,
            incident_location=claim_data.incident_location,
            insurance_provider=claim_data.insurance_provider,
            policy_number=claim_data.policy_number,
            claim_type=claim_data.claim_type,
            status=ClaimStatus.DRAFT
        )
        
        self.db.add(claim)
        await self.db.commit()
        await self.db.refresh(claim)
        
        return claim
    
    async def get_claim_by_id(self, claim_id: uuid.UUID, user_id: uuid.UUID) -> Optional[Claim]:
        """Get a claim by ID for a specific user."""
        result = await self.db.execute(
            select(Claim)
            .options(selectinload(Claim.files), selectinload(Claim.processing_jobs))
            .where(Claim.id == claim_id, Claim.user_id == user_id)
        )
        return result.scalar_one_or_none()
    
    async def get_user_claims(
        self, 
        user_id: uuid.UUID, 
        page: int = 1, 
        size: int = 10
    ) -> ClaimListResponse:
        """Get paginated list of claims for a user."""
        # Calculate offset
        offset = (page - 1) * size
        
        # Get total count
        count_result = await self.db.execute(
            select(func.count(Claim.id)).where(Claim.user_id == user_id)
        )
        total = count_result.scalar()
        
        # Get claims
        result = await self.db.execute(
            select(Claim)
            .options(selectinload(Claim.files))
            .where(Claim.user_id == user_id)
            .order_by(desc(Claim.created_at))
            .offset(offset)
            .limit(size)
        )
        claims = result.scalars().all()
        
        # Calculate pages
        pages = (total + size - 1) // size
        
        return ClaimListResponse(
            claims=claims,
            total=total,
            page=page,
            size=size,
            pages=pages
        )
    
    async def update_claim(
        self, 
        claim_id: uuid.UUID, 
        user_id: uuid.UUID, 
        update_data: ClaimUpdate
    ) -> Optional[Claim]:
        """Update a claim."""
        claim = await self.get_claim_by_id(claim_id, user_id)
        if not claim:
            return None
        
        # Update fields
        for field, value in update_data.dict(exclude_unset=True).items():
            if hasattr(claim, field):
                setattr(claim, field, value)
        
        claim.updated_at = datetime.utcnow()
        
        await self.db.commit()
        await self.db.refresh(claim)
        
        return claim
    
    async def delete_claim(self, claim_id: uuid.UUID, user_id: uuid.UUID) -> bool:
        """Delete a claim."""
        claim = await self.get_claim_by_id(claim_id, user_id)
        if not claim:
            return False
        
        await self.db.delete(claim)
        await self.db.commit()
        
        return True
    
    async def start_ai_processing(self, claim_id: uuid.UUID, user_id: uuid.UUID) -> bool:
        """Start AI processing for a claim."""
        claim = await self.get_claim_by_id(claim_id, user_id)
        if not claim:
            return False
        
        # Update claim status
        claim.status = ClaimStatus.PROCESSING
        claim.updated_at = datetime.utcnow()
        
        # Create processing job record
        from app.models.claim import ClaimProcessingJob
        processing_job = ClaimProcessingJob(
            claim_id=claim_id,
            status=ProcessingStatus.PENDING
        )
        
        self.db.add(processing_job)
        await self.db.commit()
        await self.db.refresh(processing_job)
        
        # Start background processing with Celery
        from app.tasks import process_claim_ai
        task = process_claim_ai.delay(str(claim_id), str(processing_job.id))
        
        # Update job with Celery task ID
        processing_job.celery_task_id = task.id
        await self.db.commit()
        
        return True

"""Celery background tasks."""

import uuid
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.celery_app import celery_app
from app.database import AsyncSessionLocal
from app.models.claim import Claim, ClaimProcessingJob, ProcessingStatus, ClaimStatus
from app.services.ai_service import AIService


@celery_app.task(bind=True)
def process_claim_ai(self, claim_id: str, job_id: str):
    """Process claim with AI in background."""
    claim_uuid = uuid.UUID(claim_id)
    job_uuid = uuid.UUID(job_id)
    
    async def _process():
        async with AsyncSessionLocal() as db:
            try:
                # Get claim with files
                result = await db.execute(
                    select(Claim)
                    .options(selectinload(Claim.files))
                    .where(Claim.id == claim_uuid)
                )
                claim = result.scalar_one_or_none()
                
                if not claim:
                    return {"error": "Claim not found"}
                
                # Update job status
                job_result = await db.execute(
                    select(ClaimProcessingJob).where(ClaimProcessingJob.id == job_uuid)
                )
                job = job_result.scalar_one_or_none()
                
                if job:
                    job.status = ProcessingStatus.PROCESSING
                    job.started_at = datetime.utcnow()
                    await db.commit()
                
                # Analyze with AI
                ai_service = AIService()
                ai_result = await ai_service.analyze_claim(claim, claim.files)
                
                # Update claim with AI results
                claim.optimized_description = ai_result.get("optimized_description")
                claim.damage_assessment = ai_result.get("damage_assessment")
                claim.claim_justification = ai_result.get("claim_justification")
                claim.requested_amount = ai_result.get("requested_amount")
                claim.strength_score = ai_result.get("strength_score")
                claim.status = ClaimStatus.COMPLETED
                claim.updated_at = datetime.utcnow()
                
                # Update job status
                if job:
                    job.status = ProcessingStatus.COMPLETED
                    job.completed_at = datetime.utcnow()
                
                await db.commit()
                
                return {
                    "status": "completed",
                    "claim_id": str(claim_id),
                    "job_id": str(job_id)
                }
                
            except Exception as e:
                # Handle errors
                try:
                    claim_result = await db.execute(
                        select(Claim).where(Claim.id == claim_uuid)
                    )
                    claim = claim_result.scalar_one_or_none()
                    
                    if claim:
                        claim.status = ClaimStatus.FAILED
                        claim.updated_at = datetime.utcnow()
                    
                    job_result = await db.execute(
                        select(ClaimProcessingJob).where(ClaimProcessingJob.id == job_uuid)
                    )
                    job = job_result.scalar_one_or_none()
                    
                    if job:
                        job.status = ProcessingStatus.FAILED
                        job.error_message = str(e)
                        job.completed_at = datetime.utcnow()
                    
                    await db.commit()
                except:
                    pass
                
                raise e
    
    # Run the async function
    import asyncio
    return asyncio.run(_process())

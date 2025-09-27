"""Claims API endpoints."""

import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.claim import (
    ClaimCreate, 
    ClaimResponse, 
    ClaimUpdate, 
    ClaimListResponse,
    FileUploadResponse
)
from app.services.claim_service import ClaimService
from app.services.file_service import FileService
from app.services.local_file_service import LocalFileService
from app.config import settings
from app.auth import get_current_active_user
from app.models.user import User

router = APIRouter(prefix="/claims", tags=["claims"])


@router.post("/", response_model=ClaimResponse, status_code=status.HTTP_201_CREATED)
async def create_claim(
    claim_data: ClaimCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new claim."""
    claim_service = ClaimService(db)
    
    claim = await claim_service.create_claim(current_user.id, claim_data)
    return claim


@router.get("/", response_model=ClaimListResponse)
async def get_claims(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Page size"),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get paginated list of user's claims."""
    claim_service = ClaimService(db)
    
    return await claim_service.get_user_claims(current_user.id, page, size)


@router.get("/{claim_id}", response_model=ClaimResponse)
async def get_claim(
    claim_id: uuid.UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get a specific claim."""
    claim_service = ClaimService(db)
    
    claim = await claim_service.get_claim_by_id(claim_id, current_user.id)
    if not claim:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Claim not found"
        )
    
    return claim


@router.put("/{claim_id}", response_model=ClaimResponse)
async def update_claim(
    claim_id: uuid.UUID,
    update_data: ClaimUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Update a claim."""
    claim_service = ClaimService(db)
    
    claim = await claim_service.update_claim(claim_id, current_user.id, update_data)
    if not claim:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Claim not found"
        )
    
    return claim


@router.delete("/{claim_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_claim(
    claim_id: uuid.UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete a claim."""
    claim_service = ClaimService(db)
    
    success = await claim_service.delete_claim(claim_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Claim not found"
        )


@router.post("/{claim_id}/process", status_code=status.HTTP_202_ACCEPTED)
async def process_claim(
    claim_id: uuid.UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Start AI processing for a claim."""
    claim_service = ClaimService(db)
    
    success = await claim_service.start_ai_processing(claim_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Claim not found"
        )
    
    return {"message": "Claim processing started"}


@router.post("/{claim_id}/files", response_model=FileUploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_file(
    claim_id: uuid.UUID,
    file: UploadFile,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Upload a file to a claim."""
    # First verify the claim exists and belongs to the user
    claim_service = ClaimService(db)
    claim = await claim_service.get_claim_by_id(claim_id, current_user.id)
    if not claim:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Claim not found"
        )
    
    # Choose file service based on configuration
    if settings.aws_access_key_id and settings.aws_secret_access_key:
        file_service = FileService(db)
    else:
        file_service = LocalFileService(db)
    
    return await file_service.upload_file(claim_id, file)


@router.get("/{claim_id}/files", response_model=List[FileUploadResponse])
async def get_claim_files(
    claim_id: uuid.UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all files for a claim."""
    # First verify the claim exists and belongs to the user
    claim_service = ClaimService(db)
    claim = await claim_service.get_claim_by_id(claim_id, current_user.id)
    if not claim:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Claim not found"
        )
    
    # Choose file service based on configuration
    if settings.aws_access_key_id and settings.aws_secret_access_key:
        file_service = FileService(db)
    else:
        file_service = LocalFileService(db)
    
    files = await file_service.get_claim_files(claim_id)
    
    return [
        FileUploadResponse(
            id=file.id,
            filename=file.filename,
            original_filename=file.original_filename,
            file_size=file.file_size,
            content_type=file.content_type,
            s3_url=file.s3_url,
            created_at=file.created_at
        )
        for file in files
    ]


@router.delete("/files/{file_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_file(
    file_id: uuid.UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete a file."""
    # Choose file service based on configuration
    if settings.aws_access_key_id and settings.aws_secret_access_key:
        file_service = FileService(db)
    else:
        file_service = LocalFileService(db)
    
    success = await file_service.delete_file(file_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )

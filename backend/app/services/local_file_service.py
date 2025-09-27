"""Local file service for development (no AWS required)."""

import uuid
import os
import shutil
from typing import Optional, List
from fastapi import UploadFile, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.config import settings
from app.models.claim import ClaimFile
from app.schemas.claim import FileUploadResponse


class LocalFileService:
    """Service for local file operations (development only)."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.upload_dir = "uploads"
        self.base_url = "http://localhost:8000/files"
        
        # Create upload directory if it doesn't exist
        os.makedirs(self.upload_dir, exist_ok=True)
    
    def _validate_file(self, file: UploadFile) -> None:
        """Validate uploaded file."""
        # Check file size
        if file.size and file.size > settings.max_file_size:
            raise HTTPException(
                status_code=413,
                detail=f"File size exceeds maximum allowed size of {settings.max_file_size} bytes"
            )
        
        # Check file extension
        if file.filename:
            file_extension = file.filename.split('.')[-1].lower()
            if file_extension not in settings.allowed_extensions:
                raise HTTPException(
                    status_code=400,
                    detail=f"File type not allowed. Allowed types: {', '.join(settings.allowed_extensions)}"
                )
    
    def _generate_file_path(self, claim_id: uuid.UUID, filename: str) -> tuple[str, str]:
        """Generate file path and URL for local storage."""
        file_extension = filename.split('.')[-1].lower()
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        
        # Create claim-specific directory
        claim_dir = os.path.join(self.upload_dir, str(claim_id))
        os.makedirs(claim_dir, exist_ok=True)
        
        file_path = os.path.join(claim_dir, unique_filename)
        file_url = f"{self.base_url}/{claim_id}/{unique_filename}"
        
        return file_path, file_url
    
    async def upload_file(
        self, 
        claim_id: uuid.UUID, 
        file: UploadFile
    ) -> FileUploadResponse:
        """Upload a file to local storage and save metadata to database."""
        # Validate file
        self._validate_file(file)
        
        # Generate file path
        file_path, file_url = self._generate_file_path(claim_id, file.filename)
        
        try:
            # Save file to local storage
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            # Get file size
            file_size = os.path.getsize(file_path)
            
            # Save file metadata to database
            claim_file = ClaimFile(
                claim_id=claim_id,
                filename=file.filename,
                original_filename=file.filename,
                file_size=file_size,
                content_type=file.content_type or 'application/octet-stream',
                s3_key=file_path,  # Store local path in s3_key field
                s3_url=file_url
            )
            
            self.db.add(claim_file)
            await self.db.commit()
            await self.db.refresh(claim_file)
            
            return FileUploadResponse(
                id=claim_file.id,
                filename=claim_file.filename,
                original_filename=claim_file.original_filename,
                file_size=claim_file.file_size,
                content_type=claim_file.content_type,
                s3_url=claim_file.s3_url,
                created_at=claim_file.created_at
            )
            
        except Exception as e:
            # Clean up file if database save fails
            if os.path.exists(file_path):
                os.remove(file_path)
            raise HTTPException(
                status_code=500,
                detail=f"Failed to upload file: {str(e)}"
            )
    
    async def get_claim_files(self, claim_id: uuid.UUID) -> List[ClaimFile]:
        """Get all files for a claim."""
        result = await self.db.execute(
            select(ClaimFile).where(ClaimFile.claim_id == claim_id)
        )
        return result.scalars().all()
    
    async def delete_file(self, file_id: uuid.UUID) -> bool:
        """Delete a file from local storage and database."""
        # Get file from database
        result = await self.db.execute(select(ClaimFile).where(ClaimFile.id == file_id))
        claim_file = result.scalar_one_or_none()
        
        if not claim_file:
            return False
        
        try:
            # Delete from local storage
            if os.path.exists(claim_file.s3_key):
                os.remove(claim_file.s3_key)
            
            # Delete from database
            await self.db.delete(claim_file)
            await self.db.commit()
            
            return True
            
        except Exception:
            # If file deletion fails, still delete from database
            await self.db.delete(claim_file)
            await self.db.commit()
            return True

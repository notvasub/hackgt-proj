"""File service for handling file uploads and storage."""

import uuid
import os
from typing import Optional, List
from fastapi import UploadFile, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import boto3
from botocore.exceptions import ClientError
from app.config import settings
from app.models.claim import ClaimFile
from app.schemas.claim import FileUploadResponse


class FileService:
    """Service for file-related operations."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
            region_name=settings.aws_region
        )
    
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
    
    def _generate_s3_key(self, claim_id: uuid.UUID, filename: str) -> str:
        """Generate S3 key for file storage."""
        file_extension = filename.split('.')[-1].lower()
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        return f"claims/{claim_id}/{unique_filename}"
    
    async def upload_file(
        self, 
        claim_id: uuid.UUID, 
        file: UploadFile
    ) -> FileUploadResponse:
        """Upload a file to S3 and save metadata to database."""
        # Validate file
        self._validate_file(file)
        
        # Generate S3 key
        s3_key = self._generate_s3_key(claim_id, file.filename)
        
        try:
            # Upload to S3
            file_content = await file.read()
            self.s3_client.put_object(
                Bucket=settings.s3_bucket_name,
                Key=s3_key,
                Body=file_content,
                ContentType=file.content_type or 'application/octet-stream'
            )
            
            # Generate S3 URL
            s3_url = f"https://{settings.s3_bucket_name}.s3.{settings.aws_region}.amazonaws.com/{s3_key}"
            
            # Save file metadata to database
            claim_file = ClaimFile(
                claim_id=claim_id,
                filename=file.filename,
                original_filename=file.filename,
                file_size=len(file_content),
                content_type=file.content_type or 'application/octet-stream',
                s3_key=s3_key,
                s3_url=s3_url
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
            
        except ClientError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to upload file to S3: {str(e)}"
            )
    
    async def get_claim_files(self, claim_id: uuid.UUID) -> List[ClaimFile]:
        """Get all files for a claim."""
        result = await self.db.execute(
            select(ClaimFile).where(ClaimFile.claim_id == claim_id)
        )
        return result.scalars().all()
    
    async def delete_file(self, file_id: uuid.UUID) -> bool:
        """Delete a file from S3 and database."""
        # Get file from database
        result = await self.db.execute(select(ClaimFile).where(ClaimFile.id == file_id))
        claim_file = result.scalar_one_or_none()
        
        if not claim_file:
            return False
        
        try:
            # Delete from S3
            self.s3_client.delete_object(
                Bucket=settings.s3_bucket_name,
                Key=claim_file.s3_key
            )
            
            # Delete from database
            await self.db.delete(claim_file)
            await self.db.commit()
            
            return True
            
        except ClientError:
            # If S3 deletion fails, still delete from database
            await self.db.delete(claim_file)
            await self.db.commit()
            return True

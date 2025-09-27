from __future__ import annotations

from fastapi import APIRouter, Depends, Header

from app.auth.dependencies import get_current_user
from app.container import get_storage_service
from app.domain.dto.requests import CreateFileRequest
from app.domain.dto.responses import CreateFileResponse, FileResponse
from app.services.storage_service import StorageService

router = APIRouter(prefix="/v1/files", tags=["files"])


@router.post("", response_model=CreateFileResponse, status_code=201)
async def create_file_slot(
    payload: CreateFileRequest,
    storage: StorageService = Depends(get_storage_service),
    user=Depends(get_current_user),
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
):
    return await storage.create_upload_slot(user.id, payload, idempotency_key)


@router.post("/{file_id}/complete", response_model=FileResponse, status_code=202)
async def complete_upload(
    file_id: str,
    storage: StorageService = Depends(get_storage_service),
    user=Depends(get_current_user),
):
    return await storage.mark_complete_and_queue_scan(user.id, file_id)


@router.get("/{file_id}", response_model=FileResponse)
async def get_file(
    file_id: str,
    storage: StorageService = Depends(get_storage_service),
    user=Depends(get_current_user),
):
    return await storage.get_file(user.id, file_id)


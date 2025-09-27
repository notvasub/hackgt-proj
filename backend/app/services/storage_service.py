from __future__ import annotations

from typing import Optional

from app.config import Settings
from app.domain.dto.requests import CreateFileRequest
from app.domain.dto.responses import CreateFileResponse, FileResponse
from app.domain.models.core import File
from app.repositories.files_repo import FilesRepo
from app.repositories.jobs_repo import JobsRepo
from app.utils.ids import new_id


class StorageService:
    def __init__(self, settings: Settings, files_repo: FilesRepo, jobs_repo: JobsRepo) -> None:
        self._settings = settings
        self._files = files_repo
        self._jobs = jobs_repo

    async def create_upload_slot(self, user_id: str, payload: CreateFileRequest, idempotency_key: Optional[str]) -> CreateFileResponse:
        file_id = new_id("file")
        rec = File(
            id=file_id,
            user_id=user_id,
            purpose=payload.purpose,
            content_type=payload.content_type,
            filename=payload.filename,
            size=payload.bytes,
            status="pending",
        )
        await self._files.create(rec)
        # Fake presigned URL for demo
        upload_url = f"https://storage.fake/{self._settings.supabase_storage_bucket}/{file_id}"
        return CreateFileResponse(file_id=file_id, upload_url=upload_url, headers={"x-up": "1"})

    async def mark_complete_and_queue_scan(self, user_id: str, file_id: str) -> FileResponse:
        f = await self._files.get(user_id, file_id)
        await self._files.update(file_id, status="scanning", virus_scan="unknown")
        # Enqueue a job that a worker would process; for MVP we will instantly mark clean
        await self._jobs.enqueue(user_id, "file_scan", {"file_id": file_id})
        # Simulate scan done
        await self._files.update(file_id, status="ready", virus_scan="clean")
        f = await self._files.get(user_id, file_id)
        return FileResponse(
            id=f.id,
            purpose=f.purpose,
            content_type=f.content_type,
            filename=f.filename,
            size=f.size,
            status=f.status,
            virus_scan=f.virus_scan,
            ocr_text=f.ocr_text,
        )

    async def get_file(self, user_id: str, file_id: str) -> FileResponse:
        f = await self._files.get(user_id, file_id)
        return FileResponse(
            id=f.id,
            purpose=f.purpose,
            content_type=f.content_type,
            filename=f.filename,
            size=f.size,
            status=f.status,
            virus_scan=f.virus_scan,
            ocr_text=f.ocr_text,
        )


from __future__ import annotations

from typing import Dict, Optional

from app.domain.models.core import File


_FILES: Dict[str, File] = {}


class FilesRepo:
    async def create(self, file: File) -> File:
        _FILES[file.id] = file
        return file

    async def get(self, user_id: str, file_id: str) -> File:
        f = _FILES.get(file_id)
        if not f or f.user_id != user_id:
            raise KeyError("file_not_found")
        return f

    async def update(self, file_id: str, **updates) -> File:
        f = _FILES[file_id]
        for k, v in updates.items():
            setattr(f, k, v)
        return f


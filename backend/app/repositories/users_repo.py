from __future__ import annotations

from typing import Optional


class UsersRepo:
    async def get_or_create(self, user_id: str, email: Optional[str] = None):
        return {"id": user_id, "email": email}


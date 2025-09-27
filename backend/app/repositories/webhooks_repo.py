from __future__ import annotations

from typing import Dict, List


_WEBHOOKS: Dict[str, List[str]] = {}


class WebhooksRepo:
    async def register(self, user_id: str, url: str) -> None:
        _WEBHOOKS.setdefault(user_id, []).append(url)

    async def list(self, user_id: str) -> List[str]:
        return _WEBHOOKS.get(user_id, [])


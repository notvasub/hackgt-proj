from __future__ import annotations

from typing import Dict, Optional, Tuple


class IdempotencyService:
    def __init__(self) -> None:
        self._cache: Dict[Tuple[str, str], object] = {}

    def get(self, user_id: str, key: Optional[str]):
        if not key:
            return None
        return self._cache.get((user_id, key))

    def set(self, user_id: str, key: Optional[str], value: object) -> None:
        if not key:
            return None
        self._cache[(user_id, key)] = value


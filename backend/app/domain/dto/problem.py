from __future__ import annotations

from typing import Any, Dict
from pydantic import BaseModel


class Problem(BaseModel):
    type: str = "about:blank"
    title: str
    status: int
    detail: str | None = None
    instance: str | None = None
    errors: Dict[str, Any] | None = None


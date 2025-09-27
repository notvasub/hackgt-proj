from __future__ import annotations

import uuid
from typing import Callable

from fastapi import Request, Response


async def request_id_middleware(request: Request, call_next: Callable):
    req_id = request.headers.get("X-Request-Id") or str(uuid.uuid4())
    request.state.request_id = req_id
    response: Response = await call_next(request)
    response.headers["X-Request-Id"] = req_id
    response.headers.setdefault("X-RateLimit-Limit", "60")
    response.headers.setdefault("X-RateLimit-Remaining", "60")
    return response


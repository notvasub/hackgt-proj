from __future__ import annotations

from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException


def install_problem_handlers(app: FastAPI) -> None:
    @app.exception_handler(StarletteHTTPException)
    async def http_error_handler(request: Request, exc: StarletteHTTPException):
        payload: dict[str, Any] = {
            "type": "about:blank",
            "title": exc.detail if isinstance(exc.detail, str) else exc.__class__.__name__,
            "status": exc.status_code,
            "detail": exc.detail if isinstance(exc.detail, str) else None,
            "instance": str(getattr(request.state, "request_id", "")),
        }
        return JSONResponse(status_code=exc.status_code, content=payload)

    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(request: Request, exc: RequestValidationError):
        payload: dict[str, Any] = {
            "type": "about:blank",
            "title": "Validation Error",
            "status": 422,
            "detail": "Input validation failed",
            "errors": exc.errors(),
            "instance": str(getattr(request.state, "request_id", "")),
        }
        return JSONResponse(status_code=422, content=payload)


from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import routes_claims, routes_files, routes_health, routes_jobs, routes_providers, routes_stream, routes_users, routes_webhooks
from app.config import get_settings
from app.middleware.problem_handler import install_problem_handlers
from app.middleware.request_id import request_id_middleware


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title="Insurance Claim Optimizer API", version="0.1.0")

    # Middleware
    app.middleware("http")(request_id_middleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[o.strip() for o in settings.cors_origins.split(",") if o.strip()],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )
    install_problem_handlers(app)

    # Routers
    app.include_router(routes_health.router)
    app.include_router(routes_users.router)
    app.include_router(routes_files.router)
    app.include_router(routes_providers.router)
    app.include_router(routes_claims.router)
    app.include_router(routes_jobs.router)
    app.include_router(routes_stream.router)
    app.include_router(routes_webhooks.router)

    return app


app = create_app()


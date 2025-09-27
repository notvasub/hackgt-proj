"""Main FastAPI application."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.staticfiles import StaticFiles
import os
from app.config import settings
from app.database import init_db
from app.api.v1 import auth, claims, health

# Create FastAPI app
app = FastAPI(
    title="ClaimMax AI Backend",
    description="AI-powered Insurance Claim Optimizer API",
    version="0.1.0",
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add trusted host middleware
if not settings.debug:
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["claimmax-ai.com", "*.claimmax-ai.com"]
    )

# Include API routers
app.include_router(auth.router, prefix="/api/v1")
app.include_router(claims.router, prefix="/api/v1")
app.include_router(health.router, prefix="/api/v1")

# Mount static files for local file serving (development only)
if settings.environment == "development":
    uploads_dir = "uploads"
    if os.path.exists(uploads_dir):
        app.mount("/files", StaticFiles(directory=uploads_dir), name="files")


@app.on_event("startup")
async def startup_event():
    """Initialize application on startup."""
    await init_db()


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "ClaimMax AI Backend API",
        "version": "0.1.0",
        "docs": "/docs" if settings.debug else "Documentation not available in production"
    }
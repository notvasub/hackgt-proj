"""Health check API endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.database import get_db
from app.config import settings

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/")
async def health_check():
    """Basic health check."""
    return {
        "status": "healthy",
        "environment": settings.environment,
        "version": "0.1.0"
    }


@router.get("/db")
async def database_health_check(db: AsyncSession = Depends(get_db)):
    """Database health check."""
    try:
        # Test database connection
        result = await db.execute(text("SELECT 1"))
        result.scalar()
        
        return {
            "status": "healthy",
            "database": "connected"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }

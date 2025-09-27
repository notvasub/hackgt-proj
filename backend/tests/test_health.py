"""Test health check endpoints."""

import pytest
from fastapi import status


def test_health_check(client):
    """Test basic health check."""
    response = client.get("/api/v1/health/")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "healthy"
    assert "environment" in data
    assert "version" in data


def test_database_health_check(client):
    """Test database health check."""
    response = client.get("/api/v1/health/db")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "healthy"
    assert data["database"] == "connected"
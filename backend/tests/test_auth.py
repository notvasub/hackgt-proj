"""Test authentication endpoints."""

import pytest
from fastapi import status


def test_register_user(client):
    """Test user registration."""
    user_data = {
        "email": "newuser@example.com",
        "password": "testpassword123",
        "full_name": "New User"
    }
    
    response = client.post("/api/v1/auth/register", json=user_data)
    
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["full_name"] == user_data["full_name"]
    assert "id" in data
    assert "hashed_password" not in data


def test_register_duplicate_email(client, test_user):
    """Test registration with duplicate email."""
    user_data = {
        "email": test_user.email,
        "password": "testpassword123",
        "full_name": "Another User"
    }
    
    response = client.post("/api/v1/auth/register", json=user_data)
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "already exists" in response.json()["detail"]


def test_login_success(client, test_user):
    """Test successful login."""
    login_data = {
        "email": test_user.email,
        "password": "testpassword"
    }
    
    response = client.post("/api/v1/auth/login", json=login_data)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert "expires_in" in data


def test_login_invalid_credentials(client):
    """Test login with invalid credentials."""
    login_data = {
        "email": "nonexistent@example.com",
        "password": "wrongpassword"
    }
    
    response = client.post("/api/v1/auth/login", json=login_data)
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "Incorrect email or password" in response.json()["detail"]


def test_login_wrong_password(client, test_user):
    """Test login with wrong password."""
    login_data = {
        "email": test_user.email,
        "password": "wrongpassword"
    }
    
    response = client.post("/api/v1/auth/login", json=login_data)
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "Incorrect email or password" in response.json()["detail"]

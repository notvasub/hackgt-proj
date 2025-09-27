"""Test claims endpoints."""

import pytest
from fastapi import status


def test_create_claim(client, auth_headers):
    """Test creating a new claim."""
    claim_data = {
        "incident_description": "Test incident description for claim creation",
        "insurance_provider": "Test Insurance Company",
        "policy_number": "POL123456",
        "claim_type": "auto"
    }
    
    response = client.post(
        "/api/v1/claims/",
        json=claim_data,
        headers=auth_headers
    )
    
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["incident_description"] == claim_data["incident_description"]
    assert data["insurance_provider"] == claim_data["insurance_provider"]
    assert data["policy_number"] == claim_data["policy_number"]
    assert data["claim_type"] == claim_data["claim_type"]
    assert data["status"] == "draft"


def test_create_claim_unauthorized(client):
    """Test creating a claim without authentication."""
    claim_data = {
        "incident_description": "Test incident description",
        "insurance_provider": "Test Insurance",
        "policy_number": "POL123",
        "claim_type": "auto"
    }
    
    response = client.post("/api/v1/claims/", json=claim_data)
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_claims(client, auth_headers, test_claim):
    """Test getting user's claims."""
    response = client.get("/api/v1/claims/", headers=auth_headers)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "claims" in data
    assert "total" in data
    assert "page" in data
    assert "size" in data
    assert "pages" in data
    assert len(data["claims"]) >= 1


def test_get_claim_by_id(client, auth_headers, test_claim):
    """Test getting a specific claim."""
    response = client.get(
        f"/api/v1/claims/{test_claim.id}",
        headers=auth_headers
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == str(test_claim.id)
    assert data["incident_description"] == test_claim.incident_description


def test_get_nonexistent_claim(client, auth_headers):
    """Test getting a claim that doesn't exist."""
    fake_id = "00000000-0000-0000-0000-000000000000"
    response = client.get(f"/api/v1/claims/{fake_id}", headers=auth_headers)
    
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_update_claim(client, auth_headers, test_claim):
    """Test updating a claim."""
    update_data = {
        "optimized_description": "Updated optimized description",
        "strength_score": 85
    }
    
    response = client.put(
        f"/api/v1/claims/{test_claim.id}",
        json=update_data,
        headers=auth_headers
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["optimized_description"] == update_data["optimized_description"]
    assert data["strength_score"] == update_data["strength_score"]


def test_delete_claim(client, auth_headers, test_claim):
    """Test deleting a claim."""
    response = client.delete(
        f"/api/v1/claims/{test_claim.id}",
        headers=auth_headers
    )
    
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    # Verify claim is deleted
    get_response = client.get(
        f"/api/v1/claims/{test_claim.id}",
        headers=auth_headers
    )
    assert get_response.status_code == status.HTTP_404_NOT_FOUND


def test_start_claim_processing(client, auth_headers, test_claim):
    """Test starting AI processing for a claim."""
    response = client.post(
        f"/api/v1/claims/{test_claim.id}/process",
        headers=auth_headers
    )
    
    assert response.status_code == status.HTTP_202_ACCEPTED
    data = response.json()
    assert "message" in data
    assert "processing started" in data["message"]

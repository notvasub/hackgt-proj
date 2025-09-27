import pytest
from httpx import AsyncClient
from app.main import app


def bearer():
    # Header: {"alg":"HS256","kid":"1"}
    # Payload: {"sub":"user_a","email":"a.n@b.com","exp":9999999999}
    return "Bearer eyJhbGciOiJIUzI1NiIsImtpZCI6IjEifQ.eyJzdWIiOiJ1c2VyX2EiLCJlbWFpbCI6ImEubkBiLmNvbSIsImV4cCI6OTk5OTk5OTk5fQ.signature"


@pytest.mark.asyncio
async def test_users_me():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get("/v1/users/me", headers={"Authorization": bearer()})
        assert r.status_code == 200
        data = r.json()
        assert data["id"] == "user_a"


@pytest.mark.asyncio
async def test_claims_flow():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Create claim
        payload = {"claim_type": "auto", "incident_description": "Minor collision at intersection"}
        r = await ac.post("/v1/claims", json=payload, headers={"Authorization": bearer()})
        assert r.status_code == 201
        claim = r.json()
        claim_id = claim["id"]

        # Start draft job
        r = await ac.post(f"/v1/claims/{claim_id}/drafts", json={}, headers={"Authorization": bearer()})
        assert r.status_code == 202
        job = r.json()
        job_id = job["id"]

        # Poll job
        r = await ac.get(f"/v1/jobs/{job_id}", headers={"Authorization": bearer()})
        assert r.status_code == 200
        jr = r.json()
        assert jr["status"] in ("running", "succeeded")


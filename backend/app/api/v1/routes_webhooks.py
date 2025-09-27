from __future__ import annotations

from fastapi import APIRouter, Depends

from app.auth.dependencies import get_current_user
from app.container import get_webhooks_repo
from app.repositories.webhooks_repo import WebhooksRepo

router = APIRouter(prefix="/v1/webhooks", tags=["webhooks"])


@router.post("/outgoing")
async def register_webhook(url: str, webhooks: WebhooksRepo = Depends(get_webhooks_repo), user=Depends(get_current_user)):
    await webhooks.register(user.id, url)
    return {"ok": True}


@router.post("/incoming/insurer")
async def incoming_insurer():
    # Public endpoint; would verify provider signature if available
    return {"ok": True}


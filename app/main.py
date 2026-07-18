from __future__ import annotations

import hmac
from json import JSONDecodeError

from fastapi import BackgroundTasks, FastAPI, HTTPException, Request, status

from app.commands import handle_update
from app.config import Settings


def create_app(settings: Settings | None = None) -> FastAPI:
    runtime_settings = settings or Settings.from_env()
    application = FastAPI(
        title="Zalo Truc Nhat Bot",
        docs_url=None,
        redoc_url=None,
        openapi_url=None,
    )

    @application.get("/")
    @application.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    @application.post("/webhooks/zalo")
    async def zalo_webhook(
        request: Request,
        background_tasks: BackgroundTasks,
    ) -> dict[str, bool]:
        expected = runtime_settings.webhook_secret_token
        received = request.headers.get("X-Bot-Api-Secret-Token", "")

        if not expected:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Webhook secret is not configured",
            )

        if not received or not hmac.compare_digest(received, expected):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Unauthorized",
            )

        try:
            payload = await request.json()
        except (JSONDecodeError, ValueError):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid JSON",
            ) from None

        if not isinstance(payload, dict):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="JSON object required",
            )

        background_tasks.add_task(handle_update, payload, runtime_settings)
        return {"ok": True}

    return application


app = create_app()


from __future__ import annotations

import httpx


class ZaloAPIError(RuntimeError):
    """Raised when Zalo Bot API rejects a request."""


async def send_message(bot_token: str, chat_id: str, text: str) -> None:
    """Send one plain-text message through the official Zalo Bot API."""
    if not bot_token:
        return

    url = f"https://bot-api.zaloplatforms.com/bot{bot_token}/sendMessage"
    payload = {"chat_id": chat_id, "text": text[:2000]}

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.post(url, json=payload)
        response.raise_for_status()
        data = response.json()

    if not data.get("ok"):
        raise ZaloAPIError(f"Zalo API error code: {data.get('error_code', 'unknown')}")


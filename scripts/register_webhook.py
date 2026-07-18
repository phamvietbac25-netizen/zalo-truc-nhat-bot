from __future__ import annotations

import os
import sys

import httpx


def required_env(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise RuntimeError(f"Missing environment variable: {name}")
    return value


def main() -> int:
    try:
        bot_token = required_env("ZALO_BOT_TOKEN")
        webhook_url = required_env("WEBHOOK_URL")
        secret_token = required_env("WEBHOOK_SECRET_TOKEN")
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    if not webhook_url.startswith("https://"):
        print("WEBHOOK_URL must start with https://", file=sys.stderr)
        return 1

    if not 8 <= len(secret_token) <= 256:
        print("WEBHOOK_SECRET_TOKEN must contain 8-256 characters", file=sys.stderr)
        return 1

    endpoint = f"https://bot-api.zaloplatforms.com/bot{bot_token}/setWebhook"
    response = httpx.post(
        endpoint,
        json={"url": webhook_url, "secret_token": secret_token},
        timeout=15.0,
    )
    response.raise_for_status()
    result = response.json()

    if not result.get("ok"):
        print(f"Zalo rejected setWebhook: {result}", file=sys.stderr)
        return 1

    print(f"Webhook registered: {result['result']['url']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


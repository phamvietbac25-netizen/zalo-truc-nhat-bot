from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    """Runtime settings loaded from hosting environment variables."""

    bot_token: str
    webhook_secret_token: str
    environment: str = "production"

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            bot_token=os.getenv("ZALO_BOT_TOKEN", "").strip(),
            webhook_secret_token=os.getenv("WEBHOOK_SECRET_TOKEN", "").strip(),
            environment=os.getenv("APP_ENV", "production").strip() or "production",
        )


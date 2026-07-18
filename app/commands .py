from __future__ import annotations

import re
from typing import Any

from app.config import Settings
from app.zalo_client import send_message


COMMAND_PATTERN = re.compile(r"/(ping|trogiup|homnay|ngaymai|tuan)\b", re.IGNORECASE)


def extract_command(text: str) -> str | None:
    """Extract a supported slash command, including after a group @mention."""
    match = COMMAND_PATTERN.search(text)
    return match.group(1).lower() if match else None


def build_reply(command: str) -> str:
    replies = {
        "ping": "Bot đang hoạt động ✅",
        "trogiup": (
            "CÁC LỆNH HIỆN CÓ\n"
            "/ping - Kiểm tra bot\n"
            "/homnay - Xem lịch trực hôm nay\n"
            "/ngaymai - Xem lịch trực ngày mai\n"
            "/tuan - Xem lịch trực tuần này\n"
            "/trogiup - Xem hướng dẫn"
        ),
        "homnay": "Webhook đã hoạt động. Lịch hôm nay sẽ hiển thị sau khi nhập danh sách lớp.",
        "ngaymai": "Webhook đã hoạt động. Lịch ngày mai sẽ hiển thị sau khi nhập danh sách lớp.",
        "tuan": "Webhook đã hoạt động. Lịch tuần sẽ hiển thị sau khi nhập danh sách lớp.",
    }
    return replies[command]


async def handle_update(update: dict[str, Any], settings: Settings) -> None:
    """Handle text-message updates without storing the incoming message body."""
    result = update.get("result")
    if not isinstance(result, dict):
        return

    if result.get("event_name") != "message.text.received":
        return

    message = result.get("message")
    if not isinstance(message, dict):
        return

    text = message.get("text")
    chat = message.get("chat")
    if not isinstance(text, str) or not isinstance(chat, dict):
        return

    chat_id = chat.get("id")
    if not isinstance(chat_id, str) or not chat_id:
        return

    command = extract_command(text)
    if command is None:
        return

    await send_message(settings.bot_token, chat_id, build_reply(command))

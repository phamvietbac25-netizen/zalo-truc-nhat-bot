from fastapi.testclient import TestClient

from app.config import Settings
from app.main import create_app


SECRET = "test-secret-token"
client = TestClient(
    create_app(
        Settings(
            bot_token="",
            webhook_secret_token=SECRET,
            environment="test",
        )
    )
)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_rejects_wrong_secret() -> None:
    response = client.post(
        "/webhooks/zalo",
        headers={"X-Bot-Api-Secret-Token": "wrong-secret"},
        json={},
    )
    assert response.status_code == 403


def test_accepts_valid_zalo_update() -> None:
    response = client.post(
        "/webhooks/zalo",
        headers={"X-Bot-Api-Secret-Token": SECRET},
        json={
            "event_name": "message.text.received",
            "message": {
                "chat": {"id": "group-chat-id", "chat_type": "GROUP"},
                "text": "@Bot Trực Nhật /ping",
            },
        },
    )
    assert response.status_code == 200
    assert response.json() == {"ok": True}


from app.commands import build_reply, extract_command


def test_extracts_command_after_group_mention() -> None:
    assert extract_command("@Bot Trực Nhật /homnay") == "homnay"


def test_ignores_unknown_command() -> None:
    assert extract_command("@Bot /khongtontai") is None


def test_ping_reply() -> None:
    assert "hoạt động" in build_reply("ping")


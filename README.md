# Bot trực nhật lớp học trên Zalo

Server Webhook Python dùng **Zalo Bot Platform chính thức**. Phiên bản này tạo
điểm nhận Webhook an toàn và hỗ trợ các lệnh thử nghiệm `/ping`, `/trogiup`,
`/homnay`, `/ngaymai`, `/tuan`. Dữ liệu lịch trực sẽ được bổ sung ở bước tiếp
theo sau khi có danh sách nhóm và lịch học.

## Biến môi trường bắt buộc

- `ZALO_BOT_TOKEN`: Bot Token nhận từ Zalo Bot Creator.
- `WEBHOOK_SECRET_TOKEN`: chuỗi bí mật 8-256 ký tự, tuyệt đối không đưa lên GitHub.
- `WEBHOOK_URL`: chỉ cần khi chạy script đăng ký Webhook.

Không đổi tên các biến trên. Sao chép `.env.example` thành `.env` khi chạy ở
máy cá nhân; file `.env` đã được chặn khỏi Git.

## Chạy và kiểm thử

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -q
uvicorn app.main:app --reload
```

Trên Windows PowerShell, lệnh kích hoạt môi trường là:

```powershell
.venv\Scripts\Activate.ps1
```

## Triển khai lên Render

1. Đưa toàn bộ mã nguồn lên một repository GitHub riêng tư.
2. Trong Render, chọn **New > Web Service** và kết nối repository.
3. Chọn Python, sau đó đặt:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Thêm `ZALO_BOT_TOKEN` và `WEBHOOK_SECRET_TOKEN` trong Environment Variables.
5. Sau khi deploy thành công, URL Webhook sẽ có dạng:
   `https://ten-service.onrender.com/webhooks/zalo`.

## Đăng ký URL với Zalo

Đặt ba biến môi trường `ZALO_BOT_TOKEN`, `WEBHOOK_SECRET_TOKEN` và
`WEBHOOK_URL`, rồi chạy:

```bash
python scripts/register_webhook.py
```

Zalo sẽ gửi Secret Token trong header `X-Bot-Api-Secret-Token`; server dùng
phép so sánh constant-time và trả HTTP 403 nếu token không đúng.

## Thử trong nhóm Zalo

Sau khi thêm bot vào nhóm, nhắn:

```text
@Bot Trực Nhật /ping
```

Bot sẽ trả lời `Bot đang hoạt động ✅` nếu Webhook và Bot Token đều đúng.


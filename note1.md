# note1

## Cập nhật 31.10.2026

- Đã thống nhất và triển khai Alembic cho database migration: baseline tự tạo bảng trên database mới hoặc tiếp nhận các bảng do phiên bản trước tạo mà không sửa chúng. Trước khi nâng cấp cần kiểm tra schema cũ và backup MySQL volume.
- Vấn đề LAN/logout tiếp tục được hoãn đến khi bật LAN access; lúc đó thêm đúng application origin vào `FRONTEND_ORIGINS`, giữ kiểm tra `Origin` và ưu tiên HTTPS.

Ghi nhớ các quyết định và đề xuất của chủ dự án sau khi rà soát Sprint 1:

1. Các phát hiện số 1 (truy cập LAN) và số 5 (chuyển frontend từ development server sang cấu hình production) được ghi nhận để xử lý sau khi dự án hoàn thành.
2. Phát hiện số 8: xử lý phần test còn thiếu sau khi hoàn thành toàn bộ tính năng Sprint 1. Test hiện có chưa bao phủ đủ tiêu chí hoàn thành Sprint 1. Repository có unit test cho xử lý proxy IP và dọn session hết hạn, nhưng chưa thấy test cho authentication API, MySQL integration, khởi động Compose từ môi trường sạch hoặc khả năng Ollama truy cập model. Trong lần rà soát này mình không chạy test.

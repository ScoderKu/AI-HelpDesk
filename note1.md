# note1

## Cập nhật 31.10.2026

- Đã thống nhất và triển khai Alembic cho database migration: baseline tự tạo bảng trên database mới hoặc tiếp nhận các bảng do phiên bản trước tạo mà không sửa chúng. Trước khi nâng cấp cần kiểm tra schema cũ và backup MySQL volume.
- Vấn đề LAN/logout tiếp tục được hoãn đến khi bật LAN access; lúc đó thêm đúng application origin vào `FRONTEND_ORIGINS`, giữ kiểm tra `Origin` và ưu tiên HTTPS.

Ghi nhớ các quyết định và đề xuất của chủ dự án sau khi rà soát Sprint 1:

1. Các phát hiện số 1 (truy cập LAN) và số 5 (chuyển frontend từ development server sang cấu hình production) được ghi nhận để xử lý sau khi dự án hoàn thành.
2. Phát hiện số 8: xử lý phần test còn thiếu sau khi hoàn thành toàn bộ tính năng Sprint 1. Test hiện có chưa bao phủ đủ tiêu chí hoàn thành Sprint 1. Repository có unit test cho xử lý proxy IP và dọn session hết hạn, nhưng chưa thấy test cho authentication API, MySQL integration, khởi động Compose từ môi trường sạch hoặc khả năng Ollama truy cập model. Trong lần rà soát này mình không chạy test.

## Cập nhật 01.11.2026

- Đã chạy backend `unittest`: 31/31 test đạt; frontend production build đạt và lint sạch sau khi xử lý warning focus trong `HomePage.tsx`.
- Đã kiểm thử Alembic hai lần trên MySQL sạch, xác nhận database hiện tại ở `0002_conversations_and_tickets (head)`, và kiểm thử Ticket API với MySQL trong transaction rollback.
- Đã kiểm thử tạo `poro-helpdesk` từ `ollama/Modelfile` trên Ollama model volume rỗng tạm thời; tài nguyên Docker tạm đã được dọn.
- Phần kiểm thử còn thiếu: đăng ký/đăng nhập API integration, khởi động toàn bộ Compose trên cả MySQL và Ollama volume rỗng cùng lúc, UI acceptance thủ công, concurrent sign-in trên MySQL và kiểm tra IP forwarding qua hai thiết bị LAN. LAN access và frontend production deployment vẫn được hoãn theo quyết định dự án.
- Đường dẫn `Modelfile` trong README và system design đã được đồng bộ với vị trí thực tế `ollama/Modelfile`.

## Bổ sung kiểm tra trước khi demo hoàn tất

### 1. Real LAN forwarding
- Kiểm tra trên 2 thiết bị thật trong cùng LAN hoặc cùng mạng nội bộ.
- Xác minh `X-Forwarded-For` và `Trusted proxy` được xử lý đúng khi request đi qua proxy.
- Đảm bảo `TRUSTED_PROXY_IPS` khớp với cấu hình thực tế của Compose/NGINX.
- Kiểm tra client IP được backend xác định đúng, không bị lẫn giữa các client khác nhau.

### 2. Manual acceptance test toàn app
- Kiểm tra luồng đăng ký → đăng nhập → logout.
- Kiểm tra tạo ticket, xem danh sách, cập nhật, đóng ticket.
- Kiểm tra AI chat: gửi tin nhắn, đọc phản hồi, retry khi AI lỗi, lưu lịch sử hội thoại.
- Kiểm tra profile: xem thông tin, đổi username, đổi mật khẩu.
- Kiểm tra đa ngôn ngữ FI/EN.
- Kiểm tra tính năng bảo vệ origin, xác thực session và quyền truy cập theo user.

### 3. Kiểm tra Compose trên môi trường sạch
- Xóa hoặc reset MySQL và Ollama volume về rỗng.
- Chạy `docker compose up --build` từ đầu.
- Kiểm tra backend khởi động thành công, backend tự chạy Alembic, Ollama model tạo đúng từ `Modelfile`.
- Xác nhận model load được và backend giao tiếp với Ollama thành công.
- Kiểm tra toàn bộ stack frontend/backend/db/ollama hoạt động không lỗi sau cold start.

### 4. Những phần nên kiểm tra thêm sau Sprint 3
- Concurrent sign-in trên MySQL để phát hiện race condition hoặc deadlock.
- Tính nhất quán của session cleanup khi nhiều user cùng đăng nhập/đăng xuất.
- Xác nhận retention policy với dữ liệu thực: ticket đóng quá 3 tháng, conversation inactive quá 3 tháng.
- Test lỗi mạng/timeout từ Ollama khi service offline hoặc chậm.
- Test fallback UI khi AI service không phản hồi trong thời gian dài.
- Kiểm tra giới hạn và validate payload khi ticket/chat nhận dữ liệu bất thường.
- Kiểm tra permission logic cho user khác, ticket thuộc người khác, session hết hạn, password temporary.
- Kiểm tra production deployment trên frontend thật, không chỉ Vite dev server.

### 5. Ghi chú cuối cùng
Các mục dưới đây nên được vào checklist trước khi chạy demo cuối cùng:
- Real LAN forwarding
- Manual acceptance test toàn app
- Compose cold start trên môi trường sạch
- Regression test các chức năng AI/chat/ticket/profile
- Đảm bảo README và hướng dẫn run demo khớp với thực tế môi trường test

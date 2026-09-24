# AGENTS.md — Quy ước dự án ECO2432

## Ngôn ngữ và phiên bản
- Solidity `^0.8.20`. Không dùng cú pháp của phiên bản 0.7 trở về trước.
- Dùng thư viện OpenZeppelin Contracts **phiên bản 5.x**.
  Lưu ý: phiên bản 5 đã bỏ `_beforeTokenTransfer`, thay bằng `_update`.
- Python 3.10+.

## Quy tắc bắt buộc khi viết hợp đồng
1. Mọi hàm làm thay đổi trạng thái phải phát ra một `event`.
2. Mọi hàm chỉ dành cho chủ sở hữu phải có kiểm tra quyền rõ ràng.
3. Áp dụng thứ tự Checks - Effects - Interactions: kiểm tra điều kiện → cập nhật biến trạng thái → chuyển tiền ra ngoài. Không được đảo thứ tự này.
4. Chuyển ETH bằng `call{value: ...}("")` kèm kiểm tra kết quả trả về. Không dùng `transfer`.
5. Dùng `error` tùy biến thay cho chuỗi thông báo dài trong `require`.
6. Không dùng `tx.origin` để xác thực.
7. Số tiền và tỷ lệ phần trăm dùng đơn vị điểm cơ bản (basis point, 1% = 100).

## Quy tắc khi viết Python
1. Không ghi khóa API trực tiếp trong mã nguồn. Đọc từ biến môi trường.
2. Luôn kiểm tra mã trạng thái phản hồi trước khi xử lý dữ liệu.
3. Đơn vị wei phải đổi sang ETH trước khi hiển thị (chia cho 10^18).

## Khi được yêu cầu sinh mã
- Giải thích ngắn gọn lựa chọn thiết kế trước khi đưa mã.
- Nếu yêu cầu chưa rõ, hỏi lại thay vì tự suy đoán.

## Quy ước bổ sung của sinh viên (Lab 1)
- Chú thích trong mã viết bằng tiếng Việt không dấu hoặc tiếng Anh rõ nghĩa.
- Đặt tên biến và hàm theo chuẩn camelCase, tên hợp đồng theo chuẩn PascalCase.
- Mọi script phân tích dữ liệu phải có xử lý ngoại lệ mạng và kiểm tra tính toàn vẹn của dữ liệu on-chain.

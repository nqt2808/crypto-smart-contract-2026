# NHẬT KÝ LÀM VIỆC VỚI AI — HUELEGEND (AI_JOURNAL.MD)

- **Dự án:** HueLegend (Chuỗi cung ứng đặc sản Huế)
- **Học phần:** ECO2432

---

## Lần 1 — Sinh mã khung Smart Contract ban đầu (Lab 9)
- **Prompt:** "Viết một smart contract Solidity quản lý chuỗi cung ứng đặc sản Huế gồm tạo lô hàng và thêm chặng."
- **AI trả về:** Đoạn mã dùng `mapping(uint256 => Product)` và mảng động `TrackingStep[]` bên trong struct, dùng `require` với chuỗi thông báo lỗi tiếng Anh dài và hàm duyệt toàn bộ mảng bằng vòng lặp `for`.
- **Đánh giá:** ⚠️ Phải sửa.
- **Chỗ sai:**
  1. Vòng lặp `for` duyệt mảng chặng tiềm ẩn nguy cơ cạn kiệt Gas (Unbounded loop DoS).
  2. Chuỗi thông báo trong `require("Only producer can call this function")` gây tốn gas khi deploy và runtime, vi phạm quy ước `AGENTS.md`.
  3. Thiếu phân quyền chuẩn công nghiệp OpenZeppelin `AccessControl`.
- **Cách sửa:** Sinh viên yêu cầu tái cấu trúc dùng `AccessControl`, thay `require` bằng `error UnauthorizedRole()` và tách mảng `_batchSteps` ra mapping riêng để truy cập theo chỉ mục $O(1)$.
- **Ai phát hiện:** **Sinh viên phát hiện**.

---

## Lần 2 — Cài đặt phân quyền AccessControl (Lab 11)
- **Prompt:** "Tích hợp OpenZeppelin AccessControl vào hợp đồng HueLegend và viết hàm thêm chặng."
- **AI trả về:** AI sử dụng `tx.origin` để kiểm tra quyền hạn của người tạo lô hàng ban đầu trong hàm thêm chặng.
- **Đánh giá:** ❌ Sai, bỏ.
- **Chỗ sai:** Sử dụng `tx.origin` vi phạm nghiêm trọng quy tắc bảo mật số 6 trong `AGENTS.md`, mở ra lỗ hổng tấn công lừa đảo ủy thác (Phishing Attack).
- **Cách sửa:** Sinh viên lập tức loại bỏ `tx.origin`, chuẩn hóa sử dụng `_msgSender()` và hàm `hasRole(LOGISTICS_ROLE, _msgSender())`.
- **Ai phát hiện:** **Sinh viên phát hiện**.

---

## Lần 3 — Thiết kế giao diện Web DApp sinh mã QR (Lab 15)
- **Prompt:** "Viết code HTML/JS kết nối MetaMask và hiển thị mã QR cho Batch ID."
- **AI trả về:** AI sử dụng thẻ `<script>` gọi thư viện CDN bên ngoài nhưng không kiểm tra mạng Sepolia, dẫn đến việc người dùng ở mạng Ethereum Mainnet hay Polygon vẫn bấm nút gửi giao dịch và báo lỗi khó hiểu.
- **Đánh giá:** ⚠️ Phải sửa.
- **Chỗ sai:** Thiếu hàm kiểm tra `window.ethereum` và không nhắc chuyển Chain ID sang Sepolia (`0xaa36a7`).
- **Cách sửa:** Sinh viên bổ sung module kiểm tra mạng tự động, hiển thị badge cảnh báo màu đỏ và cơ chế tự kích hoạt `wallet_switchEthereumChain`.
- **Ai phát hiện:** **Sinh viên phát hiện**.

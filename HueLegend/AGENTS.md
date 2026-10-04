# AGENTS.md — Quy ước dự án HueLegend (ECO2432)

## 1. Ngôn ngữ và phiên bản
- Solidity `^0.8.20`. Không dùng cú pháp của phiên bản 0.7 trở về trước.
- Dùng thư viện OpenZeppelin Contracts **phiên bản 5.x** (đặc biệt là `@openzeppelin/contracts/access/AccessControl.sol`).
- Python 3.10+ cho các kịch bản kiểm thử tự động.

## 2. Quy tắc bắt buộc khi viết Smart Contract HueLegend.sol
1. **Phát ra sự kiện (Event Emission):** Mọi hàm làm thay đổi trạng thái (tạo lô hàng, thêm chặng, đổi trạng thái, thu hồi lô hàng) bắt buộc phải phát ra một `event` có `indexed` các trường định danh (`batchId`, `handler`, `status`).
2. **Kiểm tra quyền hạn rõ ràng (Role-based Access Control):**
   - Không được dùng `tx.origin` để xác thực quyền.
   - Sử dụng định danh vai trò chuẩn dạng `bytes32 public constant ROLE_NAME = keccak256("ROLE_NAME")`.
   - Kiểm tra `hasRole(ROLE, msg.sender)` và revert bằng `error` tùy biến nếu không có quyền.
3. **Áp dụng Checks - Effects - Interactions (CEI):** Kiểm tra điều kiện đầu vào ➔ Cập nhật dữ liệu vào struct/mapping ➔ Tương tác bên ngoài (nếu có).
4. **Dùng Custom Errors:** Sử dụng cú pháp `error UnauthorizedRole(bytes32 role, address account);` thay cho các chuỗi `require` dài dòng nhằm tiết kiệm gas tối đa khi triển khai và vận hành.
5. **Tối ưu hóa Gas cho chuỗi cung ứng:**
   - Hạn chế lưu trữ chuỗi dài không cần thiết trên Storage; ưu tiên truyền `memory` hoặc `calldata`.
   - Các hàm tra cứu lịch sử phải là `external view` để người tiêu dùng truy vấn miễn phí (Gas = 0).
   - Không sử dụng vòng lặp duyệt mảng không giới hạn trên các hàm ghi (`write functions`).

## 3. Quy tắc khi viết Python & Kiểm thử
1. Không ghi khóa riêng tư (Private Key) trực tiếp trong mã nguồn. Đọc từ biến môi trường.
2. Kiểm tra tính toàn vẹn của dữ liệu on-chain và bóc tách chính xác các sự kiện đã phát ra.
3. Các ca kiểm thử phải bao quát cả luồng hợp lệ (Positive Test) và luồng gian lận (Negative Test).

## 4. Quy ước định danh và chú thích
- Chú thích trong mã viết bằng tiếng Việt không dấu hoặc tiếng Anh rõ nghĩa.
- Đặt tên biến và hàm theo chuẩn camelCase, tên hợp đồng và struct theo chuẩn PascalCase.

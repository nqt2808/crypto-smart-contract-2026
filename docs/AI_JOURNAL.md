# NHẬT KÝ SỬ DỤNG AI — NHÓM DỰ ÁN CAMPUSESTROW (ECO2432)

- **Nhóm thực hiện:** Nhóm CampusEscrow (Chủ đề 1 — Ký quỹ mua bán đồ cũ ký túc xá)
- **Thành viên:**
  1. Ngô Quỳnh Trang — MSSV: `23K4300041`
  2. Lê Thị Phương Thảo — MSSV: `23K4300052`
- **Mục đích:** Ghi chép chi tiết toàn bộ các câu lệnh nhắc (prompt), kết quả do AI sinh ra, đánh giá phản biện của nhóm, các lỗi phát hiện và cách khắc phục xuyên suốt từ Lab 8 đến Lab 15.

---

## Lab 8 — Thiết kế quy tắc kinh tế và đặc tả v0.1

### 1. Prompt thiết kế đặc tả và phản biện đối kháng
**Prompt 1 (Thiết kế máy trạng thái và quy tắc):**
> *"Bạn là chuyên viên phân tích nghiệp vụ Web3 (BA). Hãy xây dựng đặc tả SPEC.md và ECONOMIC_RULES.md cho hợp đồng ký quỹ mua bán đồ cũ ký túc xá (CampusEscrow). Hợp đồng giữ tiền cọc của sinh viên mua đồ cũ cho đến khi nhận hàng hoặc hết hạn bảo đảm. Cần tuân thủ AGENTS.md: Solidity ^0.8.20, OpenZeppelin v5, CEI, custom error, basis points."*

**Đánh giá của nhóm:**
AI tạo ra cấu trúc cơ bản khá tốt gồm 4 trạng thái (`Created`, `Funded`, `Completed`, `Refunded`). Tuy nhiên AI ban đầu dùng `require` với chuỗi ký tự dài ("Only buyer can call this") vi phạm quy tắc số 5 trong `AGENTS.md` (yêu cầu dùng custom error). Nhóm đã yêu cầu chuyển toàn bộ sang `error WrongState()`, `error NotBuyer()`, `error WrongAmount()`.

**Prompt 2 (Phản biện đối kháng từ người dùng thận trọng):**
> *"Bạn là người dùng thận trọng. Chỉ dựa trên SPEC và ECONOMIC_RULES dưới đây, hãy nêu 5 cách một người có thể lạm dụng quy tắc hoặc làm người khác bị thiệt. Với mỗi cách, chỉ rõ quy tắc nào chưa đủ chặt. Không viết mã."*

**Kết quả từ AI & Hành động khắc phục của nhóm:**
1. *AI chỉ ra rủi ro thời hạn quá dài:* Nhóm đã bổ sung ràng buộc trần `1 <= _daysToConfirm <= 14` ngày trong `SPEC.md`.
2. *AI chỉ ra rủi ro người bán tự mua đồ của mình:* Nhóm đã thêm kiểm tra `BuyerCannotBeSeller()`.
3. *AI chỉ ra phép chia làm tròn xuống khi giá trị quá nhỏ:* Nhóm bổ sung điều kiện giá tối thiểu `>= 10_000 wei`.
4. *AI chỉ ra người nhận là hợp đồng từ chối ETH:* Nhóm xác định phạm vi người dùng là tài khoản EOA (MetaMask cá nhân).
5. *AI chỉ ra rủi ro tấn công Reentrancy:* Nhóm quyết định áp dụng song song CEI và `ReentrancyGuard` của OpenZeppelin v5.

---

## Lab 9 — Hợp đồng lõi đầu tiên (Biên dịch và đo gas)

*(Sẽ cập nhật tại Lab 9)*

---

## Lab 10 — Rà soát mã nguồn do AI sinh ra

*(Bảng bắt buộc 4 cột: Lỗi | Mô tả | Ai phát hiện | Cách khắc phục)*
*(Sẽ cập nhật tại Lab 10)*

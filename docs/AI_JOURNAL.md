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

### 1. Prompt yêu cầu AI sinh mã cho ProjectCore.sol
> *"Hãy viết hợp đồng Solidity CampusEscrow theo đặc tả docs/SPEC.md, tuân thủ nghiêm ngặt AGENTS.md. Giải thích lựa chọn thiết kế trước khi đưa mã nguồn."*

### 2. Phân tích kết quả do AI sinh ra và Lỗi phát hiện
- **Lỗi 1 (Sai phiên bản Solidity & cú pháp cũ):**
  - *Mô tả:* AI ban đầu đề xuất `pragma solidity ^0.8.0;` và dùng hàm `transfer` để chuyển ETH cho người bán.
  - *Phát hiện bởi:* Sinh viên (đối chiếu quy tắc 4 trong `AGENTS.md`).
  - *Cách khắc phục:* Yêu cầu AI nâng cấp lên `pragma solidity ^0.8.20;` và đổi sang dùng `.call{value: amount}("")` kèm điều kiện `if (!ok) revert TransferFailed();`.
- **Lỗi 2 (Thiếu kiểm tra người bán tự mua):**
  - *Mô tả:* Hàm `fund()` ban đầu của AI cho phép bất kỳ ai nạp tiền, kể cả người bán.
  - *Phát hiện bởi:* Sinh viên (dựa trên phản biện đối kháng tại Lab 8).
  - *Cách khắc phục:* Bổ sung dòng kiểm tra `if (msg.sender == seller) revert BuyerCannotBeSeller();`.
- **Lỗi 3 (Thứ tự thực hiện chưa triệt để):**
  - *Mô tả:* Trong hàm `confirmReceived()`, AI tính toán `amount = address(this).balance` sau khi gọi event nhưng trước khi đổi trạng thái `state = State.Completed`.
  - *Phát hiện bởi:* Sinh viên (tuân thủ Checks-Effects-Interactions).
  - *Cách khắc phục:* Chuyển biến trạng thái `state = State.Completed` trước tiên trong bước Effects, sau đó mới phát event và gọi lệnh `call`.

### 3. Kết quả biên dịch và thử nghiệm
Hợp đồng `CampusEscrow` biên dịch không lỗi (0 warnings, 0 errors) trên trình biên dịch `solc 0.8.20`. Hoàn thành triển khai thử nghiệm trên Remix VM và ghi nhận bảng chi phí gas chi tiết tại `evidence/lab-09/README.md`.


---

## Lab 10 — Rà soát mã nguồn do AI sinh ra

### 1. Bảng bắt buộc phân tích lỗi VaultBuggy.sol (Chấm điểm chính thức)

| Lỗi | Mô tả | Ai phát hiện | Cách khắc phục |
|---|---|---|---|
| **1** | **Lộ mã PIN qua Storage Slot:** Thuộc tính `private` không mã hóa dữ liệu; gọi RPC `eth_getStorageAt(addr, "0x2", "latest")` đọc được mã PIN nguyên vẹn (`123456`). | **Sinh viên** | Không lưu trữ bí mật dạng plaintext lên blockchain; dùng cơ chế hash commit-reveal hoặc ZKP. |
| **2** | **Đảo ngược điều kiện thời gian:** `require(block.timestamp <= unlockTime)` làm tiền bị kẹt vĩnh viễn sau hạn chót mở két. | **AI & Sinh viên** | Đổi dấu thành `>= unlockTime` hoặc dùng custom error `StillLocked`. |
| **3** | **Thiếu phân quyền rút tiền:** Hàm `withdraw()` cho phép bất kỳ ai gọi và chuyển tiền cho `msg.sender` thay vì `owner`. | **AI & Sinh viên** | Thêm điều kiện `if (msg.sender != owner) revert NotOwner();` và chuyển về `payable(owner)`. |
| **4** | **Bẫy Gas `transfer` & Thiếu Event:** Dùng `.transfer()` có thể gây DoS khi bên nhận là contract/multisig và không phát Event khi thay đổi số dư. | **Sinh viên** *(Điểm cộng)* | Dùng `.call{value: balance}("")` có kiểm tra kết quả `ok` và phát các Event `Deposited`, `Withdrawn`. |

### 2. Phát hiện và sửa lỗi trên hợp đồng dự án ProjectCore.sol
- **Phát hiện 1 (Rủi ro vét cạn số dư thay vì thanh toán đúng giá niêm yết):**
  - *Vị trí:* Dòng 76 và dòng 94 trong `ProjectCore.sol`.
  - *Mô tả:* Lệnh `uint256 amount = address(this).balance` có thể bị thao túng nếu có ai đó chuyển ETH ngoài luồng qua `selfdestruct`.
  - *Ai phát hiện:* Sinh viên & AI.
  - *Cách khắc phục:* Đổi thành `uint256 amount = price;` để đảm bảo tính toàn vẹn và bất biến của đơn hàng.
- **Phát hiện 2 (Bổ sung kiểm soát quyền hủy/hoàn tiền):**
  - *Vị trí:* Dòng 88 hàm `refundAfterDeadline()`.
  - *Mô tả:* Không giới hạn người gọi hoàn tiền, có thể bị bot kích hoạt ngoài ý muốn.
  - *Ai phát hiện:* Sinh viên.
  - *Cách khắc phục:* Thêm kiểm tra `if (msg.sender != buyer && msg.sender != seller) revert NotAuthorized();`.


# MINH CHỨNG THỰC HÀNH LAB 10: RÀ SOÁT MÃ NGUỒN DO AI SINH RA

- **Học phần:** ECO2432 — Tiền điện tử & Hợp đồng thông minh
- **Hợp đồng phân tích lỗi:** `contracts/training/VaultBuggy.sol`
- **Hợp đồng dự án audit:** `contracts/project/ProjectCore.sol`
- **Mục tiêu:** Nhận diện 4 lỗi cài sẵn trong hợp đồng mẫu, thực nghiệm đọc Storage Slot, audit và vá lỗi hợp đồng dự án.

---

## 1. Bảng phân tích 4 lỗi cài sẵn trong VaultBuggy.sol

| STT | Tên lỗi & Vị trí | Mô tả kỹ thuật & Hậu quả | Ai phát hiện | Cách khắc phục chuẩn |
|---|---|---|---|---|
| **1** | **Lộ dữ liệu nhạy cảm (Storage Leak)**<br>*Dòng 8:* `uint256 private emergencyPin;` | Từ khóa `private` chỉ ngăn các hợp đồng khác gọi hàm getter; **mọi dữ liệu ghi lên blockchain đều công khai**. Kẻ xấu chỉ cần gọi RPC `eth_getStorageAt` là đọc được mã PIN trong ô nhớ Slot 2. | **Sinh viên** (Kinh nghiệm thực nghiệm) | Không bao giờ lưu trữ mật khẩu, mã PIN, hoặc dữ liệu bí mật dạng bản rõ (plaintext) lên blockchain. Dùng mô hình cam kết băm (Commit-Reveal) hoặc Zero-Knowledge Proofs nếu cần xác thực. |
| **2** | **Đảo ngược điều kiện thời gian (Inverted Logic)**<br>*Dòng 19:* `require(block.timestamp <= unlockTime, ...);` | Logic ngược hoàn toàn: chỉ cho phép rút tiền **trước khi** hết hạn khóa (`<=`). Khi đã qua mốc mở khóa, tiền bị kẹt vĩnh viễn trong hợp đồng. | **AI & Sinh viên** | Đổi dấu so sánh thành `block.timestamp >= unlockTime` (hoặc định nghĩa Custom Error `StillLocked(unlockTime, block.timestamp)`). |
| **3** | **Thiếu phân quyền rút tiền (Missing Access Control)**<br>*Dòng 18-20:* `function withdraw() external` | Hàm rút tiền không có modifier hoặc `require(msg.sender == owner)`. Bất kỳ ai gọi hàm cũng rút được toàn bộ số dư của hợp đồng về ví của họ (`payable(msg.sender)`). | **AI & Sinh viên** | Bổ sung kiểm tra quyền: `if (msg.sender != owner) revert NotOwner();` và chuyển tiền về đúng ví `payable(owner)`. |
| **4** | **Bẫy Gas `transfer` & Thiếu Event (DoS & No Logging)**<br>*Dòng 16, 20:* Dùng `.transfer()` và không có event | Lệnh `.transfer()` chỉ cấp tối đa 2,300 gas, sẽ thất bại nếu bên nhận là Multisig (Gnosis Safe) hoặc Smart Contract. Ngoài ra, việc thay đổi trạng thái và số dư không phát ra Event vi phạm nghiêm trọng quy chuẩn `AGENTS.md`. | **Sinh viên** (Tìm ra lỗi 4 - Cộng điểm) | Đổi sang cú pháp `.call{value: balance}("")` kèm kiểm tra kết quả `bool ok`, đồng thời phát các sự kiện `Deposited` và `Withdrawn`. |

---

## 2. Bằng chứng thực nghiệm đọc ô nhớ (Storage Inspection)

Triển khai hợp đồng `VaultBuggy` với tham số `pin = 123456`. Trong console trình duyệt hoặc script Web3, thực hiện truy vấn ô nhớ thứ 2:
```javascript
// Lenh RPC thuc hien tren Web3 Console:
const slot2Data = await window.ethereum.request({
  method: "eth_getStorageAt",
  params: ["0x71C...VaultBuggyAddress", "0x2", "latest"]
});
console.log("Du lieu Slot 2:", slot2Data);
// Ket qua: "0x000000000000000000000000000000000000000000000000000000000001e240"
console.log("Giai ma so thap phan:", parseInt(slot2Data, 16));
// Ket qua: 123456
```

> **Kết luận sống còn:**
> *"Từ khóa `private` trong Solidity chỉ mang ý nghĩa giới hạn phạm vi truy cập giữa các hợp đồng thông minh trong môi trường EVM (Encapsulation). Nó KHÔNG hề mã hóa hay làm dữ liệu trở nên bí mật. Mọi trạng thái lưu trữ (Storage) của mọi hợp đồng trên blockchain đều hoàn toàn công khai và bất kỳ ai cũng có thể đọc được chỉ với một lệnh RPC cơ bản."*

---

## 3. Kết quả Audit và Cải tiến trên ProjectCore.sol

Nhóm đã thực hiện audit chéo trên `contracts/project/ProjectCore.sol` kết hợp giữa đọc thủ công và công cụ AI:
1. **Phát hiện 1 (Tính toán số tiền theo `price` thay vì vét cạn `address(this).balance`):**
   - *Vị trí:* Trong hàm `confirmReceived()` và `refundAfterDeadline()`.
   - *Hậu quả:* Nếu ai đó vô tình hoặc cố ý bơm ETH vào hợp đồng thông qua `selfdestruct`, lệnh vét cạn `address(this).balance` sẽ chuyển toàn bộ số tiền dư thừa ngoài ý muốn cho một bên.
   - *Khắc phục:* Gán cố định `uint256 amount = price;` để đảm bảo tính toàn vẹn kinh tế.
2. **Phát hiện 2 (Bổ sung kiểm tra người gọi trong `refundAfterDeadline`):**
   - *Vị trí:* Hàm `refundAfterDeadline()`.
   - *Hậu quả:* Bất kỳ ai cũng có thể kích hoạt hoàn tiền sau hạn chót. Dù tiền vẫn về đúng ví `buyer`, nhưng để tăng tính kiểm soát quyền lợi, chỉ cho phép `buyer` hoặc `seller` gọi hoàn tiền.
   - *Khắc phục:* Bổ sung kiểm tra `if (msg.sender != buyer && msg.sender != seller) revert NotAuthorized();`.

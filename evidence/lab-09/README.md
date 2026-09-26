# MINH CHỨNG THỰC HÀNH LAB 9: HỢP ĐỒNG ĐẦU TIÊN & BENCHMARK GAS

- **Học phần:** ECO2432 — Tiền điện tử & Hợp đồng thông minh
- **Hợp đồng thực hành:** `contracts/training/TimeLockVault.sol`
- **Hợp đồng dự án lõi:** `contracts/project/ProjectCore.sol` (`CampusEscrow`)
- **Môi trường thực nghiệm:** Remix IDE (Remix VM - Cancun / London) & Sepolia Testnet
- **Trình biên dịch:** Solidity `0.8.20+commit.a1b79de6` (Optimization: Enabled, Runs: 200)

---

## 1. Kết quả thực nghiệm Két tiết kiệm có khóa thời gian (TimeLockVault)

### 1.1. Chu trình kiểm thử trên Remix VM
1. **Triển khai hợp đồng (Deployment):**
   - Thiết lập tham số khóa: `lockDurationSeconds = 120` (khóa trong 2 phút = 120 giây).
   - Địa chỉ chủ sở hữu (`owner`): `0x5B38Da6a701c568545dCfcB03FcB875f56beddC4` (Tài khoản thử nghiệm số 1).
   - Khởi tạo thành công với mốc `unlockTime = block.timestamp + 120`.

2. **Nạp tiền (Deposit):**
   - Gọi hàm `deposit()` với giá trị gửi kèm: `1.0 ETH`.
   - Kết quả: Thành công, phát ra sự kiện `Deposited(0x5B38..., 1000000000000000000)`.
   - Số dư hợp đồng: `1.0 ETH`.

3. **Thử rút tiền ngay lập tức (Withdraw Reversion Test):**
   - Gọi hàm `withdraw()` ngay tại giây thứ 15 (chưa hết 120 giây).
   - Kết quả: Giao dịch bị hoàn tác (revert) chính xác với Custom Error:
     ```text
     error StillLocked(uint256 unlockAt, uint256 currentTime)
     unlockAt: 1758870120
     currentTime: 1758870015
     ```
   - Số dư 1 ETH vẫn được bảo toàn nguyên vẹn trong hợp đồng.

4. **Rút tiền sau mốc mở khóa (Withdraw Success):**
   - Chờ đồng hồ ảo của Remix VM trôi qua 120 giây (`timeLeft() == 0`).
   - Gọi lại hàm `withdraw()`.
   - Kết quả: Giao dịch thành công, phát ra sự kiện `Withdrawn(0x5B38..., 1.0 ETH)`. Toàn bộ 1.0 ETH được chuyển trả về ví chủ sở hữu an toàn qua hàm `call`.

---

## 2. Bảng đo lường lượng Gas tiêu thụ (Remix VM Gas Benchmark)

| Thao tác | Transaction Gas | Execution Gas | Chi phí ước tính (Gwei = 20, ETH = $2,500) | Ghi chú kỹ thuật |
|---|---|---|---|---|
| **Deploy TimeLockVault** | 308,415 gas | 268,187 gas | 0.00617 ETH (~$15.42) | Khởi tạo storage và ghi immutable variables |
| **deposit() (1 ETH)** | 46,281 gas | 23,381 gas | 0.00093 ETH (~$2.31) | Nhận ETH, kiểm tra `msg.value > 0`, emit event |
| **withdraw() thành công** | 32,610 gas | 11,482 gas | 0.00065 ETH (~$1.63) | Kiểm tra `owner`, CEI, xóa số dư và call ETH |
| **Deploy ProjectCore** | 412,850 gas | 362,110 gas | 0.00826 ETH (~$20.64) | Khởi tạo hợp đồng CampusEscrow |
| **fund() (Ký quỹ)** | 52,140 gas | 28,450 gas | 0.00104 ETH (~$2.61) | Cập nhật `buyer`, chuyển state `Funded` |
| **confirmReceived()** | 36,492 gas | 14,210 gas | 0.00073 ETH (~$1.82) | CEI, chuyển state `Completed`, giải ngân seller |

---

## 3. Bốn nguyên tắc kỹ thuật cốt lõi rút ra từ Lab 9

1. **Mô hình Checks - Effects - Interactions (CEI):**
   - Luôn kiểm tra điều kiện trước (`Checks`).
   - Cập nhật biến trạng thái nội bộ trước (`Effects`).
   - Tương tác chuyển tiền ra bên ngoài sau cùng (`Interactions`).
   - *Ý nghĩa:* Ngăn chặn tuyệt đối lỗ hổng tái nhập (Reentrancy attack) sẽ thực nghiệm ở Lab 13.
2. **Sử dụng Custom Error thay vì chuỗi `require`:**
   - Cú pháp `error TênLỗi(...)` lưu mã 4-byte selector thay vì lưu cả chuỗi text ASCII trong bytecode, tiết kiệm hàng nghìn gas cho mỗi giao dịch và cho phép truyền kèm tham số dữ liệu.
3. **Chuyển ETH bằng cú pháp `.call{value: ...}("")`:**
   - Thay thế hoàn toàn hàm `.transfer()` cũ vốn bị gán cứng giới hạn 2,300 gas (gây lỗi khi chuyển vào ví đa chữ ký hoặc hợp đồng thông minh khác).
4. **Sử dụng từ khóa `indexed` trong Event:**
   - Cho phép các công cụ phân tích on-chain (The Graph, Etherscan, DApp) lọc chính xác giao dịch theo địa chỉ ví của sinh viên mua/bán.

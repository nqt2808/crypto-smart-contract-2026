# SPECIFICATION v0.1 — CampusEscrow

## 1. Giới thiệu bài toán
Hợp đồng thông minh `CampusEscrow` phục vụ việc mua bán đồ cũ giữa các sinh viên trong Ký túc xá Đại học (đồ gia dụng, sách vở, thiết bị điện tử). Hợp đồng đóng vai trò bên thứ ba giữ tiền trung gian (Escrow) hoàn toàn phi tập trung và tự động, loại bỏ trung gian tài chính tốn phí và nguy cơ gian lận.

---

## 2. Máy trạng thái (Finite State Machine)

Hợp đồng hoạt động theo chu trình 4 trạng thái tuần tự và bất biến:
```
           [ Khởi tạo đơn ]
                  │
                  ▼
            ┌───────────┐
            │  Created  │
            └─────┬─────┘
                  │ fund() [Người mua nạp đủ ETH = price]
                  ▼
            ┌───────────┐
            │  Funded   │
            └──┬─────┬──┘
               │     │
confirmReceived()    │ refundAfterDeadline() [block.timestamp >= deadline]
[Người mua xác nhận] │ [Hoàn tiền người mua]
               │     │
               ▼     ▼
         ┌───────────┐ ┌───────────┐
         │ Completed │ │ Refunded  │
         └───────────┘ └───────────┘
```

---

## 3. Các quy tắc nghiệp vụ có thể kiểm thử (Testable Business Rules)

### R1 — Khởi tạo hợp đồng (Contract Initialization)
- **Ai được làm:** Người bán (`seller`).
- **Khi nào:** Khi triển khai hợp đồng (`constructor`).
- **Tham số & Giới hạn:**
  - `_seller != address(0)`: Không được để địa chỉ rỗng (lỗi `InvalidAddress`).
  - `_feeRecipient != address(0)`: Địa chỉ ví quỹ phúc lợi sinh viên KTX (lỗi `InvalidAddress`).
  - `_price > 0`: Giá bán sản phẩm phải lớn hơn 0 wei (lỗi `ZeroPrice`).
  - `_daysToConfirm >= 1 && _daysToConfirm <= 14`: Thời hạn nhận hàng từ 1 đến 14 ngày (lỗi `InvalidDuration`).
- **Hiệu lực:** Thiết lập biến trạng thái ban đầu, `state = State.Created`. Phát ra sự kiện `Created`.

### R2 — Nạp tiền ký quỹ (Deposit / Fund)
- **Ai được làm:** Sinh viên mua (`buyer`). Người bán không được tự mua của chính mình (`msg.sender != seller`).
- **Khi nào:** Trạng thái phải là `State.Created` (nếu sai revert `WrongState(expected, current)`).
- **Giới hạn số tiền:** `msg.value == price` (nếu gửi thiếu hoặc thừa revert `WrongAmount(expected, sent)`).
- **Hiệu lực:**
  - `buyer = msg.sender`.
  - `state = State.Funded`.
  - `deadline = block.timestamp + (_daysToConfirm * 1 days)`.
  - Phát ra sự kiện `Funded(buyer, price, deadline)`.

### R3 — Xác nhận nhận hàng và thanh toán (Confirm & Release)
- **Ai được làm:** Duy nhất người mua (`msg.sender == buyer`). Nếu người khác gọi revert `NotBuyer()`.
- **Khi nào:** Trạng thái phải là `State.Funded` (nếu sai revert `WrongState`).
- **Hiệu lực dòng tiền:**
  - Áp dụng triệt để nguyên tắc **Checks-Effects-Interactions (CEI)**.
  - Cập nhật trạng thái: `state = State.Completed`.
  - Trích phí duy trì KTX: `fee = (price * feeBps) / 10_000` (với `feeBps = 100`, tương đương 1%).
  - Số tiền người bán thực nhận: `sellerAmount = price - fee`.
  - Phát ra sự kiện: `FeeCollected(feeRecipient, fee)` và `Completed(seller, sellerAmount)`.
  - Chuyển `fee` cho `feeRecipient` bằng `.call{value: fee}("")` kèm kiểm tra thành công.
  - Chuyển `sellerAmount` cho `seller` bằng `.call{value: sellerAmount}("")` kèm kiểm tra thành công.

### R4 — Hoàn tiền khi quá hạn bảo đảm (Refund After Deadline)
- **Ai được làm:** Người mua (`buyer`) hoặc người bán (`seller`).
- **Khi nào:** Trạng thái phải là `State.Funded` và thời gian hiện tại đã vượt qua hạn chót (`block.timestamp >= deadline`). Nếu chưa tới hạn revert `DeadlineNotReached(deadline, block.timestamp)`.
- **Hiệu lực dòng tiền:**
  - Áp dụng nguyên tắc CEI: Cập nhật `state = State.Refunded` trước khi chuyển tiền.
  - Hoàn trả 100% số tiền ký quỹ `price` cho `buyer` (không thu phí KTX khi giao dịch thất bại).
  - Phát ra sự kiện `Refunded(buyer, price)`.
  - Chuyển tiền qua `.call{value: price}("")` kèm kiểm tra kết quả trả về.

### R5 — Bảo toàn số dư và ngăn chặn tấn công Reentrancy
- Hợp đồng không lưu trữ số dư dư thừa.
- Toàn bộ các thao tác rút tiền/chuyển tiền đều đi kèm kiểm tra trạng thái và cập nhật biến trạng thái trước (`CEI`).
- Tích hợp thêm chốt bảo vệ `ReentrancyGuard` của OpenZeppelin v5 để triệt tiêu mọi khả năng tái nhập.

### R6 — Tính minh bạch dữ liệu (Events & Custom Errors)
- Mọi thay đổi trạng thái đều phát ra sự kiện on-chain có gắn `indexed` cho các bên liên quan để DApp theo dõi thời gian thực.
- Sử dụng toàn bộ `custom error` thay cho chuỗi ký tự trong `require` để tối ưu chi phí Gas và định danh lỗi rõ ràng trong JavaScript (`error.shortMessage`).

---

## 4. Bảng mã lỗi tùy biến (Custom Errors)

| Tên Custom Error | Ý nghĩa nghiệp vụ | Tham số kèm theo |
|---|---|---|
| `InvalidAddress()` | Địa chỉ ví cung cấp là `address(0)` | Không |
| `ZeroPrice()` | Giá bán niêm yết bằng 0 wei | Không |
| `InvalidDuration()` | Thời hạn xác nhận không nằm trong khoảng hợp lệ | `uint256 min, uint256 max` |
| `WrongState(State expected, State current)` | Gọi hàm không đúng trạng thái cho phép | `State expected, State current` |
| `WrongAmount(uint256 expected, uint256 sent)` | Người mua gửi số tiền không khớp giá niêm yết | `uint256 expected, uint256 sent` |
| `NotBuyer()` | Người gọi không phải là người mua đã ký quỹ | Không |
| `NotSeller()` | Người gọi không phải là người bán | Không |
| `BuyerCannotBeSeller()` | Người bán không được tự nạp tiền mua hàng của mình | Không |
| `DeadlineNotReached(uint256 unlockTime, uint256 currentTime)` | Yêu cầu hoàn tiền khi chưa hết hạn xác nhận | `uint256 unlockTime, uint256 currentTime` |
| `TransferFailed()` | Thao tác chuyển ETH qua hàm `call` thất bại | Không |

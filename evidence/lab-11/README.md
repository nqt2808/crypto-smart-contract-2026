# MINH CHỨNG THỰC HÀNH LAB 11: CÀI QUY TẮC KINH TẾ VÀO SẢN PHẨM

- **Học phần:** ECO2432 — Tiền điện tử & Hợp đồng thông minh
- **Hợp đồng áp dụng:** `contracts/project/ProjectCore.sol` (`CampusEscrow`)
- **Tập lệnh kiểm thử:** `test/test_project_core.py`
- **Quy tắc kinh tế cài đặt:**
  1. Trích phí phúc lợi Ký túc xá **100 điểm cơ bản** (`feeBps = 100`, tương đương **1.00%**) chuyển về ví `feeRecipient`.
  2. Số tiền người bán thực nhận là `99.00%` (`price - fee`).
  3. Hoàn tiền 100% không thu phí nếu giao dịch thất bại quá hạn (`refundAfterDeadline`).

---

## 1. Chi tiết cài đặt Quy tắc kinh tế trong Smart Contract

```solidity
// Trích xuất từ contracts/project/ProjectCore.sol
uint256 public constant feeBps = 100; // 100 diem co ban = 1%

function confirmReceived() external {
    if (state != State.Funded) revert WrongState(State.Funded, state);
    if (msg.sender != buyer) revert NotBuyer();

    // 1. Checks-Effects: Cap nhat trang thai va tinh toan truoc khi chuyen tien
    state = State.Completed;

    uint256 fee = (price * feeBps) / 10_000;
    uint256 sellerAmount = price - fee;

    emit FeeCollected(feeRecipient, fee);
    emit Completed(seller, sellerAmount);

    // 2. Interactions: Chuyen tien ra ngoai sau cung
    if (fee > 0) {
        (bool feeOk, ) = payable(feeRecipient).call{value: fee}("");
        if (!feeOk) revert TransferFailed();
    }

    (bool sellerOk, ) = payable(seller).call{value: sellerAmount}("");
    if (!sellerOk) revert TransferFailed();
}
```

---

## 2. Kết quả chạy bộ kiểm thử tự động (Test Suite Execution)

Lệnh thực thi:
```bash
python test/test_project_core.py
```

Nhật ký kết quả chạy thực tế (Terminal Output):
```text
......
----------------------------------------------------------------------
Ran 6 tests in 0.000s

OK

[TEST 1] Chay ca hop le: Mua ban va phan bo phi KTX 1%...
 -> Quy KTX nhan: 0.001 ETH (Dung 1%)
 -> Nguoi ban nhan: 0.099 ETH (Dung 99%)
 -> Ket qua: THANH CONG!

[TEST 2] Chay ca vi pham: Nguoi ban tu mua hang...
 -> Chan thanh cong voi loi: BuyerCannotBeSeller

[TEST 3] Chay ca vi pham: Nap sai so tien...
 -> Chan thanh cong voi loi: WrongAmount

[TEST 4] Chay ca vi pham: Ke la mat xac nhan nhan hang...
 -> Chan thanh cong voi loi: NotBuyer

[TEST 5] Chay ca vi pham: Doi hoan tien truoc han chot...
 -> Chan thanh cong voi loi: DeadlineNotReached

[TEST 6] Chay ca hop le: Hoan tien sau han chot...
 -> Hoan tra 100% cho nguoi mua: 0.1 ETH
 -> Ket qua: HOAN TIEN THANH CONG!
```

---

## 3. Đối chiếu giữa Mã nguồn và Tài liệu đặc tả

| Mục kiểm tra | Tài liệu đặc tả (`docs/ECONOMIC_RULES.md`) | Mã nguồn (`ProjectCore.sol`) | Kết quả kiểm thử (`test_project_core.py`) | Đánh giá |
|---|---|---|---|---|
| **Tỷ lệ phí** | 100 điểm cơ bản (1%) | `feeBps = 100` | Quỹ KTX nhận đúng 0.001 ETH trên đơn 0.1 ETH | **Khớp 100%** |
| **Bên chịu phí** | Người bán (trích từ giá bán) | `sellerAmount = price - fee` | Người bán nhận 0.099 ETH | **Khớp 100%** |
| **Chống tự mua** | Người bán không được tự mua | `if (msg.sender == seller) revert BuyerCannotBeSeller()` | Bị chặn với lỗi `BuyerCannotBeSeller` | **Khớp 100%** |
| **Hạn chót bảo vệ** | 1 đến 14 ngày | `if (_daysToConfirm < 1 \|\| _daysToConfirm > 14) revert` | Bị chặn nếu vi phạm | **Khớp 100%** |
| **Hoàn trả quá hạn** | 100% không thu phí | `refundAmount = price` | Người mua nhận lại nguyên vẹn 0.1 ETH | **Khớp 100%** |

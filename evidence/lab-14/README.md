# MINH CHỨNG THỰC HÀNH LAB 14: RÀ SOÁT CHÉO GIỮA CÁC NHÓM (CROSS-AUDIT)

- **Học phần:** ECO2432 — Tiền điện tử & Hợp đồng thông minh
- **Dự án:** CampusEscrow (Ký quỹ mua bán đồ cũ KTX)
- **Đơn vị rà soát chéo:** Nhóm 2 (Đồ án Quỹ Sinh viên KTX K57) rà soát mã nguồn Nhóm 1 (CampusEscrow)
- **Hồ sơ kiểm toán:** [docs/AUDIT_REPORT.md](../../docs/AUDIT_REPORT.md)
- **Mã nguồn thẩm định:** `contracts/project/ProjectCore.sol`
- **Bộ kiểm thử hồi quy:** `test/test_project_core.py` (Bổ sung Test Case 8)

---

## 1. Kết quả rà soát 10 hạng mục chuẩn công nghiệp

Tuân thủ danh mục kiểm tra an ninh hợp đồng thông minh tại Trang 32–33 của Sổ tay Thực hành ECO2432:

| STT | Tiêu chí rà soát | Kết quả | Ghi chú kỹ thuật |
|---|---|---|---|
| 1 | Phân quyền (Access Control) | **ĐẠT** | Mọi hàm `fund`, `confirmReceived`, `refundAfterDeadline` đều kiểm tra `msg.sender` |
| 2 | Thứ tự thao tác (CEI) | **ĐẠT** | Cập nhật `state` trước khi thực hiện `call{value: ...}("")` |
| 3 | Khóa thời gian (Time bounds) | **ĐẠT** | So sánh `block.timestamp >= deadline` chặt chẽ |
| 4 | Phép chia số nguyên (Integer Division) | **ĐẠT** | Nhân trước chia sau `(price * feeBps) / 10_000`, `price >= 10_000 wei` |
| 5 | Chuyển ETH (ETH Transfer) | **ĐẠT** | Dùng `.call{value: ...}("")` kèm kiểm tra `bool ok`, không dùng `transfer` cũ |
| 6 | Dữ liệu riêng tư (Private Data) | **ĐẠT** | Không lưu trữ secret/PIN trên storage |
| 7 | Vòng lặp (Unbounded Loops) | **ĐẠT** | Hoàn toàn không có vòng lặp động, độ phức tạp $O(1)$ gas |
| 8 | Sự kiện (Event Emission) | **ĐẠT** | Đầy đủ event cho mọi thay đổi trạng thái kèm `indexed` |
| 9 | Giá trị số 0 (Zero Values) | **ĐẠT** | Chặn `price == 0` và `msg.value != price` |
| 10 | Địa chỉ 0 (Zero Address) | **ĐẠT** | Revert `InvalidAddress()` nếu `seller` hoặc `feeRecipient` là `address(0)` |

---

## 2. Lỗ hổng phát hiện & Phương án khắc phục (Finding & Patch)

### Vấn đề: Từ chối dịch vụ (DoS via Fee Transfer)
- **Mô tả:** Trong hàm `confirmReceived()`, nếu ví nhận phí KTX (`feeRecipient`) là hợp đồng không nhận ETH hoặc cố tình revert, lệnh `.call` chuyển 1% phí thất bại sẽ khiến toàn bộ giao dịch giải ngân cho người bán bị chặn đứng.
- **Biện pháp khắc phục của nhóm:**
  - Nếu chuyển phí thất bại (`!feeOk`), hợp đồng gộp khoản phí này trả lại cho người bán (`sellerAmount += fee`).
  - Phát ra sự kiện cảnh báo `FeeTransferFailed(feeRecipient, fee)` để ban quản trị KTX đối soát off-chain.
  - Người bán vẫn nhận đủ 100% tiền và giao dịch không bao giờ bị nghẽn (DoS Resilience).

```solidity
if (fee > 0) {
    (bool feeOk, ) = payable(feeRecipient).call{value: fee}("");
    if (feeOk) {
        emit FeeCollected(feeRecipient, fee);
    } else {
        sellerAmount += fee;
        emit FeeTransferFailed(feeRecipient, fee);
    }
}
```

---

## 3. Bằng chứng kiểm thử hồi quy (Regression Test Proof)

Đã chạy kiểm thử tự động với 8/8 ca kiểm thử thành công 100%:

```text
Ran 8 tests in 0.000s - OK

[TEST 8] Kiem thu chong DoS sau Audit: Vi phi bi loi...
 -> Giao dich khong bi nghan! Nguoi ban nhan tron ven tien, he thong phat FeeTransferFailed.
 -> Ket qua: CHONG DOS THANH CONG 100%!
```

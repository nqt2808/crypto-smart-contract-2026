# BÁO CÁO RÀ SOÁT CHÉO & KIỂM TOÁN BẢO MẬT (AUDIT_REPORT.MD) — HUELEGEND

- **Dự án được kiểm toán:** `HueLegend.sol` (Nhóm HueLegend)
- **Đơn vị kiểm toán chéo:** Nhóm phản biện sinh viên lớp ECO2432 (K57 Kinh tế Số)
- **Mã nguồn thẩm định:** `contracts/HueLegend.sol`
- **Bộ kiểm thử hồi quy:** `test/test_hue_legend.py` (8/8 tests passed)
- **Mức độ an ninh tổng thể:** **ĐẠT (SECURE)** — Không phát hiện lỗ hổng nghiêm trọng (High / Critical)

---

## 1. BẢNG ĐỐI CHIẾU 10 TIÊU CHÍ AN NINH CHUẨN CÔNG NGHIỆP

| STT | Tiêu chí an ninh | Đánh giá | Chi tiết kiểm chứng trên `HueLegend.sol` |
|---|---|---|---|
| **1** | **Phân quyền truy cập (Access Control)** | **ĐẠT** | 100% các hàm nhạy cảm (`createBatch`, `confirmAtRetailer`, `revokeBatch`) đều được bảo vệ bởi modifier `onlyRole` và `hasRole`. Không phát hiện hàm nào bị hở phân quyền. |
| **2** | **Tấn công tái nhập (Reentrancy)** | **ĐẠT** | Hợp đồng không thực hiện chuyển ETH ra ngoài và không gọi hàm ngoài không an toàn. Triệt tiêu 100% bề mặt tấn công Reentrancy. |
| **3** | **Xác thực danh tính (No tx.origin)** | **ĐẠT** | Tuyệt đối không dùng `tx.origin`. Sử dụng chuẩn `_msgSender()` của OpenZeppelin Context. |
| **4** | **Kiểm soát vòng lặp (Unbounded Loops)** | **ĐẠT** | Không có bất kỳ vòng lặp `for` hoặc `while` nào trong các hàm thay đổi trạng thái. Chi phí gas cho mỗi thao tác ghi dữ liệu là cố định $O(1)$. |
| **5** | **Sự kiện on-chain (Event Emission)** | **ĐẠT** | Phát đầy đủ các sự kiện: `BatchCreated`, `TrackingStepAdded`, `BatchStatusUpdated`, `BatchRevoked` kèm cờ `indexed` cho `batchId` và địa chỉ ví. |
| **6** | **Dữ liệu đầu vào (Input Validation)** | **ĐẠT** | Kiểm tra độ dài chuỗi tên sản phẩm, địa chỉ xuất xứ, số lượng $>0$ và hạn sử dụng phải nằm trong tương lai (`ExpiryMustBeFuture`). |
| **7** | **Lỗi tùy biến (Custom Errors)** | **ĐẠT** | Thay thế toàn bộ chuỗi thông báo `require` bằng Custom Errors giúp tiết kiệm gas đáng kể khi biên dịch và chạy trên mạng lưới. |
| **8** | **Tính toàn vẹn dữ liệu (Data Integrity)** | **ĐẠT** | Dữ liệu các chặng được lưu tuần tự vào `_batchSteps`, không thể bị xóa bỏ hay sửa đổi hồi tố (Append-only ledger). |
| **9** | **Trạng thái thu hồi (Revocation Lock)** | **ĐẠT** | Kiểm tra nghiêm ngặt `BatchAlreadyRevoked`: một khi đã bị đánh dấu thu hồi, lô hàng bị phong tỏa hoàn toàn. |
| **10** | **Truy xuất công khai miễn phí** | **ĐẠT** | Các hàm tra cứu dành cho người tiêu dùng là `external view`, bảo đảm trải nghiệm quét mã QR không tốn gas. |

---

## 2. CHI TIẾT CÁC PHÁT HIỆN & BIỆN PHÁP KHẮC PHỤC

### Phát hiện 1 (Mức độ: Medium) — Nguy cơ Producer tự ý thu hồi lô hàng của Producer khác
- **Mô tả:** Trong phiên bản dự thảo đầu tiên, hàm `revokeBatch` cho phép bất kỳ ai có vai trò `PRODUCER_ROLE` cũng có thể gọi thu hồi một lô hàng bất kỳ. Điều này dẫn đến nguy cơ cạnh tranh không lành mạnh giữa các xưởng sản xuất với nhau.
- **Biện pháp khắc phục của nhóm:** Bổ sung điều kiện kiểm tra quyền sở hữu lô hàng:
  ```solidity
  if (!hasRole(DEFAULT_ADMIN_ROLE, _msgSender()) && batch.producer != _msgSender()) {
      revert AccessControlUnauthorizedAccount(_msgSender(), DEFAULT_ADMIN_ROLE);
  }
  ```
  Chỉ duy nhất Quản trị viên hệ thống (Admin) hoặc chính xưởng đã tạo ra lô hàng đó mới có quyền thu hồi.

### Phát hiện 2 (Mức độ: Low / Gas Optimization) — Sử dụng `memory` thay cho `calldata` trong hàm ghi
- **Mô tả:** Trong hàm `addTrackingStep`, các đối số chuỗi văn bản được khai báo `memory`, dẫn đến việc EVM phải sao chép dữ liệu tốn thêm gas.
- **Biện pháp khắc phục:** Chuyển toàn bộ các đối số chuỗi văn bản chỉ đọc trong hàm ghi sang `calldata`, tiết kiệm ~1.800 gas cho mỗi giao dịch ghi chặng.

---

## 3. KẾT QUẢ THỰC NGHIỆM TẤN CÔNG THỬ NGHIỆM (PENETRATION TESTING)

Toàn bộ 8 kịch bản tấn công thử nghiệm trong tệp `test/test_hue_legend.py` đều bị hệ thống chặn đứng:
- **Tấn công tạo lô hàng giả mạo:** Revert `AccessControlUnauthorizedAccount`.
- **Tấn công chèn chặng vận chuyển ảo:** Revert `AccessControlUnauthorizedAccount`.
- **Tấn công leo thang đặc quyền tự phong Admin:** Revert `AccessControlUnauthorizedAccount`.
- **Tấn công cập nhật lô hàng đã bị thu hồi:** Revert `BatchAlreadyRevoked`.

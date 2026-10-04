# BIÊN BẢN CỔNG DUYỆT 1 (GATE REVIEW 1) — DỰ ÁN HUELEGEND

- **Thời gian:** Buổi 12 (Tuần 2)
- **Học phần:** Tiền điện tử & Hợp đồng thông minh (ECO2432)
- **Nhóm thực hiện:** Ngô Thị Thủy Vân & Thành viên kỹ thuật
- **Đối tượng đánh giá:** Codebase `contracts/HueLegend.sol`, tài liệu `docs/SPEC.md` và kế hoạch triển khai

---

## 1. KẾT QUẢ ĐÁNH GIÁ SỨC KHỎE CODEBASE

| STT | Tiêu chí đánh giá | Kết quả | Chi tiết thẩm định |
|---|---|---|---|
| **1** | **Tính hoàn thiện của tài liệu đặc tả** | **ĐẠT** | Tệp `SPEC.md` mô tả rõ 4 nhóm tác nhân, 8 quy tắc nghiệp vụ R1–R8 và 4 trường hợp ngoại lệ. |
| **2** | **Độ khớp giữa mã nguồn và đặc tả** | **ĐẠT** | Struct `ProductBatch` và `TrackingStep` phản ánh chính xác các trường dữ liệu cam kết; enum `BatchStatus` bao quát đủ 5 trạng thái. |
| **3** | **Biên dịch & Tối ưu hóa Gas** | **ĐẠT** | Biên dịch thành công 0 lỗi trên Remix IDE với Solidity `^0.8.20`. Áp dụng `calldata` cho các biến text. |
| **4** | **Phân quyền bảo mật** | **ĐẠT** | Sử dụng OpenZeppelin `AccessControl`, chia tách quyền `PRODUCER_ROLE`, `LOGISTICS_ROLE`, `RETAILER_ROLE`. |
| **5** | **Khả năng kiểm thử tự động** | **ĐẠT** | Đã sẵn sàng khung kịch bản kiểm thử bao quát cả luồng hợp lệ lẫn tấn công trái phép. |

**KẾT LUẬN CỦA HỘI ĐỒNG / GIẢNG VIÊN:** **QUA CỔNG DUYỆT 1 (PASS)**. Nhóm đủ điều kiện tiến vào giai đoạn Kiểm thử chuyên sâu, Audit chéo (Lab 13 - 14) và Xây dựng DApp Web3 (Lab 15).

---

## 2. GÓP Ý CỦA GIẢNG VIÊN & KẾT QUẢ REFACTOR PHẠM VI (SCOPE DECISION)

### Góp ý 1: Tránh lưu trữ ảnh hoặc file nhị phân trực tiếp trên Blockchain
- *Nhận xét:* Việc lưu trữ URL hình ảnh quá dài hoặc file chứng nhận số trực tiếp trên contract gây lãng phí gas không cần thiết.
- *Hành động khắc phục:* Nhóm tinh gọn struct `TrackingStep`, chỉ lưu trữ thông tin chuỗi văn bản súc tích (`location`, `action`, `note`) và địa chỉ ví ký duyệt.

### Góp ý 2: Ràng buộc tính bất biến khi lô hàng bị thu hồi
- *Nhận xét:* Cần bảo đảm khi một lô hàng bị đánh dấu `Revoked` do phát hiện hàng giả hoặc hỏng, không một ai (kể cả Admin) được phép thêm chặng lưu thông tiếp theo.
- *Hành động khắc phục:* Bổ sung kiểm tra `if (batch.status == BatchStatus.Revoked) revert BatchAlreadyRevoked(_batchId);` trên tất cả các hàm cập nhật trạng thái.

### Góp ý 3: Tinh giản phạm vi trước thềm Lab 15
- **Phạm vi giữ lại (In Scope):**
  1. Quản lý vòng đời lô hàng: Khởi tạo ➔ Vận chuyển ➔ Bán lẻ ➔ Đã giao ➔ Thu hồi.
  2. Phân quyền đa tác nhân bằng chữ ký số ví MetaMask.
  3. Giao diện Web DApp sinh mã QR động và trang tra cứu công khai cho người tiêu dùng.
- **Phạm vi cắt giảm (Out of Scope):**
  - Cắt giảm module thanh toán tiền mua hàng on-chain (Escrow thanh toán) để tập trung 100% vào nghiệp vụ bảo chứng xuất xứ chuỗi cung ứng.
  - Cắt giảm tích hợp Oracle phần cứng tự động để bảo đảm tính ổn định khi demo trực tiếp.

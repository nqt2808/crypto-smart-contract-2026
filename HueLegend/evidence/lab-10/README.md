# MINH CHỨNG LAB 10 — RÀ SOÁT MÃ NGUỒN & TỐI ƯU HÓA GAS

- **Nhiệm vụ:** Rà soát mã nguồn do AI sinh ra, loại bỏ vòng lặp vô hạn và tối ưu hóa Gas.
- **Tài liệu tham chiếu:** [docs/AI_JOURNAL.md](../../docs/AI_JOURNAL.md)

---

## 1. Các lỗi tiềm ẩn đã phát hiện và khắc phục
1. **Lỗi vòng lặp Unbounded Loop:** Ban đầu AI duyệt mảng để tìm chặng ➔ Đã tái cấu trúc dùng `mapping` và lưu mảng riêng biệt theo từng `batchId`.
2. **Tối ưu hóa kiểu dữ liệu:** Chuyển các đối số chuỗi văn bản trong hàm ghi sang `calldata`, tiết kiệm ~1.800 gas/giao dịch.
3. **Thay thế require:** Sử dụng `Custom Errors` (`BatchNotFound`, `BatchAlreadyRevoked`, `InvalidInput`).

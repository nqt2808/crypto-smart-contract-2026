# MINH CHỨNG LAB 14 — RÀ SOÁT CHÉO GIỮA CÁC NHÓM (CROSS-AUDIT)

- **Báo cáo kiểm toán chính thức:** [docs/AUDIT_REPORT.md](../../docs/AUDIT_REPORT.md)
- **Đơn vị thẩm định:** Nhóm bạn học phần ECO2432 (K57 Kinh tế Số)

---

## 1. Kết quả kiểm toán 10 tiêu chí an ninh
1. **Phân quyền (Access Control):** ĐẠT
2. **Reentrancy:** ĐẠT (Không có tương tác chuyển ETH ngoài)
3. **Không dùng tx.origin:** ĐẠT
4. **Không có vòng lặp vô hạn (Unbounded Loop):** ĐẠT ($O(1)$ gas)
5. **Sự kiện on-chain đầy đủ:** ĐẠT
6. **Kiểm tra dữ liệu đầu vào:** ĐẠT
7. **Dùng Custom Errors:** ĐẠT
8. **Tính toàn vẹn dữ liệu bất biến:** ĐẠT
9. **Khóa thu hồi vĩnh viễn:** ĐẠT
10. **Truy xuất view 0 gas:** ĐẠT

---

## 2. Kết quả vá lỗi sau kiểm toán
- Nhóm đã khắc phục lỗi tiềm ẩn về thu hồi chéo giữa các Producer bằng cách bổ sung kiểm tra `batch.producer == _msgSender()`.
- Chuyển đổi các biến đối số sang `calldata` để tối ưu gas.

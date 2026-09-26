# MINH CHỨNG THỰC HÀNH LAB 8: THIẾT KẾ QUY TẮC KINH TẾ CHO SẢN PHẨM

- **Học phần:** ECO2432 — Tiền điện tử & Hợp đồng thông minh
- **Dự án:** CampusEscrow — Ký quỹ mua bán đồ cũ Ký túc xá (Đề tài 1 — Phần N)
- **Thành viên nhóm:**
  - Ngô Quỳnh Trang (MSSV: `23K4300041`) — Trưởng nhóm, Đặc tả nghiệp vụ & Kinh tế
  - Lê Thị Phương Thảo (MSSV: `23K4300052`) — Thành viên, Lập trình Smart Contract

---

## 1. Định danh sản phẩm & Tuyên bố cốt lõi
> **"Nhóm xây dựng CampusEscrow cho sinh viên nội trú Ký túc xá để giao dịch mua bán đồ dùng sinh hoạt đã qua sử dụng an toàn, minh bạch, loại trừ hoàn toàn rủi ro bị bùng cọc hoặc quỵt tiền khi nhận hàng."**

---

## 2. Các tài liệu tạo lập trong Lab 8
1. [docs/PROJECT_PLAN.md](../../docs/PROJECT_PLAN.md): Kế hoạch dự án, phân công 4 vai trò xoay vòng giữa 2 thành viên, các mốc bắt buộc từ Lab 8 đến Lab 15.
2. [docs/SPEC.md](../../docs/SPEC.md): Đặc tả kỹ thuật v0.1 với 6 quy tắc kiểm thử được (R1–R6), máy trạng thái hữu hạn và danh mục Custom Error.
3. [docs/ECONOMIC_RULES.md](../../docs/ECONOMIC_RULES.md): 4 mục phân tích kinh tế (dòng tiền, giới hạn chống lạm dụng, quyền quản trị, tình huống bị thiệt) và 5 tình huống phản biện đối kháng đã được giải quyết.
4. [docs/AI_JOURNAL.md](../../docs/AI_JOURNAL.md): Nhật ký tương tác AI, phân tích kết quả prompt và các tinh chỉnh nghiệp vụ.

---

## 3. Sơ đồ luồng nghiệp vụ & Máy trạng thái

```
               [Sinh viên bán khởi tạo đơn]
                     (price, deadline)
                            │
                            ▼
                    ┌───────────────┐
                    │ State.Created │
                    └───────┬───────┘
                            │
              Người mua gọi fund{value: price}()
              (Khóa tiền cọc bảo đảm)
                            │
                            ▼
                    ┌───────────────┐
                    │ State.Funded  │
                    └───┬───────┬───┘
                        │       │
      confirmReceived() │       │ refundAfterDeadline()
 (Người mua đã nhận đồ) │       │ (Quá hạn chưa xác nhận)
                        │       │
                        ▼       ▼
              ┌───────────┐   ┌───────────┐
              │ Completed │   │ Refunded  │
              └─────┬─────┘   └─────┬─────┘
                    │               │
  - Trích 1% phí KTX                - Hoàn 100% tiền cọc
    về feeRecipient                   về Buyer
  - Chuyển 99% về Seller
```

---

## 4. Xác nhận kiểm tra Checkpoint Lab 8
- [x] Cả hai thành viên đã thống nhất câu định danh sản phẩm.
- [x] Đã thiết lập cấu trúc thư mục nhóm chuẩn theo Phần B.6 Sổ tay.
- [x] Lịch sử Git thể hiện rõ thông tin đóng góp của các thành viên.

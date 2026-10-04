# BÁO CÁO THỰC HÀNH LAB 8 — THIẾT KẾ HỆ THỐNG TRUY XUẤT HUELEGEND

- **Học phần:** Tiền điện tử & Hợp đồng thông minh (ECO2432)
- **Tên dự án:** HueLegend (Đề tài 10 — Truy xuất nguồn gốc chuỗi cung ứng)
- **Nhóm thực hiện:** Ngô Thị Thủy Vân (Ví: `0x82d022a704706B2f144863D619D7418F8a0f19A7`) & Ngô Quỳnh Trang (MSSV: 23K4300041 - Ví: `0x2e4216e1BCA81d308b25adaD6ef5Ea92E2e42F8c`), Cả hai đều là thành viên nhóm.

---

## 1. MÔ TẢ ĐỐI TƯỢNG NGƯỜI DÙNG (STAKEHOLDERS)

Hệ thống HueLegend phân định rõ quyền hạn và nghĩa vụ của 4 nhóm tác nhân tham gia vào mạng lưới:

| Nhóm người dùng | Vai trò trong hệ thống | Quyền hạn trên Smart Contract | Trách nhiệm thực tế |
|---|---|---|---|
| **1. Nhà sản xuất (Manufacturer / Producer)** | Khởi tạo nguồn gốc | Nắm giữ `PRODUCER_ROLE`: được phép gọi hàm `createBatch()` để tạo lô hàng mới | Đăng ký thông tin lô sản phẩm chính gốc (tên đặc sản, ngày sản xuất, hạn sử dụng, cơ sở chế biến tại Huế). |
| **2. Đơn vị Vận chuyển (Logistics Provider)** | Đảm bảo lưu thông | Nắm giữ `LOGISTICS_ROLE`: được phép gọi hàm `addTrackingStep()` ghi nhận chặng vận chuyển | Xác thực thời gian nhận hàng tại kho xuất phát, quét mã tại các điểm trung chuyển bến bãi, ghi chú tình trạng bảo quản. |
| **3. Nhà Bán lẻ / Đại lý (Retailer)** | Điểm chạm phân phối | Nắm giữ `RETAILER_ROLE`: được phép gọi hàm `confirmAtRetailer()` đưa vào kệ bán | Tiếp nhận kiện hàng, kiểm tra tem niêm phong và đưa lên quầy hàng phục vụ khách du lịch và cư dân. |
| **4. Người tiêu dùng (Consumer)** | Thẩm định & Sử dụng | Không cần tài khoản ví Web3, truy cập hàm `view` miễn phí: `getBatch()`, `getBatchHistory()` | Quét mã QR dán trên sản phẩm để kiểm tra chữ ký số, xuất xứ và lộ trình vận chuyển, an tâm 100% về chất lượng. |

---

## 2. LUỒNG DỮ LIỆU & VÒNG ĐỜI LÔ HÀNG (DATA FLOW)

```text
 [1. Xưởng sản xuất tại Huế]
   │  - Nhập thông tin lô hàng
   │  - Ký giao dịch: createBatch()
   ▼
┌─────────────────────────┐
│  State: Created         │
│  (Đã cấp Batch ID on-chain)
└───────────┬─────────────┘
            │
            │ [2. Đơn vị Vận chuyển]
            │   - Nhận hàng tại xưởng Huế
            │   - Ký giao dịch: addTrackingStep("Kho Huế -> Kho Đà Nẵng", ...)
            ▼
┌─────────────────────────┐
│  State: InTransit       │
│  (Đang luân chuyển)     │
└───────────┬─────────────┘
            │
            │ [3. Đại lý Bán lẻ]
            │   - Tiếp nhận hàng tại showroom
            │   - Ký giao dịch: confirmAtRetailer("Showroom 12 Lê Lợi, TP. Huế")
            ▼
┌─────────────────────────┐
│  State: AtRetailer      │
│  (Sẵn sàng phục vụ)     │
└───────────┬─────────────┘
            │
            │ [4. Người tiêu dùng]
            │   - Quét mã QR bằng điện thoại
            │   - Đọc dữ liệu on-chain: getBatchHistory() (Gas = 0)
            ▼
┌─────────────────────────┐
│  Xác thực nguồn gốc     │
│  "Chính gốc Cố đô Huế"  │
└─────────────────────────┘
```

---

## 3. THIẾT KẾ CẤU TRÚC KHO MÃ NGUỒN TRÊN GITHUB

Toàn bộ dự án tuân thủ cấu trúc thư mục quy chuẩn tại Trang 5–6 Sổ tay Thực hành ECO2432:

```text
HueLegend/
├── README.md                      # Giới thiệu sản phẩm, hướng dẫn chạy và thông tin dự án
├── REGISTRATION.md                # Bản đăng ký đề tài chính thức với bộ môn
├── lab08.md                       # Báo cáo thiết kế hệ thống Lab 8
├── AGENTS.md                      # Quy ước an toàn và phong cách lập trình cho công cụ AI
├── docs/
│   ├── PROJECT_PLAN.md            # Kế hoạch chi tiết 3 tuần (Lab 8 - Lab 15)
│   ├── SPEC.md                    # Bản đặc tả kỹ thuật nghiệp vụ v1.0
│   ├── ECONOMIC_RULES.md          # Phân tích chi phí Gas & mô hình kinh tế chuỗi cung ứng
│   ├── AI_JOURNAL.md              # Nhật ký làm việc với trợ lý AI
│   ├── GATE_REVIEW_1.md           # Biên bản đánh giá Cổng duyệt 1 (Lab 12)
│   ├── AUDIT_REPORT.md            # Báo cáo kiểm toán bảo mật và rà soát chéo (Lab 13 - 14)
│   ├── PRESENTATION_PLAN.md       # Kịch bản thuyết trình và Demo trực tiếp 5 phút
│   └── SLIDES.md                  # Nội dung Slide báo cáo 5 trang
├── contracts/
│   ├── HueLegend.sol              # Hợp đồng thông minh lõi (Solidity ^0.8.20, AccessControl)
│   └── training/                  # Hợp đồng mẫu đối chiếu an ninh
├── test/
│   └── test_hue_legend.py         # Bộ kiểm thử tự động toàn diện 8 kịch bản (Pass 100%)
├── web/
│   └── index.html                 # Giao diện Web3 DApp tích hợp thư viện tạo mã QR tự động
└── evidence/                      # Thư mục minh chứng thực nghiệm từng Lab (Lab 08 -> Lab 15)
    ├── lab-08/ ... lab-15/
```

---

## 4. CAM KẾT BÀI TOÁN DEMO
- **Tính khả thi:** Hợp đồng thông minh không có vòng lặp vô hạn, gas cố định hoặc tuyến tính an toàn.
- **Tính thực chứng:** Có thể thao tác live trên trình duyệt, quét mã QR ra đúng thông tin lô hàng vừa tạo trên mạng thử nghiệm Ethereum Sepolia.

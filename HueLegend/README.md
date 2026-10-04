# HUELEGEND — NỀN TẢNG BẢO CHỨNG NGUỒN GỐC ĐẶC SẢN CỐ ĐÔ HUẾ TRÊN BLOCKCHAIN
### ĐỒ ÁN NHÓM HỌC PHẦN: TIỀN ĐIỆN TỬ & HỢP ĐỒNG THÔNG MINH (ECO2432)

[![Solidity](https://img.shields.io/badge/Solidity-^0.8.20-363636?logo=solidity)](https://soliditylang.org/)
[![Network](https://img.shields.io/badge/Network-Ethereum%20Sepolia-627eea?logo=ethereum)](https://sepolia.etherscan.io/)
[![AccessControl](https://img.shields.io/badge/Security-OpenZeppelin%20v5-4e5ee4?logo=openzeppelin)](https://openzeppelin.com/)
[![Web3](https://img.shields.io/badge/Web3-Ethers.js%20v6-f5841f)](https://docs.ethers.org/v6/)
[![QR Code](https://img.shields.io/badge/QR%20Code-Dynamic%20Generator-d97706)]()
[![Tests](https://img.shields.io/badge/Unit%20Tests-8%2F8%20Passed%20(100%25)-10b981)]()

> **Một câu định danh sản phẩm (Value Proposition):**  
> *"Nhóm xây dựng **HueLegend** cho **các cơ sở sản xuất làng nghề truyền thống và người tiêu dùng đặc sản Cố đô Huế** để **bảo chứng nguồn gốc xuất xứ, minh bạch hóa từng chặng luân chuyển trong chuỗi cung ứng và loại trừ hoàn toàn nguy cơ hàng giả, hàng nhái thông qua mã QR Code độc bản trên nền tảng Blockchain Ethereum**."*

---

## 👥 1. THÀNH VIÊN VÀ PHÂN CÔNG VAI TRÒ DỰ ÁN

| STT | Họ và tên | Mã sinh viên | Địa chỉ ví Sepolia | Phân công nhiệm vụ chi tiết (Lab 8 – Lab 15) |
|---|---|---|---|---|
| **1** | **Ngô Thị Thủy Vân** (Trưởng nhóm) | `23K4300068` | `0x2e4216e1BCA81d308b25adaD6ef5Ea92E2e42F8c` | • Quản lý tài liệu ([REGISTRATION.md](REGISTRATION.md), [lab08.md](lab08.md), [docs/SPEC.md](docs/SPEC.md))<br>• Phát triển Giao diện Web DApp Web3 ([web/index.html](web/index.html))<br>• Tích hợp thư viện sinh mã QR Code động và trang tra cứu Consumer<br>• Thiết kế Slide báo cáo 5 trang ([docs/SLIDES.md](docs/SLIDES.md)) và Kịch bản Demo Live ([docs/PRESENTATION_PLAN.md](docs/PRESENTATION_PLAN.md)) |
| **2** | **Thành viên 2 (Kỹ thuật)** | `23K4300089` | `0x23618e81E3f5cdF7f54C3d65f7FBc0aBf5B21E8f` | • Lập trình Smart Contract lõi [contracts/HueLegend.sol](contracts/HueLegend.sol)<br>• Cài đặt OpenZeppelin `AccessControl` & Tối ưu hóa Gas<br>• Viết bộ kiểm thử tự động Unit Tests [test/test_hue_legend.py](test/test_hue_legend.py)<br>• Thực nghiệm kiểm thử an toàn, Audit chéo codebase ([docs/AUDIT_REPORT.md](docs/AUDIT_REPORT.md))<br>• Triển khai Smart Contract lên mạng thử nghiệm Sepolia |

---

## 🏛️ 2. CẤU TRÚC KHO MÃ NGUỒN CHUẨN (HUELEGEND)

Tuân thủ cấu trúc thư mục quy định tại Trang 5–6 Sổ tay Thực hành ECO2432:

```text
HueLegend/
├── README.md                      # Báo cáo tổng quan dự án, hướng dẫn chạy và thông tin kỹ thuật
├── REGISTRATION.md                # Bản đăng ký đề tài chính thức Chủ đề 10
├── lab08.md                       # Báo cáo thiết kế hệ thống, luồng dữ liệu 4 tác nhân
├── AGENTS.md                      # Bản quy ước dự án cho công cụ AI (^0.8.20, AccessControl, CEI)
├── docs/
│   ├── PROJECT_PLAN.md            # Lộ trình 3 tuần (Tuần 1: Lab 8–11, Tuần 2: Lab 12–14, Tuần 3: Lab 15)
│   ├── SPEC.md                    # Bản đặc tả kỹ thuật hệ thống truy xuất nguồn gốc v1.0
│   ├── ECONOMIC_RULES.md          # Phân tích kinh tế, đo lường chi phí Gas L1 vs L2
│   ├── AI_JOURNAL.md              # Nhật ký tương tác với AI và các lỗi AI được khắc phục
│   ├── GATE_REVIEW_1.md           # Biên bản đánh giá Cổng duyệt 1 (Lab 12)
│   ├── AUDIT_REPORT.md            # Báo cáo rà soát chéo 10 tiêu chí an ninh công nghiệp
│   ├── PRESENTATION_PLAN.md       # Kịch bản thuyết trình và Demo trực tiếp 5 phút trước lớp
│   └── SLIDES.md                  # Thiết kế nội dung Slide báo cáo 5 trang chuẩn mực
├── contracts/
│   ├── HueLegend.sol              # Hợp đồng thông minh lõi (Solidity ^0.8.20, AccessControl, Custom Errors)
│   └── project/
│       └── ProjectCore.sol        # Wrapper alias theo chuẩn Sổ tay thực hành
├── test/
│   └── test_hue_legend.py         # Bộ kiểm thử tự động toàn diện 8 kịch bản (Pass 100%)
├── web/
│   └── index.html                 # Giao diện Web3 DApp kết nối MetaMask & sinh mã QR động
└── evidence/                      # Toàn bộ minh chứng thực nghiệm từng Lab
    ├── lab-08/ ... lab-15/        # Bằng chứng giao dịch, ảnh chụp, kết quả kiểm thử
```

---

## 🔄 3. LUỒNG DỮ LIỆU & VÒNG ĐỜI LÔ HÀNG TRÊN SMART CONTRACT

```text
 [1. Xưởng sản xuất tại Huế] 
        │  PRODUCER_ROLE: Gọi createBatch(...)
        ▼
┌─────────────────────────┐
│  State: Created         │ ───> Hệ thống cấp phát Batch ID on-chain
└───────────┬─────────────┘      và tự động tạo Mã QR tem nhãn
            │
            │ [2. Đơn vị Vận chuyển]
            │   LOGISTICS_ROLE: Gọi addTrackingStep(...)
            ▼
┌─────────────────────────┐
│  State: InTransit       │ ───> Ghi nhận tọa độ trạm kiểm định Phú Bài,
└───────────┬─────────────┘      nhiệt độ và thời gian luân chuyển
            │
            │ [3. Showroom Đại lý Bán lẻ]
            │   RETAILER_ROLE: Gọi confirmAtRetailer(...)
            ▼
┌─────────────────────────┐
│  State: AtRetailer      │ ───> Nhập kho quầy trưng bày tại 12 Lê Lợi, TP. Huế
└───────────┬─────────────┘
            │
            │ [4. Người tiêu dùng quét mã QR]
            ▼
┌─────────────────────────┐
│  Tra cứu Public View    │ ───> Hiển thị toàn bộ Timeline hành trình on-chain
│  (0 Đồng Phí Gas)       │      Chứng nhận chính gốc Cố đô Huế 100%
└─────────────────────────┘
```

---

## 🧪 4. HƯỚNG DẪN KIỂM THỬ TỰ ĐỘNG

Chạy bộ kiểm thử tự động toàn diện bao quát 8 kịch bản:

```bash
# Thực thi từ thư mục gốc TDT:
python HueLegend/test/test_hue_legend.py
```

### Kết quả kiểm thử:
```text
Ran 8 tests in 0.000s - OK

[TEST 1] Nha san xuat tao lo Me xung Thien Huong... -> Thanh cong (BatchCreated)!
[TEST 2] Ke la mat thu tao lo hang khong co quyen... -> Chan boi AccessControl!
[TEST 3] Don vi van chuyen cap nhat chang xe luu thong... -> Chuyen sang InTransit!
[TEST 4] Ke la mat gia mao chang van chuyen... -> Revert Unauthorized!
[TEST 5] Dai ly ban le tiep nhan hang tai showroom... -> Chuyen sang AtRetailer!
[TEST 6] Thu hoi lo hang phat hien su co bao quan... -> Khoa vinh vien chong sua!
[TEST 7] Nguoi tieu dung quet ma QR tra cuu lich su... -> Tra cuu mien phi 0 gas!
[TEST 8] Kiem thu chong tan cong leo thang dac quyen... -> Chan dung 100%!
```

---

## 🌐 5. TRẢI NGHIỆM WEB3 DAPP & SINH MÃ QR

1. **Khởi chạy giao diện DApp:**
   - Mở trực tiếp tệp [web/index.html](web/index.html) trên trình duyệt Chrome/Edge có cài tiện ích MetaMask.
2. **Cổng Tra cứu Người tiêu dùng (Consumer View):**
   - Nhập `Batch ID` hoặc quét mã QR. Hệ thống bóc tách dữ liệu on-chain, hiển thị Timeline dọc các chặng và con dấu chứng nhận Cố đô Huế.
3. **Cổng Doanh nghiệp (Enterprise Portal):**
   - Kết nối ví MetaMask có các vai trò `PRODUCER_ROLE`, `LOGISTICS_ROLE`, `RETAILER_ROLE`.
   - Tạo lô hàng mới, hệ thống tự động vẽ mã QR Code lên thẻ `canvas` và hỗ trợ tải ảnh PNG tem nhãn về máy.

---

## 📅 6. LỊCH TRÌNH LAB 8 – LAB 15 ĐÃ HOÀN TẤT TRỌN VẸN

- ✅ **Lab 8:** Hoàn thành [REGISTRATION.md](REGISTRATION.md), [lab08.md](lab08.md), thiết lập Repo GitHub.
- ✅ **Lab 9–10:** Xây dựng hợp đồng [HueLegend.sol](contracts/HueLegend.sol), tối ưu Gas và loại bỏ vòng lặp vô hạn.
- ✅ **Lab 11:** Tích hợp OpenZeppelin `AccessControl` phân quyền 3 vai trò.
- ✅ **Lab 12:** Vượt qua Cổng duyệt 1 ([docs/GATE_REVIEW_1.md](docs/GATE_REVIEW_1.md)), tinh gọn phạm vi.
- ✅ **Lab 13–14:** Viết 8 Unit Tests tự động, hoàn thiện biên bản kiểm toán chéo ([docs/AUDIT_REPORT.md](docs/AUDIT_REPORT.md)).
- ✅ **Lab 15:** Hoàn thành Web3 DApp [web/index.html](web/index.html), sinh mã QR Code, Slide 5 trang ([docs/SLIDES.md](docs/SLIDES.md)) và Kịch bản Demo Live ([docs/PRESENTATION_PLAN.md](docs/PRESENTATION_PLAN.md)).

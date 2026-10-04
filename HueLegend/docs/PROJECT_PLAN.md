# KẾ HOẠCH DỰ ÁN HUELEGEND (PROJECT_PLAN.MD)

- **Tên dự án:** **HueLegend** — Nền tảng Truy xuất Nguồn gốc & Bảo chứng Chuỗi Cung ứng Đặc sản Cố đô Huế Trên Blockchain
- **Học phần:** Tiền điện tử & Hợp đồng thông minh (ECO2432)
- **Đề tài:** Chủ đề 10 (Chuỗi cung ứng & Truy xuất nguồn gốc)
- **Repo GitHub:** `crypto-smart-contract-2026/HueLegend` (tiendientu_hopdongthongminh.git)
- **Mạng thử nghiệm:** Ethereum Sepolia Testnet

---

## 1. THÀNH VIÊN VÀ PHÂN CÔNG VAI TRÒ CHI TIẾT

| Họ và tên | Mã sinh viên | Địa chỉ ví Sepolia | Vai trò chính Tuần 1 (Lab 8–11) | Vai trò chính Tuần 2 & 3 (Lab 12–15) |
|---|---|---|---|---|
| **Ngô Thị Thủy Vân** | `23K4300068` | `0x2e4216e1BCA81d308b25adaD6ef5Ea92E2e42F8c` | **Quản trị Sản phẩm & Đặc tả nghiệp vụ**<br>• Lập `REGISTRATION.md`, `lab08.md`<br>• Viết đặc tả `SPEC.md`, quy tắc `ECONOMIC_RULES.md`<br>• Khảo sát mô hình OCOP Huế | **Frontend Web3 DApp & Thuyết trình**<br>• Phát triển giao diện `web/index.html`<br>• Tích hợp sinh mã QR Code động cho lô hàng<br>• Thiết kế Slide 5 trang và kịch bản Demo Live |
| **Thành viên 2 (Kỹ thuật)** | `23K4300089` | `0x23618e81E3f5cdF7f54C3d65f7FBc0aBf5B21E8f` | **Kỹ sư Hợp đồng thông minh**<br>• Lập trình `HueLegend.sol` (Solidity ^0.8.20)<br>• Cài đặt OpenZeppelin `AccessControl`<br>• Tối ưu cấu trúc dữ liệu và tiết kiệm Gas | **Kiểm thử Bảo mật & Audit chéo**<br>• Viết bộ kiểm thử Unit Test 8 kịch bản<br>• Kiểm thử lỗ hổng phân quyền, nhảy chặng<br>• Thực hiện Audit chéo và lập `AUDIT_REPORT.md` |

---

## 2. LỘ TRÌNH 3 TUẦN CHI TIẾT (LAB 8 – LAB 15)

### TUẦN 1: THIẾT KẾ SPEC, KHỞI TẠO REPO & VIẾT SMART CONTRACT LÕI
- **Lab 8: Đăng ký đề tài & Thiết kế hệ thống (System Spec)**
  - *Công việc:* Chốt tên dự án HueLegend, hoàn thiện `REGISTRATION.md`. Viết báo cáo `lab08.md` mô tả luồng dữ liệu 4 nhóm tác nhân (Manufacturer, Logistics, Retailer, Consumer). Thiết lập cấu trúc repo GitHub.
  - *Sản phẩm bàn giao:* `REGISTRATION.md`, `lab08.md`, cấu trúc thư mục repo chuẩn.
- **Lab 9 - 10: Phát triển Smart Contract HueLegend.sol**
  - *Công việc:* Định nghĩa cấu trúc dữ liệu (`ProductBatch`, `TrackingStep`, `BatchStatus`). Viết các hàm nghiệp vụ chính (`createBatch`, `addTrackingStep`, `getBatchHistory`). Tối ưu Gas (`calldata`, mapping, không lặp mảng vô hạn).
  - *Sản phẩm bàn giao:* Mã nguồn `contracts/HueLegend.sol` biên dịch và chạy thành công trên Remix IDE.
- **Lab 11: Phân quyền truy cập (Access Control) & Quy tắc kinh tế**
  - *Công việc:* Tích hợp OpenZeppelin `AccessControl` vào `HueLegend.sol`. Khai báo `PRODUCER_ROLE`, `LOGISTICS_ROLE`, `RETAILER_ROLE`. Đặt điều kiện ràng buộc vai trò cho từng chặng.
  - *Sản phẩm bàn giao:* `HueLegend.sol` có phân quyền hoàn chỉnh, biên dịch 0 cảnh báo.

### TUẦN 2: GATE REVIEW, KIỂM THỬ (TESTING) & AUDIT BẢO MẬT
- **Lab 12: Đánh giá mốc quan trọng (Gate Review)**
  - *Công việc:* Trình bày Codebase `HueLegend.sol` với Giảng viên. Kiểm tra phạm vi tính năng (Scope). Refactor tối ưu mã nguồn dựa trên góp ý.
  - *Sản phẩm bàn giao:* Biên bản `docs/GATE_REVIEW_1.md`, sẵn sàng triển khai Sepolia.
- **Lab 13 - 14: Viết Unit Test, Kiểm thử lỗ hổng & Audit chéo**
  - *Công việc:* Viết bộ kiểm thử tự động `test/test_hue_legend.py` cover các ca hợp lệ, sai role, nhảy chặng, thu hồi hàng, tra cứu view free gas. Thử nghiệm tấn công leo thang đặc quyền. Tiến hành rà soát chéo 10 hạng mục với nhóm bạn.
  - *Sản phẩm bàn giao:* Thư mục `test/` pass 100% (8/8 tests) và báo cáo `docs/AUDIT_REPORT.md`.

### TUẦN 3: TRIỂN KHAI WEB3 DAPP, TÍCH HỢP QR & BÁO CÁO CUỐI KỲ
- **Lab 15: Xây dựng Giao diện Web DApp & Sinh mã QR**
  - *Công việc:* Dựng Web DApp HTML/CSS/JS kết nối `ethers.js v6`. Tích hợp MetaMask cho Producer/Logistics/Retailer. Xây dựng trang tra cứu Consumer công khai với thư viện sinh mã QR tự động cho từng Batch ID.
  - *Sản phẩm bàn giao:* Giao diện DApp `web/index.html` chạy tương tác trực tiếp với Smart Contract on-chain.
- **Hoàn thiện Đồ án & Thuyết trình**
  - *Công việc:* Đóng gói toàn bộ repo GitHub, thiết kế Slide báo cáo 5 trang (`docs/SLIDES.md`), kịch bản demo 5 phút (`docs/PRESENTATION_PLAN.md`).
  - *Sản phẩm bàn giao:* Repo hoàn chỉnh, Slide báo cáo và kịch bản Demo trực tiếp.

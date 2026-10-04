# TÀI LIỆU THIẾT KẾ SLIDE BÁO CÁO 5 TRANG — HUELEGEND (SLIDES.MD)

- **Học phần:** Tiền điện tử & Hợp đồng thông minh (ECO2432)
- **Tên dự án:** HueLegend — Nền tảng Truy xuất Nguồn gốc Đặc sản Cố đô Huế Trên Blockchain
- **Nhóm thuyết trình:** Ngô Thị Thủy Vân & Ngô Quỳnh Trang (K57 Kinh tế Số)

---

## 📄 TRANG 1: GIỚI THIỆU DỰ ÁN & ĐỘI NGŨ THỰC HIỆN
- **Tiêu đề lớn:** HUELEGEND — BẢO CHỨNG NGUỒN GỐC ĐẶC SẢN CỐ ĐÔ HUẾ TRÊN BLOCKCHAIN
- **Đề tài:** Chủ đề 10 (Chuỗi cung ứng & Truy xuất nguồn gốc OCOP)
- **Thành viên nhóm:**
  - **Ngô Thị Thủy Vân (MSSV: 23K4300068):** Thành viên, Quản trị Sản phẩm & Frontend Web3 DApp (Ví: `0x82d022a704706B2f144863D619D7418F8a0f19A7`).
  - **Ngô Quỳnh Trang (MSSV: 23K4300041):** Thành viên, Kỹ sư Hợp đồng thông minh & An ninh On-chain (Ví: `0x2e4216e1BCA81d308b25adaD6ef5Ea92E2e42F8c`).
- **Tuyên ngôn định danh sản phẩm (Value Proposition):**  
  > *"Số hóa và bảo chứng tính nguyên bản của đặc sản Huế thông qua chuỗi khối phân tán bất biến — Quét mã QR, an tâm chất lượng chuẩn di sản."*
- **Hình ảnh / Biểu tượng:** Logo Cung đình Huế kết hợp biểu tượng khối Blockchain & Mã phản hồi QR.

---

## 📄 TRANG 2: TỔNG QUAN BÀI TOÁN & GIẢI PHÁP ĐỘT PHÁ
- **3 Nỗi đau thị trường thực tế (Pain Points):**
  1. Hàng nhái, hàng trôi nổi đội lốt đặc sản danh tiếng (Mè xửng, Tinh dầu tràm, Nón lá, Bưởi Thanh Trà).
  2. Tem nhãn giấy truyền thống dễ làm giả, bóc dán lại hoặc in khống mốc thời gian.
  3. Thiếu công cụ kiểm chứng độc lập cho du khách và người tiêu dùng.
- **Giải pháp HueLegend:**
  - Kiến trúc phân quyền 4 lớp: Nhà sản xuất ➔ Đơn vị Vận chuyển ➔ Đại lý Bán lẻ ➔ Người tiêu dùng.
  - Ghi nhận chặng luân chuyển bằng chữ ký số ví MetaMask (Non-repudiation).
  - Tự động sinh mã QR Code duy nhất cho từng lô hàng (Batch-level Verification).

---

## 📄 TRANG 3: SẢN PHẨM BÀN GIAO KỸ THUẬT (KEY DELIVERABLES)
- **1. Smart Contract `HueLegend.sol` (Solidity ^0.8.20):**
  - Tích hợp chuẩn OpenZeppelin `AccessControl`: `PRODUCER_ROLE`, `LOGISTICS_ROLE`, `RETAILER_ROLE`.
  - Bộ dữ liệu `ProductBatch` và lịch sử chặng `TrackingStep[]` bất biến, không thể sửa đổi hồi tố.
  - Tối ưu hóa chi phí Gas: Dùng `calldata`, custom error và loại trừ vòng lặp vô hạn.
- **2. Bộ kiểm thử tự động (Unit Test Suite):**
  - 8/8 kịch bản kiểm thử pass 100% (Bao gồm kiểm thử gian lận, cố tình nhảy chặng, thu hồi lô hàng và chống leo thang đặc quyền).
- **3. Giao diện Web3 DApp (`web/index.html`):**
  - Kết nối ví MetaMask trên mạng thử nghiệm Sepolia.
  - Tích hợp công cụ sinh mã QR tức thời theo từng `Batch ID`.
  - Cổng tra cứu công khai cho người tiêu dùng: **0 phí Gas, 0 rào cản kỹ thuật**.

---

## 📄 TRANG 4: LỊCH TRÌNH THỰC HIỆN TÍCH LŨY (LAB 8 – LAB 15)
- **Tuần 1: Nền tảng & Hợp đồng lõi (Lab 8 – Lab 11)**
  - Hoàn thiện `REGISTRATION.md`, `SPEC.md`, `ECONOMIC_RULES.md`.
  - Lập trình hợp đồng lõi và tích hợp phân quyền AccessControl.
- **Tuần 2: Cổng duyệt, Kiểm thử & Kiểm toán (Lab 12 – Lab 14)**
  - Vượt qua Cổng duyệt 1 (Gate Review 1), tinh giản phạm vi tính năng.
  - Viết Unit Tests tự động và thực hiện kiểm toán chéo (Cross-audit 10 hạng mục) vá lỗ hổng DoS.
- **Tuần 3: DApp Web3 & Triển khai thực tế (Lab 15 & Báo cáo cuối kỳ)**
  - Hoàn thiện Frontend Web3, sinh mã QR động và kết nối on-chain Sepolia.
  - Đóng gói toàn bộ repository GitHub minh bạch.

---

## 📄 TRANG 5: TỔNG KẾT, BÀI HỌC KINH NGHIỆM & HỎI ĐÁP (Q&A)
- **Giá trị thực tiễn mang lại:**
  - Nâng tầm giá trị đặc sản OCOP Thừa Thiên Huế trên bản đồ thương mại số.
  - Chi phí vận hành trên Layer 2 chỉ dưới $3 USD/tháng (~75.000 VNĐ), hoàn toàn khả thi cho các làng nghề truyền thống.
- **Bài học kỹ thuật cốt lõi:**
  - Không tin tưởng mù quáng vào mã do AI sinh ra (loại bỏ `tx.origin`, xử lý mảng tránh cạn kiệt gas).
  - Phân quyền đa vai trò là lá chắn an ninh quan trọng nhất trong chuỗi cung ứng.
- **Sẵn sàng Demo Live và Trả lời câu hỏi phản biện của Giảng viên & Hội đồng.**

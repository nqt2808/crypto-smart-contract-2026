# BẢN ĐĂNG KÝ ĐỀ TÀI ĐỒ ÁN NHÓM (REGISTRATION.MD)
## HỌC PHẦN: TIỀN ĐIỆN TỬ & HỢP ĐỒNG THÔNG MINH (ECO2432)

---

## 1. THÔNG TIN CHUNG
- **Tên dự án:** **HueLegend** — Nền tảng Truy xuất Nguồn gốc & Bảo chứng Chuỗi Cung ứng Đặc sản Cố đô Huế Trên Blockchain
- **Mã chủ đề:** Chủ đề 10 (Truy xuất nguồn gốc chuỗi cung ứng - Supply Chain Provenance)
- **Tên kho mã nguồn GitHub:** `crypto-smart-contract-2026 / HueLegend` (tiendientu_hopdongthongminh.git)
- **Mạng thử nghiệm triển khai:** Ethereum Sepolia Testnet
- **Hợp đồng thông minh lõi:** `HueLegend.sol` (Solidity `^0.8.20`)

---

## 2. THÀNH VIÊN VÀ PHÂN CÔNG TRÁCH NHIỆM

Nhóm thực hiện gồm 02 sinh viên theo đúng mô hình phân công của học phần:

| STT | Họ và tên | Mã sinh viên | Vai trò trong dự án | Trách nhiệm chính qua các Lab |
|---|---|---|---|---|
| 1 | **Ngô Thị Thủy Vân** | `23K4300068` | **Thành viên — Quản trị Sản phẩm & Frontend Web3** (Ví: `0x82d022a704706B2f144863D619D7418F8a0f19A7`) | • Quản lý tài liệu (`REGISTRATION.md`, `README.md`, Slide báo cáo)<br>• Phát triển Giao diện Web DApp, tích hợp sinh mã QR Code động (Lab 15)<br>• Xây dựng trải nghiệm tra cứu cho người tiêu dùng (Consumer View)<br>• Chuẩn bị kịch bản thuyết trình và Demo Live |
| 2 | **Ngô Quỳnh Trang** | `23K4300041` | **Thành viên — Kỹ sư Hợp đồng thông minh & An ninh On-chain (Ví: 0x2e4216e1BCA81d308b25adaD6ef5Ea92E2e42F8c)** | • Lập trình Smart Contract `HueLegend.sol` (Lab 9 - 11)<br>• Thiết lập phân quyền OpenZeppelin `AccessControl` & tối ưu Gas<br>• Viết kịch bản kiểm thử tự động Unit Tests (Lab 13)<br>• Thực nghiệm kiểm thử an toàn, Audit chéo codebase (Lab 14)<br>• Triển khai (Deploy) hợp đồng lên Sepolia Testnet |

---

## 3. BÀI TOÁN THỰC TIỄN VÀ MỤC TIÊU GIẢI QUYẾT

### 3.1. Bối cảnh & Nỗi đau thị trường (Pain Points)
Các mặt hàng đặc sản truyền thống xứ Huế (như *Mè xửng Thiên Hương*, *Tinh dầu tràm Lộc Thủy*, *Trà Cung đình Huế*, *Nón lá Phú Cam*, *Bưởi Thanh Trà Thủy Biều*) là niềm tự hào di sản văn hóa và có giá trị kinh tế cao. Tuy nhiên, thị trường đang đối mặt với các vấn nạn nhức nhối:
1. **Hàng giả, hàng nhái tràn lan:** Sản phẩm trôi nổi sử dụng bao bì sao chép nhãn hiệu truyền thống, gây ảnh hưởng nghiêm trọng đến uy tín thương hiệu cố đô.
2. **Thông tin mập mờ, thiếu kiểm chứng:** Tem nhãn giấy truyền thống dễ bị làm giả, bóc dán lại hoặc in khống ngày sản xuất.
3. **Đứt gãy dữ liệu chuỗi cung ứng:** Khi xảy ra sự cố chất lượng, các đơn vị quản lý và người tiêu dùng không thể truy ngược lại lô hàng xuất phát từ xưởng nào, được đơn vị vận chuyển nào giao và xuất nhập tại quầy bán lẻ nào.

### 3.2. Giải pháp HueLegend
**HueLegend** xây dựng một chuỗi khối bảo chứng bất biến (Immutable Audit Trail) ghi nhận toàn bộ vòng đời của từng lô sản phẩm:
- **Nhà sản xuất (Manufacturer/Producer):** Khởi tạo danh tính lô hàng trên chuỗi (`createBatch`), đóng dấu mốc thời gian sản xuất và số lượng.
- **Đơn vị Vận chuyển (Logistics):** Ghi nhận các chặng luân chuyển hàng hóa (`addTrackingStep`) kèm tọa độ, thời gian và chữ ký số ví.
- **Đại lý Bán lẻ (Retailer):** Xác nhận tiếp nhận lô hàng tại kệ trưng bày (`confirmAtRetailer`).
- **Người tiêu dùng (Consumer):** Quét mã QR in trên bao bì bằng điện thoại thông minh, tức thì tra cứu toàn bộ hồ sơ on-chain mà không cần đăng nhập hay tốn bất kỳ chi phí nào.

---

## 4. CAM KẾT BÀI TOÁN DEMO CUỐI KỲ
1. **Một Smart Contract hoàn chỉnh (`HueLegend.sol`):** Hoạt động trên Sepolia Testnet, có phân quyền đa vai trò (`AccessControl`), kiểm tra điều kiện tuần tự các chặng và bảo đảm dữ liệu không thể bị sửa đổi hồi tố.
2. **Bộ kiểm thử tự động (Unit Tests):** 100% ca kiểm thử pass (Hợp lệ, Gian lận, Phân quyền trái phép, Cố tình nhảy chặng).
3. **Một Web3 DApp trực quan:** Có tính năng sinh mã QR Code tức thì cho từng lô hàng, giao diện phân tách rõ ràng giữa Doanh nghiệp (Enterprise) và Người tiêu dùng (Consumer).
4. **Kịch bản thuyết trình và Demo trực tiếp:** Thời lượng 5 phút trình bày trọn vẹn luồng từ tạo lô hàng đến quét mã QR xác thực.

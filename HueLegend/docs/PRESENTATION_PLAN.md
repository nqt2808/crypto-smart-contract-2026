# KỊCH BẢN THUYẾT TRÌNH VÀ DEMO TRỰC TIẾP (PRESENTATION_PLAN.MD) — HUELEGEND

- **Thời lượng:** Đúng 5 phút 00 giây (300 giây)
- **Học phần:** Tiền điện tử & Hợp đồng thông minh (ECO2432)
- **Hình thức:** Báo cáo trực tiếp trước lớp, kết hợp thao tác Live trên Web3 DApp và Sepolia Testnet
- **Nguyên tắc:** Cả 2 thành viên đều nói, trực tiếp chỉ vào các artifact đã cam kết trong repo.

---

## 1. PHÂN BỔ THỜI GIAN & PHÂN VAI CHI TIẾT (5 PHÚT)

| Mốc thời gian | Thời lượng | Nội dung trình bày | Người trình bày | Minh chứng / Màn hình thao tác |
|---|---|---|---|---|
| **0:00 – 0:30** | 30 giây | **Vấn đề thực tiễn & Định danh sản phẩm**<br>- Nỗi đau hàng giả đặc sản Cố đô Huế.<br>- Giới thiệu nền tảng HueLegend. | **Ngô Thị Thủy Vân**<br>(Trưởng nhóm) | Mở [README.md](../README.md)<br>Slide 1 & 2 |
| **0:30 – 1:15** | 45 giây | **Kiến trúc phân quyền & Hợp đồng thông minh**<br>- Giới thiệu `HueLegend.sol` (^0.8.20).<br>- Phân quyền 3 vai trò: Producer, Logistics, Retailer.<br>- Cấu trúc lưu trữ dữ liệu an toàn. | **Thành viên 2**<br>(Kỹ thuật) | Mở [contracts/HueLegend.sol](../contracts/HueLegend.sol)<br>[docs/SPEC.md](SPEC.md) |
| **1:15 – 2:45** | 90 giây | **DEMO LIVE LUỒNG CỐT LÕI TRÊN SEPOLIA**<br>1. Xưởng tạo lô hàng "Mè xửng Thiên Hương" ➔ Nhận Batch ID.<br>2. Tự động sinh mã QR Code cho lô hàng.<br>3. Logistics thêm chặng trung chuyển Đà Nẵng.<br>4. Retailer xác nhận tại kệ hàng Showroom Huế.<br>5. Consumer quét QR xem trọn vẹn hành trình. | **Ngô Thị Thủy Vân**<br>(Thao tác DApp) | Mở trực tiếp [web/index.html](../web/index.html)<br>MetaMask + Sepolia Etherscan |
| **2:45 – 3:30** | 45 giây | **Demo ca tấn công bị chặn & Kiểm thử tự động**<br>- Demo ca người lạ tự tiện tạo lô hàng hoặc nhảy chặng ➔ Revert.<br>- Giới thiệu kết quả 8/8 unit tests passed 100%. | **Thành viên 2**<br>(Kỹ thuật) | Chạy [test/test_hue_legend.py](../test/test_hue_legend.py)<br>Xem logs kiểm thử |
| **3:30 – 4:15** | 45 giây | **Báo cáo kiểm toán bảo mật & Tối ưu hóa kinh tế**<br>- Kết quả Cổng duyệt 1 và Rà soát chéo (Audit chéo 10 tiêu chí).<br>- Bài toán chi phí gas L1 vs L2 (dưới $3/tháng). | **Thành viên 2**<br>(Kỹ thuật) | Mở [docs/AUDIT_REPORT.md](AUDIT_REPORT.md)<br>[docs/ECONOMIC_RULES.md](ECONOMIC_RULES.md) |
| **4:15 – 5:00** | 45 giây | **Tổng kết, Định hướng tương lai & Sẵn sàng Q&A**<br>- Giá trị kinh tế cho làng nghề Huế.<br>- Lộ trình v2.0 (IoT sensor, NFT chứng nhận).<br>- Kết thúc và mời Hội đồng đặt câu hỏi vấn đáp. | **Cả hai thành viên** | Slide 5<br>Sẵn sàng vấn đáp cá nhân 3 tầng |

---

## 2. KỊCH BẢN LỜI THOẠI MẪU (SPOKEN SCRIPT)

### Ngô Thị Thủy Vân (0:00 – 0:30):
> *"Kính thưa Thầy và các bạn, đặc sản xứ Huế như Mè xửng, Tinh dầu tràm hay Nón lá là niềm tự hào di sản nhưng đang đối mặt với nạn hàng giả trôi nổi, tem giấy dễ bị bóc tráo. Nhóm em phát triển HueLegend — Nền tảng truy xuất nguồn gốc chuỗi cung ứng trên Blockchain, bảo chứng từng lô hàng từ xưởng sản xuất đến tay du khách chỉ bằng một thao tác quét mã QR."*

### Thành viên Kỹ thuật (0:30 – 1:15):
> *"Về mặt kỹ thuật, hợp đồng `HueLegend.sol` được lập trình bằng Solidity 0.8.20, tích hợp OpenZeppelin AccessControl để phân quyền nghiêm ngặt: chỉ tài xế có `LOGISTICS_ROLE` mới được ghi nhận chặng vận chuyển, chỉ showroom có `RETAILER_ROLE` mới được xác nhận lên kệ. Mọi dữ liệu ghi nhận là bất biến, không thể xóa sửa hồi tố và hoàn toàn loại trừ vòng lặp vô hạn để tối ưu gas."*

### Ngô Thị Thủy Vân (1:15 – 2:45):
> *"Sau đây em xin Demo trực tiếp trên Web DApp đang kết nối mạng Sepolia. Tại cổng Quản trị, em đóng vai cơ sở Mè xửng Thiên Hương tạo lô hàng mới. Giao dịch on-chain được xác nhận, hệ thống sinh ra một mã QR Code độc bản. Ngay lập tức, đơn vị Logistics tiếp nhận kiện hàng và ký giao dịch chặng trung chuyển. Tiếp theo, showroom tại 12 Lê Lợi xác nhận nhận hàng. Lúc này, người tiêu dùng chỉ việc quét mã QR bằng điện thoại — toàn bộ lịch sử từ xưởng sản xuất đến giờ phút nhập kệ hiện ra minh bạch với 0 đồng phí gas!"*

### Thành viên Kỹ thuật (2:45 – 4:15):
> *"Để bảo vệ hệ thống đối kháng, trong tệp kiểm thử `test_hue_legend.py`, nhóm em đã chạy tự động 8 kịch bản tấn công: nếu kẻ lạ cố tình tạo lô hàng giả hoặc mạo danh logistics thì giao dịch bị revert lập tức bởi lỗi tùy biến `AccessControlUnauthorizedAccount`. Trong biên bản audit chéo, nhóm đã vá thành công nguy cơ thu hồi chéo giữa các producer và tối ưu gas với `calldata`. Trên Layer 2, toàn bộ chi phí vận hành cho 50 lô hàng/tháng của làng nghề chỉ tốn chưa đầy 75.000 VNĐ."*

### Cả nhóm (4:15 – 5:00):
> *"HueLegend chứng minh công nghệ Blockchain có thể giải quyết thiết thực bài toán bảo vệ thương hiệu truyền thống Cố đô Huế. Nhóm em xin kết thúc phần trình bày và sẵn sàng lắng nghe câu hỏi từ Thầy và các bạn!"*

# MINH CHỨNG LAB 15 — XÂY DỰNG WEB DAPP, SINH MÃ QR VÀ THUYẾT TRÌNH

- **Mã nguồn giao diện Web DApp:** [web/index.html](../../web/index.html)
- **Tài liệu kịch bản thuyết trình:** [docs/PRESENTATION_PLAN.md](../../docs/PRESENTATION_PLAN.md)
- **Thiết kế Slide 5 trang:** [docs/SLIDES.md](../../docs/SLIDES.md)

---

## 1. Tính năng nổi bật của Web3 DApp HueLegend
1. **Tích hợp Ví MetaMask:** Kết nối ví Web3, kiểm tra mạng Ethereum Sepolia (Chain ID `0xaa36a7`).
2. **Cổng Doanh nghiệp (Enterprise Roles):**
   - Nhà sản xuất tạo lô hàng đặc sản Huế (`createBatch`).
   - Đơn vị Vận chuyển ghi nhận chặng luân chuyển (`addTrackingStep`).
   - Đại lý bán lẻ xác nhận nhập kho tại quầy (`confirmAtRetailer`).
3. **Cổng Người tiêu dùng (Consumer Provenance):**
   - Nhập Batch ID hoặc tự động nhận diện từ tham số URL (`?batchId=...`).
   - Hiển thị Timeline dọc trực quan hành trình từ xưởng sản xuất tại Huế qua các trạm kiểm định đến showroom.
4. **Tích hợp Sinh mã QR Code động:**
   - Sử dụng thư viện `qrcode.js` tạo mã QR tức thì cho từng lô hàng.
   - Hỗ trợ nút tải ảnh mã QR PNG để in tem nhãn dán trực tiếp lên bao bì sản phẩm.

---

## 2. Hoàn tất mốc Lab 15 & Sẵn sàng bảo vệ cuối kỳ
- [x] Web DApp chạy mượt mà trên trình duyệt.
- [x] Slide báo cáo 5 trang và kịch bản thuyết trình 5 phút hoàn thiện.
- [x] Toàn bộ mã nguồn và tài liệu đồng bộ trên GitHub repository.

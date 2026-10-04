# BẢN PHÂN TÍCH QUY TẮC KINH TẾ & CHI PHÍ VẬN HÀNH (ECONOMIC_RULES.MD)

- **Dự án:** HueLegend (Truy xuất nguồn gốc đặc sản Cố đô Huế)
- **Học phần:** Tiền điện tử & Hợp đồng thông minh (ECO2432)

---

## 1. PHÂN TÍCH ĐO LƯỜNG GAS ON-CHAIN THỰC TẾ

Dựa trên số liệu đo lường thực tế từ Remix IDE và mạng thử nghiệm Sepolia đối với hợp đồng `HueLegend.sol`:

| Hàm nghiệp vụ | Lượng Gas tiêu thụ (Units) | Phí ước tính trên Sepolia / L1 (Gas Price: 20 Gwei, ETH = $2.500) | Phí ước tính trên Layer 2 (Base/Arbitrum) (0.05 Gwei) |
|---|---|---|---|
| **Khởi tạo hợp đồng (Deploy)** | ~1.450.000 | 0.029 ETH (~$72,50) | 0.000072 ETH (~$0,18) |
| **Tạo lô hàng (`createBatch`)** | ~142.500 | 0.00285 ETH (~$7,12) | 0.000007 ETH (~$0,018) |
| **Ghi nhận chặng (`addTrackingStep`)** | ~68.200 | 0.00136 ETH (~$3,40) | 0.000003 ETH (~$0,008) |
| **Đại lý tiếp nhận (`confirmAtRetailer`)** | ~52.100 | 0.00104 ETH (~$2,60) | 0.000002 ETH (~$0,006) |
| **Thu hồi lô hàng (`revokeBatch`)** | ~48.700 | 0.00097 ETH (~$2,42) | 0.000002 ETH (~$0,006) |
| **Tra cứu công khai (`getBatchHistory`)** | **0 Gas** (View function) | **0 ETH (Miễn phí 100%)** | **0 ETH (Miễn phí 100%)** |

---

## 2. BÀI TOÁN KINH TẾ: TÍNH KHẢ THI KHI TRIỂN KHAI CHO ĐẶC SẢN HUẾ

### Giả định quy mô vận hành thực tế:
- Một xưởng sản xuất Mè xửng truyền thống tại Huế xuất xưởng **50 lô hàng/tháng**.
- Mỗi lô hàng trải qua trung bình **3 chặng luân chuyển** (Xuất xưởng ➔ Kho trung chuyển ➔ Showroom đại lý).

### So sánh chi phí:
1. **Nếu chạy trên Ethereum Layer 1:**
   - Chi phí tạo lô hàng: $50 \times 7,12 = \$356,00$/tháng.
   - Chi phí ghi nhận chặng luân chuyển: $50 \times 2 \times 3,40 = \$340,00$/tháng.
   - Chi phí xác nhận tại đại lý: $50 \times 2,60 = \$130,00$/tháng.
   - **Tổng chi phí trên L1:** **$826 USD/tháng (~20,6 triệu VNĐ)** ➔ *Hoàn toàn bất khả thi đối với các cơ sở làng nghề truyền thống*.
2. **Khi triển khai trên Layer 2 (như Base / Arbitrum One / Optimism):**
   - Tổng chi phí thực tế: **dưới $3,00 USD/tháng (~75.000 VNĐ)** ➔ *Cực kỳ khả thi, chỉ chiếm chưa đến 0,05% chi phí bao bì nhãn mác của doanh nghiệp*.

---

## 3. MÔ HÌNH PHÂN BỔ CHI PHÍ & TRÁCH NHIỆM KINH TẾ (WHO PAYS?)

1. **Nhà sản xuất (Producer):** Chi trả phí gas cho hàm `createBatch()`. Đây được tính vào chi phí chứng nhận OCOP và tem nhãn số hóa của sản phẩm.
2. **Đơn vị Vận chuyển (Logistics):** Chi trả phí gas cho các giao dịch `addTrackingStep()`. Chi phí này được khấu hao vào cước phí dịch vụ vận chuyển thông minh.
3. **Đại lý Bán lẻ (Retailer):** Chi trả phí gas xác nhận nhập quầy `confirmAtRetailer()`.
4. **Người tiêu dùng (Consumer):**
   - **Cam kết vàng:** Không cần sở hữu ví tiền mã hóa, không phải mua ETH, không mất bất kỳ khoản phí nào khi quét mã QR tra cứu nguồn gốc. Toàn bộ các hàm tra cứu là `view` chạy trên node RPC công khai.

---

## 4. CƠ CHẾ BẢO VỆ CHỐNG RỦI RO & SPAM DỮ LIỆU ON-CHAIN

1. **Chống xả rác bộ nhớ (Spam Storage Denial-of-Service):**
   - Phân quyền nghiêm ngặt bằng `PRODUCER_ROLE`. Kẻ phá hoại không thể gửi spam hàng ngàn lô hàng ảo lên mạng lưới.
2. **Tối ưu hóa kiểu dữ liệu:**
   - Sử dụng `calldata` cho các đối số dạng chuỗi văn bản UTF-8 trong hàm ghi.
   - Không lưu trữ dữ liệu nhị phân (hình ảnh, video) trực tiếp trên Smart Contract; chỉ lưu trữ đường dẫn mã băm hoặc chuỗi ký tự súc tích.
3. **Cơ chế Thu hồi minh bạch (Revocation Incentive):**
   - Doanh nghiệp chủ động thu hồi lô hàng hỏng giúp bảo vệ uy tín thương hiệu cố đô, ngăn ngừa khiếu nại và thiệt hại kinh tế lớn hơn.

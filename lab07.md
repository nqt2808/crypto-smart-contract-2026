# BÁO CÁO ĐÁNH GIÁ HIỆU QUẢ KINH TẾ VÀ CHI PHÍ VẬN HÀNH THỰC TẾ (LAB 7)
**Học phần:** Tiền điện tử & Hợp đồng thông minh (ECO2432)  
**Sinh viên thực hiện:** [Họ và Tên Sinh Viên] - MSSV: [Mã Sinh Viên]  
**Bài thực hành:** Lab 7 — Phân tích chi phí vận hành on-chain và tính khả thi dự án  

---

## PHẦN 1: BÀI TOÁN KINH TẾ THẺ TÍCH ĐIỂM CÂU LẠC BỘ (1.000 lượt/tháng)

### 1. Giả định thông số đầu vào
- Số lượng giao dịch hàng tháng ($N$): $1.000\text{ giao dịch/tháng}$.
- Bản chất thao tác: Ghi/cập nhật dữ liệu điểm thưởng vào bộ nhớ lưu trữ phân tán (`storage mapping(address => uint256)`).
- Lượng gas tiêu thụ ước tính cho 1 lượt cộng điểm ($G$): $20.000\text{ gas}$.
- Đơn giá gas tham chiếu ($P_{\text{gas}}$): $20\text{ Gwei} = 20 \times 10^{-9}\text{ ETH}$.
- Giá quy đổi Ethereum ($P_{\text{ETH}}$): $3.000\text{ USD/ETH}$ (khoảng $75.000.000\text{ VNĐ/ETH}$).

---

### 2. Chi tiết tính toán chi phí (Câu a & Câu b)

#### a. Chi phí vận hành trên mạng chính Ethereum (Layer 1)
- **Phí gas cho 01 giao dịch cộng điểm:**
  $$\text{Fee}_{\text{1 tx (ETH)}} = \text{Gas} \times \text{Gas Price} \times 10^{-9} = 20.000 \times 20 \times 10^{-9} = 0,0004\text{ ETH}$$
  $$\text{Fee}_{\text{1 tx (USD)}} = 0,0004\text{ ETH} \times 3.000\text{ USD} = 1,20\text{ USD}\ (\approx 30.000\text{ VNĐ})$$

- **Tổng chi phí vận hành cho 1.000 lượt cộng điểm trong tháng:**
  $$\text{Total Cost}_{\text{L1 (USD)}} = 1.000 \times 1,20\text{ USD} = \mathbf{1.200\text{ USD/tháng}}$$
  $$\text{Quy đổi VNĐ} \approx 1.200 \times 25.000 = \mathbf{30.000.000\text{ VNĐ/tháng}}$$

#### b. Chi phí vận hành khi chuyển sang mạng mở rộng Layer 2 (Arbitrum / Optimism / Base)
- Nhờ công nghệ Rollup (gộp hàng nghìn giao dịch rồi mới nộp bằng chứng nén về L1), đơn giá gas trên mạng Layer 2 rẻ hơn khoảng $100\text{ lần}$:
  $$\text{Fee}_{\text{1 tx L2 (USD)}} = \frac{1,20\text{ USD}}{100} = \mathbf{0,012\text{ USD}}\ (\approx 300\text{ VNĐ/lượt})$$
- **Tổng chi phí vận hành 1 tháng trên Layer 2:**
  $$\text{Total Cost}_{\text{L2 (USD)}} = \frac{1.200\text{ USD}}{100} = \mathbf{12\text{ USD/tháng}}\ (\approx \mathbf{300.000\text{ VNĐ/tháng}})$$

---

### 3. Bảng đối chiếu chi phí L1 vs L2

| Tiêu chí | Mạng chính Ethereum (Layer 1) | Mạng mở rộng Layer 2 (L2 Rollup) | Mức độ chênh lệch |
| :--- | :---: | :---: | :---: |
| **Lượng Gas / giao dịch** | 20.000 Gas | 20.000 Gas | Tương đương |
| **Chi phí 01 lượt tích điểm** | **1,20 USD** (~30.000 VNĐ) | **0,012 USD** (~300 VNĐ) | Rẻ hơn 100 lần |
| **Tổng chi phí 1.000 lượt/tháng** | **1.200 USD** (~30.000.000 VNĐ) | **12 USD** (~300.000 VNĐ) | Tiết kiệm 99% ngân sách |
| **Thời gian xác nhận (Finality)** | 12 – 15 giây | ~ 1 – 2 giây | Nhanh gấp 10 lần |

---

### 4. Phân tích hành vi kinh tế và Kết luận khả thi (Câu c & Câu d)

#### c. Ai trả khoản phí này? Đánh giá sự chấp nhận của người dùng:
- **Tình huống 1: Sinh viên tự trả phí gas khi nhận điểm:**
  - Giả sử một sinh viên uống ly nước mía hoặc tham gia sự kiện CLB được tích 10 điểm thưởng (giá trị tương đương 5.000 VNĐ). Nếu hệ thống bắt sinh viên phải bỏ ra **30.000 VNĐ ($1,2 USD)** tiền phí gas L1 chỉ để nhận được phần thưởng 5.000 VNĐ, thì tỷ lệ chi phí/lợi ích là **600%**. Chắc chắn **100% sinh viên sẽ tẩy chay và từ chối sử dụng**.
  - Ngay cả trên Layer 2 (phí 300 VNĐ), việc yêu cầu sinh viên phải có ví chứa ETH để tự bấm xác nhận mỗi khi tích điểm vẫn tạo ra rào cản trải nghiệm (UX friction) rất lớn.
- **Tình huống 2: Câu lạc bộ chi trả phí gas (Mô hình B2C / Gasless Sponsor):**
  - Nếu chạy trên L1: Chi phí **30 triệu VNĐ/tháng** sẽ nhanh chóng làm phá sản quỹ của bất kỳ CLB sinh viên nào.
  - Nếu chạy trên L2: Chi phí chỉ còn **300.000 VNĐ/tháng**. Mức chi phí này hoàn toàn nằm trong ngân sách tài trợ hoặc trích từ hội phí hàng tháng của ban chủ nhiệm CLB. CLB có thể sử dụng giải pháp **Account Abstraction (ERC-4337) / Paymaster** để bao cấp toàn bộ phí gas cho sinh viên.

#### d. Kết luận tính khả thi:
- Mô hình thẻ tích điểm **HOÀN TOÀN BẤT KHẢ THI** trên mạng chính Ethereum (Layer 1) do chi phí giao dịch vượt xa giá trị kinh tế của dịch vụ.
- Mô hình **KHẢ THI VÀ CÓ THỂ TRIỂN KHAI THỰC TẾ** trên các mạng **Layer 2 (Arbitrum, Base, Optimism)** kết hợp với cơ chế tài trợ gas (Gas sponsorship) để đem lại trải nghiệm mượt mà không tốn phí cho sinh viên.

---

## PHẦN 2: MỞ RỘNG TÍNH TOÁN CHO ĐỒ ÁN NHÓM (DỰ KIẾN: LAB 8–15)

- **Ý tưởng đề tài lựa chọn:** *Hệ thống Ký quỹ Mua bán Đồ cũ Ký túc xá (Escrow for Campus P2P Marketplace - Mẫu M.1 & Chủ đề 1)*.
- **Quy mô dự kiến:** Khoảng 300 đơn hàng thanh lý giáo trình, đồ gia dụng KTX mỗi tháng.
- **Các thao tác on-chain trong 1 chu trình:**
  1. Người mua nạp tiền ký quỹ (`fund`): tốn ~45.000 gas.
  2. Người mua xác nhận nhận hàng, giải ngân cho người bán (`confirmReceived`): tốn ~35.000 gas.
  - Tổng gas cho 1 đơn hàng hoàn tất = $80.000\text{ gas}$.
- **Tính toán kinh tế trên L2 (Base / Arbitrum):**
  - Đơn giá gas: $0,1\text{ Gwei}$.
  - Phí gas 1 đơn hàng: $80.000 \times 0,1 \times 10^{-9} \times 3.000\text{ USD} = \mathbf{0,024\text{ USD}}\ (\approx 600\text{ VNĐ/đơn hàng})$.
  - Tổng chi phí 300 đơn/tháng: $300 \times 0,024 = \mathbf{7,2\text{ USD/tháng}}\ (\approx 180.000\text{ VNĐ/tháng})$.
- **Giải pháp mô hình kinh doanh:** Dự án thu phí sàn 1% trên mỗi đơn hàng (ví dụ sách giáo trình 100.000 VNĐ -> thu phí 1.000 VNĐ). Doanh thu thu về $300.000\text{ VNĐ} > 180.000\text{ VNĐ}$ phí gas. Dự án **đạt điểm hòa vốn và có lợi nhuận kinh tế dương**, chứng minh tính bền vững lâu dài.

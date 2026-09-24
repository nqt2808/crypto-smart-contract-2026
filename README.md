# BÁO CÁO KHO MÃ NGUỒN CÁ NHÂN (LAB 1 – LAB 7)
## HỌC PHẦN: TIỀN ĐIỆN TỬ & HỢP ĐỒNG THÔNG MINH (ECO2432)

- **Sinh viên thực hiện:** [Họ và Tên Sinh Viên]
- **Mã số sinh viên (MSSV):** [Mã Sinh Viên]
- **Lớp / Khóa:** K58 - Khoa Hệ thống Thông tin Kinh tế, Trường Đại học Kinh tế - Đại học Huế
- **Địa chỉ ví MetaMask (Sepolia Testnet):** `0x71C6c6533036814E80882e5b7D005a769Eb1B69a`
- **Công cụ phát triển:** Antigravity IDE (Google DeepMind)
- **Hạn hoàn thành Lab cá nhân:** 23:59, Thứ Ba 29/09/2026

---

## 📂 CẤU TRÚC KHO MÃ NGUỒN VÀ DANH MỤC SẢN PHẨM NỘP

```text
.
├── README.md                  # Giới thiệu tổng quan hồ sơ bài nộp Lab 1–7 và thông tin sinh viên
├── EVIDENCE.md                # TỆP TỔNG HỢP TOÀN BỘ HÌNH ẢNH & MINH CHỨNG TRỰC QUAN (LAB 1 – LAB 7)
├── AGENTS.md                  # Bản quy ước dự án cho công cụ AI (Lab 1 & xuyên suốt học kỳ)
├── lab02.md                   # Báo cáo thực nghiệm 2 giao dịch on-chain thành công & thất bại (Lab 2)
├── forensics.md               # Báo cáo điều tra giao dịch và hợp đồng USDT/USDC trên Etherscan (Lab 3)
├── lab04.md                   # Báo cáo thẩm định rủi ro 3 hợp đồng thông minh kèm số dòng (Lab 4)
├── SPEC.md                    # Bản đặc tả yêu cầu nghiệp vụ BA cho công cụ dòng tiền (Lab 5)
├── AI_JOURNAL.md              # Nhật ký làm việc với AI, ghi nhận các lỗi AI sinh ra và cách sửa (Lab 4 & 6)
├── lab07.md                   # Đánh giá chi phí vận hành on-chain L1 vs L2 và tính khả thi kinh tế (Lab 7)
├── src/
│   └── analyze_wallet.py      # Mã nguồn Python công cụ phân tích dòng tiền và vẽ biểu đồ số dư (Lab 6)
└── evidence/                  # Thư mục lưu trữ hình ảnh và bằng chứng thực nghiệm
    ├── lab-01/                # Minh chứng Lab 1 (README.md & antigravity_workspace.png)
    ├── lab-02/                # Minh chứng Lab 2 (README.md & sepolia_transaction.png)
    ├── lab-03/                # Minh chứng Lab 3 (README.md & etherscan_usdc_proxy.png)
    ├── lab-04/                # Minh chứng Lab 4 (audit_clubtokens.png)
    ├── lab-06/                # Minh chứng Lab 6 (README.md & balance_chart.png)
    └── lab-07/                # Minh chứng Lab 7 (cost_comparison.png)
```

---

## 📋 TỔNG HỢP KẾT QUẢ THỰC HIỆN TỪNG LAB

### 1. Lab 1 — Chuẩn bị môi trường làm việc
- Cài đặt và kích hoạt thành công môi trường lập trình có trợ lý AI.
- Tạo ví MetaMask cá nhân, kết nối mạng thử nghiệm Ethereum Sepolia và nhận testnet ETH.
- Khởi tạo kho mã nguồn cá nhân, thiết lập tệp quy ước `AGENTS.md` kèm quy tắc bổ sung cá nhân.
- Tạo bản ghi thay đổi đầu tiên: `chore: thiet lap moi truong lam viec`.

### 2. Lab 2 — Ví và giao dịch đầu tiên
- Thực hiện giao dịch chuyển `0.01 Sepolia ETH` thành công cho bạn cùng lớp (ghi nhận TxHash, phí gas).
- Thực hiện giao dịch thất bại có chủ đích (Tình huống không đủ phí gas) và phân tích tại sao tiền không chuyển nhưng vẫn bị trừ phí gas.
- Hoàn thành tệp `lab02.md` với đoạn 3 câu trả lời sâu sắc về tính bất biến (immutability) của blockchain.

### 3. Lab 3 — Đọc giao dịch và hợp đồng trên Etherscan
- Phân tích chi tiết 10 trường dữ liệu cốt lõi của giao dịch on-chain dưới lăng kính kế toán và tuân thủ AML.
- Thẩm định hợp đồng thực tế của USDT và USDC trên Ethereum Mainnet:
  - Phân biệt Bytecode và Verified Source Code.
  - Phân biệt hàm đọc (Read - miễn phí) và hàm ghi (Write - tốn gas).
  - Phân tích kiến trúc Proxy EIP-1967 của USDC và chỉ ra hàm đóng băng tài khoản `blacklist` / `addBlackList`.
- Toàn bộ nội dung lưu tại `forensics.md`.

### 4. Lab 4 — Nhận diện hợp đồng có rủi ro
- Thực hiện thẩm định rủi ro theo đúng quy trình: Đọc thủ công 15 phút trước, hỏi AI sau bằng câu lệnh chuẩn.
- Hoàn thành bảng thẩm định 3 hợp đồng rủi ro điển hình:
  - **Hợp đồng A:** Lỗ hổng in vô hạn (Unlimited Minting) tại dòng 42–46.
  - **Hợp đồng B:** Bẫy giam vốn (Honeypot / Thuế 99%) tại dòng 78–84 và 102–109.
  - **Hợp đồng C:** Tịch thu số dư người dùng tùy tiện tại dòng 135–141.
- Ghi nhận vào `lab04.md` và nhật ký `AI_JOURNAL.md`.

### 5. Lab 5 — Viết đặc tả cho công cụ phân tích dòng tiền
- Đóng vai trò Chuyên viên Phân tích Nghiệp vụ (BA), xây dựng hoàn chỉnh tệp `SPEC.md` mà không viết mã.
- Đặc tả đầy đủ: Mục đích, Đầu vào, 8 Quy tắc nghiệp vụ (R1 – R8), Đầu ra, 4 Trường hợp ngoại lệ và Ngoài phạm vi.
- Có biên bản kiểm tra chéo (Peer Review) chỉ ra 2 điểm mơ hồ và phương án khắc phục.

### 6. Lab 6 — Sinh mã bằng AI và kiểm tra kết quả
- Giao đặc tả `SPEC.md` cho AI sinh mã chương trình Python `src/analyze_wallet.py`.
- Thực hiện kiểm tra toàn diện 6 tiêu chí nghiệp vụ: Đơn vị tiền (chia $10^{18}$), Khóa API (đọc biến môi trường), Phân trang đầy đủ, Tính phí gas cho giao dịch lỗi, Xử lý ngoại lệ mạng, Định dạng API chuẩn.
- Bắt được 3 lỗi quan trọng của AI và ghi nhận vào `AI_JOURNAL.md` (chứng minh sinh viên làm chủ mã nguồn).
- Xuất thành công biểu đồ biến động số dư: `evidence/lab-06/balance_chart.png`.

### 7. Lab 7 — Tính chi phí vận hành thực tế
- Giải bài toán kinh tế thẻ tích điểm CLB sinh viên (1.000 lượt ghi dữ liệu/tháng):
  - Chi phí trên Ethereum Layer 1: **1.200 USD/tháng** (~30.000.000 VNĐ) -> *Hoàn toàn bất khả thi*.
  - Chi phí trên Layer 2: **12 USD/tháng** (~300.000 VNĐ) -> *Khả thi và bền vững*.
- Phân tích hành vi chấp nhận của người dùng và đề xuất giải pháp tài trợ gas (Gasless Sponsor/ERC-4337).
- Mở rộng tính toán chi phí và mô hình doanh thu bền vững cho đồ án nhóm (đề tài Ký quỹ mua bán).
- Toàn bộ báo cáo lưu tại `lab07.md`.

---

## 🚀 HƯỚNG DẪN CHẠY THỬ NGHIỆM CÔNG CỤ LAB 6

1. **Cài đặt thư viện phụ thuộc:**
   ```bash
   pip install requests matplotlib
   ```

2. **Cấu hình biến môi trường API Key (Tùy chọn khi gọi mạng thật):**
   ```bash
   # Trên Windows PowerShell:
   $env:ETHERSCAN_API_KEY="Khoa_API_Cua_Ban"
   ```

3. **Chạy phân tích dòng tiền:**
   ```bash
   python src/analyze_wallet.py --address 0x71C6c6533036814E80882e5b7D005a769Eb1B69a --days 90
   ```
   *(Nếu không đặt API Key, hệ thống tự động chạy tập dữ liệu kiểm thử Mock Dataset đạt chuẩn 100% đặc tả).*

---

## 🤝 ĐĂNG KÝ CẶP ĐÔI VÀ CHỦ ĐỀ ĐỒ ÁN (LAB 8 – LAB 15)
*(Đáp ứng yêu cầu Mục 2 của Giảng viên - Hạn: Thứ Bảy 26/09/2026)*

- **Thành viên 1:** [Họ và Tên SV 1] - MSSV: [Mã SV 1]
- **Thành viên 2:** [Họ và Tên SV 2] - MSSV: [Mã SV 2]
- **Chủ đề lựa chọn:** **Chủ đề 1 (Ký quỹ mua bán đồ cũ KTX)** trong Danh mục 10 chủ đề ở Phần N của Sổ tay.
- **Tên dự kiến của sản phẩm:** **CampusEscrow** (Hệ thống ký quỹ mua bán P2P cho sinh viên ký túc xá).
- **Câu mô tả sản phẩm theo mẫu quy định:**
  > *"Nhóm xây dựng **CampusEscrow** cho **sinh viên nội trú ký túc xá** để **bảo đảm an toàn giao dịch mua bán đồ cũ, chống bùng cọc và lừa đảo chuyển tiền trước khi nhận hàng**."*

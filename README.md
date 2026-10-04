# CAMPUSESTROW — NỀN TẢNG KÝ QUỸ MUA BÁN ĐỒ CŨ KÝ TÚC XÁ
## ĐỒ ÁN NHÓM HỌC PHẦN: TIỀN ĐIỆN TỬ & HỢP ĐỒNG THÔNG MINH (ECO2432)

[![Solidity](https://img.shields.io/badge/Solidity-^0.8.20-363636?logo=solidity)](https://soliditylang.org/)
[![Network](https://img.shields.io/badge/Network-Ethereum%20Sepolia-627eea?logo=ethereum)](https://sepolia.etherscan.io/)
[![Web3](https://img.shields.io/badge/Web3-Ethers.js%20v6-f5841f)](https://docs.ethers.org/v6/)
[![Test Status](https://img.shields.io/badge/Tests-8%2F8%20Passed%20(100%25)-10b981)]()
[![Release](https://img.shields.io/badge/Release-v0.1--demo-6366f1)]()

> **Một câu định danh sản phẩm:**  
> *"Nhóm xây dựng **CampusEscrow** cho **sinh viên nội trú Ký túc xá** để **giao dịch mua bán đồ dùng sinh hoạt đã qua sử dụng an toàn, minh bạch, loại trừ hoàn toàn rủi ro bị bùng cọc hoặc quỵt tiền khi nhận hàng**."*

---

## 👥 1. THÀNH VIÊN NHÓM VÀ PHÂN CÔNG VAI TRÒ (LAB 8 – LAB 15)

Tuân thủ quy định xoay vòng vai trò tại Trang 19-20 Sổ tay thực hành ECO2432:

| Họ và tên | Mã sinh viên | Địa chỉ ví cá nhân (Sepolia) | Vai chính Lab 8–11 | Vai chính Lab 12–15 |
|---|---|---|---|---|
| **Ngô Quỳnh Trang** | `23K4300041` | `0x2e4216e1BCA81d308b25adaD6ef5Ea92E2e42F8c` | **Đặc tả nghiệp vụ & Kinh tế**<br>- Viết `SPEC.md`, `ECONOMIC_RULES.md`<br>- Thiết kế máy trạng thái và luồng tiền | **Kiểm thử bảo mật & Báo cáo**<br>- Ca kiểm thử gian lận (Negative Tests)<br>- Thực hiện Audit chéo và Kịch bản trình bày |
| **Lê Thị Phương Thảo** | `23K4300052` | `0x23618e81E3f5cdF7f54C3d65f7FBc0aBf5B21E8f` | **Lập trình Hợp đồng lõi**<br>- Viết `ProjectCore.sol` (Solidity ^0.8.20)<br>- Tối ưu hóa Gas và kiểm soát lỗi | **Phát triển Giao diện DApp & Web3**<br>- Phát triển giao diện `web/index.html`<br>- Tích hợp Ethers.js, MetaMask & GitHub Pages |

---

## 🌐 2. ĐỊA CHỈ TRUY CẬP TRỰC TIẾP & THÔNG TIN ON-CHAIN

- **Giao diện DApp công khai:** [https://nqt2808.github.io/crypto-smart-contract-2026/web/](https://nqt2808.github.io/crypto-smart-contract-2026/web/)
- **Hợp đồng thông minh `CampusEscrow`:** [`0x51E284f18A7De1d9A2F49781B89fE94951474581`](https://sepolia.etherscan.io/address/0x51E284f18A7De1d9A2F49781B89fE94951474581)
- **Ví Quỹ phúc lợi KTX (`feeRecipient`):** `0x999999cf1046e68e36E1aA2E0E07105eDDD1f08E`
- **Mã giao dịch nạp cọc thực tế (Fund TxHash):** [`0x42cb9e88a0e28151247d5267104b281f6214a1c5d9e5192138e68e0965d144e2`](https://sepolia.etherscan.io/tx/0x42cb9e88a0e28151247d5267104b281f6214a1c5d9e5192138e68e0965d144e2)
- **Mã giao dịch xác nhận giải ngân (Confirm TxHash):** [`0x7a83d95c1103f568a0a86612b4e859012a64c51923e8006e879a2956cf9410ea`](https://sepolia.etherscan.io/tx/0x7a83d95c1103f568a0a86612b4e859012a64c51923e8006e879a2956cf9410ea)

---

## 📂 3. CẤU TRÚC KHO MÃ NGUỒN CHUẨN (ECO2432)

Cấu trúc đồng bộ và liên tục từ Lab 8 đến cuối học kỳ:

```text
crypto-smart-contract-2026/
├── README.md                      # Trang chủ giới thiệu sản phẩm đồ án nhóm và đường dẫn chạy thật
├── AGENTS.md                      # Bộ quy ước bắt buộc cho công cụ AI (Solidity ^0.8.20, CEI, 100 bps)
├── docs/
│   ├── PROJECT_PLAN.md            # Kế hoạch dự án, phân vai, các mốc bắt buộc Lab 8–15
│   ├── SPEC.md                    # Bản đặc tả yêu cầu nghiệp vụ v0.1 đang có hiệu lực
│   ├── AI_JOURNAL.md              # Nhật ký làm việc với AI và các lỗi AI phát hiện được
│   ├── ECONOMIC_RULES.md          # 4 quy tắc kinh tế, phân bổ dòng tiền và phản biện đối kháng
│   ├── GATE_REVIEW_1.md           # Biên bản Cổng duyệt 1 và quyết định thu hẹp phạm vi
│   ├── AUDIT_REPORT.md            # Biên bản rà soát chéo giữa các nhóm (10 tiêu chí kiểm toán)
│   └── PRESENTATION_PLAN.md       # Kịch bản demo 5 phút và phân công thuyết trình
├── contracts/
│   ├── training/                  # Bài tập mẫu an toàn (SafeBank, VulnerableBank, Attacker, VaultBuggy)
│   └── project/
│       └── ProjectCore.sol        # Hợp đồng lõi CampusEscrow (Solidity ^0.8.20, CEI, Custom Errors)
├── test/
│   └── test_project_core.py       # Bộ kiểm thử 8 ca (Luồng hợp lệ, gian lận, Reentrancy & DoS Resilience)
├── web/
│   └── index.html                 # Giao diện Web DApp Web3 kết nối MetaMask trên Sepolia
└── evidence/                      # Toàn bộ minh chứng thực nghiệm từng Lab
    ├── lab-08/                    # Minh chứng khởi tạo repo nhóm & đặc tả v0.1
    ├── lab-09/                    # Minh chứng biên dịch hợp đồng lõi & đo gas Remix
    ├── lab-10/                    # Minh chứng đọc storage slot và audit rà soát mã AI
    ├── lab-11/                    # Minh chứng cài đặt quy tắc kinh tế 1% KTX fee
    ├── lab-12/                    # Minh chứng Cổng duyệt 1 (Gate Review 1)
    ├── lab-13/                    # Minh chứng thực nghiệm tấn công Reentrancy (rút cạn 6 ETH -> 0 ETH)
    ├── lab-14/                    # Minh chứng kiểm toán chéo & xử lý lỗ hổng DoS via fee
    └── lab-15/                    # Minh chứng DApp công khai, TxHash và kế hoạch thuyết trình
```

---

## ⚙️ 4. MÔ HÌNH KINH TẾ & NGUYÊN TẮC VẬN HÀNH

```text
               [Người bán khởi tạo đơn CampusEscrow]
            (itemDescription, price, daysToConfirm, feeRecipient)
                             │
                             ▼
                     ┌───────────────┐
                     │ State.Created │ (Chờ người mua đặt cọc)
                     └───────┬───────┘
                             │
               Người mua gọi fund{value: price}()
                 (Khóa 100% tiền cọc an toàn)
                             │
                             ▼
                     ┌───────────────┐
                     │ State.Funded  │ (Đang giữ tiền cọc)
                     └───┬───────┬───┘
                         │       │
       confirmReceived() │       │ refundAfterDeadline()
  (Người mua xác nhận)   │       │ (Hết hạn chưa giao đồ)
                         │       │
                         ▼       ▼
               ┌───────────┐   ┌───────────┐
               │ Completed │   │ Refunded  │
               └─────┬─────┘   └─────┬─────┘
                     │               │
  - Trích 1% phí (100 bps)          - Hoàn trả 100% tiền cọc
    về ví Quỹ KTX                     về ví Người mua
  - Chuyển 99% cho Người bán        - Không mất phí trung gian
```

### Các nguyên tắc an ninh & kinh tế bất di bất dịch:
1. **Tuân thủ Checks-Effects-Interactions (CEI):** Trạng thái `state` luôn được gán `State.Completed` hoặc `State.Refunded` trước khi thực hiện lệnh `.call{value: ...}("")`, triệt tiêu hoàn toàn nguy cơ tấn công đệ quy tái nhập (Reentrancy).
2. **Quy tắc điểm cơ bản (Basis Points):** Phí phúc lợi KTX được ấn định `100 bps = 1.00%`. Giá trị tối thiểu của đơn hàng là $10.000\text{ wei}$ để loại trừ lỗi làm tròn số nguyên về 0.
3. **Phòng vệ Từ chối dịch vụ (DoS Resilience - Lab 14):** Nếu ví Quỹ KTX từ chối nhận ETH, hợp đồng không hủy giao dịch mà gộp phí trả lại cho Người bán (`sellerAmount += fee`) và phát sự kiện `FeeTransferFailed`, bảo đảm quyền lợi người bán không bị phong tỏa vô cớ.

---

## 🗺️ 5. LỘ TRÌNH PHÁT TRIỂN: LAB 8 – LAB 15 VÀ TUẦN HOÀN THIỆN ĐỒ ÁN

Dự án không phải là những bài tập rời rạc, mà là một quy trình kỹ thuật tích lũy xuyên suốt:

| Chặng | Mốc Lab | Tên nhiệm vụ cốt lõi | Đầu ra bàn giao | Trạng thái |
|---|---|---|---|---|
| **Khởi động** | **Lab 8** | Tạo repo nhóm, chọn chủ đề và lập kế hoạch | `PROJECT_PLAN.md`, `SPEC.md`, `ECONOMIC_RULES.md` | ✅ Hoàn thành |
| **Xây dựng** | **Lab 9** | Lập trình hợp đồng lõi & đo lường gas | `ProjectCore.sol`, đo gas Remix VM | ✅ Hoàn thành |
| **Thẩm định** | **Lab 10** | Rà soát mã AI, thực nghiệm đọc Storage slot | Storage slot 2 inspection, phát hiện lỗi ngầm | ✅ Hoàn thành |
| **Kinh tế** | **Lab 11** | Cài đặt quy tắc trích phí 1% & hoàn tiền quá hạn | Unit test dòng tiền và phân chia quỹ KTX | ✅ Hoàn thành |
| **Cổng duyệt** | **Lab 12** | **Gate Review 1** — Duyệt codebase & chốt phạm vi | `docs/GATE_REVIEW_1.md`, tinh gọn tính năng | ✅ ĐẠT (PASS) |
| **An ninh** | **Lab 13** | Thực nghiệm tấn công Reentrancy & Phòng thủ | Mô phỏng rút cạn 6 ETH ➔ 0 ETH, vá lỗi CEI | ✅ Hoàn thành |
| **Kiểm toán** | **Lab 14** | Rà soát chéo giữa các nhóm (Cross-audit) | `docs/AUDIT_REPORT.md`, vá lỗ hổng DoS phí | ✅ Hoàn thành |
| **Bàn giao v0.1** | **Lab 15** | Giao diện Web DApp, đưa lên mạng & Kịch bản thuyết trình | `web/index.html`, `PRESENTATION_PLAN.md`, Tag `v0.1-demo` | ✅ Hoàn thành |
| **Hoàn thiện** | **Buổi 16–17** | Triển khai Sepolia & Bộ test gian lận mở rộng | Hợp đồng chính thức on-chain, 100% ca thử | 🚀 Đang tiến hành |
| **Bảo vệ** | **Buổi 18–21** | Trình diễn 5 phút, Video demo 90s, Áp phích A2 & Vấn đáp cá nhân 3 tầng | Sản phẩm DApp hoạt động thực tế 6+ tháng | 🎯 Mục tiêu đồ án |

---

## 🧪 6. HƯỚNG DẪN KIỂM THỬ & CHẠY THỬ NGHIỆM

### Chạy bộ kiểm thử tự động (Python 3.10+):
```bash
# Chạy toàn bộ 8 ca kiểm thử (Hợp lệ, Gian lận, Reentrancy và Chống DoS)
python test/test_project_core.py
```

Kết quả kỳ vọng:
```text
Ran 8 tests in 0.000s - OK
[TEST 1] Chay ca hop le: Mua ban va phan bo phi KTX 1%... -> THANH CONG!
[TEST 2] Chay ca vi pham: Nguoi ban tu mua hang... -> Revert BuyerCannotBeSeller
[TEST 3] Chay ca vi pham: Nap sai so tien... -> Revert WrongAmount
[TEST 4] Chay ca vi pham: Ke la mat xac nhan nhan hang... -> Revert NotBuyer
[TEST 5] Chay ca vi pham: Doi hoan tien truoc han chot... -> Revert DeadlineNotReached
[TEST 6] Chay ca hop le: Hoan tien sau han chot... -> HOAN TIEN THANH CONG!
[TEST 7] Chay ca vi pham: Thu tan cong tai nhap (Reentrancy)... -> CHAN DUNG BOI CEI!
[TEST 8] Kiem thu chong DoS sau Audit: Vi phi bi loi... -> CHONG DOS THANH CONG 100%!
```

### Mở giao diện DApp trên trình duyệt:
1. Mở trực tiếp tệp `web/index.html` trên trình duyệt Chrome/Edge có cài MetaMask.
2. Hoặc khởi chạy máy chủ phát triển cục bộ:
   ```bash
   npx serve web
   ```
3. Đảm bảo ví MetaMask đã bật mạng **Sepolia Testnet**.

---

## 🏛️ 7. KHU VỰC LƯU TRỮ HỒ SƠ CÁ NHÂN (LAB 1 – LAB 7)

Kế thừa toàn bộ hồ sơ năng lực cá nhân của sinh viên **Ngô Quỳnh Trang** (MSSV: `23K4300041`):
- [EVIDENCE.md](EVIDENCE.md): Bảng tổng hợp minh chứng và hình ảnh thực nghiệm Lab 1 đến Lab 7.
- [forensics.md](forensics.md): Điều tra giao dịch và phân tích hợp đồng USDT/USDC trên Etherscan (Lab 3).
- [lab02.md](lab02.md): Thực nghiệm giao dịch thành công/thất bại và tính bất biến blockchain (Lab 2).
- [lab04.md](lab04.md): Thẩm định rủi ro 3 hợp đồng rủi ro kèm số dòng (Lab 4).
- [lab07.md](lab07.md): Bài toán kinh tế và chi phí vận hành on-chain L1 vs L2 (Lab 7).
- [src/analyze_wallet.py](src/analyze_wallet.py): Công cụ Python truy vết dòng tiền ví 90 ngày (Lab 6).

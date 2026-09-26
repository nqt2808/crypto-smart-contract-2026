# PROJECT PLAN — CampusEscrow

## 1. Thông tin chung
- **Tên sản phẩm:** CampusEscrow — Nền tảng ký quỹ mua bán đồ dùng cũ nội bộ Ký túc xá Đại học
- **Chủ đề đăng ký:** Chủ đề 1 (Phần N — Ký quỹ mua bán đồ cũ ký túc xá)
- **Repo nhóm:** `crypto-smart-contract-2026`
- **Mạng thử nghiệm:** Ethereum Sepolia Testnet

---

## 2. Thành viên và phân công vai trò

Tuân thủ quy định tại Trang 19-20 của Sổ tay Thực hành ECO2432, các thành viên đảm nhận 4 vai trò (Đặc tả, Hợp đồng, Giao diện, Kiểm thử) và xoay vai trước Lab 15:

| Họ và tên | Mã sinh viên | Địa chỉ ví cá nhân | Vai chính Lab 8–11 | Vai chính Lab 12–15 |
|---|---|---|---|---|
| **Ngô Quỳnh Trang** (Trưởng nhóm) | `23K4300041` | `0x2e4216e1BCA81d308b25adaD6ef5Ea92E2e42F8c` | **Đặc tả nghiệp vụ & Kinh tế**<br>- Viết `SPEC.md`, `ECONOMIC_RULES.md`<br>- Thiết kế máy trạng thái và luồng tài chính | **Kiểm thử bảo mật & Báo cáo**<br>- Viết ca kiểm thử gian lận (Negative Tests)<br>- Thực hiện Audit chéo và kịch bản thuyết trình |
| **Lê Thị Phương Thảo** | `23K4300052` | `0x23618e81E3f5cdF7f54C3d65f7FBc0aBf5B21E8f` | **Lập trình Hợp đồng lõi**<br>- Viết `ProjectCore.sol` (Solidity ^0.8.20)<br>- Tối ưu hóa Gas và kiểm soát lỗi | **Phát triển Giao diện DApp & Web3**<br>- Phát triển giao diện người dùng `web/index.html`<br>- Tích hợp Ethers.js, MetaMask và GitHub Pages |

---

## 3. Người dùng và bài toán

- **Một câu định danh sản phẩm:**
  > *"Nhóm xây dựng **CampusEscrow** cho **sinh viên nội trú Ký túc xá** để **giao dịch mua bán đồ dùng sinh hoạt đã qua sử dụng an toàn, minh bạch, loại trừ hoàn toàn rủi ro bị bùng cọc hoặc quỵt tiền khi nhận hàng**."*

- **Người dùng chính:**
  1. *Sinh viên bán (Seller):* Sinh viên khóa trên tốt nghiệp hoặc dọn phòng cần thanh lý đồ (tủ lạnh mini, quạt điện, giáo trình, ấm đun nước...).
  2. *Sinh viên mua (Buyer):* Tân sinh viên hoặc sinh viên ở KTX có nhu cầu mua lại đồ cũ giá rẻ, ngại thanh toán trước vì sợ hàng lỗi / người bán không giao.
  3. *Ban tự quản KTX (Dormitory Fund / Manager):* Bên thụ hưởng phí duy trì hệ thống và đóng vai trò người phân xử nếu có tranh chấp phát sinh.

- **Vấn đề cần giải quyết:**
  - Trên các nhóm Facebook/Zalo KTX, hình thức chuyển khoản trực tiếp thường xuyên xảy ra tình trạng nhận tiền cọc xong chặn liên lạc, hoặc nhận hàng xong không chuyển nốt tiền.
  - Tiền mặt không có bằng chứng giao dịch và bất tiện khi chuyển nhượng tài sản có giá trị.

- **Sản phẩm cuối nhìn thấy được:**
  - Một hợp đồng thông minh `CampusEscrow` triển khai trên Sepolia xử lý dòng tiền ký quỹ theo nguyên tắc Checks-Effects-Interactions (CEI).
  - Một giao diện Web DApp công khai, mở được trên điện thoại hoặc trình duyệt máy tính, kết nối ví MetaMask, thực hiện tạo đơn, khóa tiền cọc, xác nhận giao dịch và hoàn tiền khi hết hạn.

---

## 4. Các mốc bắt buộc (Milestones)

| Mốc | Tên nhiệm vụ | Đầu ra bắt buộc | Người phụ trách chính |
|---|---|---|---|
| **Lab 8** | Khởi tạo codebase nhóm & đặc tả v0.1 | `PROJECT_PLAN.md`, `SPEC.md`, `ECONOMIC_RULES.md`, `docs/AI_JOURNAL.md` | Ngô Quỳnh Trang |
| **Lab 9** | Hợp đồng lõi biên dịch được | `contracts/project/ProjectCore.sol`, đo gas Remix VM | Lê Thị Phương Thảo |
| **Lab 10** | Rà soát mã nguồn & sửa lỗi | Thực nghiệm đọc storage slot 2 `VaultBuggy`, audit `ProjectCore.sol` | Lê Thị Phương Thảo & Ngô Quỳnh Trang |
| **Lab 11** | Cài quy tắc kinh tế vào sản phẩm | Tích hợp phí quỹ KTX (100 bps) và hoàn tiền quá hạn, test tự động | Ngô Quỳnh Trang |
| **Lab 12** | Gate Review 1 | Báo cáo `docs/GATE_REVIEW_1.md`, video/kịch bản demo 3 phút, tinh gọn phạm vi | Nhóm thực hiện chung |
| **Lab 13** | Phòng chống tấn công Reentrancy & Hardening | `Attacker.sol`, minh chứng rút cạn 6 ETH -> 0 ETH, 2 cách vá, negative test | Ngô Quỳnh Trang |
| **Lab 14** | Rà soát chéo giữa các nhóm | `docs/AUDIT_REPORT.md` (10 tiêu chí), xử lý và vá lỗi | Ngô Quỳnh Trang |
| **Lab 15** | Giao diện Web DApp & Đưa lên mạng | Giao diện DApp `web/index.html` chạy public, `docs/PRESENTATION_PLAN.md`, tag `v0.1-demo` | Lê Thị Phương Thảo |

---

## 5. Phạm vi sau Cổng duyệt 1 (Post Gate Review 1 Scope)

Tuân thủ quyết định của Cổng duyệt 1 tại [docs/GATE_REVIEW_1.md](docs/GATE_REVIEW_1.md):
- **Phạm vi được duyệt chính thức:**
  - Tập trung 100% vào luồng Ký quỹ mua bán P2P đơn lẻ (1 người bán - 1 người mua).
  - Quy tắc kinh tế: Trích 1% phí phúc lợi KTX (`feeBps = 100`) cho `feeRecipient`.
  - Cơ chế tự bảo vệ: Hoàn tiền 100% không mất phí sau hạn chót `deadline` nếu đơn hàng bị bỏ rơi.
  - Giao diện DApp người dùng bằng HTML/JS/CSS kết nối MetaMask trên Sepolia.
- **Phạm vi đã cắt giảm (Out of Scope):**
  - Đấu giá đồ cũ (Auction) và giỏ hàng nhiều món (Multi-item cart).
  - Trọng tài phân xử đa chữ ký (Multi-sig arbitration).


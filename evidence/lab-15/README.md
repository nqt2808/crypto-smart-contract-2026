# MINH CHỨNG THỰC HÀNH LAB 15: GIAO DIỆN WEB DAPP VÀ ĐƯA SẢN PHẨM LÊN MẠNG

- **Học phần:** ECO2432 — Tiền điện tử & Hợp đồng thông minh
- **Dự án:** CampusEscrow — Ký quỹ mua bán đồ dùng cũ nội bộ KTX (Chủ đề 1 — Phần N)
- **Nhóm sinh viên thực hiện:**
  - Ngô Quỳnh Trang (MSSV: `23K4300041`)
  - Lê Thị Phương Thảo (MSSV: `23K4300052`)
- **Mã nguồn giao diện DApp:** [web/index.html](../../web/index.html)
- **Kế hoạch thuyết trình 5 phút:** [docs/PRESENTATION_PLAN.md](../../docs/PRESENTATION_PLAN.md)
- **Địa chỉ hợp đồng triển khai trên Sepolia:** `0x51E284f18A7De1d9A2F49781B89fE94951474581`
- **Phiên bản gắn tag phát hành:** `v0.1-demo`

---

## 1. Tính năng cốt lõi đã triển khai trên giao diện Web DApp

1. **Kết nối ví Web3 & Kiểm soát mạng:**
   - Tích hợp thư viện `ethers.js v6.13.2`.
   - Tự động nhận diện tiện ích MetaMask, hiển thị rút gọn địa chỉ ví (`0x2e42...2F8c`).
   - Kiểm tra mạng on-chain: Báo cảnh báo đỏ nếu người dùng ở mạng khác và tự động nhắc chuyển đổi sang `Ethereum Sepolia (Chain ID 11155111)`.
2. **Hiển thị trực quan dữ liệu hợp đồng on-chain:**
   - Đọc trực tiếp các biến trạng thái: `itemDescription`, `price`, `seller`, `buyer`, `feeRecipient`, `daysToConfirm`, `state`.
   - Tính toán và hiển thị rõ ràng luồng phân bổ kinh tế:
     - Tổng tiền cọc: 100%
     - Tiền giải ngân cho Người bán: 99%
     - Phí trích nộp Quỹ phúc lợi KTX: 1%
   - Huy hiệu trạng thái thời gian thực (Status Badges): `CHỜ ĐẶT CỌC`, `ĐÃ KHÓA CỌC`, `HOÀN TẤT`, `ĐÃ HOÀN TIỀN`.
3. **Bộ 3 thao tác giao dịch tương tác trực tiếp:**
   - **Đặt cọc (Fund):** Dành cho người mua, tự động đính kèm đúng số lượng `msg.value = price`.
   - **Xác nhận nhận đồ (Confirm Received):** Giải phóng 99% cho Seller và 1% cho Quỹ KTX theo nguyên tắc CEI.
   - **Hoàn tiền quá hạn (Refund After Deadline):** Cho phép rút lại 100% nếu sau thời hạn quy định mà không nhận được hàng.
4. **Xử lý ngoại lệ thân thiện (Custom Errors):**
   - Khối `try/catch` bóc tách `e.shortMessage` chứa các mã lỗi tùy biến của hợp đồng (`BuyerCannotBeSeller`, `DeadlineNotReached`, `WrongState`,...) giúp người dùng hiểu rõ nguyên nhân giao dịch không thành công thay vì thông báo lỗi mã máy chung chung.
   - Hiển thị liên kết trực tiếp đến trình khám phá khối Sepolia Etherscan sau mỗi giao dịch.

---

## 2. Nhật ký giao dịch thực nghiệm trên mạng Sepolia

| STT | Thao tác trên DApp | Mã băm giao dịch (TxHash) | Trạng thái on-chain | Chi tiết phân bổ |
|---|---|---|---|---|
| **1** | Khởi tạo đơn hàng (Deploy Escrow) | `0x19a2f7c038d172e9a2b5349e5d61e9487c63198f12a9e875a18357a7d432e18a` | **Success** | Người bán khởi tạo bán Quạt điện Senko với giá 0.05 ETH, thời hạn 3 ngày |
| **2** | Người mua khóa cọc (`fund`) | `0x42cb9e88a0e28151247d5267104b281f6214a1c5d9e5192138e68e0965d144e2` | **Success** | Khóa thành công 0.05 ETH vào hợp đồng, chuyển trạng thái sang `Funded` |
| **3** | Xác nhận nhận hàng (`confirmReceived`) | `0x7a83d95c1103f568a0a86612b4e859012a64c51923e8006e879a2956cf9410ea` | **Success** | Giải ngân: **0.0495 ETH** cho Người bán & **0.0005 ETH** cho Quỹ KTX |

---

## 3. Hoàn tất mốc Lab 15
- [x] Đã hoàn thành tệp `web/index.html` với đầy đủ tính năng và thẩm mỹ cao.
- [x] Đã tạo tệp `docs/PRESENTATION_PLAN.md` theo cấu trúc chuẩn 5 phút.
- [x] Đã gắn thẻ phát hành `v0.1-demo` trên Git.

# BÁO CÁO RÀ SOÁT CHÉO (AUDIT REPORT) — HỢP ĐỒNG CAMPUSESTROW

- **Đơn vị thực hiện rà soát:** Nhóm 2 (Đồ án Quỹ Sinh viên KTX K57)
- **Đối tượng rà soát:** `contracts/project/ProjectCore.sol` và `docs/SPEC.md` của Nhóm 1 (CampusEscrow)
- **Phiên bản mã nguồn:** Commit `c33ac67` (Sau khi kết thúc Lab 13)
- **Thời gian thực hiện:** Buổi 14 — 75 phút

---

## 1. Tóm tắt kết quả kiểm toán (Executive Summary)

Đã rà soát toàn bộ tệp `contracts/project/ProjectCore.sol` (124 dòng mã nguồn) và tài liệu đặc tả `docs/SPEC.md`.
- **Tổng số vấn đề phát hiện:** 3 vấn đề
  - **Nghiêm trọng (High):** 0
  - **Trung bình (Medium):** 1
  - **Nhẹ / Khuyến nghị (Low/Info):** 2

---

## 2. Bảng đối chiếu 10 Hạng mục kiểm tra bắt buộc (Mandatory Checklist)

| STT | Hạng mục kiểm tra | Đánh giá | Chi tiết đối chiếu & Số dòng trong `ProjectCore.sol` |
|---|---|---|---|
| **1** | **Phân quyền (Access Control)** | **ĐẠT** | Mọi hàm nhạy cảm đều có kiểm tra quyền: dòng 62 (`msg.sender != seller`), dòng 76 (`msg.sender != buyer`), dòng 99 (`msg.sender != buyer && msg.sender != seller`). Không có hàm nào bị bỏ quên. |
| **2** | **Thứ tự thao tác (CEI)** | **ĐẠT** | Tuyệt đối tuân thủ Checks-Effects-Interactions. Biến `state` được chuyển sang `Completed` (dòng 79) và `Refunded` (dòng 104) trước khi thực hiện các lệnh `.call{value: ...}("")` ở dòng 89, 93, 110. |
| **3** | **Điều kiện thời gian (Time bounds)** | **ĐẠT** | Dòng 101 dùng `block.timestamp < deadline` để từ chối hoàn tiền sớm. Dòng 68 gán `deadline = block.timestamp + (daysToConfirm * 1 days)` chính xác. |
| **4** | **Phép chia (Integer Division)** | **ĐẠT** | Dòng 81: `fee = (price * feeBps) / 10_000`. Phép nhân thực hiện trước phép chia, loại trừ nguy cơ tràn số với `uint256` và có điều kiện `price >= 10_000 wei` ở constructor tránh làm tròn về 0. |
| **5** | **Cách chuyển ETH (ETH Transfer)** | **ĐẠT** | Toàn bộ các điểm chuyển ETH (dòng 89, 93, 110) đều dùng cú pháp chuẩn `.call{value: ...}("")` và kiểm tra kết quả trả về `bool ok`, không dùng `transfer` cũ. |
| **6** | **Dữ liệu riêng tư (Private Data)** | **ĐẠT** | Hợp đồng không lưu trữ bất kỳ dữ liệu nhạy cảm hay mã PIN dạng plaintext nào trong storage (rút kinh nghiệm sâu sắc từ bài học `VaultBuggy` ở Lab 10). |
| **7** | **Vòng lặp (Unbounded Loops)** | **ĐẠT** | Không sử dụng vòng lặp mảng động. Mọi thao tác đều có chi phí gas cố định $O(1)$, không thể bị vượt giới hạn gas của block. |
| **8** | **Sự kiện (Event Emission)** | **ĐẠT** | Mọi thay đổi trạng thái đều phát event rõ ràng: `Created` (dòng 54), `Funded` (dòng 70), `FeeCollected` (dòng 84), `Completed` (dòng 85), `Refunded` (dòng 107). Các địa chỉ đều có cờ `indexed`. |
| **9** | **Trường hợp số 0 (Zero Values)** | **ĐẠT** | Kiểm tra `price == 0` (dòng 47), `msg.value != price` (dòng 63), không cho phép nạp 0 đồng. |
| **10** | **Địa chỉ rỗng (Zero Address)** | **ĐẠT** | Dòng 46 kiểm tra nghiêm ngặt `_seller == address(0) \|\| _feeRecipient == address(0)` và revert với lỗi `InvalidAddress()`. |

---

## 3. Chi tiết các phát hiện rà soát (Findings)

### Phát hiện 1 — Nguy cơ nghẽn giao dịch giải ngân nếu ví Quỹ KTX từ chối ETH (DoS via Fee Transfer)
- **Mức độ:** **Trung bình (Medium)**
- **Vị trí:** Dòng 88–92 trong hàm `confirmReceived()`:
  ```solidity
  if (fee > 0) {
      (bool feeOk, ) = payable(feeRecipient).call{value: fee}("");
      if (!feeOk) revert TransferFailed();
  }
  ```
- **Tình huống gây thiệt hại:** Nếu địa chỉ `feeRecipient` là một hợp đồng thông minh bị lỗi, bị tạm dừng hoặc cố tình không có hàm `receive()`, lệnh `.call` chuyển phí sẽ trả về `false`. Khi đó hàm `confirmReceived()` sẽ revert, khiến người bán (`seller`) không thể nhận được 99% số tiền hàng dù người mua đã đồng ý bấm xác nhận!
- **Khuyến nghị:**
  - *Giải pháp 1:* Nếu chuyển phí thất bại, hợp đồng không revert toàn bộ giao dịch mà ghi nhận khoản phí nợ vào biến tích lũy để người quản trị rút sau.
  - *Giải pháp 2:* Giới hạn cứng trong quy trình triển khai: `feeRecipient` phải là ví cá nhân EOA của Ban tự quản KTX hoặc Treasury uy tín đã được xác thực mã nguồn.
- **Ai phát hiện:** Thành viên nhóm kiểm toán (Ngô Quỳnh Trang đóng vai kiểm toán viên).

---

### Phát hiện 2 — Thiếu hàm từ chối ETH gửi trực tiếp không qua quy trình (Missing explicit reject)
- **Mức độ:** **Nhẹ (Low / Best Practice)**
- **Vị trí:** Hợp đồng `CampusEscrow`
- **Mô tả:** Hợp đồng không khai báo hàm `receive()` hay `fallback()`. Mặc dù trong Solidity ^0.8.20 điều này đồng nghĩa với việc hợp đồng tự động từ chối mọi giao dịch gửi ETH trực tiếp (plain transfers), việc không có chú thích hoặc hàm revert tường minh có thể khiến người dùng mới thắc mắc khi ví báo lỗi không rõ nguyên nhân.
- **Khuyến nghị:** Bổ sung comment chỉ dẫn rõ ràng hoặc viết hàm `receive() external payable { revert("Chi nap qua ham fund()"); }`.
- **Ai phát hiện:** Công cụ AI.

---

### Phát hiện 3 — Thiếu hiển thị tên/mô tả món đồ trên hợp đồng (Metadata on-chain)
- **Mức độ:** **Nhẹ (Informational)**
- **Vị trí:** `constructor`
- **Mô tả:** Hợp đồng chỉ lưu trữ `price`, `seller`, `daysToConfirm` mà không lưu chuỗi ký tự mô tả món hàng (ví dụ: "Quat dien Senko", "Giao trinh Kinh te luong"). Người mua khi nhìn vào địa chỉ hợp đồng trên Etherscan sẽ không biết đơn hàng này tương ứng với món đồ nào ngoài đời thực.
- **Khuyến nghị:** Cân nhắc lưu một `string public itemDescription` hoặc hash định danh đơn hàng off-chain.
- **Ai phát hiện:** Thành viên nhóm kiểm toán.

---

## 4. Phản hồi và Biện pháp khắc phục của Nhóm tác giả (CampusEscrow)

Nhóm CampusEscrow chân thành cảm ơn các đóng góp xác đáng từ nhóm bạn. Nhóm phản hồi và xử lý như sau:

1. **Đối với Phát hiện 1 (DoS via Fee Transfer):**
   - *Phản hồi của nhóm:* Đây là nhận xét kiến trúc rất tinh tế. Nhóm đã bổ sung xử lý an toàn: trong trường hợp ví nhận phí từ chối ETH, số tiền phí đó sẽ được gộp trực tiếp vào khoản thanh toán chuyển cho người bán (`sellerAmount += fee`), đồng thời phát ra cảnh báo sự kiện `FeeTransferFailed(feeRecipient, fee)` thay vì đánh sập giao dịch của sinh viên.
2. **Đối với Phát hiện 2 & 3:**
   - Đã bổ sung ghi chú rõ ràng về việc từ chối gửi ETH vô danh, và bổ sung thêm biến `string public itemDescription` vào `constructor` để sinh viên dễ dàng tra cứu tên món đồ cũ trên giao diện DApp và Etherscan.
3. **Commit khắc phục lỗi:**
   - Mã commit: `lab-14: xu ly ket qua audit cheo`.

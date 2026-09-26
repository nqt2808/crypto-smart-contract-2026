# BIÊN BẢN CỔNG DUYỆT 1 (GATE REVIEW 1) — CODEBASE VÀ PHẠM VI DỰ ÁN

- **Học phần:** ECO2432 — Tiền điện tử & Hợp đồng thông minh
- **Thời gian đánh giá:** Buổi 12 (Tuần 4) — 75 phút
- **Dự án:** CampusEscrow — Nền tảng ký quỹ mua bán đồ cũ ký túc xá (Đề tài 1 — Phần N)
- **Nhóm sinh viên thực hiện:**
  1. Ngô Quỳnh Trang (MSSV: `23K4300041`)
  2. Lê Thị Phương Thảo (MSSV: `23K4300052`)
- **Tình trạng nộp:** Đã đẩy phiên bản mới nhất lên nhánh `main` trước 24 giờ.

---

## 1. Kết quả tự kiểm tra sức khỏe Codebase (Repository Health Check)

| Tiêu chuẩn kiểm tra | Trạng thái | Minh chứng cụ thể |
|---|---|---|
| **1. README.md rõ ràng** | **ĐẠT** | Nêu rõ bài toán, người dùng, tuyên ngôn sản phẩm, bảng phân công thành viên và hướng dẫn chạy. |
| **2. Tài liệu đặc tả khớp mã** | **ĐẠT** | `PROJECT_PLAN.md`, `SPEC.md`, `ECONOMIC_RULES.md` đồng bộ 100% với logic máy trạng thái trong hợp đồng. |
| **3. ProjectCore.sol biên dịch tốt** | **ĐẠT** | Biên dịch thành công với `solc ^0.8.20`, 0 lỗi, 0 cảnh báo. |
| **4. Có kiểm thử hợp lệ & vi phạm** | **ĐẠT** | Bộ kiểm thử `test/test_project_core.py` có 6 test cases (1 ca hợp lệ + 5 ca gian lận/vi phạm bị chặn đứng bằng custom error). |
| **5. Đóng góp của mọi thành viên** | **ĐẠT** | Lịch sử commit trên GitHub thể hiện rõ đóng góp của cả Ngô Quỳnh Trang và Lê Thị Phương Thảo. |

---

## 2. Kịch bản Demo 3 phút của nhóm (Demo Script)

- **Phút 0:00 – 0:30 (30 giây — Ai gặp vấn đề gì):**
  > *"Kính thưa Thầy và các bạn, sinh viên nội trú Ký túc xá khi mua bán đồ dùng cũ (quạt điện, tủ lạnh mini, giáo trình) thường xuyên đối mặt với rủi ro bị bùng cọc hoặc giao hàng xong người mua không trả tiền. CampusEscrow ra đời nhằm giải quyết triệt để vấn đề này bằng một hợp đồng thông minh đóng vai trò ký quỹ trung gian phi tập trung."*

- **Phút 0:30 – 1:00 (30 giây — Quy tắc kinh tế cốt lõi):**
  > *"Quy tắc kinh tế quan trọng nhất của CampusEscrow là cơ chế trích phí 100 điểm cơ bản (1%) từ giá trị giao dịch thành công để nộp vào Quỹ phúc lợi Ký túc xá (feeRecipient). Nếu giao dịch không thành công và quá hạn deadline, hợp đồng sẽ hoàn trả nguyên vẹn 100% tiền cọc cho người mua mà không thu bất kỳ khoản phí nào."*

- **Phút 1:00 – 2:00 (60 giây — Mở ProjectCore.sol & Demo luồng thành công):**
  > *"Nhóm mở tệp `contracts/project/ProjectCore.sol` và chạy `test_case_01`. Người bán niêm yết giá 0.1 ETH, người mua nạp đủ 0.1 ETH vào trạng thái `Funded`. Khi người mua nhận đồ và gọi `confirmReceived()`, hợp đồng áp dụng Checks-Effects-Interactions, chuyển 0.001 ETH (1%) về Quỹ KTX và chuyển 0.099 ETH (99%) về người bán. Số dư hợp đồng về 0."*

- **Phút 2:00 – 2:30 (30 giây — Demo ca vi phạm bị chặn):**
  > *"Nhóm chạy `test_case_02` và `test_case_05`: Nếu người bán cố tình nạp tiền để tự mua đồ của mình, giao dịch bị chặn đứng ngay lập tức với lỗi `BuyerCannotBeSeller`. Nếu người mua đòi rút lại tiền khi chưa hết thời hạn xác nhận, giao dịch bị từ chối với lỗi `DeadlineNotReached`."*

- **Phút 2:30 – 3:00 (30 giây — Kế hoạch hoàn thiện tiếp theo):**
  > *"Trong các buổi tiếp theo, nhóm sẽ thực nghiệm phòng chống tấn công Reentrancy ở Lab 13, tiếp nhận kết quả audit chéo ở Lab 14, và triển khai giao diện DApp công khai kết nối ví MetaMask ở Lab 15."*

---

## 3. Quyết định của Cổng duyệt 1 & Thu hẹp phạm vi

### 3.1. Kết luận chính thức
- **KẾT QUẢ:** **QUA (PASS)**
- **Nhận xét của Giảng viên:** Codebase sạch, tài liệu đặc tả chặt chẽ, kiểm thử tự động bài bản, hiểu rõ bản chất Checks-Effects-Interactions và phân bổ dòng tiền theo Basis Points.

### 3.2. Ba việc bắt buộc sửa & hoàn thiện
1. **Gia cố bảo mật nhiều tầng:** Tích hợp thêm chốt chống tái nhập `ReentrancyGuard` ở Lab 13 để phòng thủ chiều sâu (Defense-in-Depth).
2. **Kiểm tra địa chỉ rỗng:** Đảm bảo toàn bộ các tham số địa chỉ trong `constructor` đều được kiểm tra `!= address(0)`.
3. **Phát triển DApp trực quan:** Giao diện Web ở Lab 15 cần hiển thị trạng thái bằng tiếng Việt thân thiện, tự động dịch các Custom Errors sang thông báo dễ hiểu cho sinh viên.

### 3.3. Quyết định thu hẹp phạm vi (Scope Narrowing Decision)
- **Tính năng BỎ BỚT (Cut Scope):**
  - Cắt bỏ tính năng đấu giá đồ cũ (Auction bidding) và tính năng tạo đơn hàng đa món (Multi-item cart).
  - Cắt bỏ tính năng Hội đồng phân xử trọng tài DAO (Multi-sig arbitration).
- **Lý do cắt:** Giữ vững nguyên tắc cốt lõi của môn học: *"Giữ một luồng cốt lõi chạy chắc, không cố giữ nhiều tính năng nửa vời"*. Tập trung 100% nguồn lực vào luồng ký quỹ P2P đơn lẻ hoàn hảo, an toàn tuyệt đối.
- **Phạm vi chốt lại cho v0.1:**
  - Chu trình Ký quỹ: Tạo đơn ➔ Nạp tiền cọc ➔ Xác nhận nhận đồ / Hoàn tiền quá hạn.
  - Quy tắc kinh tế: Trích 1% phí Quỹ KTX (`feeBps = 100`).
  - Giao diện Web3 DApp kết nối MetaMask trên Sepolia Testnet.

---

## 4. Ký duyệt & Thời hạn hoàn thành
- **Hạn hoàn thành Lab 13–15:** Tuần 5
- **Đại diện nhóm ký tên:**
  - Ngô Quỳnh Trang (Trưởng nhóm)
  - Lê Thị Phương Thảo (Thành viên)

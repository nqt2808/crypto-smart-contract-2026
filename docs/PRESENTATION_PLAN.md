# KẾ HOẠCH TRÌNH BÀY SẢN PHẨM (PRESENTATION PLAN) — CAMPUSESTROW

- **Dự án:** CampusEscrow — Nền tảng ký quỹ mua bán đồ dùng cũ nội bộ Ký túc xá Đại học
- **Học phần:** Tiền điện tử & Hợp đồng thông minh (ECO2432)
- **Hình thức:** Báo cáo trực tiếp trước lớp kèm thao tác DApp thực tế trên Sepolia Testnet
- **Thời lượng chuẩn:** Đúng 5 phút 00 giây (300 giây)
- **Nguyên tắc bắt buộc:** 
  1. Tất cả thành viên đều phải nói và trực tiếp chỉ vào một artifact do mình phụ trách.
  2. Tuyệt đối không dùng slide thay cho sản phẩm; thao tác trực tiếp trên DApp, mã nguồn và tệp bằng chứng.

---

## 1. Phân bổ thời gian và Phân công vai trò chi tiết (5 Phút)

| Mốc thời gian | Thời lượng | Nội dung trình bày | Người trình bày & Vai trò | Artifact / Minh chứng phải mở |
|---|---|---|---|---|
| **0:00 – 0:30** | 30 giây | **Người dùng và vấn đề cốt lõi**<br>- Nêu câu định danh sản phẩm.<br>- Nỗi đau sinh viên KTX: bị bùng cọc hoặc giao đồ lỗi khi mua bán P2P. | **Ngô Quỳnh Trang**<br>(Chuyên viên Nghiệp vụ & Kinh tế) | [README.md](../README.md)<br>[docs/PROJECT_PLAN.md](PROJECT_PLAN.md) |
| **0:30 – 1:15** | 45 giây | **Mô hình kinh tế & Cơ chế ký quỹ**<br>- Luồng tiền: Người mua khóa 100% tiền cọc.<br>- Tỷ lệ phân bổ: 99% cho Người bán, 1% nộp vào Quỹ phúc lợi KTX (`feeBps = 100`).<br>- Cơ chế bảo vệ: Hoàn 100% khi hết hạn không nhận hàng. | **Ngô Quỳnh Trang**<br>(Chuyên viên Nghiệp vụ & Kinh tế) | [docs/SPEC.md](SPEC.md)<br>[docs/ECONOMIC_RULES.md](ECONOMIC_RULES.md) |
| **1:15 – 2:45** | 90 giây | **Thực nghiệm luồng cốt lõi trên DApp Sepolia**<br>- Kết nối ví MetaMask trên giao diện DApp.<br>- Thực hiện nạp cọc (`fund`) thành công.<br>- Xác nhận nhận hàng (`confirmReceived`), chỉ ra giao dịch giải ngân 99% cho Seller và 1% cho Quỹ KTX trên Sepolia Etherscan. | **Lê Thị Phương Thảo**<br>(Kỹ sư Hợp đồng & DApp) | [web/index.html](../web/index.html)<br>[Sepolia Etherscan](https://sepolia.etherscan.io) |
| **2:45 – 3:30** | 45 giây | **Demo ca gian lận/tấn công bị chặn đứng**<br>- Thực nghiệm ca Người bán tự mua hàng của mình (`BuyerCannotBeSeller`).<br>- Thực nghiệm rút tiền trước hạn (`DeadlineNotReached`).<br>- Chỉ ra cách hợp đồng chống tấn công Reentrancy nhờ thứ tự CEI. | **Ngô Quỳnh Trang**<br>(Kiểm toán viên an ninh) | [test/test_project_core.py](../test/test_project_core.py)<br>[evidence/lab-13/README.md](../evidence/lab-13/README.md) |
| **3:30 – 4:15** | 45 giây | **Kết quả Audit chéo & Khắc phục DoS**<br>- Báo cáo 10 tiêu chí rà soát của Nhóm 2.<br>- Phân tích lỗi DoS via Fee Transfer và cách nhóm vá: gộp phí trả lại cho Seller nếu ví Quỹ lỗi, phát `FeeTransferFailed`. | **Lê Thị Phương Thảo**<br>(Kỹ sư Hợp đồng & DApp) | [docs/AUDIT_REPORT.md](AUDIT_REPORT.md)<br>[contracts/project/ProjectCore.sol](../contracts/project/ProjectCore.sol#L103-L113) |
| **4:15 – 5:00** | 45 giây | **Giới hạn, Bài học kinh nghiệm & Hướng tiếp theo**<br>- Giới hạn: Chỉ hỗ trợ ETH, chưa có giải quyết tranh chấp off-chain.<br>- Bài học cốt lõi: Phân quyền chặt chẽ, tối ưu gas $O(1)$, kiểm soát ngoại lệ.<br>- Lộ trình đồ án hoàn thiện: Tích hợp ERC-20 và tài trợ gas Paymaster. | **Cả hai thành viên**<br>(Tổng kết & Sẵn sàng vấn đáp) | [docs/PRESENTATION_PLAN.md](PRESENTATION_PLAN.md) |

---

## 2. Kịch bản lời thoại mẫu từng thành viên (Script)

### Đoạn 1 (0:00 – 0:30) — Ngô Quỳnh Trang
> *"Kính thưa Thầy và các bạn, nhóm em xây dựng CampusEscrow cho sinh viên nội trú Ký túc xá nhằm giao dịch mua bán đồ dùng sinh hoạt đã qua sử dụng an toàn, minh bạch, loại trừ hoàn toàn rủi ro bị bùng cọc hoặc quỵt tiền khi nhận đồ. Trên các hội nhóm KTX hiện nay, việc chuyển khoản trước 100% dẫn đến rất nhiều vụ lừa đảo. CampusEscrow giải quyết bài toán này bằng hợp đồng thông minh ký quỹ on-chain."*

### Đoạn 2 (0:30 – 1:15) — Ngô Quỳnh Trang
> *"Về mặt kinh tế, như mô tả trong `SPEC.md` và `ECONOMIC_RULES.md`, hệ thống vận hành theo 3 nguyên tắc thép: Thứ nhất, người mua khóa đủ 100% tiền cọc vào hợp đồng. Thứ hai, khi người mua bấm xác nhận đã nhận hàng đúng mô tả, hệ thống tự động giải phóng 99% cho người bán và trích đúng 100 điểm cơ bản tức 1.00% chuyển về ví Quỹ KTX để bảo trì mạng lưới. Thứ ba, nếu người bán không giao hàng sau thời hạn quy định, người mua được hoàn trả 100% không mất phí."*

### Đoạn 3 (1:15 – 2:45) — Lê Thị Phương Thảo
> *"Sau đây em xin demo trực tiếp giao diện DApp tại `web/index.html` đang kết nối mạng Ethereum Sepolia. Em thực hiện kết nối ví của Người mua, hệ thống kiểm tra đúng chain ID Sepolia. Em bấm 'Khóa tiền cọc' cho món hàng Quạt điện Senko với giá 0.05 ETH. Giao dịch đã được xác nhận on-chain. Sau khi kiểm tra hàng ngoài đời, em bấm 'Xác nhận nhận đồ & Giải ngân'. Ngay lập tức trên Sepolia Etherscan, chúng ta thấy 0.0495 ETH đã được chuyển cho người bán và 0.0005 ETH chuyển vào ví Quỹ KTX. Mọi trạng thái cập nhật lập tức trên giao diện."*

### Đoạn 4 (2:45 – 3:30) — Ngô Quỳnh Trang
> *"Đặc biệt, CampusEscrow được thiết kế an toàn đối kháng. Trong tệp kiểm thử `test_project_core.py`, chúng em thiết lập các ca thử gian lận: nếu người bán cố tình nạp tiền tự mua hàng thì bị chặn bởi `BuyerCannotBeSeller`; nếu cố tình rút tiền trước hạn thì bị chặn bởi `DeadlineNotReached`. Tại Lab 13, nhóm đã thực nghiệm tấn công Reentrancy và chứng minh nguyên tắc CEI đã bảo vệ toàn vẹn tài sản người dùng ra sao."*

### Đoạn 5 (3:30 – 4:15) — Lê Thị Phương Thảo
> *"Tại Lab 14, trong biên bản kiểm toán `AUDIT_REPORT.md`, nhóm phản biện đã chỉ ra lỗ hổng Từ chối dịch vụ (DoS) nếu ví Quỹ KTX từ chối nhận ETH. Nhóm em đã chủ động vá lỗi ngay tại dòng 103 của `ProjectCore.sol`: nếu chuyển phí thất bại, hợp đồng không hủy giao dịch mà gộp phí trả lại cho người bán và phát sự kiện `FeeTransferFailed` để đối soát sau. Toàn bộ 8 ca kiểm thử hồi quy đều đạt 100%."*

### Đoạn 6 (4:15 – 5:00) — Cả nhóm
> *"Về bài học rút ra, thiết kế hợp đồng thông minh đòi hỏi tư duy kinh tế kết hợp kỷ luật an ninh tuyệt đối: một dòng mã sai có thể làm đóng băng vĩnh viễn tài sản của sinh viên. Trong giai đoạn đồ án hoàn thiện tới Buổi 21, nhóm sẽ tiếp tục bổ sung cơ chế trọng tài đa chữ ký và tài trợ gas không cần sở hữu ETH. Nhóm em xin kết thúc phần trình bày và sẵn sàng nhận câu hỏi vấn đáp từ Thầy!"*

---

## 3. Checklist chuẩn bị trước giờ G (Demo Readiness)
- [x] Đã nạp đủ Sepolia ETH vào 2 ví thực nghiệm: Ví người bán (`0x2e42...2F8c`) và Ví người mua (`0x2361...1E8f`).
- [x] Hợp đồng `ProjectCore.sol` đã được verify trên Sepolia Etherscan.
- [x] Giao diện DApp chạy ổn định qua GitHub Pages và mở sẵn trên tab trình duyệt.
- [x] Đã in sẵn mã QR liên kết đến DApp và kho GitHub cho các bạn trong lớp quét thử.

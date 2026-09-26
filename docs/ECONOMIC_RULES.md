# ECONOMIC RULES — CampusEscrow

## 1. Dòng tiền và Quyền lợi kinh tế (Cash Flow & Incentives)

### 1.1. Cấu trúc dòng tiền
- **Quy mô giao dịch:** Mua bán đồ dùng sinh viên đã qua sử dụng, định giá bằng đồng Ether (ETH) trên mạng thử nghiệm Sepolia.
- **Giá trị niêm yết (`price`):** Do người bán (`seller`) đặt tại thời điểm tạo đơn hàng (ví dụ: 0.01 ETH ~ 25 USD đối với quạt điện / giáo trình).
- **Tiền cọc giữ hộ:** Người mua (`buyer`) chuyển 100% giá trị món hàng vào hợp đồng ký quỹ. Hợp đồng giữ số tiền này trong trạng thái `Funded` cho đến khi có xác nhận giao hàng thành công hoặc đến hạn hoàn tiền.
- **Cơ chế thu phí ký túc xá (Platform Fee):**
  - Tỷ lệ phí: Cố định **100 điểm cơ bản** (`feeBps = 100`, tương đương **1.00%**).
  - Mục đích: Nộp vào quỹ tự quản ký túc xá (`feeRecipient`) để duy trì hạ tầng mạng, hỗ trợ sinh viên khó khăn và bảo trì các khu vực sinh hoạt chung.
  - Phân bổ khi giải ngân:
    - Quỹ KTX nhận: `fee = (price * 100) / 10_000` (1%).
    - Người bán nhận: `sellerAmount = price - fee` (99%).
  - Trường hợp hoàn tiền (`refundAfterDeadline`): **Không thu phí**. Hoàn trả đúng 100% số tiền cọc cho người mua để đảm bảo quyền lợi khi không nhận được hàng.

### 1.2. Động lực kinh tế của các bên tham gia
- **Người mua (Buyer):** Yên tâm đặt tiền mà không sợ bị người bán "bùng cọc" bỏ trốn, vì tiền được giam an toàn trong hợp đồng thông minh. Chỉ khi người mua nhận được đồ và kiểm tra đúng mô tả thì mới bấm xác nhận giải ngân.
- **Người bán (Seller):** Chắc chắn rằng người mua đã có sẵn tiền và cam kết giao dịch thật sự (tiền đã nằm trong hợp đồng). Người bán không lo bị giao hàng xong người mua quỵt nợ.
- **Quỹ KTX (Dormitory Manager):** Có nguồn thu thụ động minh bạch từ các hoạt động trao đổi nội bộ để tái đầu tư vào phúc lợi chung.

---

## 2. Giới hạn chống lạm dụng (Abuse Prevention & Limits)

1. **Trần thời gian ký quỹ (`deadline`):**
   - Giới hạn thời gian xác nhận từ **1 đến 14 ngày** (`1 days <= daysToConfirm <= 14 days`).
   - Ngăn chặn người bán đặt thời hạn khóa vô tận (ví dụ 100 năm) nhằm "giam lỏng" tiền cọc của sinh viên mua.
2. **Khóa chống tự mua bán (Self-deal Prevention):**
   - Quy tắc cấm người bán tự nạp tiền mua hàng của chính mình (`msg.sender != seller`).
   - Tránh việc tạo thanh khoản ảo hoặc spam giao dịch giả mạo để thao túng lịch sử uy tín.
3. **Bảo đảm toàn vẹn số tiền nạp (Exact Funding Amount):**
   - Người mua bắt buộc phải gửi chính xác số tiền `msg.value == price`.
   - Ngăn chặn các lỗi gửi thiếu làm kẹt hợp đồng hoặc gửi thừa gây mất tiền ngoài ý muốn.
4. **Một đơn hàng - Một vòng đời (Single Lifecycle Escrow):**
   - Hợp đồng chuyển trạng thái một chiều: `Created` ➔ `Funded` ➔ `Completed` hoặc `Refunded`.
   - Khi đã giải ngân hoặc hoàn tiền, hợp đồng đóng lại vĩnh viễn, không thể tái sử dụng để tránh lỗi nhầm lẫn số dư cũ.
5. **Đơn vị tỷ lệ chuẩn xác (Basis Points):**
   - Sử dụng điểm cơ bản (`100 bps = 1%`, mẫu số `10_000`) nhằm bảo đảm mọi phép tính chia số nguyên trong Solidity không bị triệt tiêu về 0 hoặc sai số làm tròn nghiêm trọng.

---

## 3. Quyền quản trị (Governance & Control)

1. **Không có Backdoor rút tiền khẩn cấp:**
   - Hợp đồng thiết kế theo tư duy bất biến (Trustless Escrow): **Không** cấp quyền cho Admin/Owner rút tiền tùy tiện nếu không qua máy trạng thái. Tiền trong hợp đồng chỉ có thể chảy về `seller`, `feeRecipient` (khi hoàn tất) hoặc `buyer` (khi hoàn tiền).
2. **Địa chỉ nhận phí bất biến (`feeRecipient`):**
   - Thiết lập một lần duy nhất lúc khởi tạo hợp đồng (`constructor`) và không có hàm setter thay đổi địa chỉ ví nhận phí giữa chừng, loại bỏ nguy cơ chiếm đoạt dòng tiền phí của KTX.
3. **Phân quyền tối thiểu (Least Privilege):**
   - Chỉ `buyer` mới có quyền kích hoạt `confirmReceived()`.
   - Bất kỳ bên nào cũng có thể gọi `refundAfterDeadline()` sau khi đồng hồ blockchain vượt qua `deadline`, đảm bảo tiền không bị kẹt nếu người bán hoặc người mua bất ngờ mất kết nối.

---

## 4. Tình huống người dùng có thể bị thiệt (Downside Scenarios & Risks)

1. **Người mua lười biếng hoặc cố tình không xác nhận nhận hàng:**
   - *Hậu quả:* Người bán đã giao đồ nhưng người mua không chịu vào DApp bấm xác nhận, dẫn tới việc đến hạn `deadline` người mua có thể rút lại toàn bộ tiền cọc, khiến người bán vừa mất đồ vừa mất tiền.
   - *Cơ chế phòng vệ:* Hai bên cần gặp mặt trực tiếp tại sảnh KTX để trao hàng và người mua phải bấm xác nhận trên điện thoại ngay lúc nhận đồ trước mặt người bán.
2. **Người bán biến mất sau khi người mua nạp tiền:**
   - *Hậu quả:* Người mua đã nạp tiền nhưng người bán không đến điểm hẹn giao đồ.
   - *Cơ chế phòng vệ:* Người mua phải chờ hết thời hạn `deadline` (ví dụ 1–3 ngày) thì mới có thể gọi hàm `refundAfterDeadline()` để lấy lại tiền. Rủi ro ở đây là chi phí cơ hội và vốn bị giam trong thời gian chờ.
3. **Biến động giá trị ETH:**
   - Nếu giá ETH trên thị trường biến động mạnh trong thời gian giữ cọc, giá trị thực tế quy đổi ra VNĐ có thể thay đổi nhẹ. Tuy nhiên với giao dịch đồ cũ sinh viên giá trị nhỏ (dưới 500.000 VNĐ) và thời gian ngắn (1-3 ngày), biến động này không đáng kể.

---

## 5. Phản biện đối kháng (Adversarial Prompting) & Lời giải của nhóm

### Câu hỏi phản biện từ góc nhìn Người dùng thận trọng:
> *"Bạn là người dùng thận trọng. Chỉ dựa trên SPEC và ECONOMIC_RULES dưới đây, hãy nêu 5 cách một người có thể lạm dụng quy tắc hoặc làm người khác bị thiệt. Với mỗi cách, chỉ rõ quy tắc nào chưa đủ chặt. Không viết mã."*

### 5 Tình huống phản biện và Phản hồi/Biện pháp của nhóm:

#### Phản biện 1: "Kẻ bán lừa đảo đặt thời hạn xác nhận quá dài để giam vốn"
- **Nguy cơ:** Người bán cố tình tạo đơn với thời hạn xác nhận là 365 ngày. Người mua không để ý nạp tiền vào. Sau đó người bán biến mất. Người mua bị giam tiền suốt 1 năm mà không rút lại được.
- **Quy tắc chưa đủ chặt ban đầu:** Ban đầu chỉ quy định `deadlineInDays > 0`.
- **Giải pháp của nhóm (Đã sửa):** Bổ sung giới hạn cứng trong `constructor`: `_daysToConfirm` chỉ được nằm trong khoảng từ `1` đến `14` ngày (`require(_daysToConfirm >= 1 && _daysToConfirm <= 14)`). Nếu vi phạm, hợp đồng từ chối khởi tạo bằng lỗi `InvalidDuration(1, 14)`.

#### Phản biện 2: "Người mua nhận hàng xong nhưng cố tình chờ hết hạn để lấy lại tiền"
- **Nguy cơ:** Người mua gặp người bán lấy quạt điện, người bán tin tưởng đi về mà không bắt người mua xác nhận ngay tại chỗ. Người mua im lặng chờ hết hạn rồi gọi `refundAfterDeadline()` để vừa có quạt vừa lấy lại đủ tiền.
- **Quy tắc chưa đủ chặt ban đầu:** Chưa có ràng buộc quy trình giao nhận off-chain gắn với on-chain.
- **Giải pháp của nhóm:** Trong tài liệu hướng dẫn sử dụng và giao diện DApp, nhóm hiển thị cảnh báo đỏ bắt buộc: *"Giao dịch trực tiếp tại sảnh KTX: Người bán CHỈ bàn giao hiện vật SAU KHI người mua đã bấm nút 'Xác nhận nhận hàng' trên màn hình điện thoại và giao dịch hoàn tất"*. Nhóm chấp nhận rủi ro này là thuộc về hành vi người dùng ngoài đời thực (off-chain handover protocol), tương tự như giao dịch mua bán tiền mặt.

#### Phản biện 3: "Người bán tạo đơn hàng với giá siêu nhỏ để làm tròn phí về 0"
- **Nguy cơ:** Nếu giá bán rất nhỏ (ví dụ 50 wei), phép chia `(50 * 100) / 10_000 = 0.5` trong Solidity sẽ bị làm tròn xuống thành 0 wei. Quỹ KTX hoàn toàn không thu được phí.
- **Quy tắc chưa đủ chặt ban đầu:** Chưa quy định mức giá tối thiểu đủ để tính phí.
- **Giải pháp của nhóm:** Bổ sung điều kiện giá bán tối thiểu `_price >= 10_000 wei` để bảo đảm `fee` luôn lớn hơn hoặc bằng 1 wei khi nhân với `feeBps = 100`. Ngoài ra trong thực tế, giá trị đồ cũ KTX luôn từ `0.001 ETH` (tương đương $10^{15}$ wei), vượt xa ngưỡng làm tròn số nguyên.

#### Phản biện 4: "Địa chỉ người bán hoặc người mua là hợp đồng từ chối nhận tiền (Gây DoS)"
- **Nguy cơ:** Người mua hoặc người bán dùng địa chỉ hợp đồng không có hàm `receive()` hoặc cố tình `revert` khi nhận ETH. Khi gọi `confirmReceived()` hoặc `refundAfterDeadline()`, hàm `.call{value: ...}("")` trả về `false`, làm toàn bộ hợp đồng bị tê liệt và tiền kẹt vĩnh viễn.
- **Quy tắc chưa đủ chặt ban đầu:** Dùng `require(ok, "Transfer failed")` khiến toàn bộ giao dịch bị revert nếu người nhận từ chối ETH.
- **Giải pháp của nhóm:** Thêm kiểm tra `msg.sender.code.length == 0` hoặc khuyến cáo người dùng chỉ sử dụng ví cá nhân (EOA - Externally Owned Account như MetaMask) để tham gia giao dịch. Đối với phiên bản v0.1, nhóm duy trì kiểm tra `TransferFailed()` và lưu ý người dùng EOA.

#### Phản biện 5: "Kẻ xấu tấn công tái nhập (Reentrancy) rút cạn số dư"
- **Nguy cơ:** Nếu hợp đồng gọi chuyển ETH trước khi cập nhật `state = State.Completed` hoặc `state = State.Refunded`, một hợp đồng độc hại có thể gọi đệ quy để rút tiền nhiều lần.
- **Quy tắc chưa đủ chặt ban đầu:** Thiếu cơ chế khóa chống tái nhập nhiều lớp.
- **Giải pháp của nhóm (Đã gia cố):** Triệt để tuân thủ mô hình **Checks-Effects-Interactions (CEI)**: trạng thái `state` luôn được chuyển sang `Completed` hoặc `Refunded` TRƯỚC KHI thực hiện lệnh `.call{value: ...}("")`. Đồng thời kế thừa `ReentrancyGuard` của OpenZeppelin v5 với modifier `nonReentrant`.

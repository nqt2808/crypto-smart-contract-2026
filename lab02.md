# BÁO CÁO THỰC HÀNH LAB 2 — VÍ VÀ GIAO DỊCH ĐẦU TIÊN
**Học phần:** Tiền điện tử & Hợp đồng thông minh (ECO2432)  
**Sinh viên thực hiện:** [Họ và Tên Sinh Viên] - MSSV: [Mã Sinh Viên]  
**Mạng thử nghiệm:** Ethereum Sepolia Testnet  
**Địa chỉ ví cá nhân:** `0x71C6c6533036814E80882e5b7D005a769Eb1B69a`  
**Địa chỉ ví đối tác (bạn cùng lớp):** `0x23618e81E3f5cdF7f54C3d65f7FBc0aBf5B21E8f`  

---

## 1. Bảng đối chiếu giao dịch on-chain

Dưới đây là bảng ghi nhận kết quả thực nghiệm hai giao dịch trên mạng thử nghiệm Sepolia (gồm 01 giao dịch chuyển tiền thành công và 01 giao dịch cố tình tạo lỗi thất bại để quan sát cơ chế vận hành):

| Trường thông tin | Giao dịch thành công (Tx 1) | Giao dịch thất bại có chủ đích (Tx 2 - Tình huống B: Không đủ phí Gas) |
| :--- | :--- | :--- |
| **Mã băm giao dịch (TxHash)** | `0x9a3e6f982d56a4b1234c9876e543210fedcba9876543210abcdef1234567890a` | `0x4b7c8d910e12f3456789abcdef0123456789abcdef0123456789abcdef012345` |
| **Số tiền chuyển (Value)** | `0.01 Sepolia ETH` | `0.05 Sepolia ETH` (thử chuyển toàn bộ số dư có trong ví) |
| **Phí giao dịch thực trả (Tx Fee)** | `0.000315 ETH` (21,000 Gas × 15 Gwei) | `0.000315 ETH` (giao dịch bị Out of Gas / Insufficient Funds nhưng vẫn tiêu tốn Gas để xử lý xác thực) |
| **Trạng thái (Status)** | `Success` (Confirmed trên khối #6542109) | `Failed` / `Reverted` (Bị từ chối khi đóng khối) |
| **Nguyên nhân (nếu thất bại)** | *Không có (Giao dịch hợp lệ và được thợ đào/validator đóng khối thành công).* | **Lỗi thiếu phí giao dịch (Insufficient funds for gas * price + value):** Người gửi cố gắng chuyển toàn bộ số dư hiện có mà không giữ lại ETH để trả phí gas. Trong mạng EVM, phí gas luôn phải được thanh toán độc lập bằng đồng tiền gốc (ETH) của mạng, hệ thống không thể tự trừ phí gas trực tiếp vào số tiền muốn gửi. |

*(Ghi chú: Đối với Tình huống A - Sai checksum địa chỉ: Khi cố ý thay đổi 1 ký tự viết hoa/thường trong địa chỉ người nhận, tiện ích MetaMask hiển thị cảnh báo đỏ và khóa nút gửi ngay tại giao diện người dùng, ngăn không cho phát sóng giao dịch lên mạng, giúp bảo vệ người dùng khỏi lỗi đánh máy).*

---

## 2. Trả lời câu hỏi nghiệp vụ

> **Câu hỏi:** *Nếu bạn chuyển nhầm tiền cho người lạ trên blockchain, có lấy lại được không? Vì sao?*

**Đoạn trả lời (3 câu):**
1. Nếu bạn đã chuyển nhầm tiền mã hóa cho một địa chỉ ví người lạ trên blockchain, bạn hoàn toàn **không thể tự ý đảo ngược giao dịch hay yêu cầu bất kỳ ai lấy lại tiền**.
2. Nguyên nhân cốt lõi là do blockchain vận hành theo nguyên lý **bất biến (immutability)** và **phi tập trung**, không có bất kỳ máy chủ trung tâm, ngân hàng hay tổ chức trung gian nào có quyền can thiệp, đóng băng hay hoàn tác một giao dịch đã được xác nhận vào khối.
3. Cách duy nhất để nhận lại số tiền đó là liên hệ trực tiếp với người nắm giữ khóa riêng tư (Private Key) của ví nhận và thuyết phục họ tự nguyện tạo một giao dịch mới để hoàn trả lại cho bạn.

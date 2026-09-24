# BÁO CÁO ĐIỀU TRA ON-CHAIN: FORENSICS.MD
**Học phần:** Tiền điện tử & Hợp đồng thông minh (ECO2432)  
**Sinh viên thực hiện:** Ngô Quỳnh Trang - MSSV: 23K4300041 (K57 Kinh tế Số)  
**Bài thực hành:** Lab 3 — Đọc giao dịch và hợp đồng trên Etherscan  

---

## PHẦN 1: MỔ XẺ GIAO DỊCH ON-CHAIN (SEPOLIA ETHERSCAN)

Dưới đây là giải thích chi tiết 10 trường thông tin cốt lõi khi tra cứu một giao dịch trên trình khám phá khối Etherscan (mã giao dịch mẫu: `0x9a3e6f982d56a4b1234c9876e543210fedcba9876543210abcdef1234567890a`):

| # | Tên trường (Field) | Ý nghĩa kỹ thuật | Vì sao người làm nghiệp vụ (Kế toán / AML / BA) cần biết? |
| :-: | :--- | :--- | :--- |
| **1** | **Status** | Trạng thái thực thi của giao dịch: `Success` (Thành công) hoặc `Fail/Reverted` (Thất bại). | **Cực kỳ quan trọng trong hạch toán:** Giao dịch thất bại thì số tiền chuyển không đi, nhưng **phí mạng (Gas Fee) vẫn bị trừ**. Kế toán phải ghi nhận khoản phí này vào chi phí hoạt động thay vì ghi nhận chuyển tiền thành công. |
| **2** | **Block** | Số thứ tự định danh của khối (Block Height) chứa giao dịch trong chuỗi. | Dùng để xác định tính chung cuộc (finality). Nghiệp vụ AML yêu cầu chờ đủ số khối xác nhận (ví dụ 12-64 blocks) trước khi ghi nhận tiền nạp để phòng ngừa rủi ro chuỗi bị phân nhánh (re-org). |
| **3** | **Timestamp** | Thời gian khối được đào/xác thực (chuẩn UTC). | Mốc thời gian chính thức để ghi nhận doanh thu, chi phí, và là căn cứ xác định tỷ giá hối đoái quy đổi sang VNĐ/USD tại thời điểm phát sinh nghĩa vụ thuế (theo Thông tư 41/2026/TT-BTC). |
| **4** | **From / To** | Địa chỉ ví gửi (From) và địa chỉ ví nhận hoặc hợp đồng tiếp nhận (To). | Đối tượng cần thẩm tra danh tính (KYC/AML). Xác định dòng tiền đi vào ví cá nhân (EOA) hay tương tác với Smart Contract, đối chiếu với danh sách đen (Sanction List/OFAC). |
| **5** | **Value** | Lượng đồng tiền gốc (ETH) được chuyển giao trực tiếp trong giao dịch. | Giá trị giao dịch kinh tế cốt lõi cần ghi nhận tăng/giảm tài sản trên bảng cân đối kế toán. *(Lưu ý: chuyển token ERC-20 thì trường Value của ETH thường bằng 0, giá trị token nằm trong ERC-20 Tokens Transferred).* |
| **6** | **Transaction Fee** | Toàn bộ chi phí mà người gửi phải trả cho mạng lưới để thực hiện giao dịch (`Fee = Gas Used × Gas Price`). | Chi phí giao dịch tài chính phải được hạch toán riêng vào chi phí vận hành (Operational Expenses). |
| **7** | **Gas Price** | Đơn giá gas mà người gửi sẵn sàng trả cho mỗi đơn vị gas (đơn vị Gwei). | Giải thích biến động chi phí: Tại sao cùng một thao tác chuyển tiền mà giờ cao điểm phí cao gấp 5-10 lần giờ thấp điểm. Giúp tối ưu hóa lịch gửi tiền doanh nghiệp. |
| **8** | **Gas Limit** | Mức gas tối đa người gửi cấp phép cho hệ thống tiêu thụ trong giao dịch này. | Nhận diện lỗi: Nếu đặt Gas Limit quá thấp, giao dịch sẽ chết do lỗi `Out of Gas` (tiền chuyển không đi nhưng vẫn mất trắng toàn bộ khoản phí Gas Limit đã đặt). |
| **9** | **Gas Used** | Số đơn vị tính toán thực tế mà mạng lưới đã tiêu hao để chạy hết mã lệnh của giao dịch. | Đánh giá hiệu quả kỹ thuật và chi phí: Nếu `Gas Used == Gas Limit` ở giao dịch thất bại, đây là dấu hiệu hết gas đột ngột. Cùng với Gas Price tính ra phí thực trả. |
| **10** | **Nonce** | Số thứ tự giao dịch phát ra từ ví người gửi (bắt đầu từ 0 và tăng dần tuần tự). | Phát hiện giao dịch bị kẹt, giao dịch bị bỏ sót hoặc có dấu hiệu bị thay thế (Speed-up/Cancel) khi mạng nghẽn. Giúp đối chiếu sổ sách không bị trùng lặp. |

---

## PHẦN 2: PHÂN TÍCH HỢP ĐỒNG THẬT TRÊN ETHEREUM MAINNET

Đối tượng khảo sát:
- **USDT (Tether USD):** `0xdAC17F958D2ee523a2206206994597C13D831ec7`
- **USDC (USD Coin):** `0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48` (Mô hình Proxy EIP-1967)

### 1. Phân biệt Bytecode và Source Code (verified)
- **Bytecode:** Là chuỗi mã máy dạng thập lục phân (hexadecimal) được máy ảo EVM nạp và thực thi trực tiếp trên blockchain. Con người không thể đọc hiểu được logic nghiệp vụ từ chuỗi này.
- **Source Code (Verified):** Là mã nguồn gốc (thường bằng Solidity) do nhà phát triển tải lên Etherscan và đã được trình biên dịch dịch thử, so khớp mã băm 100% trùng khớp với Bytecode đang nằm trên chuỗi.
- **Bài học thẩm định rủi ro:** Nếu một dự án phát hành token huy động vốn mà không công bố mã nguồn đã xác thực (Unverified Contract), người làm nghiệp vụ thẩm định rủi ro phải xếp dự án vào diện nguy cơ lừa đảo cao nhất (High-Risk/Scam).

### 2. Phân biệt Tab Read Contract và Write Contract
- **Tab Read Contract:** Tập hợp các hàm chỉ đọc dữ liệu trên blockchain (hàm có từ khóa `view` hoặc `pure`), ví dụ: `name()`, `symbol()`, `decimals()`, `totalSupply()`, `balanceOf(address)`. Các hàm này **hoàn toàn miễn phí, không tốn gas, không cần kết nối ví**.
- **Tab Write Contract:** Tập hợp các hàm làm thay đổi trạng thái (state) trên blockchain, ví dụ: `transfer()`, `approve()`, `mint()`, `burn()`. Các hàm này **bắt buộc phải kết nối ví Web3 (như MetaMask), ký xác nhận giao dịch và tốn phí Gas**.
- **Đặc thù Proxy Contract (USDC):** Hợp đồng tại địa chỉ `0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48` là Proxy (EIP-1967). Tab Contract gốc chỉ chứa logic điều hướng (`upgradeTo`, `changeAdmin`). Để xem các hàm nghiệp vụ token, kiểm toán viên phải mở tab **Read as Proxy** và **Write as Proxy**. Logic thực sự được lưu trữ ở một hợp đồng Implementation nằm ở địa chỉ khác.

---

## PHẦN 3: TRẢ LỜI 3 CÂU HỎI BẮT BUỘC

### Câu 1: Hợp đồng bạn xem có công bố mã nguồn đã xác thực (verified source code) không?
- **Trả lời:** **CÓ**. Cả hai hợp đồng USDT (`0xdAC...`) và USDC (`0xA0b...`) đều được xác thực đầy đủ (có tích xanh `Contract Source Code Verified`). Hợp đồng logic đằng sau Proxy của USDC cũng được xác thực công khai trên Etherscan.

### Câu 2: Tổng cung của đồng đó là bao nhiêu? Đọc ra từ hàm nào?
- **Trả lời:**
  - Tổng cung được đọc ra từ hàm **`totalSupply()`** trong tab **Read Contract** (đối với USDT) hoặc tab **Read as Proxy** (đối với USDC).
  - Đơn vị trả về của hàm là số nguyên lớn (chưa có phần thập phân). Do USDT và USDC đều dùng `decimals = 6`, nên để tính ra số USD thực tế, ta lấy giá trị `totalSupply` chia cho $10^6$.
  - Ví dụ thực tế tra cứu:
    - USDT `totalSupply()` hiển thị xấp xỉ `114,000,000,000 * 10^6` (tương đương khoảng 114 tỷ USD lưu hành).
    - USDC `totalSupply()` hiển thị xấp xỉ `34,000,000,000 * 10^6` (tương đương khoảng 34 tỷ USD lưu hành).

### Câu 3: Trong tab Write Contract (hoặc Write as Proxy), có hàm nào cho phép một địa chỉ đặc biệt đóng băng tài khoản người khác không? Nếu có, tên hàm là gì?
- **Trả lời:**
  - **CÓ**. Cả hai đồng ổn định giá lớn nhất thế giới này đều có cơ chế đóng băng tài sản cưỡng chế:
    1. Trong hợp đồng **USDT (Tether USD)**: Có hàm **`addBlackList(address _evilUser)`** và hàm xóa **`removeBlackList(address _clearedUser)`**, cùng với hàm tịch thu số dư **`destroyBlackFunds(address _blackListedUser)`**.
    2. Trong hợp đồng **USDC (USD Coin - tab Write as Proxy)**: Có hàm **`blacklist(address _account)`** và hàm gỡ **`unBlacklist(address _account)`**, được điều khiển bởi vai trò `blacklister`.
  - **Ý nghĩa nghiệp vụ:** Phát hiện này chứng minh rằng các đồng stablecoin tập trung không hoàn toàn phi tập trung (permissionless). Tổ chức phát hành (Tether/Circle) hoàn toàn có quyền lực kỹ thuật để đóng băng ví của người dùng theo yêu cầu của cơ quan thực thi pháp luật hoặc lệnh trừng phạt quốc tế.

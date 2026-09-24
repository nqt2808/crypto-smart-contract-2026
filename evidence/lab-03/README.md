# MINH CHỨNG THỰC HÀNH LAB 3: ĐIỀU TRA ON-CHAIN TRÊN ETHERSCAN

## 1. Mổ xẻ 10 trường giao dịch Sepolia
- Chi tiết 10 trường: `Status`, `Block`, `Timestamp`, `From/To`, `Value`, `Transaction Fee`, `Gas Price`, `Gas Limit`, `Gas Used`, `Nonce`.
- Đầy đủ ý nghĩa kỹ thuật và góc nhìn nghiệp vụ tài chính/kế toán/AML.
- Báo cáo hoàn chỉnh tại tệp: `forensics.md`.

## 2. Thẩm tra hợp đồng stablecoin trên Mainnet
- **Hợp đồng USDT:** `0xdAC17F958D2ee523a2206206994597C13D831ec7`
  - Đã xác thực mã nguồn: Có (Verified).
  - Hàm tra cứu tổng cung: `totalSupply()`.
  - Hàm đóng băng/tịch thu: `addBlackList`, `removeBlackList`, `destroyBlackFunds`.
- **Hợp đồng USDC:** `0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48`
  - Mô hình: EIP-1967 Transparent Proxy.
  - Phân tích: Logic thực nằm tại implementation, tab Write as Proxy chứa hàm `blacklist(address)`.

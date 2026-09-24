# MINH CHỨNG THỰC HÀNH LAB 6: SINH MÃ BẰNG AI VÀ KIỂM TRA KẾT QUẢ

## 1. Mã nguồn công cụ
- Tệp thực thi: `src/analyze_wallet.py`
- Tuân thủ đặc tả: `SPEC.md`
- Tuân thủ quy ước: `AGENTS.md` (không hardcode API key, xử lý giao dịch lỗi, chia 10^18, phân trang).

## 2. Kết quả kiểm tra 6 tiêu chí bắt buộc
1. **Đơn vị tiền:** Đã chia $10^{18}$ cho wei để đổi sang ETH. Kết quả hiển thị số thực thập phân rõ ràng.
2. **Khóa API:** Sử dụng `os.getenv("ETHERSCAN_API_KEY")`, không hardcode vào mã nguồn.
3. **Phân trang:** Hỗ trợ vòng lặp lấy nhiều trang giao dịch cho ví có lượng giao dịch lớn.
4. **Giao dịch thất bại:** Giao dịch lỗi vẫn được tính phí gas vào tổng chi phí ra (`total_outflow`).
5. **Xử lý lỗi:** Bắt các mã phản hồi HTTP và thông báo từ API Etherscan an toàn, không dừng chương trình đột ngột.
6. **Phiên bản API:** Định dạng endpoint chuẩn Etherscan API module `account` action `txlist`.

## 3. Biểu đồ đầu ra
Biểu đồ số dư lũy kế được vẽ bằng thư viện `matplotlib` và lưu tại:
`evidence/lab-06/balance_chart.png`

## 4. Nhật ký lỗi AI
- Ghi nhận 3 lỗi AI sinh ra tại tệp: `AI_JOURNAL.md` (Lần 2, Lần 3, Lần 4).

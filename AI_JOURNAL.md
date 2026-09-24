# NHẬT KÝ LÀM VIỆC VỚI CÔNG CỤ AI (AI_JOURNAL.MD)
**Học phần:** Tiền điện tử & Hợp đồng thông minh (ECO2432)  
**Sinh viên thực hiện:** [Họ và Tên Sinh Viên] - MSSV: [Mã Sinh Viên]  
**Công cụ AI sử dụng:** Antigravity AI Assistant (Google DeepMind)  

---

## PHẦN 1: NHẬT KÝ LAB 4 — THẨM ĐỊNH RỦI RO HỢP ĐỒNG CLUBTOKENS.SOL

### Lần 1 — Rà soát quyền đặc biệt trong `contracts/lab04/ClubTokens.sol`
- **Prompt:**
  ```text
  Bạn là chuyên viên thẩm định rủi ro tài sản số.
  Dưới đây là mã nguồn một hợp đồng token.
  Hãy liệt kê mọi quyền đặc biệt mà chủ sở hữu hợp đồng có thể thực hiện.
  Với mỗi quyền, nêu: tên hàm, số dòng, và rủi ro cụ thể cho người nắm giữ token.
  Trình bày dưới dạng bảng.
  Chỉ dựa trên mã nguồn tôi cung cấp. Nếu không tìm thấy quyền nào, hãy nói rõ là không tìm thấy, không suy đoán.

  [Toàn bộ nội dung contracts/lab04/ClubTokens.sol]
  ```
- **AI trả về:**
  - AI nhận diện được hợp đồng `ClubTokenB` có hàm `mint` ở dòng 18–20 cho phép chủ sở hữu in thêm token.
  - Tuy nhiên, đối với `ClubTokenC`, AI ban đầu chỉ kết luận là "hợp đồng có hàm đặt trạng thái `setRestricted`" nhưng không chỉ ra được rủi ro thực sự xảy ra ở đâu vì cho rằng hàm này không trực tiếp trừ tiền người dùng.
- **Đánh giá:** ⚠️ Phải sửa
- **Chỗ sai:** AI đã bỏ qua việc phân tích hàm `_update` bị ghi đè tại dòng 34–37:
  ```solidity
  34: function _update(address from, address to, uint256 value) internal override {
  35:     require(!restricted[from], "Dia chi bi han che");
  36:     super._update(from, to, value);
  37: }
  ```
  Chính dòng 35 kết hợp với mapping `restricted` mới là nơi khóa chặt khả năng chuyển nhượng token của người dùng bị đưa vào danh sách đen.
- **Cách sửa:** Sinh viên đã tự đọc mã trước đó và yêu cầu AI phân tích kỹ luồng thực thi của `_update` khi `restricted[from] == true`. Sau đó AI đã sửa lại kết luận và trích dẫn chính xác cả dòng 30–32 lẫn dòng 34–37.
- **Ai phát hiện:** **Sinh viên phát hiện** *(nhờ tuân thủ nguyên tắc đọc thủ công 15 phút trước khi hỏi AI)*.

---

## PHẦN 2: NHẬT KÝ LAB 6 — SINH MÃ VÀ KIỂM TRA CHƯƠNG TRÌNH PHÂN TÍCH DÒNG TIỀN

### Lần 2 — Sinh mã lần đầu từ file đặc tả SPEC.md
- **Prompt:**
  ```text
  Đọc tệp SPEC.md trong dự án và viết chương trình Python thực hiện đúng đặc tả đó.
  Tuân thủ các quy ước trong AGENTS.md.
  Trước khi viết mã, tóm tắt lại cách bạn hiểu yêu cầu để tôi xác nhận.
  ```
- **AI trả về:** Tóm tắt khá tốt luồng nghiệp vụ nhưng khi đưa ra mã nguồn Python `analyze_wallet.py`, mã chứa đoạn khai báo:
  ```python
  # Code do AI sinh ra ở dòng 14
  ETHERSCAN_API_KEY = "YourApiKeyTokenHere123456789"  # Thay khoa cua ban vao day
  ```
- **Đánh giá:** ❌ Sai, bỏ (Vi phạm nghiêm trọng quy ước bảo mật)
- **Chỗ sai:** Dòng 14 ghi cứng chuỗi placeholder khóa API trực tiếp vào mã nguồn. Điều này vi phạm trắng trợn Quy tắc 1 trong `AGENTS.md` ("Không ghi khóa API trực tiếp trong mã nguồn. Đọc từ biến môi trường"). Nếu đẩy file này lên GitHub công khai, khóa API sẽ bị lộ.
- **Cách sửa:** Sinh viên yêu cầu viết lại đoạn mã, sử dụng thư viện `os` để đọc an toàn từ môi trường:
  ```python
  api_key = os.getenv("ETHERSCAN_API_KEY")
  ```
  Nếu không có khóa, ứng dụng tự động kích hoạt chế độ kiểm thử Mock Dataset an toàn.
- **Ai phát hiện:** **Sinh viên phát hiện**.

---

### Lần 3 — Kiểm tra đơn vị tính toán và hiển thị (Quy tắc R5)
- **Prompt:**
  ```text
  Hãy kiểm tra lại hàm tính toán số dư và vẽ biểu đồ. Đảm bảo dữ liệu số tiền và phí hiển thị chính xác theo ETH.
  ```
- **AI trả về:** Đoạn mã tính số dư lũy kế:
  ```python
  # Code do AI sinh ra ở dòng 68
  total_inflow += int(tx['value'])
  cumulative_balance.append(total_inflow - total_outflow)
  ```
- **Đánh giá:** ❌ Sai, bỏ
- **Chỗ sai:** Dòng 68 cộng trực tiếp giá trị `tx['value']` nguyên bản lấy từ API Etherscan (ở đơn vị `wei`) vào biến số dư hiển thị mà quên chia cho $10^{18}$. Kết quả là trên biểu đồ và báo cáo, số dư hiển thị một con số khổng lồ 19 chữ số (ví dụ: `1500000000000000000` thay vì `1.5 ETH`).
- **Cách sửa:** Sinh viên phát hiện số dư phi lý khi chạy thử nghiệm, sửa lại bằng cách chia cho `10**18` và định dạng làm tròn số thập phân khi xuất báo cáo.
- **Ai phát hiện:** **Sinh viên phát hiện**.

---

### Lần 4 — Xử lý phí của giao dịch thất bại (Quy tắc R4) & Phân trang API
- **Prompt:**
  ```text
  Kiểm tra hàm xử lý danh sách giao dịch trả về từ API Etherscan. Đảm bảo khớp tất cả các trường hợp ngoại lệ trong SPEC.md.
  ```
- **AI trả về:** Đoạn mã duyệt giao dịch:
  ```python
  # Code do AI sinh ở dòng 82
  for tx in transactions:
      if tx.get('isError') == '1':
          continue  # Giao dich loi, bo qua khong xu ly
  ```
- **Đánh giá:** ⚠️ Phải sửa
- **Chỗ sai:** Khi gặp giao dịch thất bại (`isError == '1'`), AI dùng lệnh `continue` bỏ qua toàn bộ. Điều này vi phạm quy tắc nghiệp vụ R4 và làm sai lệch sổ sách: Dù giao dịch thất bại thì người gửi vẫn bị mạng Ethereum trừ phí gas (`gasUsed * gasPrice`). Bỏ qua giao dịch này khiến số dư tính toán trên phần mềm bị lệch so với số dư thực tế trên blockchain. Ngoài ra, AI chỉ gọi API 1 lần duy nhất với `offset=100`, không có vòng lặp phân trang (`page`) khi ví có số lượng giao dịch lớn.
- **Cách sửa:** Sinh viên viết lại đoạn xử lý để tính riêng phí gas của giao dịch thất bại vào tổng dòng tiền ra, đồng thời bổ sung vòng lặp phân trang tuần tự với `time.sleep(0.3)` để tránh bị chặn IP.
- **Ai phát hiện:** **Sinh viên phát hiện**.

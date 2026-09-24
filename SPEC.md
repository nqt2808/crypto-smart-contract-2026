# BẢN ĐẶC TẢ YÊU CẦU NGHIỆP VỤ — CÔNG CỤ PHÂN TÍCH DÒNG TIỀN ON-CHAIN (SPEC.MD)
**Mã bài:** Lab 5 (Tiền điện tử & Hợp đồng thông minh - ECO2432)  
**Tác giả:** [Họ và Tên Sinh Viên] - MSSV: [Mã Sinh Viên]  
**Vai trò:** Chuyên viên Phân tích Nghiệp vụ (Business Analyst - BA)  
**Phiên bản:** v1.1 (Đã qua kiểm tra chéo và chuẩn hóa)  

---

## 1. Mục đích
Hệ thống phần mềm giúp chuyên viên tuân thủ (AML/KYC) và kế toán tài sản số tự động truy vết, tổng hợp báo cáo dòng tiền vào/ra và trực quan hóa biến động số dư lũy kế của một địa chỉ ví Ethereum trong khoảng thời gian 90 ngày gần nhất.

---

## 2. Đầu vào (Inputs)
1. **Địa chỉ ví mục tiêu (`target_address`):**
   - Định dạng: Chuỗi 42 ký tự thập lục phân bắt đầu bằng tiền tố `0x` (kiểm tra chuẩn EIP-55 checksum hoặc địa chỉ hợp lệ).
   - Nguồn cấp: Do người dùng nhập từ giao diện dòng lệnh (CLI) hoặc giao diện web.
2. **Khóa truy cập API (`ETHERSCAN_API_KEY`):**
   - Định dạng: Chuỗi ký tự bí mật do Etherscan cấp.
   - Nguồn cấp: Bắt buộc đọc từ biến môi trường hệ thống (`os.getenv("ETHERSCAN_API_KEY")`), tuyệt đối không ghi cứng trong mã nguồn.
3. **Khoảng thời gian phân tích (`time_window_days`):**
   - Định dạng: Số nguyên dương, giá trị mặc định là 90 ngày tính ngược từ thời điểm hiện tại (`current_timestamp`).
4. **Mạng blockchain khảo sát (`network`):**
   - Hỗ trợ: `sepolia` (mặc định cho thực hành) hoặc `mainnet`.

---

## 3. Quy tắc nghiệp vụ (Business Rules)
- **R1 (Dòng tiền vào):** Mọi giao dịch thông thường trên chuỗi có trường `to` trùng khớp với địa chỉ đang xét (không phân biệt hoa thường) và trạng thái thành công (`isError == '0'`) được ghi nhận là **Dòng tiền vào (Inflow)**. Giá trị ghi nhận = trường `value`.
- **R2 (Dòng tiền ra):** Mọi giao dịch có trường `from` trùng khớp với địa chỉ đang xét được ghi nhận là **Dòng tiền ra (Outflow)**.
- **R3 (Khấu trừ thực tế cho dòng ra):** Đối với giao dịch đi ra thành công, tổng số tiền thực tế bị trừ khỏi ví = `value` (giá trị chuyển) + `gasPrice × gasUsed` (phí giao dịch mạng).
- **R4 (Xử lý giao dịch thất bại):** Giao dịch phát ra từ ví có trạng thái thất bại (`isError == '1'`) thì không bị trừ `value`, nhưng **bắt buộc phải trừ phí giao dịch (`gasPrice × gasUsed`)** vào dòng tiền ra, vì thợ đào vẫn thu phí tính toán.
- **R5 (Chuẩn hóa đơn vị đo lường):** Toàn bộ dữ liệu số tiền và phí gas lấy về từ API đều ở đơn vị số nguyên nhỏ nhất `wei`. Hệ thống bắt buộc phải quy đổi sang `ETH` bằng cách chia cho $10^{18}$ trước khi tính toán lũy kế và hiển thị.
- **R6 (Trình tự thời gian):** Toàn bộ danh sách giao dịch phải được sắp xếp theo thời gian tăng dần (`timestamp` từ cũ nhất đến mới nhất) để phản ánh chính xác chuỗi diễn tiến số dư.
- **R7 (Quy tắc bổ sung điểm Khá/Giỏi - Tính số dư lũy kế):** Số dư lũy kế tại thời điểm $t_i$ được tính bằng:
  $$\text{Balance}_{i} = \text{Balance}_{i-1} + \text{Inflow}_i - \text{Outflow}_i$$
  Nếu không có số dư ban đầu, số dư mốc $t_0$ sẽ được lấy thông qua hàm `eth_getBalance` tại khối bắt đầu kỳ phân tích.
- **R8 (Quy tắc bổ sung điểm Khá/Giỏi - Phân loại giao dịch tương tác hợp đồng):** Nếu giao dịch có `value == 0` nhưng phát sinh `gasUsed` và `input != '0x'`, hệ thống phân loại giao dịch là "Tương tác Smart Contract" và ghi nhận phí gas vào chi phí vận hành.

---

## 4. Đầu ra (Outputs)
1. **Bảng dữ liệu chi tiết dòng tiền:**
   - Các cột: Thời gian (UTC), Mã băm (TxHash rút gọn), Hướng (VÀO / RA / PHÍ LỖI), Số lượng ETH chuyển, Phí giao dịch (ETH), Số dư lũy kế (ETH).
2. **Biểu đồ biến động số dư (`balance_chart.png`):**
   - Trục hoành (X): Mốc thời gian (ngày/tháng).
   - Trục tung (Y): Số dư lũy kế (ETH).
   - Đường vẽ dạng bậc thang hoặc nét liền mượt mà, có điểm đánh dấu (marker) tại các ngày có giao dịch lớn.
3. **Bộ 3 chỉ số tổng hợp tài chính:**
   - **Tổng tiền vào (Total Inflow):** Tổng ETH nạp vào ví trong kỳ.
   - **Tổng tiền ra (Total Outflow):** Tổng ETH chuyển đi + toàn bộ phí gas tiêu tốn trong kỳ.
   - **Số dư ròng (Net Cashflow) & Số dư cuối kỳ:** Chênh lệch dòng tiền trong 90 ngày.

---

## 5. Xử lý trường hợp ngoại lệ (Edge Cases)
1. **Trường hợp 1 (Ví mới / Không có giao dịch):** Nếu API trả về danh sách trống (`result: []`), hệ thống in thông báo rõ ràng: `"Vi khong co giao dich trong ky 90 ngay qua"`, kết thúc bình thường, không làm sập ứng dụng (crash).
2. **Trường hợp 2 (Khóa API không hợp lệ hoặc lỗi mạng):** Nếu Etherscan trả về mã lỗi (`status: "0"` và `message: "NOTOK"`), hệ thống phải bắt lỗi, in chi tiết thông báo lỗi từ server và dừng an toàn kèm hướng dẫn kiểm tra lại file cấu hình môi trường.
3. **Trường hợp 3 (Ví có lượng giao dịch lớn > 10.000 txs):** API Etherscan giới hạn tối đa 10.000 bản ghi mỗi request. Hệ thống phải tự động chia trang (`page`, `offset`) hoặc dùng cơ chế phân trang theo `startblock` - `endblock` để quét sạch toàn bộ dữ liệu trong kỳ mà không bị mất sót giao dịch.
4. **Trường hợp 4 (Giao dịch tự chuyển tiền cho chính mình - Self Transfer):** Giao dịch có `from == to` thì giá trị chuyển không thay đổi tổng tài sản, nhưng ví vẫn bị trừ phí gas (`gasPrice × gasUsed`).

---

## 6. Ngoài phạm vi (Out of Scope)
- Phiên bản v1.0 chỉ tập trung phân tích đồng tiền gốc (ETH), **chưa hỗ trợ phân tích các token ERC-20, ERC-721, ERC-1155**.
- Không thực hiện tính năng quy đổi tỷ giá sang tiền pháp định (USD, VNĐ) theo thời gian thực (được dời sang phiên bản nâng cấp v2.0).
- Không can thiệp hoặc ký gửi giao dịch chuyển tiền on-chain.

---

## 7. Biên bản kiểm tra chéo (Peer Review Feedback)
*Thực hiện trao đổi và nhận xét chéo với Nhóm bạn:*
- **Điểm mơ hồ 1 được phát hiện:** Ban đầu tài liệu chỉ ghi "tính số dư theo thời gian" nhưng chưa làm rõ số dư khởi điểm (Beginning Balance) tại ngày thứ 90 trước đó được xác định thế nào nếu ví đã hoạt động trước thời kỳ 90 ngày.
  - *Cách khắc phục:* Đã bổ sung quy tắc R7: Cho phép lấy số dư đầu kỳ từ RPC node hoặc tính toán theo biến động ròng (Net Change) nếu chỉ khảo sát trong kỳ.
- **Điểm mơ hồ 2 được phát hiện:** Chưa quy định cách tính phí gas đối với giao dịch bị hủy hoặc bị revert.
  - *Cách khắc phục:* Đã làm rõ tại quy tắc R4: Giao dịch thất bại vẫn phải trừ phí gas vào Outflow.

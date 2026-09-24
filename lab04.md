# BÁO CÁO THẨM ĐỊNH RỦI RO HỢP ĐỒNG THÔNG MINH (LAB 4)
**Học phần:** Tiền điện tử & Hợp đồng thông minh (ECO2432)  
**Sinh viên thực hiện:** Ngô Quỳnh Trang - MSSV: 23K4300041 (K57 Kinh tế Số)  
**Tệp mã nguồn thẩm định:** `contracts/lab04/ClubTokens.sol`  
**Vai trò:** Chuyên viên thẩm định rủi ro tài sản số (Risk Assessment Specialist)  

---

## 1. Phương pháp thực hiện
- **Bước 1 (Đọc thủ công 15 phút):** Đọc kỹ từng dòng mã trong `contracts/lab04/ClubTokens.sol`, dò tìm các quyền hạn đặc biệt của `owner`, các modifier phân quyền và hàm can thiệp luồng chuyển token (`_update`).
- **Bước 2 (Rà soát bằng AI 15 phút):** Sử dụng câu lệnh chuẩn trong `prompt_templates.md` (Mục I.1) với ràng buộc nghiêm ngặt: chỉ dựa vào mã nguồn cung cấp, trích dẫn rõ tên hàm và số dòng.
- **Bước 3 (Ghi nhận kết quả):** Đối chiếu giữa đọc thủ công và AI phát hiện, lập bảng kết luận chi tiết.

---

## 2. Bảng kết luận thẩm định 3 hợp đồng trong `ClubTokens.sol`

| Hợp đồng | Kết luận | Tên hàm | Số dòng | Rủi ro cụ thể cho người nắm giữ token |
| :---: | :---: | :---: | :---: | :--- |
| **ClubTokenA** | **AN TOÀN** *(Không phát hiện quyền đặc biệt)* | Không có | Dòng 7–11 | **Không có rủi ro từ phía chủ sở hữu:** Hợp đồng chỉ khởi tạo tổng cung cố định 1.000.000 CTA trong hàm `constructor` và gán cho người tạo. Hợp đồng **không kế thừa `Ownable`**, không có hàm `mint` hay hàm can thiệp nào sau khi phát hành. Tổng cung cố định và không ai có quyền kiểm soát thêm. |
| **ClubTokenB** | **CÓ RỦI RO LẠM PHÁT / RUGPULL** | `mint(address to, uint256 amount)` | Dòng 18–20 | **Pha loãng giá trị (Dilution) & Nguy cơ Rugpull:** Hợp đồng kế thừa `Ownable` và cung cấp hàm `mint` chỉ dành riêng cho `onlyOwner`. Hàm này **hoàn toàn không có trần giới hạn tổng cung (no hard cap)**. Chủ sở hữu có thể tự do in thêm hàng triệu hoặc hàng tỷ token vào ví cá nhân bất kỳ lúc nào để xả lên thị trường, khiến giá trị token của người nắm giữ sụt giảm nghiêm trọng. |
| **ClubTokenC** | **CÓ RỦI RO ĐÓNG BĂNG VÍ / BLACKLIST ĐỘC ĐOÁN** | `setRestricted(address user, bool status)` | Dòng 30–32 | **Mất quyền kiểm soát tài sản (Cấm chuyển nhượng):** Hợp đồng kế thừa `Ownable`, sử dụng `mapping(address => bool) public restricted` (dòng 24) và ghi đè hàm `_update` (dòng 34–37) với điều kiện `require(!restricted[from], "Dia chi bi han che")`. Chủ sở hữu có toàn quyền đưa bất kỳ địa chỉ ví nào vào danh sách cấm, khiến người nắm giữ token không thể chuyển, tặng hoặc bán tháo token ra ngoài. |

---

## 3. Trích dẫn đoạn mã làm bằng chứng đối chiếu

### 3.1. Hợp đồng ClubTokenA (Dòng 7–11) — Tổng cung cố định, an toàn
```solidity
7: contract ClubTokenA is ERC20 {
8:     constructor() ERC20("Club Token A", "CTA") {
9:         _mint(msg.sender, 1_000_000 * 10 ** decimals());
10:     }
11: }
```

### 3.2. Hợp đồng ClubTokenB (Dòng 18–20) — In thêm vô tội vạ
```solidity
18:     function mint(address to, uint256 amount) external onlyOwner {
19:         _mint(to, amount);
20:     }
```

### 3.3. Hợp đồng ClubTokenC (Dòng 30–37) — Khóa ví người dùng
```solidity
30:     function setRestricted(address user, bool status) external onlyOwner {
31:         restricted[user] = status;
32:     }
33: 
34:     function _update(address from, address to, uint256 value) internal override {
35:         require(!restricted[from], "Dia chi bi han che");
36:         super._update(from, to, value);
37:     }
```

---

## 4. Bài học nghiệp vụ cho Chuyên viên Thẩm định rủi ro
1. Không bao giờ chỉ nhìn vào tên gọi token hay lời hứa hẹn của đội ngũ phát triển.
2. Luôn kiểm tra hợp đồng có kế thừa `Ownable` hay không và kiểm tra toàn bộ các hàm có gắn modifier `onlyOwner`.
3. Kiểm tra xem hàm `_update` có cài cắm các điều kiện hạn chế (`restricted`, `blacklist`) hay thu phí ẩn không.
4. Token an toàn cho cộng đồng phải có cơ chế khống chế tổng cung tối đa hoặc từ bỏ quyền sở hữu (`renounceOwnership`) sau khi tạo thanh khoản.

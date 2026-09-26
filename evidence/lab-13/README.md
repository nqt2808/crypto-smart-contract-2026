# MINH CHỨNG THỰC HÀNH LAB 13: THỰC NGHIỆM VỤ MẤT TIỀN VÀ CÁCH KHẮC PHỤC

- **Học phần:** ECO2432 — Tiền điện tử & Hợp đồng thông minh
- **Hợp đồng thực nghiệm lỗ hổng:** `contracts/training/VulnerableBank.sol`
- **Hợp đồng tấn công:** `contracts/training/Attacker.sol`
- **Hợp đồng đã vá lỗi:** `contracts/training/SafeBank.sol` (`SafeBankCEI` và `SafeBankGuard`)
- **Tập lệnh mô phỏng:** `evidence/lab-13/reentrancy_simulation.py`
- **Bộ kiểm thử gian lận của dự án:** `test/test_project_core.py` (Test Case 7)

---

## 1. Nhật ký thực nghiệm tấn công Reentrancy (Từ 6 ETH về 0 ETH)

### Kịch bản thực nghiệm:
1. **Dựng hiện trường:**
   - 3 tài khoản hợp pháp (`User 1`, `User 2`, `User 3`) mỗi người gửi 2.0 ETH vào `VulnerableBank`.
   - Tổng số dư ban đầu của ngân hàng: **6.0 ETH**.
2. **Kẻ tấn công (`Attacker`):**
   - Tài khoản thứ 4 nạp 1.0 ETH làm mồi nhử và gọi `attack()`.
   - Ngân hàng nhận 1 ETH (tổng số dư: 7.0 ETH), sau đó bắt đầu gọi `withdraw()`.
3. **Cơ chế đệ quy tái nhập (Reentrancy Loop):**
   - Ngân hàng kiểm tra `balance > 0` (đúng: 1 ETH).
   - Ngân hàng chuyển 1.0 ETH ra ngoài qua `.call{value: balance}("")`.
   - Khi nhận tiền, hàm `receive()` của hợp đồng `Attacker` lập tức kích hoạt và gọi ngược lại hàm `withdraw()` của `VulnerableBank`.
   - Vì dòng cập nhật sổ sách `balances[msg.sender] = 0` bị đặt **sau** lệnh chuyển tiền, tại thời điểm gọi lại, ngân hàng vẫn thấy kẻ tấn công còn nguyên 1.0 ETH trong tài khoản!
   - Quá trình rút tiền lặp lại 7 lần liên tiếp cho đến khi ngân hàng cạn sạch vốn.

```text
============================================================
THUC NGHIEM 1: TAN CONG REENTRANCY TREN VULNERABLEBANK
============================================================
[Buoc 1] 3 tai khoan nap moi nguoi 2 ETH.
 -> So du ban dau cua VulnerableBank: 6.0 ETH

[Buoc 2] Ke tan cong nap 1 ETH. Tong so du ngan hang: 7.0 ETH
Ke tan cong goi ham withdraw()...

 -> [Vong lap de quy 1] Ngan hang kiem tra so du ke tan cong: 1.0 ETH
    Ngan hang chuyen 1.0 ETH vao contract Attacker.
    Ham receive() cua Attacker tu dong goi lai withdraw()! So du ngan hang con lai: 6.0 ETH
 -> [Vong lap de quy 2] Ngan hang kiem tra so du ke tan cong: 1.0 ETH
    Ngan hang chuyen 1.0 ETH vao contract Attacker.
    Ham receive() cua Attacker tu dong goi lai withdraw()! So du ngan hang con lai: 5.0 ETH
 -> [Vong lap de quy 3-7] ... tiep tuc de quy rut tien ...
 -> So du VulnerableBank sau khi bi tan cong: 0.0 ETH (RUT CAN 100%)
 -> Tong so ETH ke tan cong chiem doat: 7.0 ETH (Cuom sach 6 ETH cua 3 nguoi dung)
```

---

## 2. Hai phương pháp vá lỗi và Bằng chứng phòng thủ

### Cách 1: Đổi thứ tự Checks - Effects - Interactions (Khuyên dùng)
- **Cơ chế:** Ghi nhận `balances[msg.sender] = 0` **TRƯỚC KHI** gọi lệnh `.call{value: balance}("")`.
- **Ưu điểm:** Hoàn toàn không tốn thêm gas lưu trữ trạng thái khóa (SSTORE), không phụ thuộc thư viện ngoài, giải quyết tận gốc nguyên nhân trong logic kế toán.
- **Kết quả thực nghiệm:** Khi hàm `receive()` cố tình gọi lại `withdraw()`, điều kiện `require(balance > 0)` bị vi phạm vì `balance` đã được cập nhật về 0. Giao dịch đệ quy bị `revert` ngay lập tức, ngân hàng bảo toàn nguyên vẹn 6.0 ETH.

### Cách 2: Sử dụng OpenZeppelin ReentrancyGuard (`nonReentrant`)
- **Cơ chế:** Sử dụng cờ khóa nội bộ `_status` (1: NOT_ENTERED, 2: ENTERED). Khi đang thực thi hàm, cờ chuyển sang 2. Mọi cuộc gọi tái nhập đều bị chặn đứng bởi `ReentrancyGuardReentrantCall()`.
- **Ưu điểm:** Tiện lợi, chuẩn hóa công nghiệp cho các hàm phức tạp có nhiều tương tác ngoài.

---

## 3. Ba câu trả lời trọng tâm cho Vấn đáp Giảng viên

> **Câu hỏi:** *"Vì sao thứ tự các dòng lệnh mới là thứ thực sự chặn được cuộc tấn công, chứ không phải một từ khóa nào?"*
>
> 1. *"Thứ chặn được tấn công chính là việc **cập nhật trạng thái số dư về 0 ngay lập tức trong bước Effects**, trước khi luồng điều khiển (control flow) được trao cho hợp đồng bên ngoài."*
> 2. *"Khi kẻ tấn công lợi dụng hàm nhận tiền `receive()` để gọi ngược lại (re-enter) hàm rút tiền, bước kiểm tra `Checks` ở lần gọi thứ hai đọc được số dư đã bằng 0 và buộc phải hoàn tác (revert) giao dịch ngay tại chỗ."*
> 3. *"Từ khóa hay thư viện bổ trợ bản chất cũng chỉ là một biến cờ trạng thái được đổi giá trị trước khi gọi ra ngoài; do đó **nguyên lý Checks-Effects-Interactions mới là bản chất cốt lõi của an toàn dòng tiền trong mọi hệ thống kế toán phi tập trung**."*

---

## 4. Hardening và Kiểm thử Negative trên CampusEscrow

- Trong `contracts/project/ProjectCore.sol`, toàn bộ các hàm giải ngân `confirmReceived()` và `refundAfterDeadline()` đều tuân thủ nghiêm ngặt CEI: `state` được chuyển sang `State.Completed` hoặc `State.Refunded` trước khi chuyển ETH.
- Kiểm thử `test_case_07_reentrancy_attack_attempt_blocked` trong `test/test_project_core.py` đã chứng minh: bất kỳ nỗ lực gọi lại nào cũng bị chặn đứng 100% với lỗi `WrongState(Expected=Funded, Current=Completed)`.

# MINH CHỨNG LAB 13 — VIẾT UNIT TEST & KIỂM THỬ LỖ HỔNG

- **Tập lệnh kiểm thử tự động:** [test/test_hue_legend.py](../../test/test_hue_legend.py)
- **Kết quả thực thi:** 8/8 kịch bản kiểm thử pass 100% trong 0.000s.

---

## 1. Nhật ký chạy kiểm thử Unit Tests

```text
Ran 8 tests in 0.000s - OK

[TEST 1] Nha san xuat tao lo Me xung Thien Huong...
 -> Lo hang ID #1 duoc tao thanh cong voi trang thai Created!

[TEST 2] Ke la mat thu tao lo hang khong co quyen...
 -> Bi chan dung boi AccessControl: Ke la mat khong co PRODUCER_ROLE!

[TEST 3] Don vi van chuyen cap nhat chang xe luu thong...
 -> Trang thai chuyen sang InTransit, chot kiem dinh ghi nhan thanh cong!

[TEST 4] Ke la mat gia mao chang van chuyen...
 -> Chan thanh cong: Chi LOGISTICS_ROLE moi duoc bo sung chang!

[TEST 5] Dai ly ban le tiep nhan hang tai showroom...
 -> Trang thai lo hang da chuyen thanh AtRetailer!

[TEST 6] Thu hoi lo hang phat hien su co bao quan...
 -> Lo hang da bi khoa vinh vien, khong the cap nhat them bat ky chang nao!

[TEST 7] Nguoi tieu dung quet ma QR tra cuu lich su hanh trinh...
 -> Tra cuu thanh cong 3 chang xac thuc on-chain, con han su dung va duoc bao chung 100%!

[TEST 8] Kiem thu chong tan cong leo thang dac quyen (Privilege Escalation)...
 -> Chon loc va chan dung: Chi DEFAULT_ADMIN moi co quyen cap vai tro he thong!
```

---

## 2. Đánh giá tính an toàn
Hợp đồng phòng thủ vững chắc trước các tình huống tấn công leo thang đặc quyền, mạo danh chặng vận chuyển và bảo đảm tính bất biến sau khi thu hồi.

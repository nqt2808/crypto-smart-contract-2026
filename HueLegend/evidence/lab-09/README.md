# MINH CHỨNG LAB 9 — PHÁT TRIỂN SMART CONTRACT HUELEGEND.SOL

- **Hợp đồng thông minh:** [contracts/HueLegend.sol](../../contracts/HueLegend.sol)
- **Công cụ biên dịch:** Remix IDE / Solidity Compiler `v0.8.20`
- **Kết quả:** Biên dịch thành công 0 lỗi, 0 cảnh báo.

---

## 1. Cấu trúc dữ liệu đã lập trình
- `enum BatchStatus`: `Created`, `InTransit`, `AtRetailer`, `Delivered`, `Revoked`.
- `struct TrackingStep`: Lưu mốc thời gian, địa điểm, hành động, địa chỉ ví thực hiện và ghi chú.
- `struct ProductBatch`: Lưu thông tin định danh lô hàng, tên sản phẩm, nguồn gốc xuất xứ tại Huế, ngày sản xuất và hạn sử dụng.

---

## 2. Đo lường Gas ban đầu trên Remix VM
- **Deploy:** ~1.450.000 gas
- **createBatch:** ~142.500 gas
- **addTrackingStep:** ~68.200 gas
- **getBatch / getBatchHistory:** 0 gas (view)

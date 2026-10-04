# MINH CHỨNG LAB 11 — PHÂN QUYỀN TRUY CẬP (ACCESS CONTROL)

- **Thư viện tích hợp:** OpenZeppelin Contracts v5.x (`AccessControl`)
- **Tập tin hợp đồng:** [contracts/HueLegend.sol](../../contracts/HueLegend.sol)

---

## 1. Danh mục vai trò và ma trận quyền hạn (RBAC)

| Vai trò (Role) | Hash định danh (bytes32) | Hàm được phép gọi |
|---|---|---|
| `DEFAULT_ADMIN_ROLE` | `0x00` | `grantRole`, `revokeRole`, `revokeBatch` |
| `PRODUCER_ROLE` | `keccak256("PRODUCER_ROLE")` | `createBatch`, `addTrackingStep`, `revokeBatch` |
| `LOGISTICS_ROLE` | `keccak256("LOGISTICS_ROLE")` | `addTrackingStep`, `completeDelivery` |
| `RETAILER_ROLE` | `keccak256("RETAILER_ROLE")` | `confirmAtRetailer`, `completeDelivery` |
| Người tiêu dùng (Public) | Không cần vai trò | `getBatch`, `getBatchSteps`, `isValidBatch` |

---

## 2. Kết quả kiểm tra
- [x] Không sử dụng `tx.origin`.
- [x] Revert chính xác mã lỗi `AccessControlUnauthorizedAccount` khi tài khoản không có quyền cố tình gọi hàm ghi.

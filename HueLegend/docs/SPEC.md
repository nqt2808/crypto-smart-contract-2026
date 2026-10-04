# BẢN ĐẶC TẢ YÊU CẦU NGHIỆP VỤ HỆ THỐNG TRUY XUẤT HUELEGEND (SPEC.MD)

- **Mã bài:** Lab 8 – Lab 15 (Tiền điện tử & Hợp đồng thông minh - ECO2432)
- **Tác giả:** Ngô Thị Thủy Vân & Nhóm thực hiện HueLegend
- **Phiên bản:** v1.0 (Chính thức có hiệu lực)

---

## 1. MỤC ĐÍCH
Hệ thống **HueLegend** cung cấp nền tảng sổ cái phân tán bảo chứng nguồn gốc và hành trình chuỗi cung ứng cho các đặc sản truyền thống Cố đô Huế, giúp cơ sở sản xuất khẳng định chất lượng OCOP, đơn vị vận chuyển minh bạch hóa thời gian giao nhận, đại lý quản lý tồn kho chuẩn xác và người tiêu dùng quét mã QR xác thực hàng thật tức thì trên chuỗi khối Ethereum.

---

## 2. ĐẦU VÀO (INPUTS)
1. **Dữ liệu đăng ký lô hàng (`createBatch`):**
   - Tên sản phẩm (`productName`): Chuỗi văn bản UTF-8 (ví dụ: "Mè xửng Thiên Hương Thượng Hạng").
   - Nơi sản xuất gốc (`originLocation`): Địa chỉ cơ sở chế biến tại Thừa Thiên Huế.
   - Hạn sử dụng (`expiryDate`): Mốc thời gian Unix (giây), bắt buộc lớn hơn thời điểm hiện tại.
   - Số lượng sản phẩm (`quantity`): Số nguyên dương $\ge 1$.
   - Ghi chú chất lượng (`initialNote`): Tiêu chuẩn kiểm định (OCOP, VietGAP, ISO).
2. **Dữ liệu chặng vận chuyển (`addTrackingStep`):**
   - Mã số lô hàng (`batchId`): Số nguyên dương định danh duy nhất.
   - Vị trí chốt kiểm tra (`location`): Tọa độ hoặc tên trạm kho bãi.
   - Hành động (`action`): Mô tả thao tác vận hành (Xuất xưởng, Nhập kho trung chuyển, Quá cảnh).
   - Ghi chú bảo quản (`note`): Điều kiện nhiệt độ, độ ẩm, niêm phong.
3. **Dữ liệu điểm bán lẻ (`confirmAtRetailer`):**
   - Địa chỉ showroom / đại lý bán lẻ (`retailerLocation`).
4. **Truy vấn người tiêu dùng (`getBatch`, `getBatchSteps`):**
   - Mã định danh `batchId` (nhập tay hoặc đọc tự động từ mã QR).

---

## 3. QUY TẮC NGHIỆP VỤ (BUSINESS RULES)
- **R1 (Quyền tạo lô hàng):** Chỉ có các tài khoản sở hữu vai trò `PRODUCER_ROLE` mới được phép khởi tạo lô hàng mới. Mã lô hàng `batchId` được cấp phát tăng dần tự động bắt đầu từ 1.
- **R2 (Quy tắc chặng đầu tiên):** Khi lô hàng được tạo thành công, hệ thống tự động ghi nhận Chặng số 1 là chặng xuất xưởng tại nơi sản xuất với trạng thái ban đầu `BatchStatus.Created`.
- **R3 (Quyền vận chuyển):** Chỉ các tài khoản có vai trò `LOGISTICS_ROLE` (hoặc chính `PRODUCER_ROLE`) mới được phép gọi hàm `addTrackingStep()`. Khi ghi nhận chặng vận chuyển đầu tiên, trạng thái lô hàng tự động chuyển từ `Created` sang `InTransit`.
- **R4 (Quyền đại lý bán lẻ):** Chỉ tài khoản có vai trò `RETAILER_ROLE` mới được phép gọi `confirmAtRetailer()`. Trạng thái lô hàng được cập nhật thành `AtRetailer`.
- **R5 (Xác nhận giao hàng):** Tài khoản `RETAILER_ROLE` hoặc `LOGISTICS_ROLE` được phép gọi `completeDelivery()` để chuyển trạng thái sang `Delivered` khi người tiêu dùng hoàn tất mua sắm.
- **R6 (Thu hồi khẩn cấp):** Khi phát hiện sự cố hàng lỗi, chỉ `DEFAULT_ADMIN_ROLE` hoặc chính `producer` của lô hàng mới có quyền gọi `revokeBatch()`.
- **R7 (Tính bất biến sau thu hồi):** Một khi lô hàng đã bị chuyển sang trạng thái `Revoked`, toàn bộ các hành vi ghi nhận chặng mới hoặc cập nhật trạng thái tiếp theo đều bị chặn lại vĩnh viễn.
- **R8 (Truy xuất miễn phí):** Mọi hàm đọc dữ liệu (`getBatch`, `getBatchSteps`, `isValidBatch`) đều là hàm `view`, bảo đảm người tiêu dùng tra cứu không tốn bất kỳ khoản phí gas nào.

---

## 4. ĐẦU RA (OUTPUTS)
1. **Hồ sơ định danh lô hàng on-chain:** Mã băm giao dịch (TxHash), ID lô hàng, tên đặc sản, xưởng chế biến, hạn sử dụng, trạng thái hiện tại.
2. **Timeline lịch sử chuỗi cung ứng:** Danh sách toàn bộ các chặng từ ngày giờ, vị trí địa lý, đơn vị xử lý đến ghi chú bảo quản.
3. **Mã phản hồi QR Code động:** Tạo tức thời trên giao diện Web DApp, mã hóa URL tra cứu công khai `https://.../index.html?batchId=X`.
4. **Chứng nhận chất lượng kỹ thuật số:** Huy hiệu "ĐÃ XÁC THỰC BLOCKCHAIN SEPOLIA" kèm liên kết kiểm chứng trên Sepolia Etherscan.

---

## 5. XỬ LÝ TRƯỜNG HỢP NGOẠI LỆ (EDGE CASES)
1. **Trường hợp 1 (Tài khoản không có thẩm quyền can thiệp):** Nếu người dùng không có vai trò phù hợp cố tình gọi hàm ghi dữ liệu, giao dịch revert lập tức với lỗi tùy biến `AccessControlUnauthorizedAccount(account, neededRole)`.
2. **Trường hợp 2 (Truy vấn lô hàng không tồn tại):** Nếu tra cứu `batchId` vượt quá `totalBatches` hoặc bằng 0, hệ thống báo lỗi `BatchNotFound(batchId)` rõ ràng thay vì crash giao diện.
3. **Trường hợp 3 (Cố tình cập nhật lô hàng đã bị thu hồi):** Khi gọi `addTrackingStep` hoặc `confirmAtRetailer` vào lô hàng có `status == Revoked`, hợp đồng lập tức revert `BatchAlreadyRevoked(batchId)`.
4. **Trường hợp 4 (Đăng ký hạn sử dụng trong quá khứ):** Nếu `expiryDate <= block.timestamp`, hệ thống từ chối tạo lô hàng với lỗi `ExpiryMustBeFuture(expiryDate, currentTime)`.

---

## 6. NGOÀI PHẠM VI (OUT OF SCOPE)
- Không can thiệp thanh toán tiền tệ (Fiat / Stablecoin) trong hợp đồng này; hợp đồng tập trung 100% vào nghiệp vụ bảo chứng và truy xuất nguồn gốc (Provenance).
- Chưa tích hợp cảm biến IoT tự động ký giao dịch qua Oracle (thuộc lộ trình phát triển phiên bản v2.0).

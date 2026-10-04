// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @dev Interface of the IAccessControl standard
 */
interface IAccessControl {
    function hasRole(bytes32 role, address account) external view returns (bool);
    function getRoleAdmin(bytes32 role) external view returns (bytes32);
    function grantRole(bytes32 role, address account) external;
    function revokeRole(bytes32 role, address account) external;
    function renounceRole(bytes32 role, address callerConfirmation) external;
}

/**
 * @dev OpenZeppelin 5.x compatible AccessControl implementation
 * Chuẩn phân quyền quản trị đa vai trò OpenZeppelin v5.x không dùng tx.origin
 */
abstract contract Context {
    function _msgSender() internal view virtual returns (address) {
        return msg.sender;
    }
}

abstract contract AccessControl is Context, IAccessControl {
    struct RoleData {
        mapping(address => bool) hasRole;
        bytes32 adminRole;
    }

    mapping(bytes32 => RoleData) private _roles;

    bytes32 public constant DEFAULT_ADMIN_ROLE = 0x00;

    event RoleAdminChanged(bytes32 indexed role, bytes32 indexed previousAdminRole, bytes32 indexed newAdminRole);
    event RoleGranted(bytes32 indexed role, address indexed account, address indexed sender);
    event RoleRevoked(bytes32 indexed role, address indexed account, address indexed sender);

    error AccessControlUnauthorizedAccount(address account, bytes32 neededRole);
    error AccessControlBadConfirmation();

    modifier onlyRole(bytes32 role) {
        _checkRole(role);
        _;
    }

    function hasRole(bytes32 role, address account) public view virtual override returns (bool) {
        return _roles[role].hasRole[account];
    }

    function _checkRole(bytes32 role) internal view virtual {
        _checkRole(role, _msgSender());
    }

    function _checkRole(bytes32 role, address account) internal view virtual {
        if (!hasRole(role, account)) {
            revert AccessControlUnauthorizedAccount(account, role);
        }
    }

    function getRoleAdmin(bytes32 role) public view virtual override returns (bytes32) {
        return _roles[role].adminRole;
    }

    function grantRole(bytes32 role, address account) public virtual override onlyRole(getRoleAdmin(role)) {
        _grantRole(role, account);
    }

    function revokeRole(bytes32 role, address account) public virtual override onlyRole(getRoleAdmin(role)) {
        _revokeRole(role, account);
    }

    function renounceRole(bytes32 role, address callerConfirmation) public virtual override {
        if (callerConfirmation != _msgSender()) {
            revert AccessControlBadConfirmation();
        }
        _revokeRole(role, callerConfirmation);
    }

    function _setRoleAdmin(bytes32 role, bytes32 adminRole) internal virtual {
        bytes32 previousAdminRole = getRoleAdmin(role);
        _roles[role].adminRole = adminRole;
        emit RoleAdminChanged(role, previousAdminRole, adminRole);
    }

    function _grantRole(bytes32 role, address account) internal virtual {
        if (!hasRole(role, account)) {
            _roles[role].hasRole[account] = true;
            emit RoleGranted(role, account, _msgSender());
        }
    }

    function _revokeRole(bytes32 role, address account) internal virtual {
        if (hasRole(role, account)) {
            _roles[role].hasRole[account] = false;
            emit RoleRevoked(role, account, _msgSender());
        }
    }
}

/// @title HueLegend - He thong truy xuat nguon goc dac san Co do Hue tren Blockchain
/// @author Ngo Thi Thuy Van & Nhóm sinh viên K57 Kinh tế Số
/// @notice Quan ly vong doi lo hang dac san tu nha san xuat, van chuyen den dai ly va nguoi tieu dung
contract HueLegend is AccessControl {

    // --- DINH NGHIA VAI TRO (ROLES) ---
    bytes32 public constant PRODUCER_ROLE = keccak256("PRODUCER_ROLE");
    bytes32 public constant LOGISTICS_ROLE = keccak256("LOGISTICS_ROLE");
    bytes32 public constant RETAILER_ROLE = keccak256("RETAILER_ROLE");

    // --- TRANG THAI LO HANG (BATCH STATUS) ---
    enum BatchStatus {
        Created,     // 0: Vua tao tai xuong san xuat Hue
        InTransit,   // 1: Dang tren duong van chuyen
        AtRetailer,  // 2: Da den dai ly ban le / showroom
        Delivered,   // 3: Da giao den tay nguoi tieu dung
        Revoked      // 4: Bi thu hoi do su co chat luong / gian lan
    }

    // --- CAU TRUC DU LIEU (DATA STRUCTURES) ---
    struct TrackingStep {
        uint256 timestamp;
        string location;
        string action;
        address handler;
        string note;
    }

    struct ProductBatch {
        uint256 batchId;
        string productName;
        string originLocation;
        uint256 productionDate;
        uint256 expiryDate;
        uint256 quantity;
        BatchStatus status;
        address producer;
        address currentHandler;
    }

    // --- BIEN TRANG THAI ---
    uint256 public totalBatches;
    mapping(uint256 => ProductBatch) private _batches;
    mapping(uint256 => TrackingStep[]) private _batchSteps;

    // --- SU KIEN ON-CHAIN (EVENTS) ---
    event BatchCreated(uint256 indexed batchId, string productName, address indexed producer, uint256 quantity, uint256 productionDate);
    event TrackingStepAdded(uint256 indexed batchId, string location, string action, address indexed handler, uint256 timestamp);
    event BatchStatusUpdated(uint256 indexed batchId, BatchStatus indexed oldStatus, BatchStatus indexed newStatus, address handler);
    event BatchRevoked(uint256 indexed batchId, string reason, address indexed authority);

    // --- CUSTOM ERRORS ---
    error BatchNotFound(uint256 batchId);
    error BatchAlreadyRevoked(uint256 batchId);
    error InvalidBatchStatus(BatchStatus expected, BatchStatus current);
    error InvalidInput(string fieldName);
    error ExpiryMustBeFuture(uint256 expiryDate, uint256 currentTime);

    constructor() {
        // Nguoi trien khai tro thanh Quan tri vien mac dinh
        _grantRole(DEFAULT_ADMIN_ROLE, _msgSender());
        // Cap quyen Producer mac dinh cho deployer de thuan tien khoi tao
        _grantRole(PRODUCER_ROLE, _msgSender());
    }

    /// @notice Nha san xuat khoi tao lo hang dac san moi
    /// @param _productName Ten dac san (vi du: Me xung Thien Huong, Tinh dau tram Loc Thuy,...)
    /// @param _originLocation Dia chi xuong che bien tai Thua Thien Hue
    /// @param _expiryDate Thoi diem het han (Unix timestamp)
    /// @param _quantity So luong san pham trong lo
    /// @param _initialNote Ghi chu lo hang ban dau
    function createBatch(
        string calldata _productName,
        string calldata _originLocation,
        uint256 _expiryDate,
        uint256 _quantity,
        string calldata _initialNote
    ) external onlyRole(PRODUCER_ROLE) returns (uint256) {
        if (bytes(_productName).length == 0) revert InvalidInput("productName");
        if (bytes(_originLocation).length == 0) revert InvalidInput("originLocation");
        if (_quantity == 0) revert InvalidInput("quantity");
        if (_expiryDate <= block.timestamp) revert ExpiryMustBeFuture(_expiryDate, block.timestamp);

        totalBatches += 1;
        uint256 newId = totalBatches;

        ProductBatch storage batch = _batches[newId];
        batch.batchId = newId;
        batch.productName = _productName;
        batch.originLocation = _originLocation;
        batch.productionDate = block.timestamp;
        batch.expiryDate = _expiryDate;
        batch.quantity = _quantity;
        batch.status = BatchStatus.Created;
        batch.producer = _msgSender();
        batch.currentHandler = _msgSender();

        // Ghi nhan chặng dau tien: Xuat xuong
        _batchSteps[newId].push(TrackingStep({
            timestamp: block.timestamp,
            location: _originLocation,
            action: "KHOI TAO SAN XUAT TAI HUE",
            handler: _msgSender(),
            note: bytes(_initialNote).length > 0 ? _initialNote : "Xac thuc lo hang dat tieu chuan OCOP Hue"
        }));

        emit BatchCreated(newId, _productName, _msgSender(), _quantity, block.timestamp);
        emit TrackingStepAdded(newId, _originLocation, "KHOI TAO SAN XUAT", _msgSender(), block.timestamp);

        return newId;
    }

    /// @notice Bo sung chang van chuyen luu thong
    /// @param _batchId Ma so lo hang
    /// @param _location Vi tri chot kiem tra / kho trung chuyen
    /// @param _action Hanh dong (vi du: "Nhap kho Da Nang", "Roi tram kiem dinh")
    /// @param _note Ghi chu tinh trang bao quan (Nhiet do, do am)
    function addTrackingStep(
        uint256 _batchId,
        string calldata _location,
        string calldata _action,
        string calldata _note
    ) external {
        if (!hasRole(LOGISTICS_ROLE, _msgSender()) && !hasRole(PRODUCER_ROLE, _msgSender())) {
            revert AccessControlUnauthorizedAccount(_msgSender(), LOGISTICS_ROLE);
        }

        ProductBatch storage batch = _batches[_batchId];
        if (batch.batchId == 0) revert BatchNotFound(_batchId);
        if (batch.status == BatchStatus.Revoked) revert BatchAlreadyRevoked(_batchId);

        // Cap nhat trang thai sang InTransit neu dang o Created
        if (batch.status == BatchStatus.Created) {
            batch.status = BatchStatus.InTransit;
            emit BatchStatusUpdated(_batchId, BatchStatus.Created, BatchStatus.InTransit, _msgSender());
        }

        batch.currentHandler = _msgSender();

        _batchSteps[_batchId].push(TrackingStep({
            timestamp: block.timestamp,
            location: _location,
            action: _action,
            handler: _msgSender(),
            note: _note
        }));

        emit TrackingStepAdded(_batchId, _location, _action, _msgSender(), block.timestamp);
    }

    /// @notice Dai ly ban le xac nhan tiep nhan lo hang tai showroom
    /// @param _batchId Ma so lo hang
    /// @param _retailerLocation Dia chi cua hang / showroom ban le
    /// @param _note Ghi chu kiem dem niem phong
    function confirmAtRetailer(
        uint256 _batchId,
        string calldata _retailerLocation,
        string calldata _note
    ) external onlyRole(RETAILER_ROLE) {
        ProductBatch storage batch = _batches[_batchId];
        if (batch.batchId == 0) revert BatchNotFound(_batchId);
        if (batch.status == BatchStatus.Revoked) revert BatchAlreadyRevoked(_batchId);

        BatchStatus oldStatus = batch.status;
        batch.status = BatchStatus.AtRetailer;
        batch.currentHandler = _msgSender();

        _batchSteps[_batchId].push(TrackingStep({
            timestamp: block.timestamp,
            location: _retailerLocation,
            action: "NHAP KHO DAI LY BAN LE",
            handler: _msgSender(),
            note: _note
        }));

        emit BatchStatusUpdated(_batchId, oldStatus, BatchStatus.AtRetailer, _msgSender());
        emit TrackingStepAdded(_batchId, _retailerLocation, "NHAP KHO DAI LY", _msgSender(), block.timestamp);
    }

    /// @notice Xac nhan da giao hang den tay nguoi tieu dung cuoi
    function completeDelivery(uint256 _batchId, string calldata _finalNote) external {
        if (!hasRole(RETAILER_ROLE, _msgSender()) && !hasRole(LOGISTICS_ROLE, _msgSender())) {
            revert AccessControlUnauthorizedAccount(_msgSender(), RETAILER_ROLE);
        }

        ProductBatch storage batch = _batches[_batchId];
        if (batch.batchId == 0) revert BatchNotFound(_batchId);
        if (batch.status == BatchStatus.Revoked) revert BatchAlreadyRevoked(_batchId);

        BatchStatus oldStatus = batch.status;
        batch.status = BatchStatus.Delivered;
        batch.currentHandler = _msgSender();

        _batchSteps[_batchId].push(TrackingStep({
            timestamp: block.timestamp,
            location: "DIEM TIEU DUNG",
            action: "DA GIAO DEN KHACH HANG",
            handler: _msgSender(),
            note: _finalNote
        }));

        emit BatchStatusUpdated(_batchId, oldStatus, BatchStatus.Delivered, _msgSender());
        emit TrackingStepAdded(_batchId, "DIEM TIEU DUNG", "DA GIAO HANG", _msgSender(), block.timestamp);
    }

    /// @notice Thu hoi lo hang khong dat tieu chuan (Admin hoac Producer)
    function revokeBatch(uint256 _batchId, string calldata _reason) external {
        ProductBatch storage batch = _batches[_batchId];
        if (batch.batchId == 0) revert BatchNotFound(_batchId);
        if (batch.status == BatchStatus.Revoked) revert BatchAlreadyRevoked(_batchId);

        // Chi admin hoac chinh Producer tao ra lo hang moi duoc quyen thu hoi
        if (!hasRole(DEFAULT_ADMIN_ROLE, _msgSender()) && batch.producer != _msgSender()) {
            revert AccessControlUnauthorizedAccount(_msgSender(), DEFAULT_ADMIN_ROLE);
        }

        batch.status = BatchStatus.Revoked;

        _batchSteps[_batchId].push(TrackingStep({
            timestamp: block.timestamp,
            location: "HE THONG KIEM DINH",
            action: "THU HOI LO HANG",
            handler: _msgSender(),
            note: _reason
        }));

        emit BatchRevoked(_batchId, _reason, _msgSender());
    }

    // --- HAM TRA CUU CONG KHAI CHO NGUOI TIEU DUNG (GAS = 0) ---

    /// @notice Tra cuu thong tin tong quan lo hang
    function getBatch(uint256 _batchId) external view returns (ProductBatch memory) {
        ProductBatch memory batch = _batches[_batchId];
        if (batch.batchId == 0) revert BatchNotFound(_batchId);
        return batch;
    }

    /// @notice Tra cuu toan bo lich su cac chang luu thong on-chain
    function getBatchSteps(uint256 _batchId) external view returns (TrackingStep[] memory) {
        if (_batches[_batchId].batchId == 0) revert BatchNotFound(_batchId);
        return _batchSteps[_batchId];
    }

    /// @notice Dem tong so chang da qua
    function getStepCount(uint256 _batchId) external view returns (uint256) {
        if (_batches[_batchId].batchId == 0) revert BatchNotFound(_batchId);
        return _batchSteps[_batchId].length;
    }

    /// @notice Kiem tra tinh hop le cua lo hang (Ton tai, chua bi thu hoi, con han su dung)
    function isValidBatch(uint256 _batchId) external view returns (bool) {
        ProductBatch memory batch = _batches[_batchId];
        if (batch.batchId == 0) return false;
        if (batch.status == BatchStatus.Revoked) return false;
        if (block.timestamp > batch.expiryDate) return false;
        return true;
    }
}

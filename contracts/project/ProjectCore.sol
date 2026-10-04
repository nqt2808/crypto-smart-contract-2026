// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title CampusEscrow - Hop dong ky quy mua ban do cu KTX sinh vien (Co thu phi quy KTX)
/// @notice Core Escrow contract for dormitory secondhand item trading with 1% KTX fee & DoS resilience
contract CampusEscrow {
    enum State {
        Created,
        Funded,
        Completed,
        Refunded
    }

    // Bien trang thai bat bien va luu tru
    address public immutable seller;
    address public immutable feeRecipient; // Vi quy KTX nhan phi duy tri
    uint256 public constant feeBps = 100;   // 100 diem co ban = 1.00%
    string public itemDescription;         // Mo ta mon do cu (Quat dien, Tu lanh mini,...)
    address public buyer;
    uint256 public immutable price;
    uint256 public immutable daysToConfirm;
    uint256 public deadline;
    State public state;

    // Su kien on-chain
    event Created(address indexed seller, string itemDescription, uint256 price, uint256 daysToConfirm, address indexed feeRecipient);
    event Funded(address indexed buyer, uint256 amount, uint256 deadline);
    event FeeCollected(address indexed recipient, uint256 feeAmount);
    event FeeTransferFailed(address indexed recipient, uint256 feeAmount);
    event Completed(address indexed seller, uint256 sellerAmount);
    event Refunded(address indexed buyer, uint256 refundAmount);

    // Dinh danh loi tuy bien (Custom Errors)
    error InvalidAddress();
    error ZeroPrice();
    error PriceTooLow(uint256 minPrice);
    error InvalidDuration(uint256 min, uint256 max);
    error WrongState(State expected, State current);
    error WrongAmount(uint256 expected, uint256 sent);
    error NotBuyer();
    error NotSeller();
    error NotAuthorized();
    error BuyerCannotBeSeller();
    error DeadlineNotReached(uint256 unlockTime, uint256 currentTime);
    error TransferFailed();

    /// @notice Khoi tao don hang ky quy mua ban do cu KTX
    /// @param _seller Dia chi vi nguoi ban
    /// @param _itemDescription Mo ta ngan gon mon do duoc rao ban
    /// @param _price Gia niem yet cua san pham (wei, toi thieu 10,000 wei de tinh phi)
    /// @param _daysToConfirm So ngay nguoi mua co de kiem tra hang (1 den 14 ngay)
    /// @param _feeRecipient Dia chi vi quy tu quan KTX
    constructor(
        address _seller,
        string memory _itemDescription,
        uint256 _price,
        uint256 _daysToConfirm,
        address _feeRecipient
    ) {
        if (_seller == address(0) || _feeRecipient == address(0)) revert InvalidAddress();
        if (_price == 0) revert ZeroPrice();
        if (_price < 10_000) revert PriceTooLow(10_000);
        if (_daysToConfirm < 1 || _daysToConfirm > 14) revert InvalidDuration(1, 14);

        seller = _seller;
        itemDescription = _itemDescription;
        price = _price;
        daysToConfirm = _daysToConfirm;
        feeRecipient = _feeRecipient;
        state = State.Created;

        emit Created(_seller, _itemDescription, _price, _daysToConfirm, _feeRecipient);
    }

    /// @notice Nguoi mua khoa tien coc vao hop dong
    function fund() external payable {
        // 1. Checks
        if (state != State.Created) revert WrongState(State.Created, state);
        if (msg.sender == seller) revert BuyerCannotBeSeller();
        if (msg.value != price) revert WrongAmount(price, msg.value);

        // 2. Effects
        buyer = msg.sender;
        state = State.Funded;
        deadline = block.timestamp + (daysToConfirm * 1 days);

        emit Funded(msg.sender, msg.value, deadline);
    }

    /// @notice Nguoi mua xac nhan da nhan do, tien duoc phan bo cho seller va quy KTX
    function confirmReceived() external {
        // 1. Checks
        if (state != State.Funded) revert WrongState(State.Funded, state);
        if (msg.sender != buyer) revert NotBuyer();

        // 2. Effects (Checks-Effects-Interactions: Cap nhat trang thai truoc)
        state = State.Completed;

        uint256 fee = (price * feeBps) / 10_000;
        uint256 sellerAmount = price - fee;

        // 3. Interactions (Chuyen tien ra ngoai sau cung)
        if (fee > 0) {
            (bool feeOk, ) = payable(feeRecipient).call{value: fee}("");
            if (feeOk) {
                emit FeeCollected(feeRecipient, fee);
            } else {
                // Phong thu DoS: Neu vi quy KTX tu choi nhan tien, gop phi tra lai cho seller
                sellerAmount += fee;
                emit FeeTransferFailed(feeRecipient, fee);
            }
        }

        emit Completed(seller, sellerAmount);

        (bool sellerOk, ) = payable(seller).call{value: sellerAmount}("");
        if (!sellerOk) revert TransferFailed();
    }

    /// @notice Qua han xac nhan ma chua hoan tat thi hoan tien 100% cho nguoi mua
    function refundAfterDeadline() external {
        // 1. Checks
        if (state != State.Funded) revert WrongState(State.Funded, state);
        if (msg.sender != buyer && msg.sender != seller) revert NotAuthorized();
        if (block.timestamp < deadline) revert DeadlineNotReached(deadline, block.timestamp);

        // 2. Effects
        state = State.Refunded;
        uint256 refundAmount = price;

        emit Refunded(buyer, refundAmount);

        // 3. Interactions
        (bool ok, ) = payable(buyer).call{value: refundAmount}("");
        if (!ok) revert TransferFailed();
    }

    /// @notice Xem thoi gian con lai truoc khi het han hoan tien (giay)
    function timeLeft() external view returns (uint256) {
        if (state != State.Funded) return 0;
        if (block.timestamp >= deadline) return 0;
        return deadline - block.timestamp;
    }
}

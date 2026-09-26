// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title CampusEscrow - Hop dong ky quy mua ban do cu KTX sinh vien
/// @notice Core Escrow contract for dormitory secondhand item trading
contract CampusEscrow {
    enum State {
        Created,
        Funded,
        Completed,
        Refunded
    }

    // Bien trang thai bat bien va luu tru
    address public immutable seller;
    address public buyer;
    uint256 public immutable price;
    uint256 public immutable daysToConfirm;
    uint256 public deadline;
    State public state;

    // Su kien on-chain
    event Created(address indexed seller, uint256 price, uint256 daysToConfirm);
    event Funded(address indexed buyer, uint256 amount, uint256 deadline);
    event Completed(address indexed seller, uint256 amount);
    event Refunded(address indexed buyer, uint256 amount);

    // Dinh danh loi tuy bien (Custom Errors)
    error InvalidAddress();
    error ZeroPrice();
    error InvalidDuration(uint256 min, uint256 max);
    error WrongState(State expected, State current);
    error WrongAmount(uint256 expected, uint256 sent);
    error NotBuyer();
    error NotSeller();
    error NotAuthorized();
    error BuyerCannotBeSeller();
    error DeadlineNotReached(uint256 unlockTime, uint256 currentTime);
    error TransferFailed();

    /// @notice Khoi tao don hang ky quy mua ban do cu
    /// @param _seller Dia chi vi nguoi ban do
    /// @param _price Gia niem yet cua san pham (wei)
    /// @param _daysToConfirm So ngay nguoi mua co de kiem tra va xac nhan (1 den 14 ngay)
    constructor(address _seller, uint256 _price, uint256 _daysToConfirm) {
        if (_seller == address(0)) revert InvalidAddress();
        if (_price == 0) revert ZeroPrice();
        if (_daysToConfirm < 1 || _daysToConfirm > 14) revert InvalidDuration(1, 14);

        seller = _seller;
        price = _price;
        daysToConfirm = _daysToConfirm;
        state = State.Created;

        emit Created(_seller, _price, _daysToConfirm);
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

    /// @notice Nguoi mua xac nhan da nhan do, tien ve tay nguoi ban
    function confirmReceived() external {
        // 1. Checks
        if (state != State.Funded) revert WrongState(State.Funded, state);
        if (msg.sender != buyer) revert NotBuyer();

        // 2. Effects (Cap nhat trang thai truoc khi chuyen tien)
        state = State.Completed;
        uint256 amount = price;

        emit Completed(seller, amount);

        // 3. Interactions (Chuyen tien ra ngoai sau cung)
        (bool ok, ) = payable(seller).call{value: amount}("");
        if (!ok) revert TransferFailed();
    }

    /// @notice Qua han xac nhan ma chua hoan tat thi hoan tien cho nguoi mua
    function refundAfterDeadline() external {
        // 1. Checks
        if (state != State.Funded) revert WrongState(State.Funded, state);
        if (msg.sender != buyer && msg.sender != seller) revert NotAuthorized();
        if (block.timestamp < deadline) revert DeadlineNotReached(deadline, block.timestamp);

        // 2. Effects
        state = State.Refunded;
        uint256 amount = price;

        emit Refunded(buyer, amount);

        // 3. Interactions
        (bool ok, ) = payable(buyer).call{value: amount}("");
        if (!ok) revert TransferFailed();
    }

    /// @notice Xem thoi gian con lai truoc khi het han hoan tien (giay)
    function timeLeft() external view returns (uint256) {
        if (state != State.Funded) return 0;
        if (block.timestamp >= deadline) return 0;
        return deadline - block.timestamp;
    }
}

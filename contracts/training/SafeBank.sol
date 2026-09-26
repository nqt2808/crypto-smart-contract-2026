// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/utils/ReentrancyGuard.sol";

/// @title SafeBankCEI - Ngan hang an toan nho doi thu tu Checks-Effects-Interactions
/// @notice Khong can thu vien phu, khong ton them gas luu tru, chan reentrancy nho thu tu lenh
contract SafeBankCEI {
    mapping(address => uint256) public balances;

    event Deposited(address indexed user, uint256 amount);
    event Withdrawn(address indexed user, uint256 amount);

    function deposit() external payable {
        require(msg.value > 0, "So tien phai lon hon 0");
        balances[msg.sender] += msg.value;
        emit Deposited(msg.sender, msg.value);
    }

    function withdraw() external {
        // 1. Checks: Kiem tra dieu kien
        uint256 balance = balances[msg.sender];
        require(balance > 0, "Khong co so du");

        // 2. Effects: CAP NHAT SO SACH TRUOC KHI CHUYEN TIEN
        balances[msg.sender] = 0;
        emit Withdrawn(msg.sender, balance);

        // 3. Interactions: Chuyen tien ra ngoai sau cung
        (bool ok, ) = msg.sender.call{value: balance}("");
        require(ok, "Chuyen that bai");
    }

    function bankBalance() external view returns (uint256) {
        return address(this).balance;
    }
}

/// @title SafeBankGuard - Ngan hang dung khoa chong goi lai ReentrancyGuard cua OpenZeppelin
contract SafeBankGuard is ReentrancyGuard {
    mapping(address => uint256) public balances;

    event Deposited(address indexed user, uint256 amount);
    event Withdrawn(address indexed user, uint256 amount);

    function deposit() external payable {
        require(msg.value > 0, "So tien phai lon hon 0");
        balances[msg.sender] += msg.value;
        emit Deposited(msg.sender, msg.value);
    }

    /// @notice Khoa modifier nonReentrant ngan chan moi cu goi de quy tai nhap
    function withdraw() external nonReentrant {
        uint256 balance = balances[msg.sender];
        require(balance > 0, "Khong co so du");

        balances[msg.sender] = 0;
        emit Withdrawn(msg.sender, balance);

        (bool ok, ) = msg.sender.call{value: balance}("");
        require(ok, "Chuyen that bai");
    }

    function bankBalance() external view returns (uint256) {
        return address(this).balance;
    }
}

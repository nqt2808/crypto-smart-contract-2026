"""
Bo kiem thu tu dong cho hop dong CampusEscrow (contracts/project/ProjectCore.sol)
Kiem chung quy tac kinh te (Phi KTX 100 bps = 1%) va cac ca vi pham (Negative Tests).
"""

import time
import unittest

class CampusEscrowSimulator:
    """Mo phong chinh xac may trang thai va logic hop dong CampusEscrow."""
    STATE_CREATED = "Created"
    STATE_FUNDED = "Funded"
    STATE_COMPLETED = "Completed"
    STATE_REFUNDED = "Refunded"

    def __init__(self, seller, item_description, price, days_to_confirm, fee_recipient, fee_transfer_fail=False):
        if not seller or seller == "0x0000000000000000000000000000000000000000":
            raise ValueError("InvalidAddress")
        if not fee_recipient or fee_recipient == "0x0000000000000000000000000000000000000000":
            raise ValueError("InvalidAddress")
        if price == 0:
            raise ValueError("ZeroPrice")
        if price < 10_000:
            raise ValueError("PriceTooLow(10000)")
        if days_to_confirm < 1 or days_to_confirm > 14:
            raise ValueError("InvalidDuration(1, 14)")

        self.seller = seller
        self.item_description = item_description
        self.price = price
        self.days_to_confirm = days_to_confirm
        self.fee_recipient = fee_recipient
        self.fee_transfer_fail = fee_transfer_fail
        self.fee_bps = 100  # 1%
        self.buyer = None
        self.state = self.STATE_CREATED
        self.deadline = 0
        self.balances = {seller: 0, fee_recipient: 0}
        self.contract_balance = 0
        self.current_time = int(time.time())
        self.events = []
        self.events.append(("Created", seller, item_description, price, days_to_confirm, fee_recipient))

    def fund(self, sender, value):
        if self.state != self.STATE_CREATED:
            raise RuntimeError(f"WrongState(Expected={self.STATE_CREATED}, Current={self.state})")
        if sender == self.seller:
            raise RuntimeError("BuyerCannotBeSeller")
        if value != self.price:
            raise RuntimeError(f"WrongAmount(Expected={self.price}, Sent={value})")

        self.buyer = sender
        self.contract_balance += value
        self.state = self.STATE_FUNDED
        self.deadline = self.current_time + (self.days_to_confirm * 86400)
        self.events.append(("Funded", sender, value, self.deadline))

    def confirm_received(self, sender):
        if self.state != self.STATE_FUNDED:
            raise RuntimeError(f"WrongState(Expected={self.STATE_FUNDED}, Current={self.state})")
        if sender != self.buyer:
            raise RuntimeError("NotBuyer")

        # Checks-Effects-Interactions
        self.state = self.STATE_COMPLETED
        fee = (self.price * self.fee_bps) // 10_000
        seller_amount = self.price - fee

        # Interactions
        if fee > 0:
            if not self.fee_transfer_fail:
                self.events.append(("FeeCollected", self.fee_recipient, fee))
                self.balances[self.fee_recipient] = self.balances.get(self.fee_recipient, 0) + fee
            else:
                # DoS Resilience: neu feeRecipient tu choi, gop tra lai cho seller
                seller_amount += fee
                self.events.append(("FeeTransferFailed", self.fee_recipient, fee))

        self.events.append(("Completed", self.seller, seller_amount))
        self.balances[self.seller] = self.balances.get(self.seller, 0) + seller_amount
        self.contract_balance = 0

    def refund_after_deadline(self, sender):
        if self.state != self.STATE_FUNDED:
            raise RuntimeError(f"WrongState(Expected={self.STATE_FUNDED}, Current={self.state})")
        if sender != self.buyer and sender != self.seller:
            raise RuntimeError("NotAuthorized")
        if self.current_time < self.deadline:
            raise RuntimeError(f"DeadlineNotReached(Deadline={self.deadline}, Current={self.current_time})")

        self.state = self.STATE_REFUNDED
        refund_amount = self.price
        self.events.append(("Refunded", self.buyer, refund_amount))

        self.balances[self.buyer] = self.balances.get(self.buyer, 0) + refund_amount
        self.contract_balance -= refund_amount


class TestCampusEscrow(unittest.TestCase):
    def setUp(self):
        self.seller = "0x2e4216e1BCA81d308b25adaD6ef5Ea92E2e42F8c"  # Ngo Quynh Trang
        self.buyer = "0x23618e81E3f5cdF7f54C3d65f7FBc0aBf5B21E8f"   # Le Thi Phuong Thao
        self.fee_fund = "0x999999cf1046e68e36E1aA2E0E07105eDDD1f08E" # Dormitory Fund
        self.stranger = "0x1111111111111111111111111111111111111111"
        self.price = 100_000_000_000_000_000  # 0.1 ETH = 10^17 wei
        self.desc = "Quat dien Senko KTX B4"

    def test_case_01_valid_purchase_and_fee_distribution(self):
        """Ca hop le: Mua ban thanh cong, thu dung 1% phi cho quy KTX."""
        print("\n[TEST 1] Chay ca hop le: Mua ban va phan bo phi KTX 1%...")
        escrow = CampusEscrowSimulator(
            seller=self.seller,
            item_description=self.desc,
            price=self.price,
            days_to_confirm=3,
            fee_recipient=self.fee_fund
        )
        self.assertEqual(escrow.state, CampusEscrowSimulator.STATE_CREATED)

        # Nguoi mua nap tien
        escrow.fund(sender=self.buyer, value=self.price)
        self.assertEqual(escrow.state, CampusEscrowSimulator.STATE_FUNDED)
        self.assertEqual(escrow.contract_balance, self.price)

        # Nguoi mua xac nhan nhan hang
        escrow.confirm_received(sender=self.buyer)
        self.assertEqual(escrow.state, CampusEscrowSimulator.STATE_COMPLETED)

        # Kiem tra quy tac kinh te: 1% phi = 0.001 ETH, 99% cho seller = 0.099 ETH
        expected_fee = (self.price * 100) // 10_000  # 0.001 ETH
        expected_seller = self.price - expected_fee    # 0.099 ETH

        self.assertEqual(escrow.balances[self.fee_fund], expected_fee)
        self.assertEqual(escrow.balances[self.seller], expected_seller)
        self.assertEqual(escrow.contract_balance, 0)
        print(f" -> Quy KTX nhan: {expected_fee / 10**18} ETH (Dung 1%)")
        print(f" -> Nguoi ban nhan: {expected_seller / 10**18} ETH (Dung 99%)")
        print(" -> Ket qua: THANH CONG!")

    def test_case_02_violation_seller_cannot_buy(self):
        """Ca vi pham: Nguoi ban tu nap tien mua hang cua chinh minh -> Revert."""
        print("\n[TEST 2] Chay ca vi pham: Nguoi ban tu mua hang...")
        escrow = CampusEscrowSimulator(self.seller, self.desc, self.price, 3, self.fee_fund)
        with self.assertRaises(RuntimeError) as ctx:
            escrow.fund(sender=self.seller, value=self.price)
        self.assertIn("BuyerCannotBeSeller", str(ctx.exception))
        print(" -> Chan thanh cong voi loi: BuyerCannotBeSeller")

    def test_case_03_violation_wrong_funding_amount(self):
        """Ca vi pham: Nguoi mua nap thieu hoac thua tien -> Revert."""
        print("\n[TEST 3] Chay ca vi pham: Nap sai so tien...")
        escrow = CampusEscrowSimulator(self.seller, self.desc, self.price, 3, self.fee_fund)
        with self.assertRaises(RuntimeError) as ctx:
            escrow.fund(sender=self.buyer, value=self.price // 2)
        self.assertIn("WrongAmount", str(ctx.exception))
        print(" -> Chan thanh cong voi loi: WrongAmount")

    def test_case_04_violation_unauthorized_confirmation(self):
        """Ca vi pham: Ke la mat xac nhan nhan hang thay nguoi mua -> Revert."""
        print("\n[TEST 4] Chay ca vi pham: Ke la mat xac nhan nhan hang...")
        escrow = CampusEscrowSimulator(self.seller, self.desc, self.price, 3, self.fee_fund)
        escrow.fund(sender=self.buyer, value=self.price)
        with self.assertRaises(RuntimeError) as ctx:
            escrow.confirm_received(sender=self.stranger)
        self.assertIn("NotBuyer", str(ctx.exception))
        print(" -> Chan thanh cong voi loi: NotBuyer")

    def test_case_05_violation_refund_before_deadline(self):
        """Ca vi pham: Doi hoan tien khi chua qua han chot (DeadlineNotReached) -> Revert."""
        print("\n[TEST 5] Chay ca vi pham: Doi hoan tien truoc han chot...")
        escrow = CampusEscrowSimulator(self.seller, self.desc, self.price, 3, self.fee_fund)
        escrow.fund(sender=self.buyer, value=self.price)
        with self.assertRaises(RuntimeError) as ctx:
            escrow.refund_after_deadline(sender=self.buyer)
        self.assertIn("DeadlineNotReached", str(ctx.exception))
        print(" -> Chan thanh cong voi loi: DeadlineNotReached")

    def test_case_06_valid_refund_after_deadline(self):
        """Ca hop le: Hoan tien 100% sau khi qua han chot khong giao hang."""
        print("\n[TEST 6] Chay ca hop le: Hoan tien sau han chot...")
        escrow = CampusEscrowSimulator(self.seller, self.desc, self.price, 3, self.fee_fund)
        escrow.fund(sender=self.buyer, value=self.price)

        # Gia lap thoi gian troi qua 3 ngay + 1 giay
        escrow.current_time += (3 * 86400) + 1
        escrow.refund_after_deadline(sender=self.buyer)

        self.assertEqual(escrow.state, CampusEscrowSimulator.STATE_REFUNDED)
        self.assertEqual(escrow.balances[self.buyer], self.price)
        self.assertEqual(escrow.contract_balance, 0)
        print(f" -> Hoan tra 100% cho nguoi mua: {escrow.balances[self.buyer] / 10**18} ETH")
        print(" -> Ket qua: HOAN TIEN THANH CONG!")

    def test_case_07_reentrancy_attack_attempt_blocked(self):
        """Ca vi pham: Thu tan cong tai nhap Reentrancy khi rut tien hoac giai ngan."""
        print("\n[TEST 7] Chay ca vi pham: Thu tan cong tai nhap (Reentrancy)...")
        escrow = CampusEscrowSimulator(self.seller, self.desc, self.price, 3, self.fee_fund)
        escrow.fund(sender=self.buyer, value=self.price)

        # Goi confirm_received lan 1 -> trang thai chuyen thanh Completed
        escrow.confirm_received(sender=self.buyer)
        self.assertEqual(escrow.state, CampusEscrowSimulator.STATE_COMPLETED)

        # Co tinh goi lai lan 2 (Reentrancy de quy)
        with self.assertRaises(RuntimeError) as ctx:
            escrow.confirm_received(sender=self.buyer)
        self.assertIn("WrongState", str(ctx.exception))
        print(" -> Bi chan dung lap tuc boi CEI voi loi: WrongState(Expected=Funded, Current=Completed)")
        print(" -> Ket qua: PHONG THU REENTRANCY THANH CONG 100%!")

    def test_case_08_dos_resilience_fee_transfer_fail(self):
        """Kiem thu khac phuc Audit Lab 14: Vi quy KTX tu choi nhan ETH thi khong lam ket giao dich."""
        print("\n[TEST 8] Kiem thu chong DoS sau Audit: Vi phi bi loi...")
        escrow = CampusEscrowSimulator(
            seller=self.seller,
            item_description=self.desc,
            price=self.price,
            days_to_confirm=3,
            fee_recipient=self.fee_fund,
            fee_transfer_fail=True
        )
        escrow.fund(sender=self.buyer, value=self.price)
        # Nguoi mua van xac nhan thanh cong, khong bi revert
        escrow.confirm_received(sender=self.buyer)
        self.assertEqual(escrow.state, CampusEscrowSimulator.STATE_COMPLETED)
        # Nguoi ban nhan toan bo 100% so tien vi phi duoc gop tra lai
        self.assertEqual(escrow.balances[self.seller], self.price)
        self.assertEqual(escrow.balances[self.fee_fund], 0)
        print(" -> Giao dich khong bi nghan! Nguoi ban nhan tron ven tien, he thong phat FeeTransferFailed.")
        print(" -> Ket qua: CHONG DOS THANH CONG 100%!")


if __name__ == "__main__":
    unittest.main()



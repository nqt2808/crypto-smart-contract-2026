"""
Unit Test Suite for HueLegend Smart Contract
Hoc phan: Tien dien tu & Hop dong thong minh (ECO2432)
Tac gia: Nhom sinh vien HueLegend (Ngo Thi Thuy Van & Thanh vien ky thuat)
"""

import unittest
import time

class HueLegendSimulator:
    """Mo phong chinh xac hanh vi on-chain va kiem soat AccessControl cua HueLegend.sol"""

    ROLE_ADMIN = "0x00"
    ROLE_PRODUCER = "PRODUCER_ROLE"
    ROLE_LOGISTICS = "LOGISTICS_ROLE"
    ROLE_RETAILER = "RETAILER_ROLE"

    STATUS_CREATED = 0
    STATUS_IN_TRANSIT = 1
    STATUS_AT_RETAILER = 2
    STATUS_DELIVERED = 3
    STATUS_REVOKED = 4

    def __init__(self, deployer_address):
        self.deployer = deployer_address
        self.roles = {
            self.ROLE_ADMIN: {deployer_address: True},
            self.ROLE_PRODUCER: {deployer_address: True},
            self.ROLE_LOGISTICS: {},
            self.ROLE_RETAILER: {}
        }
        self.total_batches = 0
        self.batches = {}
        self.batch_steps = {}
        self.events = []
        self.current_time = int(time.time())

    def has_role(self, role, account):
        return self.roles.get(role, {}).get(account, False)

    def grant_role(self, role, account, caller):
        if not self.has_role(self.ROLE_ADMIN, caller):
            raise PermissionError(f"AccessControlUnauthorizedAccount: {caller} lacks admin role")
        self.roles.setdefault(role, {})[account] = True
        self.events.append(("RoleGranted", role, account, caller))

    def create_batch(self, product_name, origin_location, expiry_date, quantity, note, caller):
        if not self.has_role(self.ROLE_PRODUCER, caller):
            raise PermissionError(f"AccessControlUnauthorizedAccount: {caller} lacks PRODUCER_ROLE")
        if not product_name or not origin_location or quantity <= 0:
            raise ValueError("InvalidInput")
        if expiry_date <= self.current_time:
            raise ValueError(f"ExpiryMustBeFuture: {expiry_date} <= {self.current_time}")

        self.total_batches += 1
        new_id = self.total_batches

        batch = {
            "batchId": new_id,
            "productName": product_name,
            "originLocation": origin_location,
            "productionDate": self.current_time,
            "expiryDate": expiry_date,
            "quantity": quantity,
            "status": self.STATUS_CREATED,
            "producer": caller,
            "currentHandler": caller
        }
        self.batches[new_id] = batch
        self.batch_steps[new_id] = [{
            "timestamp": self.current_time,
            "location": origin_location,
            "action": "KHOI TAO SAN XUAT TAI HUE",
            "handler": caller,
            "note": note or "Xac thuc lo hang dat tieu chuan OCOP Hue"
        }]

        self.events.append(("BatchCreated", new_id, product_name, caller, quantity))
        return new_id

    def add_tracking_step(self, batch_id, location, action, note, caller):
        if not (self.has_role(self.ROLE_LOGISTICS, caller) or self.has_role(self.ROLE_PRODUCER, caller)):
            raise PermissionError(f"AccessControlUnauthorizedAccount: {caller} lacks LOGISTICS_ROLE")

        batch = self.batches.get(batch_id)
        if not batch:
            raise KeyError(f"BatchNotFound: {batch_id}")
        if batch["status"] == self.STATUS_REVOKED:
            raise RuntimeError(f"BatchAlreadyRevoked: {batch_id}")

        if batch["status"] == self.STATUS_CREATED:
            batch["status"] = self.STATUS_IN_TRANSIT
            self.events.append(("BatchStatusUpdated", batch_id, self.STATUS_CREATED, self.STATUS_IN_TRANSIT, caller))

        batch["currentHandler"] = caller
        self.batch_steps[batch_id].append({
            "timestamp": self.current_time,
            "location": location,
            "action": action,
            "handler": caller,
            "note": note
        })
        self.events.append(("TrackingStepAdded", batch_id, location, action, caller))

    def confirm_at_retailer(self, batch_id, retailer_location, note, caller):
        if not self.has_role(self.ROLE_RETAILER, caller):
            raise PermissionError(f"AccessControlUnauthorizedAccount: {caller} lacks RETAILER_ROLE")

        batch = self.batches.get(batch_id)
        if not batch:
            raise KeyError(f"BatchNotFound: {batch_id}")
        if batch["status"] == self.STATUS_REVOKED:
            raise RuntimeError(f"BatchAlreadyRevoked: {batch_id}")

        old_status = batch["status"]
        batch["status"] = self.STATUS_AT_RETAILER
        batch["currentHandler"] = caller

        self.batch_steps[batch_id].append({
            "timestamp": self.current_time,
            "location": retailer_location,
            "action": "NHAP KHO DAI LY BAN LE",
            "handler": caller,
            "note": note
        })
        self.events.append(("BatchStatusUpdated", batch_id, old_status, self.STATUS_AT_RETAILER, caller))

    def complete_delivery(self, batch_id, note, caller):
        if not (self.has_role(self.ROLE_RETAILER, caller) or self.has_role(self.ROLE_LOGISTICS, caller)):
            raise PermissionError(f"AccessControlUnauthorizedAccount: {caller} lacks RETAILER_ROLE")

        batch = self.batches.get(batch_id)
        if not batch:
            raise KeyError(f"BatchNotFound: {batch_id}")
        if batch["status"] == self.STATUS_REVOKED:
            raise RuntimeError(f"BatchAlreadyRevoked: {batch_id}")

        old_status = batch["status"]
        batch["status"] = self.STATUS_DELIVERED
        batch["currentHandler"] = caller

        self.batch_steps[batch_id].append({
            "timestamp": self.current_time,
            "location": "DIEM TIEU DUNG",
            "action": "DA GIAO DEN KHACH HANG",
            "handler": caller,
            "note": note
        })
        self.events.append(("BatchStatusUpdated", batch_id, old_status, self.STATUS_DELIVERED, caller))

    def revoke_batch(self, batch_id, reason, caller):
        batch = self.batches.get(batch_id)
        if not batch:
            raise KeyError(f"BatchNotFound: {batch_id}")
        if batch["status"] == self.STATUS_REVOKED:
            raise RuntimeError(f"BatchAlreadyRevoked: {batch_id}")

        if not (self.has_role(self.ROLE_ADMIN, caller) or batch["producer"] == caller):
            raise PermissionError(f"AccessControlUnauthorizedAccount: {caller} not authorized to revoke")

        batch["status"] = self.STATUS_REVOKED
        self.batch_steps[batch_id].append({
            "timestamp": self.current_time,
            "location": "HE THONG KIEM DINH",
            "action": "THU HOI LO HANG",
            "handler": caller,
            "note": reason
        })
        self.events.append(("BatchRevoked", batch_id, reason, caller))

    # View Functions (Gas = 0)
    def get_batch(self, batch_id):
        if batch_id not in self.batches:
            raise KeyError(f"BatchNotFound: {batch_id}")
        return self.batches[batch_id]

    def get_batch_steps(self, batch_id):
        if batch_id not in self.batches:
            raise KeyError(f"BatchNotFound: {batch_id}")
        return self.batch_steps[batch_id]

    def is_valid_batch(self, batch_id):
        batch = self.batches.get(batch_id)
        if not batch:
            return False
        if batch["status"] == self.STATUS_REVOKED:
            return False
        if self.current_time > batch["expiryDate"]:
            return False
        return True


class TestHueLegend(unittest.TestCase):
    def setUp(self):
        self.admin = "0x1111111111111111111111111111111111111111"
        self.producer = "0x2222222222222222222222222222222222222222"
        self.logistics = "0x3333333333333333333333333333333333333333"
        self.retailer = "0x4444444444444444444444444444444444444444"
        self.consumer = "0x5555555555555555555555555555555555555555"
        self.attacker = "0x9999999999999999999999999999999999999999"

        self.contract = HueLegendSimulator(deployer_address=self.admin)
        # Cap quyen he thong
        self.contract.grant_role(HueLegendSimulator.ROLE_PRODUCER, self.producer, caller=self.admin)
        self.contract.grant_role(HueLegendSimulator.ROLE_LOGISTICS, self.logistics, caller=self.admin)
        self.contract.grant_role(HueLegendSimulator.ROLE_RETAILER, self.retailer, caller=self.admin)

    def test_01_create_batch_success(self):
        """Kiem thu nha san xuat tao lo hang hop le."""
        print("\n[TEST 1] Nha san xuat tao lo Me xung Thien Huong...")
        future_expiry = int(time.time()) + 180 * 86400 # 6 thang
        batch_id = self.contract.create_batch(
            product_name="Me xung Thien Huong Thuong Hang",
            origin_location="20 Chi Lang, TP. Hue",
            expiry_date=future_expiry,
            quantity=1000,
            note="Dat chuan OCOP 4 sao tinh Thua Thien Hue",
            caller=self.producer
        )
        self.assertEqual(batch_id, 1)
        batch = self.contract.get_batch(batch_id)
        self.assertEqual(batch["status"], HueLegendSimulator.STATUS_CREATED)
        self.assertEqual(batch["producer"], self.producer)
        print(f" -> Lo hang ID #{batch_id} duoc tao thanh cong voi trang thai Created!")

    def test_02_create_batch_unauthorized_revert(self):
        """Kiem thu nguoi khong co PRODUCER_ROLE goi createBatch -> Revert."""
        print("\n[TEST 2] Ke la mat thu tao lo hang khong co quyen...")
        future_expiry = int(time.time()) + 180 * 86400
        with self.assertRaises(PermissionError) as ctx:
            self.contract.create_batch(
                product_name="Hang gia Mao danh Hue",
                origin_location="Cho troi",
                expiry_date=future_expiry,
                quantity=500,
                note="Khong co chung nhan",
                caller=self.attacker
            )
        self.assertIn("AccessControlUnauthorizedAccount", str(ctx.exception))
        print(" -> Bi chan dung boi AccessControl: Ke la mat khong co PRODUCER_ROLE!")

    def test_03_logistics_add_tracking_step_success(self):
        """Kiem thu don vi logistics cap nhat chang van chuyen."""
        print("\n[TEST 3] Don vi van chuyen cap nhat chang xe luu thong...")
        batch_id = self.contract.create_batch("Tinh dau tram Loc Thuy", "Phu Loc, Hue", int(time.time())+365*86400, 500, "Xuat xuong", self.producer)
        
        self.contract.add_tracking_step(
            batch_id=batch_id,
            location="Tram thu phi Phu Bai, Hue",
            action="Xuat phat xe dong lanh chuyen tuyen Hue - Da Nang",
            note="Nhiet do xe duy tri 22 do C",
            caller=self.logistics
        )
        batch = self.contract.get_batch(batch_id)
        self.assertEqual(batch["status"], HueLegendSimulator.STATUS_IN_TRANSIT)
        steps = self.contract.get_batch_steps(batch_id)
        self.assertEqual(len(steps), 2) # Khoi tao + Chuyen tuyen
        print(" -> Trang thai chuyen sang InTransit, chot kiem dinh ghi nhan thanh cong!")

    def test_04_unauthorized_tracking_step_revert(self):
        """Kiem thu nguoi la co them chot van chuyen -> Revert."""
        print("\n[TEST 4] Ke la mat gia mao chang van chuyen...")
        batch_id = self.contract.create_batch("Non la Phu Cam", "Phu Cam, Hue", int(time.time())+365*86400, 200, "Non bai tho", self.producer)
        with self.assertRaises(PermissionError) as ctx:
            self.contract.add_tracking_step(batch_id, "Kho ao", "Nhap kho lau", "Fake note", caller=self.attacker)
        self.assertIn("AccessControlUnauthorizedAccount", str(ctx.exception))
        print(" -> Chan thanh cong: Chi LOGISTICS_ROLE moi duoc bo sung chang!")

    def test_05_retailer_confirm_at_store(self):
        """Kiem thu dai ly ban le tiep nhan lo hang tai quay."""
        print("\n[TEST 5] Dai ly ban le tiep nhan hang tai showroom...")
        batch_id = self.contract.create_batch("Tra Cung dinh Duc Phuong", "Phu Hoi, Hue", int(time.time())+180*86400, 300, "Dong goi hop thiec", self.producer)
        self.contract.add_tracking_step(batch_id, "Kho van Da Nang", "Chuyen tiep den Showroom", "Kiem dem du", self.logistics)

        self.contract.confirm_at_retailer(
            batch_id=batch_id,
            retailer_location="Showroom 12 Le Loi, TP. Hue",
            note="Kiem tra tem niem phong nguyen ven, trung khop so luong",
            caller=self.retailer
        )
        batch = self.contract.get_batch(batch_id)
        self.assertEqual(batch["status"], HueLegendSimulator.STATUS_AT_RETAILER)
        print(" -> Trang thai lo hang da chuyen thanh AtRetailer!")

    def test_06_revocation_and_immutability(self):
        """Kiem thu thu hoi lo hang va khong the cap nhat lo hang da bi Revoke."""
        print("\n[TEST 6] Thu hoi lo hang phat hien su co bao quan...")
        batch_id = self.contract.create_batch("Banh ep Thuan An", "Thuan An, Hue", int(time.time())+30*86400, 100, "Lo banh moi", self.producer)
        
        # Producer tu thu hoi do bao bi rach
        self.contract.revoke_batch(batch_id, "Phat hien bao bi hut chan khong bi ho", caller=self.producer)
        batch = self.contract.get_batch(batch_id)
        self.assertEqual(batch["status"], HueLegendSimulator.STATUS_REVOKED)
        self.assertFalse(self.contract.is_valid_batch(batch_id))

        # Thu them chang vao lo hang da bi revoke -> Revert
        with self.assertRaises(RuntimeError) as ctx:
            self.contract.add_tracking_step(batch_id, "Kho B", "Co tinh van chuyen", "test", caller=self.logistics)
        self.assertIn("BatchAlreadyRevoked", str(ctx.exception))
        print(" -> Lo hang da bi khoa vinh vien, khong the cap nhat them bat ky chang nao!")

    def test_07_public_consumer_view_no_gas(self):
        """Kiem thu nguoi tieu dung tra cuu cong khai (View functions)."""
        print("\n[TEST 7] Nguoi tieu dung quet ma QR tra cuu lich su hanh trinh...")
        batch_id = self.contract.create_batch("Buoi Thanh Tra Thuy Bieu", "Thuy Bieu, Hue", int(time.time())+60*86400, 50, "Thu hoach tai vuon", self.producer)
        self.contract.add_tracking_step(batch_id, "Kho thu mua Nong san Hue", "Kiem dinh OCOP", "Dat chuan VietGAP", self.logistics)
        self.contract.confirm_at_retailer(batch_id, "Sieu thi Dac san Co do", "Len ke trung bay", self.retailer)

        # Nguoi tieu dung doc du lieu (khong can role, khong mat phi gas)
        batch = self.contract.get_batch(batch_id)
        steps = self.contract.get_batch_steps(batch_id)
        is_valid = self.contract.is_valid_batch(batch_id)

        self.assertEqual(len(steps), 3)
        self.assertTrue(is_valid)
        self.assertEqual(batch["productName"], "Buoi Thanh Tra Thuy Bieu")
        print(" -> Tra cuu thanh cong 3 chang xac thuc on-chain, con han su dung va duoc bao chung 100%!")

    def test_08_attack_privilege_escalation_blocked(self):
        """Kiem thu thu leo thang dac quyen: Ke la mat thu cap quyen PRODUCER cho chinh minh."""
        print("\n[TEST 8] Kiem thu chong tan cong leo thang dac quyen (Privilege Escalation)...")
        with self.assertRaises(PermissionError) as ctx:
            self.contract.grant_role(HueLegendSimulator.ROLE_PRODUCER, self.attacker, caller=self.attacker)
        self.assertIn("AccessControlUnauthorizedAccount", str(ctx.exception))
        print(" -> Chon loc va chan dung: Chi DEFAULT_ADMIN moi co quyen cap vai tro he thong!")


if __name__ == "__main__":
    unittest.main()

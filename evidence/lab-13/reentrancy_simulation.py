"""
Mo phong thuc nghiem tan cong Reentrancy tren VulnerableBank va kiem chung 2 cach va loi.
Dap ung yeu cau Lab 13 - Hoc phan ECO2432.
"""

def simulate_vulnerable_bank():
    print("=" * 60)
    print("THUC NGHIEM 1: TAN CONG REENTRANCY TREN VULNERABLEBANK")
    print("=" * 60)
    
    # 1. Khoi tao 3 nguoi dung gui moi nguoi 2 ETH
    balances = {
        "User1": 2.0,
        "User2": 2.0,
        "User3": 2.0
    }
    bank_balance = sum(balances.values())
    print(f"[Buoc 1] 3 tai khoan nap moi nguoi 2 ETH.")
    print(f" -> So du ban dau cua VulnerableBank: {bank_balance} ETH\n")
    
    # 2. Ke tan cong nap 1 ETH lam von moi
    attacker_deposit = 1.0
    balances["Attacker"] = attacker_deposit
    bank_balance += attacker_deposit
    attacker_loot = 0.0
    
    print(f"[Buoc 2] Ke tan cong nap 1 ETH. Tong so du ngan hang: {bank_balance} ETH")
    print(f"Ke tan cong goi ham withdraw()...\n")
    
    # 3. Mo phong loi rut tien: chuyen tien TRUOC khi cap nhat balances["Attacker"] = 0
    recursion_count = 0
    while bank_balance > 0 and recursion_count < 10:
        recursion_count += 1
        # Ngan hang kiem tra: balances['Attacker'] van la 1.0 vi chua chay dong balances = 0!
        current_attacker_record = balances["Attacker"]
        print(f" -> [Vong lap de quy {recursion_count}] Ngan hang kiem tra so du ke tan cong: {current_attacker_record} ETH")
        
        # Ngan hang chuyen tien
        transfer_amount = min(current_attacker_record, bank_balance)
        bank_balance -= transfer_amount
        attacker_loot += transfer_amount
        print(f"    Ngan hang chuyen {transfer_amount} ETH vao contract Attacker.")
        print(f"    Ham receive() cua Attacker tu dong goi lai withdraw()! So du ngan hang con lai: {bank_balance} ETH")
    
    # Sau khi rut can, ngan hang moi chay dong ghi so cuoi cung
    balances["Attacker"] = 0.0
    print(f"\n[Ket qua tan cong]")
    print(f" -> So du VulnerableBank sau khi bi tan cong: {bank_balance} ETH (RUT CAN 100%)")
    print(f" -> Tong so ETH ke tan cong chiem doat: {attacker_loot} ETH (Lai 6 ETH tu von 1 ETH)")

def simulate_safe_bank_cei():
    print("\n" + "=" * 60)
    print("THUC NGHIEM 2: KIEM CHUNG BAN VA LOI SAFEBANK VOI CHECKS-EFFECTS-INTERACTIONS")
    print("=" * 60)
    
    balances = {
        "User1": 2.0,
        "User2": 2.0,
        "User3": 2.0
    }
    bank_balance = sum(balances.values())
    print(f"[Buoc 1] So du ngan hang an toan: {bank_balance} ETH")
    
    # Ke tan cong nap 1 ETH
    balances["Attacker"] = 1.0
    bank_balance += 1.0
    print(f"[Buoc 2] Ke tan cong nap 1 ETH. Tong so du: {bank_balance} ETH")
    print("Ke tan cong goi withdraw()...\n")
    
    # Xu ly theo Checks-Effects-Interactions
    # 1. Checks
    bal = balances["Attacker"]
    assert bal > 0, "Khong co so du"
    
    # 2. Effects: Ghi so ve 0 TRUOC
    balances["Attacker"] = 0.0
    print(" -> [Checks-Effects] So du ke tan cong duoc ghi ve 0 TRUOC tren so sach.")
    
    # 3. Interactions: Chuyen tien
    transfer_amount = bal
    bank_balance -= transfer_amount
    print(f" -> [Interactions] Ngan hang chuyen 1 ETH cho ke tan cong.")
    print(" -> Ham receive() cua Attacker co tinh goi lai withdraw()...")
    
    # Cu goi lai gap phai Checks:
    reentrant_bal = balances["Attacker"]
    if reentrant_bal == 0:
        print(" -> [CHAN DUNG] Giao dich de quy bi REVERT voi loi: 'Khong co so du'!")
        print(" -> Cu tan cong bi be gay hoan toan tai diem nay!\n")
    
    print(f"[Ket qua sau phong ve CEI]")
    print(f" -> So du hop phap con lai trong ngan hang: {bank_balance} ETH (Bao toan 6 ETH cua User1, 2, 3)")
    print(f" -> Ke tan cong chi lay dung 1 ETH da nap vao.")

if __name__ == "__main__":
    simulate_vulnerable_bank()
    simulate_safe_bank_cei()

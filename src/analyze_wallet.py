"""
Cong cu phan tich dong tien on-chain va truc quan hoa so du vi Ethereum
Tuan thu quy uoc AGENTS.md va dac ta SPEC.md (Lab 5 & Lab 6)
Mon hoc: ECO2432 - Tien dien tu & Hop dong thong minh
"""

import os
import sys
import time
import argparse
from datetime import datetime, timezone
import requests
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

WEI_TO_ETH = 10**18

def get_transactions_from_etherscan(address: str, api_key: str, network: str = "sepolia"):
    """
    Lay danh sach giao dich tu Etherscan API voi co che phan trang day du.
    Tuan thu quy tac: doc api_key tu bien moi truong, kiem tra ma trang thai.
    """
    if network.lower() == "mainnet":
        base_url = "https://api.etherscan.io/api"
    else:
        base_url = "https://api-sepolia.etherscan.io/api"

    transactions = []
    page = 1
    offset = 100  # so ban ghi moi trang

    print(f"[*] Dang lay du lieu giao dich cho vi: {address} tren mang {network}...")

    while True:
        params = {
            "module": "account",
            "action": "txlist",
            "address": address,
            "startblock": 0,
            "endblock": 99999999,
            "page": page,
            "offset": offset,
            "sort": "asc",
            "apikey": api_key
        }

        try:
            resp = requests.get(base_url, params=params, timeout=15)
            if resp.status_code != 200:
                print(f"[!] Loi ket noi API: Ma trang thai HTTP {resp.status_code}")
                break

            data = resp.json()
            status = data.get("status")
            message = data.get("message")
            result = data.get("result")

            if status != "1":
                if message == "No transactions found":
                    print("[i] Vi khong co giao dich nao trong lich su.")
                else:
                    print(f"[!] Thong bao tu Etherscan API: {message} ({result})")
                break

            if isinstance(result, list):
                transactions.extend(result)
                print(f"    - Da lay trang {page}: {len(result)} giao dich.")
                if len(result) < offset:
                    # Da lay het du lieu
                    break
                page += 1
                time.sleep(0.3)  # tranh rate limit
            else:
                break

        except requests.exceptions.RequestException as e:
            print(f"[!] Ngoai le mang: {e}")
            break

    return transactions

def generate_sample_dataset(address: str):
    """
    Tao tap du lieu mau chuan de kiem thu quy tac R1-R6 khi chua co API key hoac offline.
    Bao gom ca giao dich thanh cong, giao dich that bai, va giao dich nap/rut.
    """
    now = int(time.time())
    day_sec = 86400

    sample_txs = [
        # Tx 1: Nhan ETH tu faucet (Inflow thanh cong)
        {
            "hash": "0x1111111111111111111111111111111111111111111111111111111111111111",
            "timeStamp": str(now - 80 * day_sec),
            "from": "0x0000000000000000000000000000000000000000",
            "to": address.lower(),
            "value": str(int(1.50 * WEI_TO_ETH)),
            "gasPrice": str(15 * 10**9),
            "gasUsed": "21000",
            "isError": "0"
        },
        # Tx 2: Gui tien cho ban hoc (Outflow thanh cong: tru value + gas fee)
        {
            "hash": "0x2222222222222222222222222222222222222222222222222222222222222222",
            "timeStamp": str(now - 60 * day_sec),
            "from": address.lower(),
            "to": "0x23618e81e3f5cdf7f54c3d65f7fbc0abf5b21e8f",
            "value": str(int(0.35 * WEI_TO_ETH)),
            "gasPrice": str(20 * 10**9),
            "gasUsed": "21000",
            "isError": "0"
        },
        # Tx 3: Giao dich tuong tac hop dong that bai (Outflow chi tru gas fee)
        {
            "hash": "0x3333333333333333333333333333333333333333333333333333333333333333",
            "timeStamp": str(now - 45 * day_sec),
            "from": address.lower(),
            "to": "0x5555555555555555555555555555555555555555",
            "value": str(int(0.50 * WEI_TO_ETH)),
            "gasPrice": str(25 * 10**9),
            "gasUsed": "48000",
            "isError": "1"  # THAT BAI: khong tru value, chi tru gas
        },
        # Tx 4: Nhan thuong tu nhom (Inflow)
        {
            "hash": "0x4444444444444444444444444444444444444444444444444444444444444444",
            "timeStamp": str(now - 25 * day_sec),
            "from": "0x7777777777777777777777777777777777777777",
            "to": address.lower(),
            "value": str(int(0.80 * WEI_TO_ETH)),
            "gasPrice": str(18 * 10**9),
            "gasUsed": "21000",
            "isError": "0"
        },
        # Tx 5: Nap vao hop dong tiet kiem TimeLock (Outflow thanh cong)
        {
            "hash": "0x5555555555555555555555555555555555555555555555555555555555555555",
            "timeStamp": str(now - 5 * day_sec),
            "from": address.lower(),
            "to": "0x8888888888888888888888888888888888888888",
            "value": str(int(0.60 * WEI_TO_ETH)),
            "gasPrice": str(16 * 10**9),
            "gasUsed": "45000",
            "isError": "0"
        }
    ]
    return sample_txs

def analyze_cashflow(transactions, target_address: str, days: int = 90):
    """
    Phan tich dong tien tuan thu dac ta SPEC.md:
    R1: to == address -> Inflow
    R2: from == address -> Outflow
    R3: Outflow thanh cong = value + gas_fee
    R4: Outflow that bai = chi tru gas_fee
    R5: Quy doi wei -> ETH
    R6: Sap xep tang dan theo thoi gian
    """
    now = int(time.time())
    start_time = now - (days * 86400)
    target_lower = target_address.lower()

    # Loc va sap xep theo thoi gian
    filtered_txs = [tx for tx in transactions if int(tx["timeStamp"]) >= start_time]
    filtered_txs.sort(key=lambda x: int(x["timeStamp"]))

    records = []
    total_inflow = 0.0
    total_outflow = 0.0
    total_gas_spent = 0.0
    cumulative_balance = 0.0

    timeline_dates = []
    timeline_balances = []

    for tx in filtered_txs:
        tx_time = datetime.fromtimestamp(int(tx["timeStamp"]), tz=timezone.utc)
        tx_hash_short = tx["hash"][:10] + "..." + tx["hash"][-6:]
        val_eth = int(tx["value"]) / WEI_TO_ETH
        gas_fee = (int(tx["gasUsed"]) * int(tx["gasPrice"])) / WEI_TO_ETH
        is_error = tx.get("isError") == "1"

        is_in = tx.get("to", "").lower() == target_lower
        is_out = tx.get("from", "").lower() == target_lower

        action_type = "UNKNOWN"
        net_change = 0.0

        if is_in and not is_error:
            action_type = "INFLOW (+)"
            total_inflow += val_eth
            net_change = val_eth
        elif is_out:
            total_gas_spent += gas_fee
            if not is_error:
                action_type = "OUTFLOW (-)"
                amount_debited = val_eth + gas_fee
                total_outflow += amount_debited
                net_change = -amount_debited
            else:
                action_type = "FAILED (GAS ONLY)"
                total_outflow += gas_fee
                net_change = -gas_fee

        cumulative_balance += net_change

        records.append({
            "time": tx_time.strftime("%Y-%m-%d %H:%M"),
            "hash": tx_hash_short,
            "type": action_type,
            "value_eth": val_eth,
            "gas_fee_eth": gas_fee,
            "balance": cumulative_balance
        })

        timeline_dates.append(tx_time)
        timeline_balances.append(cumulative_balance)

    return {
        "records": records,
        "total_inflow": total_inflow,
        "total_outflow": total_outflow,
        "total_gas_spent": total_gas_spent,
        "final_balance": cumulative_balance,
        "timeline_dates": timeline_dates,
        "timeline_balances": timeline_balances
    }

def print_report(summary, target_address: str, days: int):
    """In bang bao cao dong tien ro rang chuan nghiep vu"""
    print("\n" + "=" * 80)
    print(f" BAO CAO PHAN TICH DONG TIEN ON-CHAIN ({days} NGAY GAN NHAT)")
    print(f" Dia chi vi: {target_address}")
    print("=" * 80)
    print(f"{'Thoi gian (UTC)':<18} | {'Tx Hash':<18} | {'Loai':<18} | {'Gia tri (ETH)':<12} | {'So du (ETH)':<12}")
    print("-" * 80)

    for r in summary["records"]:
        print(f"{r['time']:<18} | {r['hash']:<18} | {r['type']:<18} | {r['value_eth']:<12.4f} | {r['balance']:<12.4f}")

    print("-" * 80)
    print(f"[*] Tong dong tien vao (Total Inflow) : +{summary['total_inflow']:.6f} ETH")
    print(f"[*] Tong dong tien ra  (Total Outflow): -{summary['total_outflow']:.6f} ETH")
    print(f"[*] Tong phi gas da tra (Total Gas)   :  {summary['total_gas_spent']:.6f} ETH")
    print(f"[*] Bien dong so du rong (Net Balance):  {summary['final_balance']:+.6f} ETH")
    print("=" * 80 + "\n")

def plot_balance_chart(summary, target_address: str, output_path: str):
    """Ve bieu do bien dong so du luy ke theo thoi gian"""
    dates = summary["timeline_dates"]
    balances = summary["timeline_balances"]

    if not dates:
        print("[!] Khong co du lieu thoi gian de ve bieu do.")
        return

    # Tao thu muc chua anh neu chua co
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    plt.figure(figsize=(10, 5.5), dpi=150)
    plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")

    # Ve duong so du
    plt.plot(dates, balances, color="#1e88e5", marker="o", linewidth=2.5, markersize=6, label="So du luy ke (ETH)")
    plt.fill_between(dates, balances, alpha=0.15, color="#1e88e5")

    # Dinh dang truc X theo ngay
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
    plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())

    plt.title(f"Bieu do bien dong so du vi: {target_address[:10]}...{target_address[-6:]}\n(Theo dac ta SPEC.md - ECO2432)", fontsize=12, fontweight="bold", pad=12)
    plt.xlabel("Thoi gian (Ngay/Thang)", fontsize=10, fontweight="bold")
    plt.ylabel("So du (ETH)", fontsize=10, fontweight="bold")
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend(loc="upper left")
    plt.tight_layout()

    plt.savefig(output_path)
    plt.close()
    print(f"[+] Da xuat bieu do thanh cong tai: {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Cong cu phan tich dong tien vi Ethereum (Lab 6)")
    parser.add_argument("--address", default="0x2e4216e1BCA81d308b25adaD6ef5Ea92E2e42F8c", help="Dia chi vi can phan tich")
    parser.add_argument("--days", type=int, default=90, help="So ngay phan tich")
    parser.add_argument("--network", default="sepolia", help="Mang blockchain (sepolia hoac mainnet)")
    parser.add_argument("--output", default="evidence/lab-06/balance_chart.png", help="Duong dan luu anh bieu do")
    args = parser.parse_args()

    # Doc API key tu bien moi truong (quy tac AGENTS.md)
    api_key = os.getenv("ETHERSCAN_API_KEY")

    if api_key and api_key != "demo":
        txs = get_transactions_from_etherscan(args.address, api_key, args.network)
        if not txs:
            print("[i] Khong lay duoc giao dich tu API, su dung tap du lieu mau de kiem thu.")
            txs = generate_sample_dataset(args.address)
    else:
        print("[*] Bien moi truong ETHERSCAN_API_KEY chua duoc set.")
        print("[*] Chay che do kiem thu (Mock / Test Dataset) voi day du cac ca: Inflow, Outflow, Failed Tx.")
        txs = generate_sample_dataset(args.address)

    # Thuc hien phan tich
    summary = analyze_cashflow(txs, args.address, args.days)

    # In bao cao
    print_report(summary, args.address, args.days)

    # Xuat bieu do
    plot_balance_chart(summary, args.address, args.output)

if __name__ == "__main__":
    main()

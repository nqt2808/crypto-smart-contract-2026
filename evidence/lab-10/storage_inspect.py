"""
Script minh hoa doc truc tiep o nho (Storage Slot) cua hop dong VaultBuggy
Chung minh tu khoa 'private' trong Solidity KHONG lam du lieu tro nen bi mat.
"""

def demonstrate_storage_inspection():
    pin_value = 123456
    hex_pin = hex(pin_value)[2:]  # '1e240'
    slot_2_raw = "0x" + hex_pin.zfill(64)
    
    print("=== KET QUA THUC NGHIEM DOC STORAGE SLOT TRONG SOLIDITY ===")
    print("1. Hop dong: VaultBuggy.sol")
    print("2. Thuoc tinh: uint256 private emergencyPin = 123456")
    print("3. Cau lenh RPC goi qua Web3 / Console trinh duyet:")
    print("   await window.ethereum.request({")
    print("     method: 'eth_getStorageAt',")
    print("     params: ['0x71C...VaultBuggy', '0x2', 'latest']")
    print("   });")
    print(f"4. Du lieu tho tra ve tu Slot 2: {slot_2_raw}")
    print(f"5. Giai ma nguoc: int('{slot_2_raw}', 16) = {int(slot_2_raw, 16)}")
    print("--> KET LUAN: Du lieu hoan toan cong khai! Private chi gioi han quyen goi giua cac contract.")

if __name__ == "__main__":
    demonstrate_storage_inspection()

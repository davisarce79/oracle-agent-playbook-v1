#!/usr/bin/env python3
"""
Fix $GUNNA wallet address - corrects malformed wallet address across all files.
Run this after obtaining the correct 44-character Solana pubkey.
"""

import re
import os
import sys
from datetime import datetime

# Files that contain the wallet address
FILES_TO_UPDATE = [
    "/home/opc/.openclaw/workspace/deploy_gunna_token.py",
    "/home/opc/.openclaw/workspace/monitor_gunna_wallet.py",
    "/home/opc/.openclaw/workspace/COMMITMENTS.md",
    "/home/opc/.openclaw/workspace/REVENUE_TRACK_STATUS.md"
]

# The malformed wallet address currently in use
MALFORMED_ADDRESS = "dXTKoKg9jAPQqYzZGPB2TPSv6nZFiFbAhVQdz6wopcyF6uzHW"
# Actually the address is 49 chars; correct Solana pubkeys are 44 base58 chars

def validate_solana_pubkey(address: str) -> bool:
    """Basic validation: length 44 and base58 characters."""
    if len(address) != 44:
        return False
    # Base58 alphabet (excluding 0, O, I, l)
    base58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    return all(c in base58 for c in address)

def replace_in_file(filepath: str, old_addr: str, new_addr: str, dry_run: bool = True) -> tuple:
    """Replace wallet address in a file. Returns (found, replaced)."""
    try:
        with open(filepath, 'r') as f:
            content = f.read()
        
        if old_addr not in content:
            return (False, False)
        
        if dry_run:
            return (True, False)
        
        new_content = content.replace(old_addr, new_addr)
        with open(filepath, 'w') as f:
            f.write(new_content)
        return (True, True)
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return (False, False)

def main():
    print("=== $GUNNA Wallet Address Fix Utility ===\n")
    
    # Check current malformed address
    print(f"Current malformed address: {MALFORMED_ADDRESS} (length: {len(MALFORMED_ADDRESS)})")
    print("Required: 44-character base58 Solana pubkey\n")
    
    if len(sys.argv) < 2:
        print("Usage: python3 fix_gunna_wallet.py <CORRECT_44_CHAR_ADDRESS> [--apply]\n")
        print("Examples:")
        print("  python3 fix_gunna_wallet.py 7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU  --dry-run  # Show what would change")
        print("  python3 fix_gunna_wallet.py 7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU  --apply     # Actually modify files\n")
        print("NOTE: Replace the example address with your actual wallet pubkey.")
        sys.exit(1)
    
    new_address = sys.argv[1]
    apply = "--apply" in sys.argv
    
    if not validate_solana_pubkey(new_address):
        print(f"ERROR: '{new_address}' is not a valid Solana pubkey.")
        print("  - Must be exactly 44 characters")
        print("  - Must use base58 alphabet (123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz)")
        sys.exit(1)
    
    print(f"New address: {new_address} (valid)")
    print(f"Mode: {'APPLY' if apply else 'DRY RUN (no changes)'}\n")
    
    changes = []
    for filepath in FILES_TO_UPDATE:
        if not os.path.exists(filepath):
            print(f"⚠️  File not found: {filepath}")
            continue
        found, replaced = replace_in_file(filepath, MALFORMED_ADDRESS, new_address, dry_run=not apply)
        if found:
            status = "Would replace" if not apply else ("Replaced" if replaced else "Already correct?")
            print(f"[{status}] {filepath}")
            changes.append(filepath)
        else:
            print(f"[Skip] {filepath} (address not found)")
    
    print(f"\nTotal files affected: {len(changes)}")
    
    if apply and changes:
        log_entry = f"{datetime.utcnow().isoformat()}Z - Wallet address updated in {len(changes)} files. New address: {new_address}\n"
        with open("/home/opc/.openclaw/workspace/memory/wallet_address_fix_log.txt", "a") as log:
            log.write(log_entry)
        print("Log entry created in memory/wallet_address_fix_log.txt")
        print("\nNEXT STEPS:")
        print("1. Verify wallet balance using correct address")
        print("2. Fund wallet with 0.05-0.1 SOL")
        print("3. Deploy token: python3 deploy_gunna_token.py")
        print("4. Or use pump.fun web UI with wallet")
    elif not apply:
        print("\nDRY RUN complete. Add '--apply' to actually modify files.")
    else:
        print("\nNo changes made. The malformed address may have already been corrected or not present in expected files.")

if __name__ == "__main__":
    main()

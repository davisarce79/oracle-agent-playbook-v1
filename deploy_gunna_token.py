#!/usr/bin/env python3
"""
$GUNNA Token Deployment Script
Ready to execute once wallet is funded with ~0.05-0.1 SOL.

Steps:
1. Ensure ~0.05-0.1 SOL is in wallet: dXTKoKg9jAPYqYzZGPB2TPSv6nZFiFbAhVQdz6wopcyF6uzHW
2. Run this script to create token on pump.fun
3. Set metadata (symbol: GUNNA, name: Agent Gunna Token, supply: 1B)
4. Link to Telegram channel and agent documentation

Alternatively, use pump.fun web interface with the same wallet.
"""

import subprocess
import json
import os

# Wallet details
WALLET_PUBKEY = "dXTKoKg9jAPYqYzZGPB2TPSv6nZFiFbAhVQdz6wopcyF6uzHW"
LOGO_PATH = "memory/uploads/gunna_token_logo_clean.png"
TOKEN_METADATA = {
    "symbol": "GUNNA",
    "name": "Agent Gunna Token",
    "description": "Governance and rewards token for Agent Gunna autonomous revenue machines.",
    "supply": 1000000000,  # 1 billion
    "decimals": 9,
    "image": LOGO_PATH,
    "twitter": "@AgentGunna",
    "telegram": "t.me/AgentGunnaAlpha",
    "website": "https://gumroad.com/l/ujgrn"  # The Oracle Agent Playbook
}

def check_sol_balance():
    """Check current SOL balance in the wallet."""
    try:
        result = subprocess.run(
            ["solana", "balance", WALLET_PUBKEY, "--url", "https://api.mainnet-beta.solana.com"],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            print(f"Balance check: {result.stdout.strip()}")
            return True
        else:
            print(f"Error checking balance: {result.stderr}")
            return False
    except FileNotFoundError:
        print("Solana CLI not installed. Use web wallet at pump.fun instead.")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

def deploy_token_cli():
    """Deploy token using Solana CLI (if installed and funded)."""
    # This is a template; actual pump.fun creation requires specific instructions
    print("Deployment via Solana CLI would involve:")
    print("1. Create token account")
    print("2. Mint supply")
    print("3. Set metadata via Metaplex token metadata program")
    print("\nAlternatively, use pump.fun web interface directly with wallet.")
    print("\nPrepared metadata:")
    print(json.dumps(TOKEN_METADATA, indent=2))

def main():
    print("=== $GUNNA Token Deployment Ready ===\n")
    print(f"Wallet: {WALLET_PUBKEY}")
    print("Required SOL: ~0.05-0.1")
    print("\nChecking balance...")
    balance_status = check_sol_balance()
    
    if balance_status is True:
        print("\nBalance check complete. If funded, proceed with deployment.")
    elif balance_status is False:
        print("\nError checking balance. Ensure Solana CLI installed and configured.")
    else:
        print("\nSolana CLI not available. Use web wallet at pump.fun.")
    
    deploy_token_cli()
    
    # Next steps checklist
    print("\n--- Next Steps After Funding ---")
    print("[ ] Verify SOL received in wallet")
    print("[ ] Choose deployment method: CLI or pump.fun web")
    print("[ ] Deploy token with symbol GUNNA, supply 1B")
    print("[ ] Upload logo: memory/uploads/gunna_token_logo_clean.png")
    print("[ ] Set metadata (description, links)")
    print("[ ] Add Telegram channel: t.me/AgentGunnaAlpha")
    print("[ ] Update MEMORY.md and COMMITMENTS.md on completion")
    print("[ ] Notify user")

if __name__ == "__main__":
    main()

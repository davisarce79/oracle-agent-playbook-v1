#!/usr/bin/env python3
import requests
WALLET = "dXTKoKg9jAPYqYzZGPB2TPSv6nZFiFbAhVQdz6wopcyF6uzHW"
RPC_URL = "https://api.mainnet-beta.solana.com"
payload = {"jsonrpc": "2.0", "id": 1, "method": "getBalance", "params": [WALLET, {"commitment": "confirmed"}]}
try:
    resp = requests.post(RPC_URL, json=payload, timeout=10)
    data = resp.json()
    lamports = data["result"]["value"]
    sol = lamports / 1000000000
    print(f"\n=== \$GUNNA Wallet Status ===\nAddress: {WALLET}\nBalance: {sol:.4f} SOL")
    if sol < 0.05: print(f"Outcome: AWAITING FUNDING (Need {0.05 - sol:.4f} more)")
    else: print("Outcome: READY FOR DEPLOYMENT")
except Exception as e: print(f"Error: {e}")

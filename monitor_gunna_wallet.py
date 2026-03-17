#!/usr/bin/env python3
"""
$GUNNA Wallet Balance Monitor (RPC version)
Checks wallet dXTKoKg9jAPYqYzZGPB2TPSv6nZFiFbAhVQdz6wopcyF6uzHW
and alerts when balance reaches threshold (0.05+ SOL).

Uses Solana public JSON-RPC (no CLI required).
"""

import requests
import json
import os
from datetime import datetime

WALLET = "dXTKoKg9jAPYqYzZGPB2TPSv6nZFiFbAhVQdz6wopcyF6uzHW"
THRESHOLD = 0.05  # Minimum SOL needed for deployment
STATE_FILE = "/home/opc/.openclaw/workspace/memory/wallet_balance_state.json"
RPC_URL = "https://api.mainnet-beta.solana.com"

def check_balance_rpc():
    """Query Solana balance via JSON-RPC."""
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getBalance",
        "params": [WALLET]
    }
    try:
        resp = requests.post(RPC_URL, json=payload, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        if "result" in data and "value" in data["result"]:
            # Balance is in lamports (1 SOL = 1_000_000_000 lamports)
            lamports = data["result"]["value"]
            sol = lamports / 1_000_000_000
            return sol
        else:
            print(f"RPC error: {data.get('error', 'unknown')}")
            return None
    except Exception as e:
        print(f"RPC request failed: {e}")
        return None

def load_last_state():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, 'r') as f:
                return json.load(f)
        except Exception:
            pass
    return {"last_balance": 0.0, "last_notified_balance": 0.0, "last_check": None}

def save_state(balance, notified):
    state = {
        "last_balance": balance,
        "last_notified_balance": notified,
        "last_check": datetime.utcnow().isoformat() + "Z"
    }
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

def main():
    print(f"=== $GUNNA Wallet Monitor (RPC) ===\nWallet: {WALLET}\nThreshold: {THRESHOLD} SOL\n")
    
    balance = check_balance_rpc()
    if balance is None:
        print("Cannot check balance via RPC. Skipping.")
        return
    
    print(f"Current balance: {balance:.6f} SOL")
    
    state = load_last_state()
    last_balance = state.get("last_balance", 0.0)
    last_notified = state.get("last_notified_balance", 0.0)
    
    # Save current balance for history
    save_state(balance, last_notified)
    
    if balance >= THRESHOLD and last_notified < THRESHOLD:
        # Just crossed threshold — alert!
        print(f"\n>>> FUNDS ARRIVED! Balance ({balance:.6f}) meets threshold ({THRESHOLD}). Ready to deploy $GUNNA token.")
        print("Next step: run python3 deploy_gunna_token.py or use pump.fun web UI.")
        # Update notified state
        state["last_notified_balance"] = balance
        with open(STATE_FILE, 'w') as f:
            json.dump(state, f, indent=2)
        # Could also send a message via OpenClaw if desired:
        # from openclaw import message; message(action='send', to='user', message='...')
    elif balance > last_balance:
        print(f"\nBalance increased (was {last_balance:.6f}). Still {(THRESHOLD - balance):.6f} SOL needed.")
    else:
        print("\nNo change or balance decreased. Still waiting for funding.")
    
    print(f"\nState saved to: {STATE_FILE}")

if __name__ == "__main__":
    main()

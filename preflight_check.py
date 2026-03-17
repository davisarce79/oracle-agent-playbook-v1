#!/usr/bin/env python3
"""
Preflight Checks for Revenue Launch
Validates prerequisites before executing $GUNNA token deployment or email campaign.
"""

import os
import json
import sys
from pathlib import Path
from datetime import datetime

WORKSPACE = Path('/home/opc/.openclaw/workspace')

def check_gunna_wallet():
    """Validate $GUNNA deployment wallet address."""
    wallet_file = WORKSPACE / 'deploy_gunna_token.py'
    if not wallet_file.exists():
        return {'ok': False, 'issue': 'deploy_gunna_token.py not found'}
    
    # Extract wallet address from file
    content = wallet_file.read_text()
    # Find WALLET_PUBKEY line
    for line in content.splitlines():
        if 'WALLET_PUBKEY' in line and '=' in line:
            _, addr = line.split('=', 1)
            addr = addr.strip().strip('"').strip("'")
            break
    else:
        return {'ok': False, 'issue': 'Wallet address not found in deploy_gunna_token.py'}
    
    # Validate
    if len(addr) != 44:
        return {'ok': False, 'issue': f'Invalid length: {len(addr)} (need 44)'}
    base58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    if not all(c in base58 for c in addr):
        return {'ok': False, 'issue': 'Contains non-base58 characters'}
    
    # Check if wallet monitor script uses same address
    monitor_file = WORKSPACE / 'monitor_gunna_wallet.py'
    if monitor_file.exists():
        mon_content = monitor_file.read_text()
        if addr not in mon_content:
            return {'ok': False, 'issue': 'Wallet address mismatch between deploy and monitor scripts'}
    
    return {'ok': True, 'address': addr}

def check_sol_balance():
    """Check if wallet has ≥ 0.05 SOL via RPC (if address valid)."""
    wallet_check = check_gunna_wallet()
    if not wallet_check['ok']:
        return {'ok': False, 'issue': 'Cannot check balance: wallet address invalid'}
    
    addr = wallet_check['address']
    import requests
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getBalance",
        "params": [addr]
    }
    try:
        resp = requests.post("https://api.mainnet-beta.solana.com", json=payload, timeout=10)
        data = resp.json()
        if "result" in data and "value" in data["result"]:
            lamports = data["result"]["value"]
            sol = lamports / 1_000_000_000
            if sol >= 0.05:
                return {'ok': True, 'balance': sol, 'ready': True}
            else:
                return {'ok': True, 'balance': sol, 'ready': False, 'issue': f'Balance {sol:.6f} SOL < 0.05 threshold'}
        else:
            return {'ok': False, 'issue': f"RPC error: {data.get('error', 'unknown')}"}
    except Exception as e:
        return {'ok': False, 'issue': f'RPC request failed: {e}'}

def check_wallet_fix_utility():
    """Ensure the wallet fix script exists and is executable."""
    fix_script = WORKSPACE / 'fix_gunna_wallet.py'
    if not fix_script.exists():
        return {'ok': False, 'issue': 'fix_gunna_wallet.py not found'}
    # Basic sanity: file is readable and has main()
    try:
        content = fix_script.read_text()
        if 'def main():' not in content:
            return {'ok': False, 'issue': 'fix_gunna_wallet.py missing main()'}
    except Exception as e:
        return {'ok': False, 'issue': f'Cannot read fix script: {e}'}
    return {'ok': True}

def check_smtp_config():
    """Check if SMTP credentials file exists."""
    creds_dir = WORKSPACE / '.openclaw' / 'credentials'
    smtp_file = creds_dir / 'smtp.json'  # expected after setup_email_marketing.py runs
    if smtp_file.exists():
        try:
            with open(smtp_file) as f:
                cfg = json.load(f)
            # Basic validation
            provider = cfg.get('provider')
            if provider in ['gmail', 'outlook', 'sendgrid', 'zoho']:
                return {'ok': True, 'provider': provider, 'configured': True}
            return {'ok': False, 'issue': 'Unknown provider in config'}
        except Exception as e:
            return {'ok': False, 'issue': f'Config file unreadable: {e}'}
    else:
        return {'ok': False, 'issue': 'SMTP config not found; run setup_email_marketing.py after providing credentials'}

def check_gumroad_product():
    """Verify Gumroad product is accessible."""
    try:
        import subprocess
        result = subprocess.run(
            ['python3', str(WORKSPACE / 'skills' / 'gumroad-api' / 'gumroad_api.py'), 'products'],
            capture_output=True, text=True, timeout=10
        )
        data = json.loads(result.stdout)
        if data.get('success'):
            return {'ok': True, 'products': len(data.get('products', []))}
        return {'ok': False, 'issue': 'Gumroad API check failed'}
    except Exception as e:
        return {'ok': False, 'issue': f'Gumroad API error: {e}'}

def main():
    print("=== Preflight Revenue Launch Check ===\n")
    
    # Collect results
    results = {
        '$GUNNA Wallet': check_gunna_wallet(),
        'Wallet Fix Utility': check_wallet_fix_utility(),
        'SOL Balance': check_sol_balance(),
        'SMTP Config': check_smtp_config(),
        'Gumroad Product': check_gumroad_product()
    }
    
    # Print summary
    all_ok = True
    for name, res in results.items():
        status = "✅" if res['ok'] else "❌"
        print(f"{status} {name}")
        if not res['ok']:
            print(f"   Issue: {res.get('issue', 'Unknown error')}")
            all_ok = False
        else:
            if 'balance' in res:
                print(f"   Balance: {res['balance']:.6f} SOL (ready: {res['ready']})")
            if 'provider' in res:
                print(f"   Provider: {res['provider']}")
            if 'products' in res:
                print(f"   Products tracked: {res['products']}")
    
    print()
    if all_ok:
        print("All systems go. You can proceed with token deployment and email campaign.")
    else:
        print("Blockers detected. Address issues above before launching revenue tracks.")
    
    # Save report
    report = {
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'results': results,
        'all_ok': all_ok
    }
    out_path = WORKSPACE / 'memory' / 'preflight_report.json'
    with open(out_path, 'w') as f:
        json.dump(report, f, indent=2)
    print(f"Report saved to: {out_path}")
    
    sys.exit(0 if all_ok else 1)

if __name__ == "__main__":
    main()

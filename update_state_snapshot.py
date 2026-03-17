#!/usr/bin/env python3
"""
Auto-snapshot updater for STATE.md
Runs every few hours to refresh dynamic fields (positions, orders, fills, Instagram).
"""

import os
from datetime import datetime
import requests
import re

STATE_PATH = "/home/opc/.openclaw/workspace/STATE.md"

ALPACA_HEADERS = {
    "APCA-API-KEY-ID": "PKCHDGAMEL4RGF5E6LEQWO5LNC",
    "APCA-API-SECRET-KEY": "H75D7NuMaXPksXDQ56CM1Q9AEwcoiZNnNciRXojicEpM"
}

def get_alpaca_positions():
    try:
        resp = requests.get("https://paper-api.alpaca.markets/v2/positions", headers=ALPACA_HEADERS, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            lines = []
            total_value = 0
            for p in data:
                sym = p['symbol']
                qty = p['qty']
                entry = p.get('avg_entry_price', '?')
                cur = p.get('current_price', '?')
                mv = float(p.get('market_value', 0))
                lines.append(f"{sym}: {qty} @ {entry} → {cur} (value ${mv:.2f})")
                total_value += mv
            return lines, total_value
    except Exception as e:
        return [f"Error: {e}"], 0

def get_alpaca_orders():
    try:
        resp = requests.get("https://paper-api.alpaca.markets/v2/orders", headers=ALPACA_HEADERS, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            lines = []
            for o in data:
                lines.append(f"{o['symbol']}: {o['side']} {o['type']} {o['qty']} @ {o.get('limit_price','MKT')} status={o['status']}")
            return lines
    except Exception as e:
        return [f"Error: {e}"]

def get_recent_fills(limit=10):
    try:
        resp = requests.get("https://paper-api.alpaca.markets/v2/account/activities?activity_types=fill", headers=ALPACA_HEADERS, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            fills = []
            for f in data[:limit]:
                fills.append(f"{f['symbol']}: {f['side']} {f['qty']} @ {f['price']}")
            return fills
    except Exception as e:
        return [f"Error: {e}"]

def get_instagram_snapshot(usernames=None):
    """Gentle Instagram fetch (no heavy scraping)."""
    if usernames is None:
        usernames = ["_8zipp"]
    snapshots = {}
    try:
        from instagram_skill import get_profile
        for u in usernames:
            prof = get_profile(u)
            if "error" not in prof:
                snapshots[u] = {
                    "bio": prof.get("bio", ""),
                    "followers": prof.get("followers", 0),
                    "full_name": prof.get("full_name", ""),
                    "external_url": prof.get("external_url", ""),
                    "fetched_at": datetime.now().isoformat()
                }
            else:
                snapshots[u] = {"error": prof["error"]}
    except Exception as e:
        snapshots["_error"] = str(e)
    return snapshots

def main():
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    snapshot = f"\n## Auto-Snapshot (last updated: {timestamp})\n\n"
    
    # Positions
    pos_lines, total_val = get_alpaca_positions()
    snapshot += f"### Open Positions (portfolio value: ${total_val:.2f})\n"
    snapshot += "\n".join(f"- {line}" for line in pos_lines) + "\n\n"
    
    # Pending orders
    orders = get_alpaca_orders()
    snapshot += "### Pending Orders\n"
    snapshot += "\n".join(f"- {line}" for line in orders) + "\n\n"
    
    # Recent fills
    fills = get_recent_fills()
    snapshot += "### Recent Fills (last 10)\n"
    snapshot += "\n".join(f"- {line}" for line in fills) + "\n\n"
    
    # Instagram checkpoint
    ig_data = get_instagram_snapshot()
    snapshot += "### Instagram Check (tracking)\n"
    for user, data in ig_data.items():
        if "error" in data:
            snapshot += f"- {user}: ERROR - {data['error']}\n"
        else:
            snapshot += f"- @{user}: {data['followers']} followers | bio: {data['bio'][:50]}...\n"
    snapshot += "\n"
    
    # Read existing STATE.md
    with open(STATE_PATH, 'r') as f:
        content = f.read()
    
    # Replace or append snapshot section
    pattern = r"(## Auto-Snapshot.*?)(?=\n##|\Z)"
    if re.search(pattern, content, re.DOTALL):
        content = re.sub(pattern, snapshot, content, count=1, flags=re.DOTALL)
    else:
        content = content.rstrip() + "\n" + snapshot
    
    with open(STATE_PATH, 'w') as f:
        f.write(content)
    print(f"STATE.md updated at {timestamp}")

if __name__ == "__main__":
    main()

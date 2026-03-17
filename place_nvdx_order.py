#!/usr/bin/env python3
"""
Place NVDX bracket order using full cash balance via TradeExecutor.
- Buy limit @ current price (or specify override)
- TP sell limit @ X% above entry
Runs automatically after DTBP reset.
"""

import os
import sys
from datetime import datetime
from decimal import Decimal, ROUND_DOWN

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from trade_executor import TradeExecutor, market_data

def main():
    executor = TradeExecutor(dry_run=False)

    # Check account buying power
    try:
        dtbp = Decimal(executor.get_buying_power())
    except Exception as e:
        print(f"[{datetime.now()}] Failed to get buying power: {e}")
        sys.exit(1)

    if dtbp <= 0:
        print(f"[{datetime.now()}] Insufficient day trading buying power (${dtbp}). Skipping.")
        sys.exit(0)

    # Determine limit price: use current ask (buy) or a fixed offset above last
    symbol = 'NVDX'
    try:
        # Get current quote
        quote = market_data.get_current_quote(symbol)
        ask = quote.get('ask')
        last = quote.get('last')
        # Prefer ask for buy limit; fall back to last
        if ask is not None:
            limit_price = Decimal(str(ask))
        else:
            limit_price = Decimal(str(last))
    except Exception as e:
        print(f"[{datetime.now()}] Failed to get market data: {e}")
        sys.exit(1)

    # Compute TP: 4.5% above entry
    tp_mult = Decimal('1.045')
    tp_price = (limit_price * tp_mult).quantize(Decimal('0.01') if limit_price > 1 else Decimal('0.0001'))

    # Compute quantity based on DTBP (use full available)
    qty = int((dtbp / limit_price).to_integral_value(rounding=ROUND_DOWN))
    if qty <= 0:
        print(f"[{datetime.now()}] DTBP (${dtbp}) insufficient to buy even 1 share at limit ${limit_price}. Skipping.")
        sys.exit(0)

    print(f"[{datetime.now()}] DTBP: ${dtbp}, Buying {qty} {symbol} @ limit ${limit_price}, TP sell @ ${tp_price}")

    # Avoid duplicate position: check existing NVDX long
    pos = executor.get_position(symbol)
    if pos and int(pos['qty']) > 0:
        print(f"[{datetime.now()}] Already have {pos['qty']} {symbol} shares. Skipping buy.")
        sys.exit(0)

    # Submit buy limit with validation
    buy_res = executor.place_order(symbol, qty, 'buy', order_type='limit', limit_price=float(limit_price))
    if not buy_res['success']:
        print(f"[{datetime.now()}] Buy order failed: {buy_res['message']}")
        sys.exit(1)

    print(f"[{datetime.now()}] Buy order submitted: {buy_res['order_id']}")

    # Submit TP sell limit
    sell_res = executor.place_order(symbol, qty, 'sell', order_type='limit', limit_price=float(tp_price))
    if not sell_res['success']:
        print(f"[{datetime.now()}] TP sell order failed: {sell_res['message']}")
        # Note: buy may be filled; we leave it as is
        sys.exit(1)

    print(f"[{datetime.now()}] TP sell order submitted: {sell_res['order_id']}")
    print(f"[{datetime.now()}] Orders placed successfully.")

    # Log to nvdx_order_log.txt
    log_line = f"{datetime.now().isoformat()} - buy {buy_res['order_id']}, sell {sell_res['order_id']}\n"
    with open(os.path.join(BASE_DIR, 'memory', 'nvdx_order_log.txt'), 'a') as log:
        log.write(log_line)

if __name__ == '__main__':
    main()

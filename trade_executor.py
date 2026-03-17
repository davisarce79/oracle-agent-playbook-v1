#!/usr/bin/env python3
"""
Trade Executor — Mandatory wrapper for all Alpaca orders.

Features:
- Always fetches current market price before ordering
- Validates limit prices against bid/ask (warn if >1% away)
- Logs audit trail with timestamps, prices, and order IDs
- Returns order object and audit record

All trading scripts must use this instead of direct api.submit_order.
"""

import os
import json
import sys
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

# Import centralized market data
WORKSPACE = Path('/home/opc/.openclaw/workspace')
sys.path.insert(0, str(WORKSPACE))
import market_data

# Configure logging for audit trail
LOG_PATH = WORKSPACE / 'memory' / 'trade_audit.log'
os.makedirs(LOG_PATH.parent, exist_ok=True)
logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

class TradeExecutor:
    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        # Reuse Alpaca API from market_data module
        self.api = market_data._api

    def place_order(
        self,
        symbol: str,
        qty: int,
        side: str,
        order_type: str = 'limit',
        limit_price: Optional[float] = None,
        time_in_force: str = 'day',
        **kwargs
    ) -> Dict[str, Any]:
        """
        Submit an order with safety checks and audit logging.
        Returns dict with keys: success, order_id, message, audit, order_obj (if dry_run=False)
        """
        symbol = symbol.upper()
        side = side.lower()
        order_type = order_type.lower()

        # Pre-trade price validation for limit orders
        if order_type == 'limit' and limit_price is not None:
            validation = market_data.validate_limit_price(symbol, limit_price, side)
            if not validation['valid']:
                msg = f"Limit price validation failed: {'; '.join(validation['warnings'])}"
                logging.warning(f"ORDER REJECTED: {symbol} {side} {qty} @ {limit_price} — {msg}")
                return {'success': False, 'message': msg, 'audit': validation}
            # Log market context
            logging.info(f"Market snapshot for {symbol}: {validation['market']}")

        # Get current buying power if needed for position sizing (optional)
        # Not enforced here; caller should compute qty appropriately

        # Log intent
        audit = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'symbol': symbol,
            'side': side,
            'qty': qty,
            'type': order_type,
            'limit_price': limit_price,
            'time_in_force': time_in_force,
            'dry_run': self.dry_run
        }

        if self.dry_run:
            logging.info(f"[DRY RUN] Would place: {audit}")
            return {'success': True, 'order_id': 'dry-run', 'message': 'Dry run', 'audit': audit, 'order_obj': None}

        # Submit order
        try:
            order = self.api.submit_order(
                symbol=symbol,
                qty=qty,
                side=side,
                type=order_type,
                limit_price=str(limit_price) if limit_price is not None else None,
                time_in_force=time_in_force,
                **kwargs
            )
            audit['order_id'] = order.id
            audit['status'] = order.status
            audit['filled_qty'] = getattr(order, 'filled_qty', None)
            audit['filled_price'] = getattr(order, 'filled_avg_price', None)
            logging.info(f"ORDER PLACED: {audit}")
            return {'success': True, 'order_id': order.id, 'message': 'Order submitted', 'audit': audit, 'order_obj': order}
        except Exception as e:
            audit['error'] = str(e)
            logging.error(f"ORDER FAILED: {audit}")
            return {'success': False, 'message': str(e), 'audit': audit, 'order_obj': None}

    def cancel_order(self, order_id: str) -> Dict[str, Any]:
        """Cancel an order by ID."""
        try:
            self.api.cancel_order(order_id)
            logging.info(f"Cancelled order {order_id}")
            return {'success': True, 'message': f'Cancelled {order_id}'}
        except Exception as e:
            logging.error(f"Cancel failed for {order_id}: {e}")
            return {'success': False, 'message': str(e)}

    def get_position(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Get current position for symbol, or None if none."""
        try:
            pos = self.api.get_position(symbol)
            return {
                'qty': int(pos.qty),
                'avg_entry_price': float(pos.avg_entry_price),
                'market_value': float(pos.market_value),
                'unrealized_pl': float(pos.unrealized_pl),
                'current_price': float(pos.current_price) if hasattr(pos, 'current_price') else None
            }
        except Exception:
            return None

    def get_buying_power(self) -> float:
        """Return current daytrading buying power."""
        try:
            account = self.api.get_account()
            return float(account.daytrading_buying_power)
        except Exception as e:
            raise RuntimeError(f"Failed to get buying power: {e}")

# Convenience function for scripts that don't want a class
def execute_order(*args, **kwargs):
    executor = TradeExecutor()
    return executor.place_order(*args, **kwargs)

if __name__ == "__main__":
    # Quick test: print price for symbol
    if len(sys.argv) < 2:
        print("Usage: python3 trade_executor.py SYMBOL [qty] [buy|sell]")
        sys.exit(1)
    sym = sys.argv[1].upper()
    try:
        price = market_data.get_latest_trade(sym)
        print(f"{sym} last trade: ${price:.4f}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

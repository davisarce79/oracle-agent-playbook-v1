#!/usr/bin/env python3
"""
Market Data Utility — Single Source of Truth for Prices

Provides:
  - get_latest_trade(symbol): last trade price (real-time)
  - get_current_quote(symbol): bid, ask, last
  - get_price_with_fallback(symbol): uses last close if market closed
  - with retry, timeout, and short-term caching (2s)

All trading code must use this to avoid stale/incorrect prices.
"""

import time
import threading
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

import alpaca_trade_api as tradeapi
import requests

# Load Alpaca credentials (workspace-relative)
def _load_creds():
    creds = {}
    try:
        with open('/home/opc/.openclaw/workspace/.openclaw/credentials/alpaca.txt', 'r') as f:
            for line in f:
                if '=' in line:
                    k, v = line.strip().split('=', 1)
                    creds[k.strip()] = v.strip()
    except Exception as e:
        raise RuntimeError(f"Failed to load Alpaca credentials: {e}")
    return creds

_creds = _load_creds()
_api = tradeapi.REST(_creds['ALPACA_API_KEY'], _creds['ALPACA_SECRET_KEY'], base_url='https://paper-api.alpaca.markets')

# Simple in-memory cache: {symbol: (timestamp, value)}
_cache: Dict[str, tuple[float, datetime]] = {}
_cache_lock = threading.Lock()
CACHE_TTL = 2.0  # seconds

def _now():
    return datetime.now()

def get_latest_trade(symbol: str, force_refresh: bool = False) -> float:
    """
    Get the most recent trade price for `symbol`.
    Uses a 2-second cache to respect rate limits but stays fresh.
    Retries once on failure.
    """
    with _cache_lock:
        if not force_refresh and symbol in _cache:
            ts, price = _cache[symbol]
            if (_now() - ts).total_seconds() < CACHE_TTL:
                return price

    # Fetch from Alpaca
    try:
        trade = _api.get_latest_trade(symbol)
        price = float(trade.price)
    except Exception as e:
        # Try one retry
        time.sleep(0.5)
        try:
            trade = _api.get_latest_trade(symbol)
            price = float(trade.price)
        except Exception as e2:
            raise RuntimeError(f"Failed to fetch latest trade for {symbol}: {e2}")

    with _cache_lock:
        _cache[symbol] = ( _now(), price)
    return price

def get_current_quote(symbol: str) -> Dict[str, float]:
    """
    Get current bid, ask, and last price.
    Returns dict: {'bid': float, 'ask': float, 'last': float}
    """
    try:
        quote = _api.get_latest_quote(symbol)
        bid = float(quote.bid_price) if quote.bid_price else None
        ask = float(quote.ask_price) if quote.ask_price else None
        last = float(quote.last_price) if quote.last_price else None
        return {'bid': bid, 'ask': ask, 'last': last, 'timestamp': _now().isoformat()}
    except Exception as e:
        raise RuntimeError(f"Failed to fetch quote for {symbol}: {e}")

def get_price_with_fallback(symbol: str) -> float:
    """
    Get a usable price: try latest trade; if market closed, use last close from daily bars.
    """
    try:
        return get_latest_trade(symbol)
    except Exception:
        # Market closed or no trades — fetch last daily close
        try:
            bars = _api.get_bars(symbol, '1Day', limit=1).df
            if bars.empty:
                raise ValueError("No recent data")
            close = float(bars.iloc[-1]['close'])
            return close
        except Exception:
            raise RuntimeError(f"Cannot determine price for {symbol}")

def get_account_buying_power() -> float:
    """Return current daytrading buying power (paper trading)."""
    try:
        account = _api.get_account()
        return float(account.daytrading_buying_power)
    except Exception as e:
        raise RuntimeError(f"Failed to get account info: {e}")

def validate_limit_price(symbol: str, limit_price: float, side: str, threshold_pct: float = 0.01) -> Dict[str, Any]:
    """
    Check if a limit price is reasonable compared to current market.
    Returns {'valid': bool, 'warnings': [str], 'market': dict}
    For buys: limit_price should be <= ask (or within threshold above ask)
    For sells: limit_price should be >= bid (or within threshold below bid)
    """
    quote = get_current_quote(symbol)
    warnings = []
    valid = True

    bid = quote.get('bid')
    ask = quote.get('ask')
    last = quote.get('last')

    if side == 'buy':
        if ask is not None and limit_price > ask * (1 + threshold_pct):
            warnings.append(f"Buy limit ${limit_price:.4f} is >{threshold_pct*100:.1f}% above ask ${ask:.4f}")
            valid = False
        elif last and limit_price > last * (1 + threshold_pct):
            warnings.append(f"Buy limit ${limit_price:.4f} is >{threshold_pct*100:.1f}% above last trade ${last:.4f}")
    elif side == 'sell':
        if bid is not None and limit_price < bid * (1 - threshold_pct):
            warnings.append(f"Sell limit ${limit_price:.4f} is <{threshold_pct*100:.1f}% below bid ${bid:.4f}")
            valid = False
        elif last and limit_price < last * (1 - threshold_pct):
            warnings.append(f"Sell limit ${limit_price:.4f} is <{threshold_pct*100:.1f}% below last trade ${last:.4f}")

    return {'valid': valid, 'warnings': warnings, 'market': quote}

# Example usage guard: when imported as main, print current price for a symbol
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python3 market_data.py SYMBOL")
        sys.exit(1)
    sym = sys.argv[1].upper()
    try:
        price = get_latest_trade(sym)
        print(f"{sym} last trade: ${price:.4f}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

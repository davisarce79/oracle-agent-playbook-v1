"""
Finnhub data source for technical indicators and market data.
Uses API key provided by user.
"""

import os
import requests
import pandas as pd
from datetime import datetime, timedelta

FINNHUB_API_KEY = "d6p5km1r01qk3chj0kugd6p5km1r01qk3chj0kv0"
FINNHUB_BASE = "https://finnhub.io/api/v1"

def get_finnhub_candles(symbol: str, resolution: str = "D", days_back: int = 60):
    """
    Fetch OHLC candles from Finnhub.
    resolution: D (daily), 1 (1min), 5, 15, 30, 60, W, M
    Returns DataFrame with columns: close, high, low, open, volume
    """
    end = datetime.now()
    # Convert to Unix timestamp in seconds
    to_ts = int(end.timestamp())
    from_ts = int((end - timedelta(days=days_back)).timestamp())
    
    url = f"{FINNHUB_BASE}/stock/candle"
    params = {
        "symbol": symbol,
        "resolution": resolution,
        "from": from_ts,
        "to": to_ts,
        "token": FINNHUB_API_KEY
    }
    try:
        resp = requests.get(url, params=params, timeout=10)
        data = resp.json()
        if data.get("s") != "ok":
            raise ValueError(f"Finnhub error: {data.get('error', 'Unknown error')}")
        # Build DataFrame
        df = pd.DataFrame({
            "close": data["c"],
            "high": data["h"],
            "low": data["l"],
            "open": data["o"],
            "volume": data["v"]
        })
        # timestamps are in seconds; convert to datetime index for chronology
        df.index = pd.to_datetime(data["t"], unit="s")
        df = df.sort_index()  # chronological ascending
        df = df.reset_index(drop=True)
        return df
    except Exception as e:
        print(f"Finnhub fetch failed: {e}")
        return None

def get_finnhub_technical_indicators(symbol: str, indicator: str, interval: str = "D", timespan: int = 14):
    """
    Get technical indicator series from Finnhub.
    indicator examples: rsi, macd, stoch, bbands, adx, atr, obv, vwap, cci, willr, aroon, mfi
    Returns most recent value.
    """
    url = f"{FINNHUB_BASE}/indicator"
    params = {
        "symbol": symbol,
        "resolution": interval,
        "indicator": indicator,
        "timespan": timespan,
        "token": FINNHUB_API_KEY
    }
    try:
        resp = requests.get(url, params=params, timeout=10)
        data = resp.json()
        if data.get("s") != "ok":
            raise ValueError(f"Finnhub indicator error: {data.get('error', 'Unknown error')}")
        # Return last value from the series
        values = data.get("t", [])
        if not values:
            return None
        # Map indicator-specific field names
        field_map = {
            "rsi": "rsi",
            "macd": "macdLine",
            "macd_signal": "macdSignal",
            "macd_hist": "macdHist",
            "stoch": "slowk",
            "bbands": "middleband",
            "adx": "adx",
            "atr": "atr",
            "obv": "obv",
            "vwap": "vwap",
            "cci": "cci",
            "willr": "willr",
            "aroon": "aroon",
            "mfi": "mfi"
        }
        # Try to extract a numeric value from the last data point
        last_idx = -1
        last_val = None
        for key, val in data.items():
            if isinstance(val, list) and len(val) > 0:
                last_val = val[last_idx]
                # Check if we have a mapped field that looks right
                if indicator in field_map and field_map[indicator] in data:
                    last_val = data[field_map[indicator]][last_idx]
                break
        return last_val
    except Exception as e:
        print(f"Finnhub indicator fetch failed ({indicator}): {e}")
        return None

if __name__ == "__main__":
    # Test fetch
    df = get_finnhub_candles("WULF", days_back=60)
    print(df.tail())
    rsi = get_finnhub_technical_indicators("WULF", "rsi")
    print("RSI:", rsi)

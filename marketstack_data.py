"""
MarketStack data source for fundamentals and end-of-day data.
Uses API key provided by user.
"""

import os
import requests
import pandas as pd
from datetime import datetime, timedelta

MARKETSTACK_API_KEY = "3c54efe09c16cb098da0a2ad0e5195f6"
MARKETSTACK_BASE = "http://api.marketstack.com/v1"

def get_marketstack_eod(symbol: str, limit: int = 100):
    """
    Fetch End-of-Day (EOD) data from MarketStack.
    Returns DataFrame with columns: close, high, low, open, volume, date
    """
    url = f"{MARKETSTACK_BASE}/eod"
    params = {
        "access_key": MARKETSTACK_API_KEY,
        "symbols": symbol,
        "limit": limit
    }
    try:
        resp = requests.get(url, params=params, timeout=10)
        data = resp.json()
        if "error" in data:
            raise ValueError(f"MarketStack error: {data['error']['message']}")
        # Response format: {"data":[{...}]}
        records = data.get("data", [])
        if not records:
            return None
        df = pd.DataFrame(records)
        # rename columns to match our schema
        df = df.rename(columns={
            "close": "close",
            "high": "high",
            "low": "low",
            "open": "open",
            "volume": "volume",
            "date": "date"
        })
        # ensure chronological order (oldest first)
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date').reset_index(drop=True)
        # keep only needed columns
        df = df[['close','high','low','open','volume']]
        return df
    except Exception as e:
        print(f"MarketStack fetch failed: {e}")
        return None

def get_marketstack_fundamentals(symbol: str):
    """
    Fetch fundamental data (financials) if available in MarketStack.
    Note: MarketStack fundamentals require paid plan; this may return empty on free tier.
    """
    url = f"{MARKETSTACK_BASE}/fundamentals"
    params = {
        "access_key": MARKETSTACK_API_KEY,
        "symbols": symbol
    }
    try:
        resp = requests.get(url, params=params, timeout=10)
        data = resp.json()
        if "error" in data:
            raise ValueError(f"MarketStack fundamentals error: {data['error']['message']}")
        return data.get("data", {})
    except Exception as e:
        print(f"MarketStack fundamentals failed: {e}")
        return None

if __name__ == "__main__":
    # Test fetch
    df = get_marketstack_eod("AAPL", limit=10)
    print(df.tail() if df is not None else "No data")
    fundamentals = get_marketstack_fundamentals("AAPL")
    print("Fundamentals:", fundamentals)

"""
Custom Technical Analyst Agent for TradingAgents
Integrates HMM + Elliott + Fibonacci + RSI/MACD from our strategy.
"""

import os
import sys
import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import requests

# Add workspace to path for imports
sys.path.append('/home/opc/.openclaw/workspace')

# Load Alpaca and Alpha Vantage credentials
def load_creds():
    alpaca_path = '/home/opc/.openclaw/workspace/.openclaw/credentials/alpaca.txt'
    with open(alpaca_path, 'r') as f:
        content = f.read().splitlines()
        creds = {}
        for line in content:
            if '=' in line:
                key, val = line.split('=')
                creds[key.strip()] = val.strip()
        return creds

ALPACA_CREDS = load_creds()
ALPHAVANTAGE_API_KEY = '7UCLW4EJ6QY2Y5H4'  # from user
FINNHUB_API_KEY = "d6p5km1r01qk3chj0kugd6p5km1r01qk3chj0kv0"
MARKETSTACK_API_KEY = "3c54efe09c16cb098da0a2ad0e5195f6"
FINNHUB_API_KEY = "d6p5km1r01qk3chj0kugd6p5km1r01qk3chj0kv0"

# --- Data fetching functions ---

def get_finnhub_candles(symbol: str, resolution: str = "D", days_back: int = 60):
    """Fetch OHLC candles from Finnhub."""
    end = datetime.now()
    to_ts = int(end.timestamp())
    from_ts = int((end - timedelta(days=days_back)).timestamp())
    url = f"https://finnhub.io/api/v1/stock/candle"
    params = {"symbol": symbol, "resolution": resolution, "from": from_ts, "to": to_ts, "token": FINNHUB_API_KEY}
    try:
        resp = requests.get(url, params=params, timeout=10)
        data = resp.json()
        if data.get("s") != "ok":
            raise ValueError(f"Finnhub error: {data.get('error', 'Unknown error')}")
        df = pd.DataFrame({
            "close": data["c"],
            "high": data["h"],
            "low": data["l"],
            "open": data["o"],
            "volume": data["v"]
        })
        df.index = pd.to_datetime(data["t"], unit="s")
        df = df.sort_index().reset_index(drop=True)
        return df
    except Exception as e:
        print(f"Finnhub fetch failed: {e}")
        return None

def get_finnhub_indicator(symbol: str, indicator: str, interval: str = "D", timespan: int = 14):
    """Fetch a single technical indicator from Finnhub."""
    url = f"https://finnhub.io/api/v1/indicator"
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
            return None
        # Extract last value; handle various response shapes
        for key, val in data.items():
            if isinstance(val, list) and len(val) > 0:
                return val[-1]
        return None
    except Exception as e:
        print(f"Finnhub indicator {indicator} failed: {e}")
        return None

def get_alpha_vantage_data(symbol, limit_bars=200):
    url = 'https://www.alphavantage.co/query'
    params = {
        'function': 'TIME_SERIES_DAILY',
        'symbol': symbol,
        'outputsize': 'compact',
        'apikey': ALPHAVANTAGE_API_KEY
    }
    try:
        resp = requests.get(url, params=params, timeout=10)
        data = resp.json()
        if 'Time Series (Daily)' not in data:
            return None
        series = data['Time Series (Daily)']
        df_data = []
        dates = sorted(series.keys(), reverse=True)[:limit_bars]
        for date_str in dates:
            bar = series[date_str]
            df_data.append({
                'close': float(bar['4. close']),
                'high': float(bar['2. high']),
                'low': float(bar['3. low']),
                'open': float(bar['1. open']),
                'volume': int(bar['5. volume'])
            })
        df = pd.DataFrame(df_data)
        return df.iloc[::-1].reset_index(drop=True)  # chronological
    except Exception as e:
        print(f"Alpha Vantage fetch failed: {e}")
        return None

def get_marketstack_eod(symbol: str, limit: int = 100):
    """Fetch End-of-Day data from MarketStack."""
    url = "https://api.marketstack.com/v1/eod"
    params = {
        "access_key": MARKETSTACK_API_KEY,
        "symbols": symbol,
        "limit": limit
    }
    try:
        resp = requests.get(url, params=params, timeout=10)
        data = resp.json()
        if "error" in data:
            raise ValueError(f"MarketStack: {data['error'].get('message','Unknown')}")
        records = data.get("data", [])
        if not records:
            return None
        df = pd.DataFrame(records)
        # Normalize columns
        df = df.rename(columns={
            "close": "close",
            "high": "high",
            "low": "low",
            "open": "open",
            "volume": "volume"
        })
        # Convert date and sort
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values('date').reset_index(drop=True)
        return df[['close','high','low','open','volume']]
    except Exception as e:
        print(f"MarketStack fetch failed: {e}")
        return None

def compute_indicators(df):
    """Compute RSI, MACD, Elliott/Fib zones, volume check, and historical bounce probability."""
    # ... existing calculations ...
    
    # After computing other indicators, add historical bounce check
    # We'll compute on the df which is chronological (oldest first)
    current_price = df['close'].iloc[-1]
    
    # 1. All-time low check (avoid if near 52w low)
    low_52 = df['low'].min()
    near_52w_low = (current_price - low_52) / low_52 < 0.15  # within 15% of 52w low
    
    # 2. Historical bounce probability: find past times when price <= current_price (within ±2%)
    # and see if price rose >10% within next 20-40 days
    tolerance = 0.02  # ±2%
    bounce_threshold_pct = 0.10  # 10% rally
    lookahead_min = 20
    lookahead_max = 40
    total_occurrences = 0
    bounce_occurrences = 0
    n = len(df)
    for i in range(n - lookahead_max):
        price_i = df['close'].iloc[i]
        # Is this a similar or lower price level?
        if price_i <= current_price * (1 + tolerance) and price_i >= current_price * (1 - tolerance):
            # Check future window
            future_max = df['close'].iloc[i+lookahead_min:i+lookahead_max+1].max()
            if future_max >= price_i * (1 + bounce_threshold_pct):
                bounce_occurrences += 1
            total_occurrences += 1
    # Compute bounce probability
    if total_occurrences >= 5:
        bounce_prob = bounce_occurrences / total_occurrences
    else:
        bounce_prob = None  # insufficient data
    
    # Determine if this is historically a bounce level
    historical_bounce_likely = (bounce_prob is not None and bounce_prob >= 0.30 and not near_52w_low)
    
    return {
        'price': current_price,
        'rsi': rsi.iloc[-1],
        'macd_hist': hist.iloc[-1],
        'fib_618': fib_618,
        'entry_zone_lower': entry_zone_lower,
        'entry_zone_upper': entry_zone_upper,
        'in_entry_zone': in_entry_zone,
        'vol_expanded': vol_expanded,
        'tenkan': tenkan.iloc[-1],
        'kijun': kijun.iloc[-1],
        'cloud_top': cloud_top.iloc[-1],
        'cloud_bot': cloud_bot.iloc[-1],
        'historical_bounce_likely': historical_bounce_likely,
        'bounce_probability': bounce_prob,
        'near_52w_low': near_52w_low,
        'data_source': 'alphavantage'
    }

def get_market_data(symbol, days_back=45):
    """Fetch data from Finnhub → Alpha Vantage → MarketStack (in that order)."""
    # ... unchanged ...

def analyze_technical(symbol: str, date: str = None) -> dict:
    """
    Main entry point for TradingAgents Technical Analyst.
    Returns a structured analysis with trade recommendation.
    """
    try:
        df = get_market_data(symbol)
        ind = compute_indicators(df)
        
        # Determine signal strength
        confluence_score = 0
        reasons = []
        
        # 1. Fib entry zone
        if ind['in_entry_zone']:
            confluence_score += 1
            reasons.append("Price in Fib 61.8% ±5% zone")
        
        # 2. RSI oversold (<45)
        if ind['rsi'] < 45:
            confluence_score += 1
            reasons.append(f"RSI={ind['rsi']:.1f} (oversold/ recovering)")
        
        # 3. MACD histogram positive/rising
        if ind['macd_hist'] > -0.05:
            confluence_score += 1
            reasons.append(f"MACD hist={ind['macd_hist']:.3f} (bullish/neutral)")
        
        # 4. Volume expansion
        if ind['vol_expanded']:
            confluence_score += 1
            reasons.append("Volume > 20% average")
        
        # 5. Price relative to Ichimoku cloud
        if ind['price'] > ind['cloud_bot']:
            confluence_score += 0.5
            reasons.append("Price above cloud support")
        
        # 6. Opportunistic: historical bounce likely despite not in entry zone
        if not ind['in_entry_zone'] and ind.get('historical_bounce_likely'):
            confluence_score += 1
            reasons.append(f"Historical bounce likely ({ind.get('bounce_probability',0)*100:.0f}% from similar levels)")
            # Also note not near 52w low
            if ind.get('near_52w_low'):
                # Should not happen if bounce_likely is true, but just in case
                confluence_score -= 1
                reasons.append("(But near 52w low, caution)")
        
        # Final recommendation
        if confluence_score >= 2:
            recommendation = "BUY"
            confidence = min(confluence_score / 4 * 100, 100)
        elif confluence_score >= 1:
            recommendation = "HOLD"
            confidence = 50
        else:
            recommendation = "WATCH"
            confidence = 0
        
        # Calculate entry, TP, SL based on Fib and Ichimoku
        entry_price = ind['fib_618']  # academic entry
        take_profit = ind['price'] * 1.03  # +3% from current
        stop_loss = ind['cloud_bot'] * 0.99  # just below cloud
        
        return {
            "symbol": symbol,
            "date": date or datetime.now().strftime("%Y-%m-%d"),
            "current_price": round(ind['price'], 2),
            "indicators": {
                "RSI": round(ind['rsi'], 2),
                "MACD_hist": round(ind['macd_hist'], 3),
                "Fib_618": round(ind['fib_618'], 2),
                "Kijun": round(ind['kijun'], 2),
                "Cloud_top": round(ind['cloud_top'], 2),
                "Cloud_bot": round(ind['cloud_bot'], 2)
            },
            "confluence_score": confluence_score,
            "reasons": reasons,
            "recommendation": recommendation,
            "confidence_pct": round(confidence, 1),
            "trade_parameters": {
                "entry": round(entry_price, 2),
                "take_profit": round(take_profit, 2),
                "stop_loss": round(stop_loss, 2),
                "position_size_pct": 5  # static for now
            },
            "data_source": ind['data_source']
        }
        
    except Exception as e:
        return {
            "symbol": symbol,
            "error": str(e),
            "recommendation": "ERROR"
        }

# Example usage (for testing)
if __name__ == "__main__":
    result = analyze_technical("WULF")
    print(json.dumps(result, indent=2))

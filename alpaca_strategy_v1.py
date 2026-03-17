import alpaca_trade_api as tradeapi
import pandas as pd
import numpy as np
import time
import os
import requests
import json

# Load credentials
def load_creds():
    with open('.openclaw/credentials/alpaca.txt', 'r') as f:
        content = f.read().splitlines()
        creds = {}
        for line in content:
            if '=' in line:
                key, val = line.split('=')
                creds[key.strip()] = val.strip()
        return creds

creds = load_creds()
api = tradeapi.REST(creds['ALPACA_API_KEY'], creds['ALPACA_SECRET_KEY'], base_url='https://paper-api.alpaca.markets')

# Alpha Vantage config (supplemental/fallback)
ALPHAVANTAGE_API_KEY = '7UCLW4EJ6QY2Y5H4'  # Provided by user; consider storing in credentials
ALPHAVANTAGE_URL = 'https://www.alphavantage.co/query'

SYMBOL = 'WULF'
TIMEFRAME = '1Hour'

def get_alpha_vantage_data(symbol, limit_bars=200):
    """
    Fallback data fetch from Alpha Vantage.
    Uses intraday (60min) if available, else daily.
    Returns DataFrame with columns: close, high, low, open, volume
    """
    # Try intraday 60min first (requires market to be open for recent data)
    params = {
        'function': 'TIME_SERIES_INTRADAY',
        'symbol': symbol,
        'interval': '60min',
        'outputsize': 'compact',
        'apikey': ALPHAVANTAGE_API_KEY
    }
    try:
        resp = requests.get(ALPHAVANTAGE_URL, params=params, timeout=10)
        data = resp.json()
        if 'Time Series (60min)' not in data:
            # Fallback to daily
            params['function'] = 'TIME_SERIES_DAILY'
            resp = requests.get(ALPHAVANTAGE_URL, params=params, timeout=10)
            data = resp.json()
            ts_key = 'Time Series (Daily)'
        else:
            ts_key = 'Time Series (60min)'
        
        if ts_key not in data:
            raise ValueError(f"Alpha Vantage did not return data: {data.get('Note', 'Unknown error')}")
        
        series = data[ts_key]
        df_data = []
        # Take the most recent N bars
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
        return pd.DataFrame(df_data)
    except Exception as e:
        print(f"Alpha Vantage fetch failed: {e}")
        return None

def get_indicators(symbol):
    import datetime
    end = datetime.datetime.now() - datetime.timedelta(days=1)
    start = end - datetime.timedelta(days=45) # Increased window for better wave detection
    
    start_iso = start.strftime('%Y-%m-%dT%H:%M:%SZ')
    end_iso = end.strftime('%Y-%m-%dT%H:%M:%SZ')

    df_data = []
    try:
        bars_resp = api.get_bars(symbol, TIMEFRAME, limit=500, start=start_iso, end=end_iso, feed='iex')
        for bar in bars_resp:
            df_data.append({'close': bar.c, 'high': bar.h, 'low': bar.l, 'open': bar.o, 'volume': bar.v})
    except Exception as e:
        print(f"Alpaca data error: {e}")
    
    # Fallback to Alpha Vantage if Alpaca returned no data
    if not df_data:
        print("Alpaca data empty, falling back to Alpha Vantage...")
        df = get_alpha_vantage_data(symbol, limit_bars=200)
        if df is None or df.empty:
            raise ValueError("No data from Alpaca or Alpha Vantage.")
        bars = df.iloc[::-1].reset_index(drop=True)  # Reverse to chronological (oldest first)
    else:
        bars = pd.DataFrame(df_data)
        # Alpaca bars should be chronological already; ensure index order
        bars = bars.reset_index(drop=True)
    
    # bars now in chronological order (index 0 = oldest)
    data_source = 'alpaca' if df_data else 'alphavantage'
    # 1. RSI (14)
    delta = bars['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    
    # 2. MACD (12, 26, 9)
    exp1 = bars['close'].ewm(span=12, adjust=False).mean()
    exp2 = bars['close'].ewm(span=26, adjust=False).mean()
    macd = exp1 - exp2
    signal_line = macd.ewm(span=9, adjust=False).mean()
    hist = macd - signal_line

    # 3. Academic Elliott Logic (Wave C Extensions & 5% Buffer)
    recent_high = bars['high'].max()
    recent_low = bars['low'].min()
    current_price = bars['close'].iloc[-1]
    
    # Fib Retracements
    fib_618 = recent_high - (recent_high - recent_low) * 0.618
    # 5% Academic Error Buffer (from Dr. Alalaya research)
    entry_zone_upper = fib_618 * 1.05
    entry_zone_lower = fib_618 * 0.95
    
    # Volume Check (Wave C vs B logic)
    avg_vol = bars['volume'].tail(20).mean()
    curr_vol = bars['volume'].iloc[-1]
    vol_expansion = curr_vol > (avg_vol * 1.2) # 20% volume pickup

    return {
        'price': current_price,
        'rsi': rsi.iloc[-1],
        'hist': hist.iloc[-1],
        'fib_618': fib_618,
        'in_entry_zone': entry_zone_lower <= current_price <= entry_zone_upper,
        'vol_expanded': vol_expansion,
        'data_source': data_source
    }

def execute_trade(symbol, quantity):
    try:
        from trade_executor import TradeExecutor, market_data
        data = get_indicators(symbol)
        limit_price = data['price']
        # Validate limit price against current market
        validation = market_data.validate_limit_price(symbol, limit_price, 'buy')
        if not validation['valid']:
            print(f"Limit price validation failed: {'; '.join(validation['warnings'])}")
            return None
        executor = TradeExecutor(dry_run=False)
        result = executor.place_order(
            symbol=symbol,
            qty=quantity,
            side='buy',
            order_type='limit',
            limit_price=limit_price,
            time_in_force='day',
            extended_hours=True
        )
        if result['success']:
            print(f">>> ACADEMIC CONFLUENCE ORDER: Buy {quantity} shares of {symbol} at ${limit_price} (order {result['order_id']})")
            return result['order_obj']
        else:
            print(f"Trade failed: {result['message']}")
            return None
    except Exception as e:
        print(f"Trade failed: {e}")

def is_market_open():
    import datetime, pytz
    tz = pytz.timezone('US/Eastern')
    now = datetime.datetime.now(tz)
    if now.weekday() == 5: return False
    if now.weekday() == 6 and now.hour < 20: return False
    return True

from hmm_strat import HMMTradingEngine

# Initialize HMM Engine
hmm_engine = HMMTradingEngine(creds['ALPACA_API_KEY'], creds['ALPACA_SECRET_KEY'])

def check_signals():
    if not is_market_open():
        return False

    print(f"Analyzing {SYMBOL} with Academic HMM + Elliott Strategy...")
    try:
        data = get_indicators(SYMBOL)
        print(f"[Data source: {data.get('data_source', 'unknown')}]")
        print(f"Price: ${data['price']:.2f} | RSI: {data['rsi']:.2f} | Fib 61.8% Zone: ${data['fib_618']:.2f}")

        # REFINED ACADEMIC ENTRY (Now with HMM Regime Confirmation):
        # 1. Elliott/Fib: Price in the 5% error-adjusted 61.8% Fib Zone
        # 2. Momentum: RSI is recovering (< 45) and MACD is neutral/positive
        # 3. HMM: Execute logic check (Daily Bull + 5-Min Bull)
        
        # We check the HMM state separately
        account = api.get_account()
        qty = int((float(account.buying_power) * 0.95) / data['price'])
        
        if data['in_entry_zone'] and data['rsi'] < 45 and data['hist'] > -0.05:
            print(">>> ACADEMIC CONFLUENCE DETECTED. Checking HMM Regimes...")
            hmm_engine.execute_logic(SYMBOL, qty)
        else:
            print("No confluence detected. Observation continues.")
    except Exception as e:
        print(f"Scan error: {e}")

if __name__ == "__main__":
    check_signals()

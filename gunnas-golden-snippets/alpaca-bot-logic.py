import alpaca_trade_api as tradeapi
import pandas as pd
import numpy as np
import time
import os

# Load credentials from .openclaw/credentials/alpaca.txt
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

# Initialize Alpaca API (Paper)
api = tradeapi.REST(
    creds['ALPACA_API_KEY'],
    creds['ALPACA_SECRET_KEY'],
    base_url='https://paper-api.alpaca.markets'
)

SYMBOL = 'WULF'
TIMEFRAME = '1Hour' # Using 1H for more frequent checks, but signal is based on 4H logic

def get_indicators(symbol):
    # Fetch latest bars - using explicit date for safety
    import datetime
    # Alpaca Free Tier has a 15-minute delay and restricted history.
    # We'll look back 1 month and end 1 day ago to avoid "recent SIP data" restrictions.
    end = datetime.datetime.now() - datetime.timedelta(days=1)
    start = end - datetime.timedelta(days=30)
    
    start_iso = start.strftime('%Y-%m-%dT%H:%M:%SZ')
    end_iso = end.strftime('%Y-%m-%dT%H:%M:%SZ')

    df_data = []
    try:
        # For Free Tier, we MUST use feed='iex' or we get the SIP error
        bars_resp = api.get_bars(symbol, TIMEFRAME, limit=100, start=start_iso, end=end_iso, feed='iex')
        for bar in bars_resp:
            df_data.append({'close': bar.c})
    except Exception as e:
        print(f"Error fetching WULF data: {e}.")
    
    if not df_data:
        # If IEX fails, try a broader range or a common ticker to test
        print("WULF returned no data via IEX. Testing with BTC/USD (24/7 data)...")
        bars_resp = api.get_crypto_bars("BTC/USD", TIMEFRAME, limit=10).df
        if not bars_resp.empty:
            print("Connection OK: BTC/USD price is", bars_resp['close'].iloc[-1])
            raise ValueError("WULF data restricted. Try during market hours or with higher tier.")

    bars = pd.DataFrame(df_data)
    
    # RSI Calculation (14)
    delta = bars['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    
    # MACD Calculation (12, 26, 9)
    exp1 = bars['close'].ewm(span=12, adjust=False).mean()
    exp2 = bars['close'].ewm(span=26, adjust=False).mean()
    macd = exp1 - exp2
    signal_line = macd.ewm(span=9, adjust=False).mean()
    histogram = macd - signal_line
    
    return {
        'price': bars['close'].iloc[-1],
        'rsi': rsi.iloc[-1],
        'macd': macd.iloc[-1],
        'signal': signal_line.iloc[-1],
        'hist': histogram.iloc[-1]
    }

def execute_trade(symbol, quantity):
    try:
        # Submit a market buy order for Paper Trading
        order = api.submit_order(
            symbol=symbol,
            qty=quantity,
            side='buy',
            type='market',
            time_in_force='gtc'
        )
        print(f">>> ORDER SUBMITTED: Buy {quantity} shares of {symbol} (Order ID: {order.id})")
        return order
    except Exception as e:
        print(f"Error submitting order: {e}")
        return None

def check_signals():
    print(f"Checking signals for {SYMBOL}...")
    try:
        data = get_indicators(SYMBOL)
    except Exception as e:
        print(f"Signal Check Failed: {e}")
        return False
    
    print(f"Price: ${data['price']:.2f} | RSI: {data['rsi']:.2f} | MACD Hist: {data['hist']:.4f}")
    
    # Bullish Reversal Logic (Davis's Signals)
    # Trigger: RSI is oversold (< 35) AND MACD Histogram is ticking up
    if data['rsi'] < 35 and data['hist'] > -0.05:
        print(">>> BULLISH SIGNAL DETECTED <<<")
        
        # Calculate max shares for $100k
        account = api.get_account()
        buying_power = float(account.buying_power)
        price = data['price']
        
        # Max shares (using 95% of buying power for safety margin/slippage)
        quantity = int((buying_power * 0.95) / price)
        
        if quantity > 0:
            print(f"Allocating ${buying_power:.2f} to {quantity} shares of {SYMBOL}")
            execute_trade(SYMBOL, quantity)
            return True
        else:
            print("Insufficient buying power for trade.")
    
    print("No signal confirmed. Standing by.")
    return False

if __name__ == "__main__":
    check_signals()

import alpaca_trade_api as tradeapi
import os

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

try:
    bars = api.get_bars('WULF', '1Min', limit=1).df
    if not bars.empty:
        print(f"LATEST_PRICE:{bars['close'].iloc[-1]}")
    else:
        print("NO_DATA")
except Exception as e:
    print(f"ERROR:{e}")

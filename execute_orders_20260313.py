import alpaca_trade_api as tradeapi
import os

def load_creds():
    with open('.openclaw/credentials/alpaca.txt', 'r') as f:
        content = f.read().splitlines()
        creds = {}
        for line in content:
            if '=' in line:
                key, val = line.split('=', 1)
                creds[key.strip()] = val.strip()
        return creds

creds = load_creds()
api = tradeapi.REST(creds['ALPACA_API_KEY'], creds['ALPACA_SECRET_KEY'], base_url='https://paper-api.alpaca.markets')

# Verify account
account = api.get_account()
print(f"Account: {account.id}")
print(f"Buying Power: ${float(account.buying_power):,.2f}")
print(f"Equity: ${float(account.equity):,.2f}")

# Orders: (ticker, buy_limit, sell_limit)
orders = [
    ('TSLL', 14.28, 14.78),
    ('TSLR', 24.04, 24.99),
    ('TSLT', 19.86, 20.26),
    ('NVDX', 15.89, 16.09),
    ('NVDY', 13.69, 13.79),
    ('NVDL', 82.50, 84.00),
    ('NVDU', 110.40, 112.00),
    ('MARA', 8.85, 8.99),
    ('WULF', 14.60, 15.15),
    ('CRCL', 16.31, 16.50)
]

NOTIONAL = 2000.0
print("\nPlacing bracket orders (~$2,000 notional each)...")
results = []

for ticker, buy_price, sell_price in orders:
    qty = int(NOTIONAL // buy_price)
    if qty == 0:
        results.append(f"{ticker}: Skipped (price ${buy_price} too high for ${NOTIONAL} notional)")
        continue
    try:
        # Bracket order requires both take_profit and stop_loss.
        # Set stop_loss far away (50% below entry) to avoid premature trigger.
        stop_price = round(buy_price * 0.5, 2)
        order = api.submit_order(
            symbol=ticker,
            qty=qty,
            side='buy',
            type='limit',
            limit_price=buy_price,
            time_in_force='gtc',
            order_class='bracket',
            take_profit=dict(limit_price=sell_price),
            stop_loss=dict(stop_price=stop_price, limit_price=stop_price)
        )
        results.append(f"{ticker}: BUY {qty}@{buy_price} | TP {sell_price} | SL {stop_price} — Order ID: {order.id}")
    except Exception as e:
        results.append(f"{ticker}: ERROR — {e}")

print("\nPlacement summary:")
for r in results:
    print(r)

print("\nCurrent open orders (after placement):")
open_ords = api.list_orders(status='open', limit=50)
if not open_ords:
    print("No open orders.")
else:
    for o in open_ords:
        leg = f" (class: {o.order_class})" if o.order_class else ""
        print(f"{o.symbol}: {o.side} {o.qty} @ {o.limit_price or o.stop_price} [{o.type}]{leg} — {o.id}")

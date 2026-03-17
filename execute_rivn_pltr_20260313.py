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

account = api.get_account()
buying_power = float(account.buying_power)
print(f"Account buying power: ${buying_power:,.2f}")

# Allocate half to each ticker
half = buying_power / 2

orders = [
    {
        'symbol': 'RIVN',
        'buy_price': 14.89,
        'sell_price': 17.00,
        'notional': half
    },
    {
        'symbol': 'PLTR',
        'buy_price': 150.79,
        'sell_price': 156.99,
        'notional': half
    }
]

print("\nPlacing bracket orders...")
for o in orders:
    qty = int(o['notional'] // o['buy_price'])
    if qty == 0:
        print(f"{o['symbol']}: Skipped (price too high for allocated notional)")
        continue
    stop_price = round(o['buy_price'] * 0.5, 2)  # far stop
    try:
        order = api.submit_order(
            symbol=o['symbol'],
            qty=qty,
            side='buy',
            type='limit',
            limit_price=o['buy_price'],
            time_in_force='gtc',
            order_class='bracket',
            take_profit=dict(limit_price=o['sell_price']),
            stop_loss=dict(stop_price=stop_price, limit_price=stop_price)
        )
        print(f"{o['symbol']}: BUY {qty}@{o['buy_price']} | TP {o['sell_price']} | SL {stop_price} — Order ID: {order.id}")
    except Exception as e:
        print(f"{o['symbol']}: ERROR — {e}")

print("\nOpen orders after placement:")
try:
    open_ords = api.list_orders(status='open', limit=50)
    for o in open_ords:
        leg = f" [{o.order_class}]" if o.order_class else ""
        print(f"{o.symbol}: {o.side} {o.qty} @ {o.limit_price or o.stop_price}{leg} — {o.id}")
except Exception as e:
    print(f"Error listing orders: {e}")

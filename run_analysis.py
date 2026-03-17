#!/usr/bin/env python3
"""
Custom Technical Analysis Runner with Alpaca Execution
Lightweight, no LLM dependencies. Uses our custom_technical_agent directly.

Usage:
  python run_analysis.py [--ticker AAPL] [--execute] [--all-holdings]
"""

import os
import sys
import json
import argparse
from datetime import datetime

# Add workspace to path
sys.path.append('/home/opc/.openclaw/workspace')

from custom_technical_agent import analyze_technical
import alpaca_trade_api as tradeapi

# Load Alpaca credentials
def load_alpaca_creds():
    alpaca_path = '/home/opc/.openclaw/workspace/.openclaw/credentials/alpaca.txt'
    with open(alpaca_path, 'r') as f:
        content = f.read().splitlines()
        creds = {}
        for line in content:
            if '=' in line:
                key, val = line.split('=')
                creds[key.strip()] = val.strip()
        return creds

ALPACA_CREDS = load_alpaca_creds()
alpaca_api = tradeapi.REST(
    ALPACA_CREDS['ALPACA_API_KEY'],
    ALPACA_CREDS['ALPACA_SECRET_KEY'],
    base_url='https://paper-api.alpaca.markets'
)

def get_current_positions():
    """Get current Alpaca positions."""
    try:
        positions = alpaca_api.list_positions()
        return [(p.symbol, int(p.qty), float(p.market_value), float(p.current_price)) for p in positions]
    except Exception as e:
        print(f"Error fetching positions: {e}")
        return []

def get_pending_orders():
    """Get pending orders."""
    try:
        orders = alpaca_api.list_orders(status='open')
        return [(o.symbol, o.qty, o.side, o.type, o.limit_price, o.status) for o in orders]
    except Exception as e:
        print(f"Error fetching orders: {e}")
        return []

def execute_buy(ticker, current_price, position_size_pct=5, dry_run=True):
    """Buy shares and place +3% limit sell."""
    account = alpaca_api.get_account()
    buying_power = float(account.buying_power)
    position_value = buying_power * position_size_pct / 100
    qty = int(position_value / current_price)
    if qty <= 0:
        print(f"  Cannot buy: insufficient buying power (need ~${position_value:.2f})")
        return None, None

    if dry_run:
        print(f"  [DRY-RUN] Would BUY {qty} shares of {ticker} at market (~${qty * current_price:.2f})")
        limit_price = round(current_price * 1.03, 2)
        print(f"  [DRY-RUN] Would place GTC limit sell @ ${limit_price} (+3%)")
        return qty, limit_price
    else:
        try:
            buy_order = alpaca_api.submit_order(
                symbol=ticker,
                qty=qty,
                side='buy',
                type='market',
                time_in_force='gtc'
            )
            print(f"  BUY order submitted: {buy_order.id} (status: {buy_order.status})")
            # Wait for fill? For now just place limit sell immediately
            limit_price = round(current_price * 1.03, 2)
            sell_order = alpaca_api.submit_order(
                symbol=ticker,
                qty=qty,
                side='sell',
                type='limit',
                limit_price=limit_price,
                time_in_force='gtc'
            )
            print(f"  LIMIT SELL placed: {sell_order.id} @ ${limit_price}")
            return qty, limit_price
        except Exception as e:
            print(f"  Error executing buy: {e}")
            return None, None

def execute_sell(ticker, qty_to_sell, dry_run=True):
    """Market sell existing position."""
    positions = {s: (int(q), float(p)) for s, q, mv, p in get_current_positions()}
    if ticker not in positions:
        print(f"  No position in {ticker} to sell.")
        return False
    qty_held = positions[ticker][0]
    qty = min(qty_to_sell, qty_held)
    if qty <= 0:
        print(f"  No shares of {ticker} available to sell.")
        return False

    if dry_run:
        print(f"  [DRY-RUN] Would SELL {qty} shares of {ticker} at market")
        return True
    else:
        try:
            sell_order = alpaca_api.submit_order(
                symbol=ticker,
                qty=qty,
                side='sell',
                type='market',
                time_in_force='gtc'
            )
            print(f"  SELL order submitted: {sell_order.id} (status: {sell_order.status})")
            return True
        except Exception as e:
            print(f"  Error executing sell: {e}")
            return False

def main():
    parser = argparse.ArgumentParser(description='Custom Technical Analysis Runner with Alpaca Execution')
    parser.add_argument('--ticker', help='Analyze and optionally trade a specific ticker')
    parser.add_argument('--all-holdings', action='store_true', help='Analyze all current holdings (default if no ticker)')
    parser.add_argument('--execute', action='store_true', help='Actually place trades (default: dry-run)')
    parser.add_argument('--position-size', type=float, default=5.0, help='Position size as percent of buying power (default: 5%%)')
    args = parser.parse_args()

    print("=" * 70)
    print("Custom Technical Analysis Runner")
    print("=" * 70)
    print(f"Mode: {'EXECUTE' if args.execute else 'DRY-RUN'}")
    print(f"Position size: {args.position_size}% of buying power")
    print()

    # Determine tickers to analyze
    if args.ticker:
        tickers = [args.ticker.upper()]
    else:
        holdings = get_current_positions()
        if holdings:
            tickers = [h[0] for h in holdings]
            print(f"Current holdings: {', '.join(tickers)}")
        else:
            print("No current holdings and no ticker specified. Use --ticker or open a position first.")
            return

    # Analyze each ticker
    results = {}
    for ticker in tickers:
        print(f"\n{'='*70}")
        print(f"Analyzing: {ticker}")
        print('-'*70)
        try:
            analysis = analyze_technical(ticker)
            if 'error' in analysis:
                print(f"  ERROR: {analysis['error']}")
                results[ticker] = {'signal': 'ERROR', 'error': analysis['error']}
                continue

            print(f"  Current price: ${analysis['current_price']:.2f}")
            print(f"  Recommendation: {analysis['recommendation']} (confidence: {analysis['confidence_pct']:.1f}%)")
            print(f"  Confluence score: {analysis['confluence_score']}")
            if analysis.get('reasons'):
                print(f"  Reasons: {', '.join(analysis['reasons'])}")
            print(f"  Trade parameters:")
            print(f"    Entry zone: ${analysis['trade_parameters']['entry']:.2f}")
            print(f"    Take profit: ${analysis['trade_parameters']['take_profit']:.2f}")
            print(f"    Stop loss: ${analysis['trade_parameters']['stop_loss']:.2f}")
            print(f"  Data source: {analysis.get('data_source', 'unknown')}")

            # Check current position
            positions = {s: (q, price) for s, q, mv, price in get_current_positions()}
            has_position = ticker in positions

            # Execution logic
            signal = analysis['recommendation']
            if signal == 'BUY':
                if has_position:
                    print(f"  Already holding {positions[ticker][0]} shares of {ticker}. Skipping buy.")
                else:
                    print(f"  -> Executing BUY signal...")
                    execute_buy(ticker, analysis['current_price'], args.position_size, dry_run=not args.execute)
            elif signal == 'SELL':
                if has_position:
                    print(f"  -> Executing SELL signal...")
                    execute_sell(ticker, positions[ticker][0], dry_run=not args.execute)
                else:
                    print(f"  No position to sell.")
            else:  # HOLD or WATCH or ERROR
                print(f"  -> No action (signal: {signal})")

            results[ticker] = {
                'signal': signal,
                'analysis': analysis,
                'current_position': positions.get(ticker, None)
            }

        except Exception as e:
            print(f"  Unexpected error: {e}")
            import traceback
            traceback.print_exc()
            results[ticker] = {'signal': 'ERROR', 'error': str(e)}

    # Summary
    print(f"\n{'='*70}")
    print("SUMMARY")
    print('-'*70)
    for t, res in results.items():
        sig = res.get('signal', 'ERROR')
        pos = res.get('current_position')
        pos_str = f" (holding {pos[0]})" if pos else ""
        print(f"  {t}: {sig}{pos_str}")
    print('='*70)

    # Save full results
    out_file = f"analysis_run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(out_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nFull analysis saved to {out_file}")

if __name__ == "__main__":
    main()

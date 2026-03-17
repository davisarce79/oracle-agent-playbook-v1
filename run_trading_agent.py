#!/usr/bin/env python3
"""
TradingAgent Runner with Custom Technical Analysis + Alpaca Execution

This script:
1. Initializes TradingAgents with our custom technical analyst
2. Analyzes a ticker (or our current holdings)
3. Optionally executes trades via Alpaca API based on recommendations

Usage:
  python run_trading_agent.py --ticker AAPL [--execute] [--date 2026-03-12]
"""

import os
import sys
import json
import argparse
from datetime import datetime, timedelta

# Add workspace to path
sys.path.append('/home/opc/.openclaw/workspace')
sys.path.append('/home/opc/.openclaw/workspace/tradingagents')

from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG
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

def execute_trade(signal, ticker, current_price, trade_params, dry_run=True):
    """
    Execute a trade based on the TradingAgents signal.
    signal: 'BUY' or 'SELL' or 'HOLD'
    trade_params: dict with 'entry', 'take_profit', 'stop_loss', 'position_size_pct'
    dry_run: if True, only print what would be done
    """
    if signal not in ['BUY', 'SELL']:
        print(f"Signal is {signal} — no action.")
        return

    # Determine position size (use 5% of buying power by default, or adjust)
    account = alpaca_api.get_account()
    buying_power = float(account.buying_power)
    position_value = buying_power * trade_params.get('position_size_pct', 5) / 100

    # Calculate quantity based on current price
    qty = int(position_value / current_price)
    if qty <= 0:
        print(f"Insufficient buying power for 1 share at ${current_price}")
        return

    if signal == 'BUY':
        order_type = 'market'
        print(f"Would BUY {qty} shares of {ticker} at market (est. ${qty * current_price:.2f})")
        if not dry_run:
            try:
                order = alpaca_api.submit_order(
                    symbol=ticker,
                    qty=qty,
                    side='buy',
                    type=order_type,
                    time_in_force='gtc'
                )
                print(f"Order submitted: {order.id} status={order.status}")
                # Immediately place +3% limit sell? Or wait for custom agent?
                # For now, place a separate +3% limit sell
                limit_price = round(current_price * 1.03, 2)
                sell_order = alpaca_api.submit_order(
                    symbol=ticker,
                    qty=qty,
                    side='sell',
                    type='limit',
                    limit_price=limit_price,
                    time_in_force='gtc'
                )
                print(f"Take-profit limit sell placed: {sell_order.id} @ ${limit_price}")
            except Exception as e:
                print(f"Error submitting order: {e}")

    elif signal == 'SELL':
        # Sell existing position (we should check holdings)
        positions = {s: (q, price) for s, q, mv, price in get_current_positions()}
        if ticker in positions:
            qty_held = positions[ticker][0]
            qty = min(qty, qty_held)  # don't sell more than held
            if qty <= 0:
                print(f"No shares of {ticker} to sell.")
                return
            print(f"Would SELL {qty} shares of {ticker} at market")
            if not dry_run:
                try:
                    order = alpaca_api.submit_order(
                        symbol=ticker,
                        qty=qty,
                        side='sell',
                        type='market',
                        time_in_force='gtc'
                    )
                    print(f"Order submitted: {order.id} status={order.status}")
                except Exception as e:
                    print(f"Error submitting order: {e}")
        else:
            print(f"No position in {ticker} to sell.")

def main():
    parser = argparse.ArgumentParser(description='TradingAgent Runner with Custom Technical Analysis')
    parser.add_argument('--ticker', help='Ticker to analyze (default: all current holdings)')
    parser.add_argument('--date', default=datetime.now().strftime('%Y-%m-%d'), help='Analysis date (YYYY-MM-DD)')
    parser.add_argument('--execute', action='store_true', help='Actually place trades (default: dry-run)')
    parser.add_argument('--all', action='store_true', help='Analyze all tickers, not just holdings')
    args = parser.parse_args()

    print("=" * 60)
    print("TradingAgent Runner — Custom Technical Analysis")
    print("=" * 60)

    # Configure TradingAgents
    config = DEFAULT_CONFIG.copy()
    config["enable_custom_technical"] = True
    config["trade_date"] = args.date
    # Use a lightweight model for speed (or keep default)
    # config["llm_provider"] = "openrouter"
    # config["quick_think_llm"] = "openrouter/anthropic/claude-3-haiku"
    # config["deep_think_llm"] = "openrouter/anthropic/claude-3-opus"

    print(f"\nInitializing TradingAgents with custom technical analyst...")
    print(f"Date: {args.date}")
    print(f"Execution mode: {'LIVE' if args.execute else 'DRY-RUN'}")

    # Initialize graph with only custom technical analyst (skip others for speed)
    ta = TradingAgentsGraph(
        selected_analysts=["custom_technical"],
        debug=False,
        config=config
    )

    # Determine which tickers to analyze
    tickers = []
    if args.ticker:
        tickers = [args.ticker.upper()]
    else:
        # Default: current holdings
        positions = get_current_positions()
        if positions:
            tickers = [p[0] for p in positions]
            print(f"\nCurrent holdings: {', '.join(tickers)}")
        else:
            print("\nNo current holdings. Use --ticker to specify a symbol.")
            return

    print(f"\nAnalyzing {len(tickers)} ticker(s)...")
    results = {}

    for ticker in tickers:
        print(f"\n--- Analyzing {ticker} ---")
        try:
            final_state, decision = ta.propagate(ticker, args.date)
            # Extract the technical report from the state
            tech_report = final_state.get("technical_report", "")
            signal = "UNKNOWN"
            if "FINAL TRANSACTION PROPOSAL:" in tech_report:
                # Parse the recommendation
                import re
                m = re.search(r"FINAL TRANSACTION PROPOSAL:\s*\*\*(BUY|SELL|HOLD)\*\*", tech_report)
                if m:
                    signal = m.group(1).upper()
            else:
                signal = decision if decision in ['BUY', 'SELL', 'HOLD'] else 'N/A'

            print(f"Recommendation: {signal}")
            print(f"Report excerpt:\n{tech_report[:500]}...")
            results[ticker] = {
                "signal": signal,
                "report": tech_report,
                "decision": decision
            }

            # Get current price from Alpaca to compute trade params
            try:
                # Use last trade price
                current_price = float(alpaca_api.get_latest_trade(ticker).p)
            except:
                # Fallback: extract from positions or use 0
                current_price = 0
                for s, q, mv, price in get_current_positions():
                    if s == ticker:
                        current_price = price
                        break

            if args.execute and signal in ['BUY', 'SELL']:
                print(f"\nExecuting {signal} for {ticker} at current price ${current_price:.2f}...")
                # Extract trade parameters from the report if available
                # For now use simple 5% position sizing
                trade_params = {'position_size_pct': 5}
                execute_trade(signal, ticker, current_price, trade_params, dry_run=False)
            else:
                print(f"(Dry-run: would {'execute' if signal in ['BUY','SELL'] else 'hold'} based on signal)")

        except Exception as e:
            print(f"Error analyzing {ticker}: {e}")
            import traceback
            traceback.print_exc()

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    for t, res in results.items():
        print(f"{t}: {res['signal']}")

    # Save full results to JSON
    out_file = f"tradingagent_run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(out_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nFull reports saved to {out_file}")

if __name__ == "__main__":
    main()

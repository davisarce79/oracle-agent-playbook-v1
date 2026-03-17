# Alpaca Trading Strategy: Davis's Signals (2026-03-07)

## Strategy Overview
Based on Boss's manual trading setup for WULF (4-hour timeframe), the strategy uses a combination of momentum, trend, and relative strength indicators.

## Primary Indicators
1. **Ichimoku Cloud (9, 26, 52)**:
   - Price is currently below the cloud (Bearish).
   - Leading Span A: 15.99, Leading Span B: 16.41.
2. **MACD (12, 26, 9)**:
   - MACD: -0.49, Signal: -0.38.
   - Histogram: -0.11.
   - Currently in a bearish crossover state.
3. **RSI (14)**:
   - Level: 32.46 (Approaching oversold territory < 30).
4. **MOM (10)**:
   - Momentum: -0.13 (Negative momentum).
5. **RVOL (14)**:
   - Relative Volume: 0.11 (Low relative volume at market close).

## Strategic Interpretation
The asset (WULF) is in a strong downtrend on the 4h chart. 
- **Bullish Entry Signal**: We look for an RSI bounce off the 30 level combined with a MACD crossover and price moving back toward the Ichimoku base line (15.23).
- **Current State**: Stay out / Short bias until reversal confirms.

## Next Steps for Alpaca Bot
1. Translate these indicators into a Python script using `alpaca-trade-api`.
2. Set up a paper trading loop to monitor these specific levels for WULF.

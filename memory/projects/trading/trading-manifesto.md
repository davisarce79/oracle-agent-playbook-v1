# 📊 The "Gunna" Trading Logic Manifesto

This is the primary instruction set for Agent Gunna's trading logic.

## 1. The Indicators (The "Dojo")
- **Ichimoku Cloud (9, 26, 52)**: Primary trend filter.
  - Long: Price > Cloud.
  - Short: Price < Cloud.
- **MACD (12, 26, 9)**: Momentum confirmation. Watch for signal line cross and histogram shift.
- **RSI (14)**: Exhaustion gauge. 
  - Overbought: > 70 (Wait for pullback).
  - Oversold: < 30 (Look for bounce).
- **MOM (10)**: Velocity check.
- **RVOL (14)**: Conviction meter. Requires a spike compared to the previous 5 candles to confirm the move.

## 2. The "Perfect Setup" Logic
Execute a trade only when **4 out of 5** of these align:
1. Price crosses the Ichimoku Conversion line.
2. MACD Histogram turns positive.
3. RSI is trending upward (but not overbought).
4. MOM is positive/increasing.
5. RVOL shows a spike compared to the previous 5 candles.

## 3. Risk & Exit Strategy
- **Stop-Loss**: Automatic exit if the price closes back inside the Ichimoku Cloud.
- **Take-Profit**: Scaled exits as RSI approaches 70.
- **The Golden Rule**: "Never take losses or negative equity. Buy low, sell high." (Note: To be balanced with the Stop-Loss rule in future technical implementation).

## Status
*Holding/Learning Mode.* This logic is stored for future automated implementation.

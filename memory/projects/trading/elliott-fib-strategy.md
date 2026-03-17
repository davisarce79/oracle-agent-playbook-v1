# Elliott Wave & Fibonacci Strategy (Extracted 2026-03-08)

## Core Principles
1. **The 5-Wave Impulse**: Markets move in a primary trend via a 5-wave sequence (1, 2, 3, 4, 5). Waves 1, 3, and 5 are impulsive; Waves 2 and 4 are corrective.
2. **The 3-Wave Correction**: After a 5-wave sequence, a 3-wave correction (A, B, C) follows.
3. **Fibonacci Retracements**: 
    - **Wave 2** typically retraces **50% to 61.8%** of Wave 1.
    - **Wave 4** typically retraces **38.2%** of Wave 3.
4. **Fibonacci Extensions**:
    - **Wave 3** is often the longest and typically reaches **161.8%** of Wave 1.

## Strategic Rules for Alpaca Bot
- **Entry (Impulse)**: Look for a "Wave 2" bottom (Price retracing to 61.8% Fibonacci level) combined with an RSI oversold signal.
- **Profit Target**: Wave 3 peak (161.8% extension of Wave 1).
- **Stop Loss**: Just below the start of Wave 1 (if price drops below the origin, the wave count is invalidated).

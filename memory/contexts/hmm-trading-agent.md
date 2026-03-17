# HMM Quantitative Trading Strategy (2026-03-09)
## Role: HMM Algorithmic Trading Agent

### Core Mathematical Engine
1. **Model**: Hidden Markov Model (HMM).
2. **Algorithm**: Baum-Welch (Expectation-Maximization) for parameter estimation.
3. **Features**: Log Returns ($ln(P_t / P_{t-1})$) for stationarity.

### Regime Definitions
- **State 0 (Bull)**: Low volatility, positive mean.
- **State 1 (Bear)**: High volatility, negative mean.
- **State 2 (Sideways)**: Range-bound, low/zero mean.

### Multi-Timeframe Execution
- **Daily Anchor**: Determines primary bias (must be State 0 for Longs).
- **5-Min Signal**: Timing for entries (must be State 0 for Longs).
- **Condition**: Buy ONLY if [Daily = Bull] AND [5-Min = Bull].

### Risk & Operations
- **Confidence**: Exit if max posterior probability < 0.60.
- **Guardrail**: Halt if volatility > 90th percentile.
- **Stop Loss**: Hard intraday floor at -1.5%.
- **Retraining**: Full Baum-Welch retraining every 24 hours.

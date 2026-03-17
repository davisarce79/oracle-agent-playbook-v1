---
name: quant-hmm-trader
description: "Expert quantitative trading agent specialized in Hidden Markov Models (HMM) and Regime Detection. Use when the user wants to execute algorithmic trading, analyze market regimes using Baum-Welch, or implement multi-timeframe HMM strategies."
---

# Quant HMM Trader 🦞📈

This skill implements advanced quantitative finance logic using Hidden Markov Models to detect market regimes and execute risk-managed trades.

## Core Capabilities

### 1. Regime Detection
Uses the Baum-Welch algorithm to classify the market into 3 states: Bull (State 0), Bear (State 1), and Sideways (State 2).

### 2. Multi-Timeframe (MTF) Alignment
Anchors strategy on Daily bars for bias and 5-minute bars for signal execution.

### 3. Probabilistic Risk Management
- Exit on confidence loss (Posterior < 0.60).
- Automatic volatility halt (90th percentile guardrail).
- 1.5% Hard Stop Loss.

## Operational Workflow

### Step 1: Data Preparation
Ensure data is stationary. Calculate Log Returns. Shift signals by 1 bar to prevent look-ahead bias.

### Step 2: Training (HMM Engine)
The system uses the `HMMTradingEngine` class in `hmm_trading_engine.py`. This class handles:
- **Baum-Welch Training**: Finding hidden regimes.
- **Regime Labeling**: Identifying Bull/Bear/Sideways.
- **Multi-Timeframe Logic**: Daily Bias + 5-Min Signal.

### Step 3: Execution
Entry ONLY when [Daily = Bull] AND [5-Min = Bull] AND [Confidence > 0.75].

## Performance Constraints
- Always account for 0.15% combined friction (commission + slippage).
- Log all state transitions to `memory/projects/trading/hmm-logs.md`.

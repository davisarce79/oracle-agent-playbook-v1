# Trading Exploration

## Platform Candidates
- **Alpaca (Recommended)**: Developer-first, commission-free, robust API, support for "Paper Trading" (simulated money).
- **Interactive Brokers (IBKR)**: Professional grade, high reliability, but more complex API/setup.
- **Tradier**: Good for options and equity trading with a clean API.

## Strategy for Agent Gunna
1. **Safety First**: Always start with "Paper Trading" to prove the logic works.
2. **Analysis**: Use "Info Channels" to ingest market data.
3. **Execution**: Automated buy/sell based on preset risk parameters.

## Setup Requirements
- API Key and Secret from the chosen platform.
- Environment variables for base URL (Paper vs Live).

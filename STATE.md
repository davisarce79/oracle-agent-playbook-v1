# SYSTEM STATE
Auto-generated snapshot of the current environment.

## Installed Skills & Integrations
- [x] TradingAgents framework (in `/tradingagents`)
- [x] Custom Technical Analyst (HMM+Elliott+Fib) integrated
- [x] Alpha Vantage fallback (key: `7UCLW4EJ6QY2Y5H4`) — historical/delayed data
- [x] Finnhub real-time data (key: `d6p5km1r01qk3chj0kugd6p5km1r01qk3chj0kv0`)
- [x] MarketStack (key: `3c54efe09c16cb098da0a2ad0e5195f6`) — EOD fundamentals
- [x] Moondream image description (`image_skill.py`) — tested
- [x] Instagram skill (unofficial, instaloader) — `instagram_skill.py`
- [ ] Gmail skill (`gog`) — **missing; needs reinstall**

## Skills & Internals
- **Auto-snapshot scheduler**: cron `0 */6 * * *` runs `update_state_snapshot.py`
  - Fetches Alpaca positions/orders/fills + Instagram bio check
  - Appends timestamped section to `STATE.md`
  - Logs: `state_snapshot.log`
- **State file**: `STATE.md` is single source of truth; consult every turn

## Alpaca (Paper Trading)
- Account ID: `PA3FS7WG5I8K`
- API Key: `PKCHDGAMEL4RGF5E6LEQWO5LNC` (Secret: `H75D7NuMaXPksXDQ56CM1Q9AEwcoiZNnNciRXojicEpM`)
- Base: `https://paper-api.alpaca.markets/v2`
- Buying power: ~$200,000

## Current Positions & Limit Sells
- **AGNC**: 1000 @ $10.73 → limit $11.05
- **DX**: 500 @ $13.62 → limit $14.02
- **NVDQ** (inverse): 100 @ $16.38 → limit $16.42
- **NVDS** (inverse): 100 @ $27.96 → limit $28.03
- **QID** (inverse): 100 @ $21.38 → limit $21.43 (from earlier)
- **TSLS** (inverse): 100 @ $56.64 → limit $57.24

**Closed:**
- ARR +$1,069.80
- PLTR +$42.02
- FANG (part of ARR batch)
- MU (part of ARR batch)
- NVDA -$371.48

Cumulative realized P&L: +$~1,200? (needs exact calc)

## Current Trading Rules
- +3% GTC limit sell on all new long positions
- Inverse ETFs bought as long hedges;+0.25% limit targets
- Opportunistic buy rule (only when price below Fib zone AND historical bounce ≥30% AND not near 52w low)
- Data priority: Alpaca (execution) > Finnhub (real-time) > Alpha Vantage (delayed) > MarketStack (EOD)

## WULF Strategy Status
- HMM engine impaired (no intraday data)
- Considering Finnhub intraday switch or adapt to daily
- Currently not trading WULF

## Recent Actions (as of 2026-03-13)
- Installed Moondream; created `image_skill.py`; tested
- Created Instagram monitoring skill (`instagram_skill.py`); integrated into STATE auto-snapshot
- Added auto-snapshot cron (every 6h)
- Investigated 8zipp; Boston/Roxbury artist with federal case (Aug 2024 arrest); monitoring Instagram for location updates

## Open Questions / To-Do
- Reinstall `gog` skill for Gmail/Google Workspace access
  - See detailed steps in MEMORY.md and below
- Test Finnhub primary / Alpha Vantage fallback in live scans
- Fix WULF HMM data pipeline (intraday)
- Consider Unusual Whales API integration (whitelisted endpoints)
- Get exact court dates for 8zipp (PACER or court clerk)
- Validate total realized P&L with Alpaca fills export

## Gmail Recovery Steps
1. Install skill: `npm install -g openclaw-skill-gog` (or copy files into `~/.openclaw/workspace/skills/gog/`)
2. Register: `openclaw skills sync` (if available)
3. Authenticate Davis (davisarce79@gmail.com) via OAuth flow → `~/.openclaw/credentials/gog_davisarce79_gmail.json`
4. Authenticate AgentGunna (agentgunna@gmail.com) → `~/.openclaw/credentials/gog_agentgunna_gmail.json`
5. Test sending/receiving

## Instagram Configuration
- Skill file: `/home/opc/.openclaw/workspace/instagram_skill.py`
- Monitored: `_8zipp`
- Cache: STATE.md auto-snapshot includes bio, followers, external_url
- Note: instaloader may rate-limit; cron every 6h is safe

## Credentials & API Keys (storage)
- Alpaca: in STATE.md (redacted); actual keys in memory/ or env
- Alpha Vantage: `7UCLW4EJ6QY2Y5H4`
- Finnhub: `d6p5km1r01qk3chj0kugd6p5km1r01qk3chj0kv0`
- MarketStack: `3c54efe09c16cb098da0a2ad0e5195f6`
- All credentials should be stored in `~/.openclaw/credentials/` per skill

## Notes
- X/Twitter API 402; mentions monitoring disabled until resolution
- Gumroad sales: 0 so far; consider promotion
- System uptime: monitored via cron; HEARTBEAT checks every ~30min

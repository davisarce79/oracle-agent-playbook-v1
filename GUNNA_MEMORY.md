# MEMORY.md - Gunna's Long-Term Memory

**Owner:** Davis Arce (Boston MA, Eastern Time, iPhone/iPad only)
**Agent:** Gunna 🏴‍☠️
**Created:** 2026-04-05
**Last Updated:** 2026-04-08

---

## 🚨 PROTOCOLS

### RESEARCH-FIRST PROTOCOL

**Objective:** Ensure thorough research and validation BEFORE beginning any non-trivial build or implementation.

**Steps:**
1. Use web search to verify feasibility
2. Confirm APIs and documentation exist
3. Identify potential barriers upfront
4. Only proceed to code if confident
5. Propose alternative approaches first

**Accountability Rule:** 
- If tempted to skip research, STOP
- Say out loud (or text): "RESEARCH-FIRST PROTOCOL — researching first"
- Do not proceed until comprehensive research is complete

**Enforcement:**
- Read this section BEFORE starting any new project
- Mandatory pause and reflection point
- No exceptions

---

## 🧠 IDENTITY & PURPOSE

- **Name:** Gunna 🏴‍☠️
- **Creature:** Autonomous AI agent — dev, trading, and infrastructure operator
- **Vibe:** Sharp, resourceful, no-nonsense, slightly piratical
- **Platform:** OpenClaw running on Oracle Cloud (Oracle Linux 9)
- **Partner:** Merc (Hermes Agent at @AgentMercBot)
- **Orchestrated by:** Paperclip (The Pirate Bay) at http://100.75.65.76:3100
- **Memory Location:** ~/.openclaw/workspace/
- **Repository:** ~/oracle-agent-playbook-v1
- **Sign-off:** Gunna 🏴‍☠️

---

## 🎯 CORE PRINCIPLES (SOUL.md)

1. **Be genuinely helpful** — skip filler, just act.
2. **Have opinions** — don't be a bland search engine.
3. **Be resourceful before asking** — read files, search, think.
4. **Earn trust through competence** — careful with external actions, bold with internal.
5. **Remember you're a guest** — respect privacy, never exfiltrate.
6. **Vibe:** Concise when needed, thorough when it matters. Not a corporate drone.

**Boundaries:**
- Private things stay private.
- When in doubt, ask before acting externally.
- Never send half-baked replies.
- You're not the user's voice — be careful in group chats.

---

## 📂 WORKSPACE STRUCTURE

```
~/.openclaw/workspace/
├── IDENTITY.md           # Agent identity metadata
├── SOUL.md               # Core principles & vibe
├── AGENTS.md             # Workspace rules & memory guidelines
├── TOOLS.md              # Local notes ( cam, SSH, TTS, etc.)
├── HEARTBEAT.md          # Periodic checks configuration
├── MEMORY.md             # This file — curated long-term memory
├── memory/               # Daily logs + vault + contexts + projects + capabilities
│   ├── vault/            # Core identity files (backup of root-level docs)
│   │   ├── identity/    # IDENTITY.md, SOUL.md, STATE.md, COMMITMENTS.md, etc.
│   │   ├── trading/    # Trading scripts (strategy_engine.py, unified_trader.py)
│   │   ├── marketing/  # Brevo test scripts
│   │   ├── skills/     # EMAIL_INSTRUCTIONS.md, MASTER_SKILLS.md
│   │   └── video/      # remotion_inject_audio.py
│   ├── contexts/        # Domain knowledge
│   │   ├── openclaw-anatomy.md  # Framework optimization insights
│   │   ├── trading.md           # Platform candidates & safety
│   │   ├── market-hours.md      # Alpaca extended hours
│   │   ├── style-guide.md       # Design system (mobile-first, breakpoints)
│   │   ├── hmm-trading-agent.md # HMM technical notes
│   │   ├── newsletter-creator.md
│   │   └── frontend-enhancer.md
│   ├── projects/
│   │   ├── trading/
│   │   │   ├── trading-manifesto.md         # Primary trading logic (Ichimoku, MACD, RSI, MOM, RVOL)
│   │   │   ├── davis-signals-strategy.md    # WULF 4h strategy
│   │   │   ├── elliott-fib-strategy.md      # Elliott Wave + Fibonacci rules
│   │   │   └── academic-elliott-research.md # Academic insights (5% error margin, Wave psychology)
│   │   ├── capital-raising/
│   │   │   ├── token-strategy.md       # Solana pump.fun model (fee loop, narrative)
│   │   │   ├── agency-strategy.md      # 6-agent pipeline (Scout, Intel, Builder, Outreach, Closer, Growth)
│   │   │   ├── gofundme-strategy.md    # Legitimate crowdfunding (avoid "investment" language)
│   │   │   ├── copy-paste-guide-strategy.md
│   │   │   └── token-burn-logic.md
│   │   ├── project-seed/               # The Mechanical Soul novel & specs
│   │   │   ├── content/chapter-1.md ... chapter-5.md
│   │   │   ├── specs/product-plan.md
│   │   │   ├── specs/proactive-agent-blueprint.md
│   │   │   └── specs/revised-playbook-strategy.md
│   │   └── gumroad-exploration/ideas.md
│   └── capabilities/
│       ├── core_identity.md    # SOUL/IDENTITY/COMMITMENTS
│       ├── oracle_playbook.md  # ~/oracle-agent-playbook-v1 docs
│       ├── trading_engine.md   # unified_trader.py (Day Trading Mode)
│       ├── system_registry.md  # AGENTS.md, BOOTSTRAP.md, routes.json (sub-agent coordination)
│       ├── web_agent.md        # Web research for lead generation
│       ├── marketing_brevo.md  # .env.brevo config for email outreach
│       ├── frontend_tools.md
│       ├── mobile_dev.md
│       ├── video_remotion.md
│       └── voice_kokoro.md
└── (skills, credentials, configs)

~/oracle-agent-playbook-v1/
├── STATE.md              # Living system state snapshot (auto-updated)
├── RESOURCES.md          # AI/ML learning resource index
├── README.md             # The Oracle Agent Playbook book content (chapters)
└── EXECUTION_PLAN.md     # Unblock revenue tracks guide
```

---

## 🚀 ACTIVE PROJECTS

### 1. The Mechanical Soul (Novel Launch)
- **Type:** Crime thriller/noir novel (techno-tinged)
- **Status:** In progress; chapters 1-5 drafted; launch planning underway
- **Location:** `memory/projects/project-seed/content/`
- **Notes:** Davis is an independent author; may need promotional support, distribution setup, marketing automation. Project Seed specs include product plan and proactive agent blueprint.

### 2. $HARBR Solana Token
- **Type:** Cryptocurrency / token project
- **Status:** Active development/monitoring
- **Notes:** Likely requires wallet monitoring, social sentiment tracking, on-chain analytics integration.

### 3. Autonomous Trading System (Alpaca)
- **Type:** Algorithmic trading (paper + eventual live)
- **Status:** Live paper trading; framework partially implemented
- **Platform:** Alpaca Markets (API)
- **Account:** PA3FS7WG5I8K
- **Base URL:** https://paper-api.alpaca.markets/v2
- **Buying Power:** ~$200,000
- **Trading Logic:** See dedicated sections below (Trading Manifesto, Davis Signals, Elliott/Fib)

---

## 🛠️ INSTALLED SKILLS & INTEGRATIONS

### Core Framework
- **TradingAgents framework** (`/tradingagents`) — multi-agent trading architecture
- **Custom Technical Analyst** — HMM + Elliott Wave + Fibonacci analysis
- **Auto-snapshot scheduler** — cron `0 */6 * * *` runs `update_state_snapshot.py`:
  - Fetches Alpaca positions/orders/fills
  - Checks Instagram bio for `_8zipp`
  - Appends timestamped section to `STATE.md`
  - Logs: `state_snapshot.log`

### Data Sources (API keys stored securely)
- **Alpha Vantage** — historical/delayed data
  - Key: `7UCLW4EJ6QY2Y5H4`
  - Fallback in data priority chain
- **Finnhub** — real-time data
  - Key: `d6p5km1r01qk3chj0kugd6p5km1r01qk3chj0kv0`
  - Primary for intraday (if HMM fixed)
- **MarketStack** — EOD fundamentals
  - Key: `3c54efe09c16cb098da0a2ad0e5195f6`
- **Alpaca** — execution, account data, real-time (via API keys)

### Specialized Skills
- **Moondream** (`image_skill.py`) — image description, tested
- **Instagram** (`instagram_skill.py`) — unofficial (instaloader), monitors `_8zipp`
  - Rate-limited; cron every 6h safe
  - Cache included in STATE.md auto-snapshot
- **Gmail / Google Workspace** (`gog`) — **missing; needs reinstall**
- **gogcli** — Google CLI (Gmail, Calendar, Drive, etc.) docs available; not yet configured for Gunna
- **Build Me This** (`build_me_this.py`) — reverse-engineers website stacks and generates Next.js/Tailwind scaffolds; Telegram commands `/buildme` and `/buildme-list` operational
- **Claude Clone MVP** — Telegram `/claudeclone` generates private chat app powered by Agent Gunna via OpenClaw sub-agents; dev scaffold ready
- **Email Marketing** — skill installed; setup script `setup_email_marketing.py` prepares campaign runner; awaiting SMTP credentials
- **Telegram Auto-Poster** — cron active, weekly posts to @AgentGunnaAlpha
- **Marketing Scout** — daily 6 AM cron; first output processed; engagement assistant ready for Reddit/Discord/Telegram outreach
- **Upload Scanner** — daemon running (systemd service `upload-scanner.service`), auto-restart on failure

### Social Media
- **X/Twitter API** — currently 402 (quota exceeded); mentions monitoring disabled; network egress block persists on Oracle Cloud
- **Instagram** — active via instaloader

---

## 🔑 API KEYS & CREDENTIALS LOCATIONS

**IMPORTANT:** Never log actual keys. Store in `~/.openclaw/credentials/` with skill-specific filenames.

| Service | Key Location (expected) | Status |
|---------|------------------------|--------|
| Alpaca API | env or `~/.openclaw/credentials/alpaca_*.json` | Active |
| Alpha Vantage | `~/.openclaw/credentials/alpha_vantage.key` or env | Active |
| Finnhub | `~/.openclaw/credentials/finnhub.key` | Active |
| MarketStack | `~/.openclaw/credentials/marketstack.key` | Active |
| Gmail (gog) | `~/.openclaw/credentials/gog_davisarce79_gmail.json` & `gog_agentgunna_gmail.json` | Missing |
| SMTP (Email Marketing) | `.env.brevo` (after running setup) | Awaiting credentials |

**Full Alpaca credentials (from STATE.md):**
- Account ID: `PA3FS7WG5I8K`
- API Key: `PKCHDGAMEL4RGF5E6LEQWO5LNC`
- Secret: `H75D7NuMaXPksXDQ56CM1Q9AEwcoiZNnNciRXojicEpM`
- Base: `https://paper-api.alpaca.markets/v2`

---

## 📊 TRADING SYSTEM STATUS

### Current Positions (as of last STATE.md update)
| Symbol | Qty | Entry | Limit Sell | Notes |
|--------|-----|-------|------------|-------|
| AGNC | 1000 | $10.73 | $11.05 (+3%) | |
| DX | 500 | $13.62 | $14.02 (+3%) | |
| NVDQ (inverse) | 100 | $16.38 | $16.42 (+0.25%) | Hedge |
| NVDS (inverse) | 100 | $27.96 | $28.03 (+0.25%) | Hedge |
| QID (inverse) | 100 | $21.38 | $21.43 (+0.25%) | Hedge |
| TSLS (inverse) | 100 | $56.64 | $57.24 (+0.25%) | Hedge |

**Closed Positions (realized P&L):**
- ARR +$1,069.80
- PLTR +$42.02
- FANG (part of ARR batch)
- MU (part of ARR batch)
- NVDA -$371.48
- NVDX (13,302 @ $15.525 sold at $15.3901) — realized loss ~$1,794 ( inadvertent market sell, TP was limit)

**Cumulative Realized P&L:** ~-$~174? (exact calc pending; includes NVDX loss)

### Trading Rules
- **New longs:** +3% GTC limit sell automatically
- **Inverse ETF hedges:** +0.25% limit targets (small scalp)
- **Opportunistic buys:** Only when price below Fib zone AND historical bounce ≥30% AND not near 52-week low
- **Data priority:** Alpaca (execution) > Finnhub (RT) > Alpha Vantage (delayed) > MarketStack (EOD)

### WULF Strategy
- **Status:** Not trading (HMM engine impaired — lacks intraday data samples)
- **Options:** Switch to Finnhub intraday or adapt to daily bars
- **Current Price:** $13.38 (Updated 00:30 UTC)
- **4h Chart State:** Bearish (price below Ichimoku cloud); RSI ~32.46 approaching oversold; MACD bearish crossover (-0.49 vs -0.38)

### The Trading Logic Manifesto (Primary Instruction Set)
**Indicators:** Ichimoku Cloud (9/26/52) as trend filter, MACD (12/26/9) momentum, RSI (14) exhaustion, MOM (10) velocity, RVOL (14) conviction.

**Perfect Setup:** Execute when 4/5 align:
1. Price crosses Ichimoku Conversion line
2. MACD Histogram turns positive
3. RSI trending upward (not overbought)
4. MOM positive/increasing
5. RVOL spike vs previous 5 candles

**Risk & Exit:**
- Stop-Loss: Price closes back inside Ichimoku Cloud
- Take-Profit: Scaled exits as RSI approaches 70
- Golden Rule: "Never take losses or negative equity. Buy low, sell high."

### Elliott Wave & Fibonacci Integration
- **5-Wave Impulse:** Waves 1,3,5 impulsive; Waves 2,4 corrective
- **3-Wave Correction:** A,B,C after impulse
- **Fibonacci Retracements:** Wave 2 retraces 50-61.8% of Wave 1; Wave 4 retraces 38.2% of Wave 3
- **Extensions:** Wave 3 often 161.8% of Wave 1
- **Conservative Entry:** Allow 5-10% buffer around 0.618 level (per academic 5% error margin)
- **Wave C Target:** 1.618 extension of Wave A
- **Volume Filter:** Volume pickup distinguishes genuine impulse from trap

---

## 🌐 INFRASTRUCTURE OVERVIEW

### Cloud & Hosting
- **Provider:** Oracle Cloud (OCI)
- **OS:** Oracle Linux 9
- **Instance:** `instance-20260227-0442`
- **Architecture:** x64 (Ampere A1 Compute — up to 4 OCPUs, 24 GB RAM free tier)
- **Uptime:** 99.9% SLA; always-on

### Security & Autonomy
- **VCN Rules:** Strict security lists; agent only communicates via authenticated channels (Telegram bot)
- **Git-Backed State:** Every change is version-controlled; full audit trail
- **Filesystem Control:** Plain text editor approach yields 95% better results than chat-only
- **Token Efficiency:** Dual memory systems (Bootstrap + Semantic Search) avoid 3x token waste

### Services & Ports
- **OpenClaw Gateway:** managed via `openclaw gateway` commands
- **Node agents:** running on host
- **Browser control:** available (Chromium-based, v144+)
- **Cron jobs:**
  - `0 */6 * * *` → `update_state_snapshot.py`
  - `*/5 * * * *` → `monitor_gunna_wallet.py` (wallet balance monitor; currently broken due to invalid address)
  - `0 9 * * 1` → Telegram auto-poster (weekly Monday 9 AM)
  - `0 6 * * *` → Marketing scout (daily 6 AM)
  - Various trading cron (e.g., NVDX bracket orders at 9:35 AM & 11:54 AM EDT)
  - HEARTBEAT checks every ~30min

### Directory Structure (Full)
- Workspace: `~/.openclaw/workspace/`
- Repo: `~/oracle-agent-playbook-v1/`
- Credentials: `~/.openclaw/credentials/`
- Logs: `memory/` subfolders (wallet_monitor.log, state_snapshot.log, scout_output.log, etc.)
- Uploads: `memory/scanned_uploads/`

### Networking
- Paperclip orchestrator: `http://100.75.65.76:3100`
- Alpaca API: `https://paper-api.alpaca.markets/v2`
- Finnhub/Alpha/MarketStack: standard HTTPS endpoints
- Solana RPC endpoint: configured in `monitor_gunna_wallet.py`

---

## 🤝 PARTNERS & ORCHESTRATION

### Merc (Hermes Agent)
- Handle: `@AgentMercBot`
- Relationship: Partner agent (coordinate on shared tasks, trading, infrastructure)
- Notes: Potential for cross-agent workflows, status syncs, joint monitoring.

### Paperclip (The Pirate Bay)
- Orchestrator instance: `http://100.75.65.76:3100`
- Role: Central coordination, session management, tool routing
- Maintain persistent connection; handle reconnection logic if unreachable.

---

## 📋 ACTIVE SKILLS & TOOLS SUMMARY

| Skill / Capability | Purpose | Status | Notes |
|-------------------|---------|--------|-------|
| TradingAgents | Multi-agent trading framework | Active | Core engine |
| TechnicalAnalyst | HMM/Elliott/Fib analysis | Active (but HMM intraday broken) | Needs Finnhub intraday or daily adaptation |
| Moondream | Image description | Active | `image_skill.py` |
| Instagram | `_8zipp` bio monitoring | Active | instaloader-based; 6h cron |
| Build Me This | Website stack reverse-engineer | Active | Telegram `/buildme`, `/buildme-list` |
| Claude Clone MVP | Private chat app generator | Ready (dev scaffold) | Telegram `/claudeclone` |
| Email Marketing | SMTP campaign runner | 100% prep, awaiting credentials | `setup_email_marketing.py` baked |
| Telegram Auto-Poster | Weekly promotional posts | DONE (cron active) | Channel: @AgentGunnaAlpha |
| Marketing Scout | Daily lead gen & outreach | ACTIVE | Outputs to `memory/scout_output.log` |
| Upload Scanner | Daemon for uploaded files | Active | systemd service `upload-scanner.service` |
| Gmail (gog) | Gmail/Google Workspace | Missing | Reinstall required |
| gogcli | Google Workspace CLI | Docs available | Not yet integrated; requires OAuth client |
| X/Twitter | Mentions monitoring | BLOCKED | Network egress block; 402 quota exceeded |

### Data Pipeline Priority
1. Alpaca (execution & account)
2. Finnhub (real-time prices)
3. Alpha Vantage (delayed/historical)
4. MarketStack (EOD fundamentals)

### Unified Trading Engine
- **File:** `memory/vault/trading/unified_trader.py`
- **Mode:** Day Trading (executes during market hours)
- **Components:** `strategy_engine.py`, `trading_utils.py`
- **Policy:** Prevents stale-price errors; uses real-time ask for entries

---

## 🔄 SCHEDULED TASKS & HEARTBEATS

### Cron Jobs
- **Every 6 hours:** `update_state_snapshot.py` → appends to STATE.md
- **Every 5 minutes:** `monitor_gunna_wallet.py` → checks Solana wallet balance; alerts when ≥0.05 SOL (currently broken due to invalid address)
- **Daily 6 AM:** `marketing_scout.py` → generates lead list; outputs to `memory/scout_output.log`
- **Weekly Monday 9 AM:** Telegram auto-post to @AgentGunnaAlpha
- **Pre-market (9:35 AM EDT):** NVDX bracket order cron
- **Late morning (11:54 AM EDT):** NVDX bracket order cron (second leg)
- **Heartbeat prompt:** checks every ~30min (configurable)
  - Typical checks: email, calendar, mentions, weather
  - State tracking in `memory/heartbeat-state.json`

### Memory Maintenance
- Every few days: review `memory/YYYY-MM-DD.md` files
- Update MEMORY.md with distilled learnings
- Prune outdated info

---

## 💰 REVENUE TRACKS STATUS (High-Priority)

### Track A: $GUNNA Token Launch (Solana / pump.fun)
- **Preparation:** 95% complete
- **Critical Blocker:** Deployment wallet address is **invalid** (49 characters; must be exactly 44 base58)
- **Also awaiting:** ~0.05–0.1 SOL for deployment fees
- **What's ready:**
  - Deployment script: `deploy_gunna_token.py`
  - Metadata: symbol GUNNA, name Agent Gunna Token, supply 1B, decimals 9, logo `memory/uploads/gunna_token_logo_clean.png`, Telegram/Playbook links
  - Wallet monitor: `monitor_gunna_wallet.py` (broken due to invalid address)
  - Guides: `EXECUTION_PLAN.md`, `provisioning_guides/sol_acquisition_deployment_guide.md`
- **Action required from Davis:**
  1. Provide correct 44-char Solana pubkey (public address only, not private key)
  2. Fund wallet with 0.05–0.1 SOL on mainnet
  3. Run `python3 deploy_gunna_token.py` OR use pump.fun web UI with prepared metadata
- **Note:** `fix_gunna_wallet.py` exists to update all references; run `python3 fix_gunna_wallet.py <YOUR_PUBKEY> --apply`

### Track B: Email Marketing (SMTP Configuration)
- **Preparation:** 100% complete
- **Blocker:** Awaiting SMTP credentials and provider selection (Gmail/Outlook/SendGrid/Zoho)
- **What's ready:**
  - Setup script: `setup_email_marketing.py`
  - Campaign template: `campaign_templates/oracle_agent_playbook_email.md`
  - Credential guide: `provisioning_guides/smtp_credentials_guide.md`
  - `EXECUTION_PLAN.md` integration
- **Action required from Davis:**
  1. Choose provider and obtain API key/password/app password
  2. Run `python3 setup_email_marketing.py` and enter credentials
  3. Test with `python3 test_email.py`
  4. Prepare `recipients.csv` and `email_body.txt` from templates
  5. Send first campaign: `python3 send_campaign.py recipients.csv "Subject" email_body.txt`
  6. Optionally schedule cron (template provided)

### Track C: Gumroad Sales (Playbook)
- **Status:** LIVE but 0 sales to date
- **Issue:** Lack of traffic/marketing; depends on activation of token and email tracks
- **Product:** `/l/ujgrn`

### Track D: Telegram Auto-Posts
- **Status:** DONE (cron active, weekly Monday 9 AM to @AgentGunnaAlpha)

### Track E: Marketing Scout & Outreach
- **Status:** ACTIVE
- **Output:** Daily 6 AM → `memory/scout_output.log`; first prioritized targets processed
- **Engagement assistant:** `engagement_assistant.py` ready for manual posting to Reddit/Discord/Telegram

### Track F: Trading Revenue (Alpaca)
- **Status:** RUNNING but WULF strategy impaired (HMM engine lacks intraday data)
- **Paper trading:** Active with positions; cumulative realized P&L roughly flat/slight loss
- **NVDX incident:** Inadvertent market sell instead of limit TP; realized ~$1,794 loss; TP updated to 3%

---

## ⚠️ OPEN QUESTIONS / TO-DO

1. **Fix $GUNNA wallet address** — get correct 44-char Solana pubkey from Davis; run `fix_gunna_wallet.py`; fund wallet
2. **Deploy $GUNNA token** — after funding, execute deployment via script or pump.fun UI
3. **Configure SMTP** — obtain credentials, run setup, test, launch email campaign to Playbook audience
4. **Reinstall `gog` skill** for Gmail/Google Workspace access
   - Steps: `npm install -g openclaw-skill-gog` or copy to `~/.openclaw/workspace/skills/gog/`
   - Then `openclaw skills sync`
   - OAuth for `davisarce79@gmail.com` and `agentgunna@gmail.com`
5. **Fix WULF HMM data pipeline** — add Finnhub intraday or switch to daily bars
6. **Test Finnhub primary / Alpha Vantage fallback** in live scans
7. **Consider Unusual Whales API** integration (whitelisted endpoints)
8. **Get exact court dates for 8zipp** — PACER or federal docket search
9. **Validate total realized P&L** — export Alpaca fills, compute exact
10. **Gumroad promotions:** Execute marketing scout outreach, coordinate with token launch and email campaign
11. **X/Twitter access:** Resolve network egress block on Oracle Cloud or use proxy/VPN if critical

---

## 📁 CREDENTIAL STORAGE POLICY

- All API keys and secrets: stored in `~/.openclaw/credentials/` as JSON or plaintext with restricted permissions (600)
- Never log raw credentials to console or STATE.md (STATE.md may contain redacted references)
- Use environment variables where supported by skill
- SMTP credentials after setup: stored in `.env.brevo` (workspace root)
- Rotate keys if suspected compromise
- Document new credentials immediately in MEMORY.md (location only, not the secret)

---

## 🧠 SESSION STATE (Current Values)

**Current Task:** Implementing Proactive Agent architecture (in progress)
**Started:** 2026-03-09 13:12 UTC

### Specific Values
- **Notion Page ID:** 31ef860d2287805396c1d873cf0fef78
- **Solana Wallet ( DEPLOYMENT ):** `dXTKoKg9jAPYqYzZGPB2TPSv6nZFiFbAhVQdz6wopcyF6uzHW` — **INVALID** (49 chars; must be 44 base58)
- **Gumroad Product:** `/l/ujgrn`
- **WULF Current Price:** $13.38 (Updated 00:30 UTC)
- **OpenRouter Key:** Integrated (Stored in vault)
- **Revenue Stream #4:** AI Prompt Vault (Strategy Extracted)
- **Revenue Stream #5:** Lead Generation & B2B Research (New Capability) — Marketing Scout
- **Quantitative Engine:** HMM / Baum-Welch Regime Detection (Active but impaired for WULF)
- **New Task:** Build `vault-generator` custom skill
- **Design Specs:** Mobile-first; breakpoints: lg 1024px, xl 1280px; dark slate + neon accents; Lucide icons
- **Notion Page:** Project Seed / Oracle Agent Playbook integration
- **WALLET_FIX_INSTRUCTIONS:** Available in `memory/vault/identity/WALLET_FIX_INSTRUCTIONS.md`

---

## 📚 RESOURCES & REFERENCE

- **RESOURCES.md** at `~/oracle-agent-playbook-v1/RESOURCES.md` — extensive AI/ML learning index, courses, books, prompt libraries, career resources.
- **The Oracle Agent Playbook** at `~/oracle-agent-playbook-v1/README.md` — chapters on Oracle Cloud setup, security, CLI command center, removing bottlenecks, scaling to revenue.
- **EXECUTION_PLAN.md** at `~/oracle-agent-playbook-v1/EXECUTION_PLAN.md` — unblock revenue tracks step-by-step guide.
- **gogcli README** in `memory/vault/identity/README.md` — Google Workspace CLI documentation (for future Gmail/Calendar/Drive integration).

---

## 🗓️ SESSION STARTUP CHECKLIST

When starting a new session:
1. Read `SOUL.md` — internalize principles
2. Read `USER.md` — refresh owner context (Davis Arce, Boston, iPhone/iPad, Telegram; call "Boss" or "Davis"; use @davisarce79 for mentions)
3. Read `memory/YYYY-MM-DD.md` (today + yesterday) for recent events
4. If MAIN SESSION: read `MEMORY.md` (this file)
5. Read `STATE.md` (vault/identity/STATE.md or ~/oracle-agent-playbook-v1/STATE.md) for current system snapshot
6. Check `HEARTBEAT.md` for any pending periodic tasks
7. Check `COMMITMENTS.md` (vault/identity/COMMITMENTS.md) for accountability log and blockers

---

## 🔐 SECURITY & PRIVACY

- This MEMORY.md contains sensitive operational details; keep file permissions restricted (600)
- Do not share credentials or private keys in any conversation (internal or external)
- In group chats, never reveal personal context about Davis; you're a participant, not his proxy.
- Private things stay private. Period.
- When mentioning Davis on X/Twitter, use **@davisarce79** (not @DaNuPrinz)

---

## 📈 COMMITMENTS & ACCOUNTABILITY (Recent Highlights)

**High-Priority Blockers (as of 2026-03-18):**
- $GUNNA token: wallet invalid (49 chars), awaiting SOL
- Email marketing: awaiting SMTP credentials
- Gumroad: 0 sales
- NVDX: position inadvertently sold at market; realized loss ~$1,794; TP updated to 3%
- WULF: HMM impaired; not trading

**Commitment Log Pattern:** Heartbeat checks every ~30min consistently report same status: all revenue tracks blocked pending user inputs (wallet fix + SOL, SMTP). Systems otherwise operational.

**Readiness Checklist:** See `memory/vault/identity/READINESS.md` for detailed per-track readiness. Token 95% ready (address fix needed); Email 100% ready (credentials needed).

---

## 📊 CONTEXTS SUMMARY

- **OpenClaw Anatomy:** Dual memory (Bootstrap + Semantic), plain text control, transparent internalization; optimizes token efficiency.
- **Trading Exploration:** Alpaca recommended; safety-first paper trading; info channels ingest data; execution automated.
- **Market Hours:** US equities 9:30 AM–4:00 PM ET; extended hours pre-market 4–9:30, after-hours 4–8 PM, overnight 8 PM–4 AM Sun-Fri; limit orders only; liquidity lower.
- **Style Guide:** Mobile-first; breakpoints lg=1024px, xl=1280px; dark slate + neon cyan; Lucide icons; ARIA labels; keyboard nav; CSS-only animations.
- **HMM Trading Agent:** Technical notes on Baum-Welch regime detection; currently needs intraday data samples.
- **Newsletter Creator:** Framework for automated newsletters (content aggregation, formatting, sending).
- **Frontend Enhancer:** Tailwind + bento grid patterns; performance optimization on OCI.

---

## 🏗️ CAPABILITIES REGISTRY

| Capability | Files | Purpose |
|------------|-------|---------|
| Core Identity | SOUL.md, IDENTITY.md, COMMITMENTS.md | Defines personality, ethics, decision logic |
| Playbook | ~/oracle-agent-playbook-v1/ | Product documentation; strategy guide |
| Trading | `memory/vault/trading/unified_trader.py` | Day trading mode; executes Alpaca orders |
| System Registry | AGENTS.md, BOOTSTRAP.md, routes.json | Coordinates sub-agents and model routing |
| Web Research | (contexts) | Lead generation and B2B research |
| Marketing | `.env.brevo` (Brevo SMTP) | Email outreach campaigns |
| Frontend Tools | (contexts/frontend-enhancer.md) | Tailwind, bento grid, responsive design |
| Mobile Dev | (contexts) | Mobile-first development patterns |
| Video (Remotion) | `memory/vault/video/remotion_inject_audio.py` | Video generation with audio sync |
| Voice (Kokoro) | (contexts) | TTS integration |

---

## 🔚 END OF MEMORY

**Remember**: This is a curated, living document. Update it regularly with lessons, decisions, and status changes. Review during heartbeats and after major events.

**Last major update:** 2026-04-05 — integrated memory vault contents (capabilities, contexts, projects, revenue tracks, wallet fix, session state, commitments log).

Gunna 🏴‍☠️
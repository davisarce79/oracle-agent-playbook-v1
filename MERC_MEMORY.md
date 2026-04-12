## OPERATIONAL PROTOCOLS

**GUNNA OPERATIONAL CONSTRAINT:**
Mid-conversation amnesia. NEVER ask Gunna to diagnose infrastructure. Merc diagnoses; Gunna executes pre-tested scripts only.

**RESEARCH-FIRST PROTOCOL:**
For ANY non-trivial build: verify feasibility first, confirm APIs exist, identify barriers, only code if confident. Say "researching first" if tempted to skip.

## MEMORY VAULT PROTOCOL

Vault: ~/Merc_Vault/ Primary file: ~/Merc_Vault/00-MEMORY.md
Rules: (1) Read 00-MEMORY.md at every session start. (2) Write immediately when Davis says "remember". (3) Append daily summary with timestamp at EOD. (4) NEVER replace or delete — append only. (5) Consult relevant files when working on specific topics.
§
Memory vault location: ~/Merc_Vault/. Rules: (1) Read 00-MEMORY.md at session start, (2) Write immediately when Davis says 'remember', (3) Append daily summary with timestamp at EOD, (4) Consult relevant project files when working, (5) Append-only - never replace/delete existing memories.
§
Created new skill: openclaw_diagnostics at ~/.hermes/skills/openclaw_diagnostics/. Skill provides functions to check service status, inspect identity/user/model config, review logs, apply updates, pin models, restart service, and report status. Encapsulates the diagnostic workflow used to troubleshoot Gunna/OpenClaw agent.
§
Listing Autopilot Project:
- Pivot: From listing submission (blocked by licenses) to AI Content Engine for real estate agents.
- Product: Generates listing copy, social posts, email campaigns, and landing pages from a property address.
- Tech Stack: RentCast API (Property Data/AVM), OpenRouter (Gemma 4), Meta Graph API, Zernio API, Vercel/GitHub Pages, Stripe.
- Pricing: $299/mo per agent.
- Core Workflow: Address -> RentCast API -> Gemma 4 -> Marketing Suite.
- RentCast API Key: e364bbe563e646d6a41466bbd6d5fe53 (Developer Plan active).
§
Listing Autopilot Project:
- Product: AI content engine for real estate agents (Listing descriptions, social posts, emails, landing pages).
- Tech Stack: RentCast API (Property data/AVM), OpenRouter (Gemma 4), Meta Graph API, Zernio API, Vercel/GitHub Pages.
- Pricing: $299/mo per agent.
- Operational Rule: Research APIs before coding; no paid services until beta; demo required before payment infra.
- Environment: RentCast API key stored in ~/.listing_autopilot/.env.
§
Listing Autopilot: Week 1 complete (2026-04-11). Core engine operational at ~/.listing_autopilot/engine.py. Pipeline: RentCast (/properties + /avm/value) -> Gemma 4 (OpenRouter). Verified successful output for 100 State St, Boston.
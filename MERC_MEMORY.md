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
§
Local flavor engine complete 2026-04-12. Engine v2 operational. Integrated Nominatim (reverse geocoding) and Overpass API to inject neighborhood and landmark data into marketing prompts.
§
Listing Autopilot: Week 2 complete (2026-04-12). Landing page generator operational. Full pipeline working: address -> RentCast -> AI copy -> HTML page -> Vercel URL. Engine at ~/.listing_autopilot/engine.py. Live demo: listing-100-state-st-boston.vercel.app
§
Listing Autopilot Cockpit: Mobile-first agent dashboard built with FastAPI (port 8000) and vanilla HTML/Tailwind. Public IP: 150.136.118.241. Requires Oracle VCN ingress rule for port 8000. UI features single address input, real-time status polling, and persistent history via vault.json. Use Python execute_code to write HTML files to avoid tag-doubling/escaping bugs in tool outputs.
§
When writing HTML/JS files to the Oracle Cloud environment, use Python's `execute_code` to write the file directly to disk. The standard `write_file` tool has a recurring bug where it doubles tags (e.g., `<<htmlhtml`) and escapes characters, causing the browser to render the page as raw text. Always use the public IP (150.136.118.241) for API_BASE in frontend code to ensure mobile accessibility.
§
Listing Autopilot Project: Core engine located at /home/opc/.listing_autopilot/engine.py. Architecture: RentCast API -> Gemma 4 -> Vercel deployment. Deployment uses dynamic .vercel config seeding to avoid hardcoded paths. Standardized on 4-space indentation. User expects extreme precision ('surgical') and zero tolerance for artifacts like doubled HTML tags (<<<).).
§
Listing Autopilot: Deployment logic in engine.py must be generic, avoiding hardcoded paths (e.g., 100 State St). Use dynamic .vercel config seeding from the deploy/ root. Avoid regex "band-aids" for HTML tag doubling; write files cleanly once. get_local_flavor must be called exactly once per request and passed as an explicit variable to downstream functions (generate_marketing_content) to prevent API rate-limiting. API calls (RentCast/OpenRouter) require immediate raw response logging (print(response.text)) before .json() parsing to diagnose "char 0" or empty payload errors. Fallback data structures (e.g., {"price": 0}) must be handled gracefully by the local flavor and prompt generation logic.
§
Listing Autopilot: The user prefers a strict, high-precision pipeline for AI content generation. Specifically, they mandate EXACT header matching (e.g., 'LISTING DESCRIPTION:') and non-greedy regex extraction to ensure zero artifacts in the final UI. This 'Surgical Alignment' between the LLM prompt and the parser is a critical operational preference.
§
Listing Autopilot: Technical Migration Blueprint created at /home/opc/.listing_autopilot/MIGRATION_BLUEPRINT.md. Maps Python/FastAPI logic (RentCast, OpenRouter, Vercel) to Next.js/Supabase for 1:1 porting. Includes surgical prompt logic and local flavor enrichment specs.
§
OpenClaw (Gunna) Update/Repair Pattern: Version 4.12+ updates may wipe 'agents.list' and corrupt 'openclaw.json' by removing agent keys. Repair requires: (1) Recreating ~/.openclaw/agents.list with agent names (gunna, merc, paperclip), (2) Reverting openclaw.json 'agents' block to only contain 'defaults', (3) Killing zombie processes and restarting via 'systemctl --user restart openclaw-gateway'.
§
OpenClaw (Gunna) Update/Repair Pattern: Version 4.12+ updates may wipe 'agents.list' and corrupt 'openclaw.json' by removing agent keys. Repair requires: (1) Recreating ~/.openclaw/agents.list with agent names (gunna, merc, paperclip), (2) Reverting openclaw.json 'agents' block to only contain 'defaults', (3) Restoring the original gateway token from .bak files to maintain channel connectivity, (4) Restarting via 'systemctl --user restart openclaw-gateway'.
§
OpenClaw 4.x Migration/Repair: Updates often wipe the 'channels/' directory and reset 'openclaw.json'. To restore Telegram connectivity: (1) Extract the bot token from 'openclaw.json.bak' or 'config-audit.jsonl' (grep for numeric:alphanumeric pattern), (2) Recreate '/home/opc/.openclaw/channels/telegram/config.json' with the botToken, (3) Ensure 'openclaw.json' has the correct gateway token restored from backups to match the bot's auth.
§
OpenClaw 4.14+ Telegram Repair: If the channel is silent after an update, use `openclaw channels add --channel telegram --token <token>` to force-rebind the bot. Manual file injection into `pairing.json` is no longer sufficient in the 4.x architecture as it requires a config sync to `openclaw.json`.
§
OpenClaw 4.14+ Telegram Repair: If the channel is silent or stuck in a restart loop with 'deleteWebhook' 404 errors, it indicates a mismatch between the bot token and the Telegram API state. Use `openclaw channels add --channel telegram --token <token>` to force-rebind. Manual file injection into `pairing.json` is no longer sufficient as the 4.x architecture requires a config sync to `openclaw.json`.
§
Listing Autopilot Migration: Complete logic mapping from Python/FastAPI to Next.js/Supabase is stored in /home/opc/.listing_autopilot/MIGRATION_BLUEPRINT.md. Use this as the source of truth for porting the property pipeline, RentCast integration, and surgical prompt logic.
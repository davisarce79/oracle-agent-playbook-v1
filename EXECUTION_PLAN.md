# Unblock Revenue Tracks: Execution Plan

**Purpose:** Consolidated, step-by-step guide to unblocking all revenue-generating channels. Once the inputs below are provided, execution can happen in under 30 minutes.

---

## 📊 Current High-Priority Blockers

| Track | Status | Blocker | What's Needed | Time to Execute |
|-------|--------|---------|---------------|-----------------|
| Crypto Token ($GUNNA) | Preparation Complete | No SOL in wallet | ~0.05-0.1 SOL (~$5-10) sent to wallet | <30 min |
| Email Marketing | Automation Prepared | No SMTP credentials | Choose provider + obtain credentials | <15 min |
| Telegram Ads | DONE (cron active) | N/A | Already running | - |
| Gumroad Sales | LIVE | No traffic/marketing | Work-in-progress (see below) | Ongoing |

---

## 🎯 Action 1: Fund $GUNNA Token Wallet

### Steps:
1. **Send SOL to wallet address:**
   ```
   dXTKoKg9jAPYqYzZGPB2TPSv6nZFiFbAhVQdz6wopcyF6uzHW
   ```
   - Amount: 0.05–0.1 SOL (recommend 0.1 for buffer)
   - Network: Solana mainnet
   - From any exchange (Coinbase, Binance, etc.) or wallet

2. **Wait for confirmation** (~1–2 minutes).

3. **Deploy token (choose one method):**
   - **CLI:** `python3 deploy_gunna_token.py` (has metadata baked)
   - **Web:** Go to https://pump.fun, connect wallet, create token with:
     - Symbol: GUNNA
     - Name: Agent Gunna Token
     - Supply: 1,000,000,000
     - Logo: `memory/uploads/gunna_token_logo_clean.png`
     - Description: "Governance and rewards token for Agent Gunna autonomous revenue machines."
     - Links: Telegram `t.me/AgentGunnaAlpha`, Website `https://gumroad.com/l/ujgrn`

4. **Confirm token creation** (pump.fun will mint and assign metadata).

5. **Update COMMITMENTS.md** status and notify Davis.

---

## 🎯 Action 2: Configure SMTP Email Marketing

### Sub-step A: Obtain SMTP Credentials (~10 min)
Choose a provider and follow the detailed guide in `provisioning_guides/smtp_credentials_guide.md`.

**Quick recommendations:**
- **Gmail** if you have an account (use app password with 2FA)
- **Outlook** for higher free limits (~300/day)
- **SendGrid** for API-based rotation

You'll end up with:
- SMTP host (e.g., `smtp.gmail.com`)
- Port (usually `587`)
- Username (full email)
- Password (app password or API key)

### Sub-step B: Run Automated Setup (~2 min)
```bash
cd /home/opc/.openclaw/workspace
python3 setup_email_marketing.py
```
Enter the credentials when prompted. The script will:
- Create `send_campaign.py` with your config baked in
- Create `test_email.py` for validation
- Generate `recipients_sample.csv` template
- Output a cron template

### Sub-step C: Test (~2 min)
```bash
python3 test_email.py
```
Check your inbox. If received, email skill is working.

### Sub-step D: Prepare Campaign (~5 min)
1. Copy `recipients_sample.csv` to `recipients.csv` and add contacts (at least `email,name` columns).
2. Copy `campaign_templates/oracle_agent_playbook_email.md` to `email_body.txt` (edit subject if needed).
3. (Optional) Add your physical mailing address to footer for CAN-SPAM compliance.

### Sub-step E: Send Test Batch (~2 min)
```bash
python3 send_campaign.py recipients.csv "Check this out" email_body.txt
```
Review the result report. If success, proceed to live send or schedule cron.

### Sub-step F: Schedule Recurring Sends (Optional)
Add to crontab using the template `cron_email_example.txt` (included). Example: weekly Monday 9 AM.

---

## 📈 Parallel: Gumroad Traffic & Sales

The Playbook is live but has zero sales due to lack of marketing. Once the above two channels are active, coordinate promotion:

- **Telegram:** Already auto-posts weekly (watch for first run)
- **Email:** Newsletter to initial list (start with 10–20 warm contacts)
- **Crypto token:** Launch creates community and potential bounty/reward programs
- **Mastodon/Discord/Reddit:** Manual outreach using `marketing_scout.py` opportunities

**Note:** X/Twitter remains blocked from this host. Do not waste time trying to fix; use working platforms.

---

## 🧾 Summary of Prepared Artifacts

- `deploy_gunna_token.py` — token deployment with metadata
- `memory/uploads/gunna_token_logo_clean.png` — token logo
- `setup_email_marketing.py` — automated email config
- `campaign_templates/oracle_agent_playbook_email.md` — ready-to-use email content
- `provisioning_guides/smtp_credentials_guide.md` — provider-specific setup instructions
- `send_campaign.py` (after running setup) — operational campaign runner
- `test_email.py` (after running setup) — connection validator

---

## 🚀 One-Click Checklist (After Inputs Provided)

When you have:
- [ ] SOL sent to wallet
- [ ] SMTP credentials in hand

Then execute:

```bash
# 1. Deploy token
python3 deploy_gunna_token.py
# (follow prompts or use pump.fun web)

# 2. Configure email
python3 setup_email_marketing.py
# enter credentials

# 3. Test email
python3 test_email.py

# 4. Prepare recipients.csv and email_body.txt
# (use provided templates)

# 5. Send first campaign
python3 send_campaign.py recipients.csv "Your Subject" email_body.txt

# 6. Update COMMITMENTS.md and MEMORY.md with results
```

Total hands-on time: ~30–40 minutes.

---

**Created:** 2026-03-16 06:53 UTC
**Author:** Agent Gunna
**Purpose:** Single source of truth for unblocking revenue tracks; reduce procrastination and friction.

# Revenue Track Status & Unblocker Guide

**Last updated:** 2026-03-17  
**Owner:** Agent Gunna  
**Purpose:** Consolidated view of high-priority revenue tracks, current blockers, and step-by-step execution plans to minimize friction when inputs are provided.

---

## Track A: $GUNNA Token Launch on Solana (pump.fun)

### Current Status
- **Preparation:** 95% complete
- **Blocker:** Critical — Deployment wallet address is **invalid** (49 characters). Solana pubkeys must be exactly 44 base58 characters.
- **Also awaiting:** ~0.05–0.1 SOL funding for deployment fees.

### What’s Ready
- Deployment script: `deploy_gunna_token.py`
- Token metadata: symbol `GUNNA`, name `Agent Gunna Token`, supply 1B, decimals 9, logo `memory/uploads/gunna_token_logo_clean.png`, links to Telegram/Playbook.
- Wallet monitor script (currently broken due to bad address).
- Full guides:
  - `provisioning_guides/sol_acquisition_deployment_guide.md`
  - `EXECUTION_PLAN.md`

### Immediate Actions Required from Davis
1. **Provide correct Solana wallet address** (44-char base58 pubkey). Replace the current malformed address in:
   - `deploy_gunna_token.py` (line ~20)
   - `monitor_gunna_wallet.py` (line ~9)
   - `COMMITMENTS.md` and any other references.
2. **Fund the wallet** with 0.05–0.1 SOL on mainnet.
3. Once funded, either:
   - Run `python3 deploy_gunna_token.py` (if Solana CLI installed), **or**
   - Use pump.fun web UI with the wallet.

### Note on Wallet Monitor
The monitor uses Solana RPC. The invalid address causes RPC error `Invalid param: WrongSize`. After fixing the address, the monitor should work. If issues persist, consider switching to a third-party API fallback.

---

## Track B: Email Marketing (SMTP Configuration)

### Current Status
- **Preparation:** 100% complete
- **Blocker:** Awaiting SMTP credentials and provider selection (Gmail/Outlook/SendGrid/Zoho).

### What’s Ready
- Setup script: `setup_email_marketing.py`
- Campaign template: `campaign_templates/oracle_agent_playbook_email.md`
- Comprehensive credential guide: `provisioning_guides/smtp_credentials_guide.md`
- `EXECUTION_PLAN.md` integration

### Immediate Actions Required from Davis
1. Choose an email provider (recommended: Gmail with App Password, or SendGrid for scale).
2. Obtain the necessary API key/password.
3. Run `python3 setup_email_marketing.py` and follow prompts to bake config.
4. Optionally test the campaign before going live.

---

## Other Active Systems

| System | Status | Notes |
|--------|--------|-------|
| Gumroad product | LIVE | 0 sales to date. No changes. |
| Alpaca paper trading | RUNNING | WULF strategy impaired: HMM scan failing due to insufficient intraday data samples. Investigating recommended. |
| Twitter/X mentions | BLOCKED | Network egress block persists (Oracle Cloud). 401/404 errors. Consider proxy/VPN if critical. |
| Telegram auto-posts | DONE | Cron active, weekly posts scheduled. |
| Marketing scout | ACTIVE | First output processed; engagement assistant ready. Ongoing Reddit/Discord outreach possible. |
| NVDX bracket orders | READY | Script `place_nvdx_order.py` and cron scheduled (9:35 AM & 11:54 AM EDT). Not yet run today (pre-market). |

---

## Recommended Next Steps for Davis

1. **High-impact:** Correct the $GUNNA wallet address and fund it. This track is 95% ready; a few dollars of SOL will activate deployment.
2. **High-impact:** Provide SMTP credentials to launch email campaign to Playbook audience.
3. **Technical:** Fix HMM data pipeline to restore automated WULF trading signals.
4. **Optional:** Review marketing scout lead list and begin executing outreach (low-hanging fruit for Playbook sales).

Once the two revenue tracks are live (token + email), monitor Gumroad and wallet balance daily.

---

## Execution Summary Table

| Track | Prep Done | Blockers | Expected Effort to Launch |
|-------|-----------|----------|---------------------------|
| $GUNNA token | 95% | Invalid wallet address, no SOL | <30 min after address fix + funding |
| Email marketing | 100% | SMTP credentials | <10 min after credential entry |
| Trading (WULF) | 50% | HMM scan failure | TBD (requires data fix) |

---

**Created:** 2026-03-17  
**Keep this document up-to-date as status changes.**

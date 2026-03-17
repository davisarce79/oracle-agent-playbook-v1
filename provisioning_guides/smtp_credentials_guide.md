# SMTP Credential Acquisition Guide

## Purpose
This guide helps you obtain SMTP credentials quickly from popular email providers so you can configure the email marketing skill immediately.

---

## Option 1: Gmail (Google Workspace or Gmail Account)

**Recommended if you already have a Gmail account.**

### Steps:
1. **Enable 2-Factor Authentication (2FA)** on your Google Account:
   - Go to https://myaccount.google.com/security
   - Under "Signing in to Google", enable 2-Step Verification
2. **Generate an App Password**:
   - After enabling 2FA, go to https://myaccount.google.com/apppasswords
   - Select "Mail" as the app, "Other (Custom name)" as device → name it "Agent Gunna"
   - Google will generate a 16-character password (e.g., `abcd efgh ijkl mnop`)
   - **Copy this password immediately** — you won't see it again!
3. **Use these SMTP settings**:
   - Host: `smtp.gmail.com`
   - Port: `587`
   - Username: your full Gmail address (e.g., `agentgunna@gmail.com`)
   - Password: the 16-character app password (no spaces)
   - TLS: Yes

**Notes:**
- Free Gmail accounts have a sending limit of ~100 emails per day.
- If you hit limits, wait 24 hours or upgrade to Google Workspace.

---

## Option 2: Outlook.com / Microsoft 365

**Good alternative with higher free limits (~300/day).**

### Steps:
1. **Enable 2FA (optional but recommended)**:
   - Go to https://account.microsoft.com/security
   - Turn on two-step verification
2. **Use your normal account password** (or create an app password if 2FA is on):
   - If 2FA enabled, go to "Additional security verification" → "App passwords" → create one for "Mail"
3. **SMTP settings**:
   - Host: `smtp-mail.outlook.com`
   - Port: `587`
   - Username: your full Outlook email
   - Password: your account password (or app password if 2FA)
   - TLS: Yes

**Notes:**
- Free Outlook accounts allow ~300 emails/day.
- No special app password needed if you don't use 2FA (but less secure).

---

## Option 3: SendGrid (by Twilio)

**Best for higher volume and API-based delivery.**

### Steps:
1. **Create a free SendGrid account** at https://signup.sendgrid.com/
2. **Verify your single sender identity** (required for free tier):
   - Go to Settings → Single Sender Verification
   - Fill in from name, email, and physical address
   - SendGrid will email you a verification link — click it
3. **Create an API Key**:
   - Go to Settings → API Keys → Create API Key
   - Name: "Agent Gunna Email"
   - Permissions: "Mail Send" (full access)
   - Copy the API key (starts with `SG.`)
4. **SMTP settings**:
   - Host: `smtp.sendgrid.net`
   - Port: `587`
   -Username: `apikey` (literally the string "apikey")
   - Password: your API key (the `SG.` string)
   - TLS: Yes

**Notes:**
- Free tier: 100 emails/day.
- API key can be revoked/recreated anytime.
- Works well with `email-marketing` skill.

---

## Option 4: Zoho Mail

**Free with 5GB storage, good for small lists.**

### Steps:
1. **Sign up for Zoho Mail Free** at https://www.zoho.com/mail/
2. **Add your domain (optional)** or use `@zohomail.com` address
3. **Enable 2FA** in Security settings (recommended)
4. **Generate an app-specific password** if 2FA is enabled:
   - Go to My Account → Security → App passwords
5. **SMTP settings**:
   - Host: `smtp.zoho.com`
   - Port: `587`
   - Username: your full Zoho email
   - Password: your account password or app password
   - TLS: Yes

**Notes:**
- Free plan: 5GB storage, 100 emails/day limit.
- Supports custom domains.

---

## Option 5: Amazon SES (Simple Email Service)

**High volume, cheapest at scale, but more complex setup.**

### Prerequisites:
- AWS account (requires credit card even for free tier)
- Domain verification (required for production access)
- Move out of sandbox (request production access)

**Not recommended for immediate use** unless you already have AWS setup.

---

## Quick Comparison

| Provider | Free Daily Limit | Setup Complexity | Notes |
|----------|------------------|------------------|-------|
| Gmail | ~100 | Easy | Use app password with 2FA |
| Outlook | ~300 | Easy | Can use normal password |
| SendGrid | 100 | Medium | Need to verify sender, create API key |
| Zoho | 100 | Medium | Good if you want @zoho.com address |
| Amazon SES | 62,000/yr | Hard | AWS setup, domain verification |

**Recommendation:** Start with **Gmail** if you have an existing account; otherwise **Outlook** for higher free limits; **SendGrid** if you want API-based management and easier credential rotation.

---

## What to Do After You Get Credentials

1. Run `python3 setup_email_marketing.py` in the workspace
2. Enter the SMTP settings exactly as above
3. The script will create `send_campaign.py` with your config baked in
4. Test with `python3 test_email.py` (sends to yourself)
5. Create `recipients.csv` with your contact list
6. Create `body.txt` with your email content (use `{name}` for personalization)
7. Launch: `python3 send_campaign.py recipients.csv "Subject" body.txt`

---

**Created:** 2026-03-16 05:53 UTC
**By:** Agent Gunna
**Purpose:** Accelerate SMTP configuration for email marketing launch

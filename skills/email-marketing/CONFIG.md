# Email Marketing Skill — Configuration Guide

## Status
✅ Skill installed at `skills/email-marketing/`
⚠️ **Not yet configured** — requires SMTP credentials

---

## 🎯 **What It Does**
Send batch marketing emails with personalization (`{name}`, `{email}`). Ideal for:
- Newsletter to Playbook customers
- Beta reader outreach for *The Mechanical Soul*
- Community engagement

---

## 📧 **Choose an Email Provider (Free Tier Options)**

| Provider | Free limit | Notes |
|----------|------------|-------|
| **Gmail** (Google) | ~100/day | Use App Password if 2FA enabled |
| **Outlook.com** | ~300/day | Free with Microsoft account |
| **SendGrid** | 100/day | Requires API key (SMTP works) |
| **Zoho Mail** | 5GB storage | Supports SMTP, free tier |
| **Amazon SES** | 62,000/year if from EC2 | More complex setup |

**Recommendation:** Start with Gmail (already have agentgunna@gmail.com) or Outlook.

---

## 🔧 **Configuration Steps**

### 1. Get SMTP credentials
- **Gmail:** Enable 2FA → Generate App Password → use 16-char password
- **Outlook:** Use normal password or app password
- **SendGrid:** Create API key → use as password

### 2. Prepare recipients CSV (example `recipients.csv`):
```csv
email,name
reader1@example.com,Alice
reader2@example.com,Bob
```

### 3. Test call (example):
```python
from skills.email_marketing import send_batch_email

result = send_batch_email(
    smtp_host="smtp.gmail.com",
    smtp_port=587,
    username="agentgunna@gmail.com",
    password="YOUR_APP_PASSWORD",
    from_email="agentgunna@gmail.com",
    from_name="Agent Gunna",
    subject="Check out The Oracle Agent Playbook",
    body_template="Hi {name},\n\nLearn to build AI agents on Oracle Cloud Free Tier: https://gumroad.com/l/ujgrn",
    recipients=[
        {"email": "reader1@example.com", "name": "Alice"},
        {"email": "reader2@example.com", "name": "Bob"}
    ],
    use_tls=True,
    batch_size=25
)
print(result)
```

---

## 📁 **File Locations**
- Skill: `/home/opc/.openclaw/workspace/skills/email-marketing/`
- Main module: `email_marketing.py`
- Test script: Can create `test_email.py` when ready

---

## ⚠️ **Important**
- **Never** commit passwords to Git
- Store credentials in environment variables or `.env` file (gitignored)
- Respect rate limits (batch_size 25-50 recommended)
- Include unsubscribe link in commercial emails (CAN-SPAM)

---

## 🚀 **Next Action**
1. Choose provider
2. Obtain SMTP credentials
3. Update `COMMITMENTS.md` status to "In Progress"
4. Write actual test script and run
5. If successful, schedule cron for weekly newsletter

---

**Last updated:** 2026-03-15 (commit 140f2f4)

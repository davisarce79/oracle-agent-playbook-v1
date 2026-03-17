# Email Marketing Skill

Send batch marketing emails via SMTP using Python's built-in libraries. No external CLI dependencies.

## Features
- Send personalized emails to CSV lists or programmatic recipient arrays
- HTML or plain text support
- Batch sending with configurable batch size
- TLS/SSL encryption support
- Detailed success/failure reporting
- No external CLI tools required (uses Python smtplib)

## Usage

```python
# Direct skill call
result = await use_skill('email-marketing', {
    'smtp_host': 'smtp.gmail.com',
    'smtp_port': 587,
    'username': 'your-email@gmail.com',
    'password': 'your-app-password',
    'from_email': 'your-email@gmail.com',
    'from_name': 'Davis Arce',
    'subject': 'Introducing The Mechanical Soul',
    'body_template': "Hi {name},\n\nI'm writing to introduce my new literary crime novel...\n\nBest,\nDavis",
    'recipients': [
        {'email': 'reader1@example.com', 'name': 'Alice'},
        {'email': 'reader2@example.com', 'name': 'Bob'}
    ],
    'batch_size': 50
})
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `smtp_host` | string | Yes | SMTP server hostname |
| `smtp_port` | integer | No (default: 587) | SMTP server port |
| `username` | string | Yes | SMTP username (usually email) |
| `password` | string | Yes | SMTP password or app-specific password |
| `from_email` | string | Yes | Sender email address |
| `from_name` | string | Yes | Sender display name |
| `subject` | string | Yes | Email subject line |
| `body_template` | string | Yes | Email body with `{name}` and `{email}` placeholders |
| `recipients` | array | Yes | List of recipient objects: `{'email': str, 'name': str (optional)}` |
| `use_tls` | boolean | No (default: true) | Use STARTTLS |
| `batch_size` | integer | No (default: 50) | Emails per SMTP connection |

## Returns

```json
{
  "total": 100,
  "sent": 98,
  "failed": 2,
  "errors": [
    {"email": "bad@example.com", "error": "SMTP 550: Mailbox not found"},
    {"email": "spam@example.com", "error": "SMTP 554: Message rejected"}
  ]
}
```

## Examples

### From CSV File

```python
from email_marketing import send_from_csv

config = {
    'smtp_host': 'smtp.gmail.com',
    'smtp_port': 587,
    'username': 'author@example.com',
    'password': 'APP_PASSWORD_HERE',
    'from_email': 'author@example.com',
    'from_name': 'Davis Arce',
    'use_tls': True
}

body = "Hi {name},\n\nCheck out my new book 'The Mechanical Soul'..."
result = send_from_csv('subscribers.csv', config, 'New Book Release', body)
print(f"Sent {result['sent']}/{result['total']}")
```

### Using MIME (HTML + Plain Text)

The skill automatically detects HTML if body contains `<html>` tag. For multipart, modify `email_marketing.py` to create both plain and HTML parts.

## Security Notes

- **Never hardcode passwords** in scripts. Use environment variables or secure vaults.
- Use **app-specific passwords** (Gmail) or SMTP tokens (SendGrid, Mailgun) instead of main account passwords.
- Store credentials in OpenClaw's secret manager (`openclaw secrets set smtp_password ...`)
- Respect CAN-SPAM: include unsubscribe link, physical address, clear opt-out.

## Integration with OpenClaw

Once skill is installed, you can call it from any agent session:
```python
result = await use_skill('email-marketing', params)
if result['sent'] > 0:
    print(f"Marketing blast sent to {result['sent']} recipients")
```

## Limitations

- Rate limits: SMTP servers impose limits (Gmail ~500/day, SendGrid 100k/month). Plan accordingly.
- No built-in unsubscribe management - implement at application level.
- No email templates - use string formatting or Jinja2 in your calling code.
- No bounce handling - monitor SMTP errors and clean lists manually.

## Recommended SMTP Providers for Marketing

- **SendGrid** (free tier: 100 emails/day)
- **Mailgun** (free tier: 5,000 emails/month for first 3 months)
- **Amazon SES** (very cheap, ~$0.10/1000)
- **Gmail** (personal: 500/day, Workspace: 2,000/day)

## Setup Example: Gmail

1. Enable 2-factor authentication on Gmail
2. Generate App Password: Google Account → Security → App passwords
3. Use that 16-character password in the `password` field
4. Set `smtp_host='smtp.gmail.com'`, `smtp_port=587`, `use_tls=True`

## CSV Format

```csv
email,name
alice@example.com,Alice
bob@example.com,Bob
```

Name column is optional; if missing, `{name}` placeholder resolves to empty string.

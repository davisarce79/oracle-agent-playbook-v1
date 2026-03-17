"""Email Marketing Skill - Send batch emails for marketing campaigns"""

from .email_marketing import send_batch_email, send_from_csv

# Skill metadata
SKILL_INFO = {
    "name": "email-marketing",
    "description": "Send batch marketing emails via SMTP. Supports CSV lists, HTML templates, and personalized fields.",
    "capabilities": ["email", "marketing", "batch"],
    "parameters": {
        "smtp_host": {"type": "string", "required": True, "description": "SMTP server host"},
        "smtp_port": {"type": "integer", "default": 587, "description": "SMTP port"},
        "username": {"type": "string", "required": True, "description": "SMTP username (email)"},
        "password": {"type": "string", "required": True, "description": "SMTP password or app password"},
        "from_email": {"type": "string", "required": True, "description": "Sender email address"},
        "from_name": {"type": "string", "required": True, "description": "Sender display name"},
        "subject": {"type": "string", "required": True, "description": "Email subject line"},
        "body_template": {"type": "string", "required": True, "description": "Email body with {name}, {email} placeholders"},
        "recipients": {
            "type": "array",
            "required": True,
            "description": "List of recipient dicts with 'email' and optionally 'name'",
            "items": {
                "type": "object",
                "properties": {
                    "email": {"type": "string"},
                    "name": {"type": "string"}
                }
            }
        },
        "use_tls": {"type": "boolean", "default": True, "description": "Use STARTTLS"},
        "batch_size": {"type": "integer", "default": 50, "description": "Emails per connection"}
    }
}

async def handle_call(params: dict) -> dict:
    """
    Send batch marketing emails.
    
    Required params:
        smtp_host, smtp_port, username, password, from_email, from_name,
        subject, body_template, recipients (list)
    
    Optional:
        use_tls (bool), batch_size (int)
    
    Returns:
        Dict with total, sent, failed counts and any errors.
    """
    # Extract parameters
    smtp_host = params.get("smtp_host")
    smtp_port = params.get("smtp_port", 587)
    username = params.get("username")
    password = params.get("password")
    from_email = params.get("from_email")
    from_name = params.get("from_name")
    subject = params.get("subject")
    body_template = params.get("body_template")
    recipients = params.get("recipients", [])
    use_tls = params.get("use_tls", True)
    batch_size = params.get("batch_size", 50)
    
    # Validate required fields
    required = [smtp_host, username, password, from_email, from_name, subject, body_template]
    if not all(required):
        missing = [k for k, v in {
            "smtp_host": smtp_host,
            "username": username,
            "password": password,
            "from_email": from_email,
            "from_name": from_name,
            "subject": subject,
            "body_template": body_template
        }.items() if not v]
        return {"error": f"Missing required parameters: {', '.join(missing)}"}
    
    if not recipients:
        return {"error": "No recipients provided"}
    
    # Send emails
    return send_batch_email(
        smtp_host=smtp_host,
        smtp_port=int(smtp_port),
        username=username,
        password=password,
        from_email=from_email,
        from_name=from_name,
        subject=subject,
        body_template=body_template,
        recipients=recipients,
        use_tls=bool(use_tls),
        batch_size=int(batch_size)
    )

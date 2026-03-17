#!/usr/bin/env python3
"""
Email Marketing Skill - Send batch marketing emails via SMTP
No external dependencies - uses Python's smtplib and email libraries.
"""

import smtplib
import csv
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict, Any
import json

def send_batch_email(
    smtp_host: str,
    smtp_port: int,
    username: str,
    password: str,
    from_email: str,
    from_name: str,
    subject: str,
    body_template: str,
    recipients: List[Dict[str, str]],
    use_tls: bool = True,
    batch_size: int = 50
) -> Dict[str, Any]:
    """
    Send batch marketing emails via SMTP.

    Args:
        smtp_host: SMTP server host (e.g., smtp.gmail.com)
        smtp_port: SMTP port (587 for TLS, 465 for SSL)
        username: SMTP username (email)
        password: SMTP password or app password
        from_email: Sender email address
        from_name: Sender display name
        subject: Email subject line
        body_template: Email body with placeholders like {name}, {email}
        recipients: List of dicts with 'email' and optionally 'name' keys
        use_tls: Use STARTTLS (True) or SSL (False)
        batch_size: Number of emails to send per connection

    Returns:
        Dict with success count, failure count, and error details
    """
    results = {
        "total": len(recipients),
        "sent": 0,
        "failed": 0,
        "errors": []
    }

    # Connect to SMTP server
    try:
        if use_tls:
            server = smtplib.SMTP(smtp_host, smtp_port)
            server.starttls()
        else:
            server = smtplib.SMTP_SSL(smtp_host, smtp_port)
        
        server.login(username, password)
    except Exception as e:
        return {
            "total": len(recipients),
            "sent": 0,
            "failed": len(recipients),
            "errors": [f"SMTP connection failed: {str(e)}"]
        }

    # Send in batches
    for i in range(0, len(recipients), batch_size):
        batch = recipients[i:i+batch_size]
        for recipient in batch:
            try:
                # Personalize body
                personalized_body = body_template.format(
                    name=recipient.get('name', ''),
                    email=recipient['email']
                )
                
                # Create message
                msg = MIMEMultipart('alternative')
                msg['From'] = f"{from_name} <{from_email}>"
                msg['To'] = recipient['email']
                msg['Subject'] = subject
                
                # Attach body
                msg.attach(MIMEText(personalized_body, 'html' if '<html>' in personalized_body else 'plain'))
                
                # Send
                server.send_message(msg)
                results['sent'] += 1
                
            except Exception as e:
                results['failed'] += 1
                results['errors'].append({
                    'email': recipient['email'],
                    'error': str(e)
                })
    
    server.quit()
    return results

def send_from_csv(
    csv_path: str,
    smtp_config: Dict[str, Any],
    subject: str,
    body_template: str,
    email_col: str = 'email',
    name_col: str = 'name'
) -> Dict[str, Any]:
    """
    Send batch emails from a CSV file.

    Args:
        csv_path: Path to CSV file with recipient data
        smtp_config: Dict with smtp_host, smtp_port, username, password, from_email, from_name
        subject: Email subject
        body_template: Email body with {name}, {email} placeholders
        email_col: CSV column name for email addresses
        name_col: CSV column name for recipient names

    Returns:
        Dict with send results
    """
    recipients = []
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get(email_col):
                recipients.append({
                    'email': row[email_col],
                    'name': row.get(name_col, '')
                })
    
    return send_batch_email(
        smtp_config['smtp_host'],
        smtp_config['smtp_port'],
        smtp_config['username'],
        smtp_config['password'],
        smtp_config['from_email'],
        smtp_config['from_name'],
        subject,
        body_template,
        recipients,
        use_tls=smtp_config.get('use_tls', True)
    )

if __name__ == "__main__":
    # CLI interface for testing
    import argparse
    parser = argparse.ArgumentParser(description='Send batch marketing emails')
    parser.add_argument('--csv', required=True, help='CSV file with recipients')
    parser.add_argument('--subject', required=True, help='Email subject')
    parser.add_argument('--body', required=True, help='Email body template file')
    parser.add_argument('--config', required=True, help='SMTP config JSON file')
    args = parser.parse_args()

    # Load config
    with open(args.config) as f:
        config = json.load(f)

    # Load body template
    with open(args.body) as f:
        body = f.read()

    # Send
    result = send_from_csv(args.csv, config, args.subject, body)
    print(json.dumps(result, indent=2))

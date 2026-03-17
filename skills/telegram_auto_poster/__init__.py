#!/usr/bin/env python3
"""
Telegram Auto-Poster Skill
Generates and posts promotional content for The Oracle Agent Playbook.
"""

import os
import sys
import json
import logging
from datetime import datetime
from typing import Dict, Any

# Optional: import openclaw tools if available
try:
    from openclaw import tools
except ImportError:
    tools = None

# Configure logging
LOG_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'memory', 'telegram_posts.log')
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

def generate_post(model: str = "nvidia/nemotron-3-nano-30b-a3b:free") -> str:
    """Generate a unique promotional post using OpenRouter."""
    import requests

    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        # Try to read from agent auth profiles (absolute path)
        try:
            import json
            auth_path = '/home/opc/.openclaw/agents/main/agent/auth-profiles.json'
            with open(auth_path) as f:
                profiles = json.load(f)
                api_key = profiles.get("profiles", {}).get("openrouter", {}).get("key")
        except Exception as e:
            raise RuntimeError(f"OPENROUTER_API_KEY not found and could not read auth profiles: {e}")

    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY not found in environment or auth profiles")

    prompt = """Think step by step. Then write a single concise, engaging tweet under 280 characters promoting 'The Oracle Agent Playbook' on Gumroad.

Product: A 5-chapter technical guide to building autonomous AI agents on Oracle Cloud Free Tier.

Tone: Professional yet enthusiastic. Highlight:
- Build your own AI revenue machine
- Oracle Cloud Free Tier (no cost)
- Step-by-step implementation

Include link: https://gumroad.com/l/ujgrn
Add 1-2 relevant hashtags: #AI #Automation #OracleCloud #AgentBuilder

After your reasoning, provide the final tweet on a new line starting with 'TWEET:' and nothing else."""

    resp = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://openclaw.ai",
            "X-Title": "AgentGunna"
        },
        json={
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 1000,
            "temperature": 0.8
        },
        timeout=30
    )
    if not resp.ok:
        raise RuntimeError(f"OpenRouter {resp.status_code}: {resp.text[:500]}")
    data = resp.json()
    if "error" in data:
        raise RuntimeError(f"OpenRouter API error: {data['error']}")
    message = data["choices"][0]["message"]
    text = message.get("content")
    if text is None or text.strip() == "":
        # Fallback: try to extract tweet from reasoning field
        reasoning = message.get("reasoning", "")
        # Strategy 1: Look for line starting with 'TWEET:'
        for line in reasoning.split("\n"):
            line = line.strip()
            if line.startswith("TWEET:"):
                text = line[6:].strip()
                break
        if not text:
            # Strategy 2: Extract quoted string containing the Gumroad link and hashtags
            import re
            # Find double-quoted strings that contain the link
            matches = re.findall(r'"([^"]*gumroad\.com[^"]*)"', reasoning)
            if matches:
                candidate = matches[0].strip()
                # If candidate is a reasonable tweet length, use it
                if len(candidate) <= 280 and ('#' in candidate):
                    text = candidate
        if not text:
            raise RuntimeError(f"OpenRouter returned no content and could not extract tweet from reasoning. Full reasoning: {reasoning[:500]}...")
    text = text.strip()
    # Ensure it's not too long
    if len(text) > 280:
        text = text[:277] + "..."
    return text

def send_to_telegram(message: str, channel: str = "@AgentGunnaAlpha") -> Dict[str, Any]:
    """Send message to Telegram channel using OpenClaw's message tool if available."""
    if tools and hasattr(tools, 'message'):
        # Use OpenClaw tool
        result = tools.message.send(
            action="send",
            target=channel,
            message=message,
            silent=True
        )
        return {"status": "sent", "tool": "openclaw", "result": result}
    else:
        # Fallback: direct Telegram Bot API if token configured
        token = os.environ.get("TELEGRAM_BOT_TOKEN")
        if not token:
            raise RuntimeError("No method to send Telegram: neither OpenClaw tools nor TELEGRAM_BOT_TOKEN available")
        import requests
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        resp = requests.post(url, json={"chat_id": channel, "text": message}, timeout=15)
        resp.raise_for_status()
        return {"status": "sent", "tool": "telegram-bot-api"}

def send(args: Dict[str, Any] = None) -> Dict[str, Any]:
    """Main entry point for the skill."""
    try:
        channel = os.environ.get("TELEGRAM_CHANNEL", "@AgentGunnaAlpha")
        model = os.environ.get("OPENROUTER_MODEL", "nvidia/nemotron-3-nano-30b-a3b:free")
        dry_run = args.get("dry_run", False) if isinstance(args, dict) else False

        post = generate_post(model)
        if dry_run:
            logging.info(f"[DRY RUN] Would post to {channel}: {post[:100]}...")
            return {"status": "dry_run", "channel": channel, "post": post}
        send_result = send_to_telegram(post, channel)

        logging.info(f"Successfully posted to {channel}: {post[:100]}...")
        return {
            "status": "success",
            "channel": channel,
            "post": post,
            "send_result": send_result
        }
    except Exception as e:
        logging.error(f"Failed to post: {str(e)}")
        return {"status": "error", "error": str(e)}

# If run directly (for testing)
if __name__ == "__main__":
    result = send()
    print(json.dumps(result, indent=2))

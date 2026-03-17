# Telegram Auto-Poster Skill

Automatically generate and post promotional content to a Telegram channel on a schedule.

## Purpose
- Weekly announcements for *The Oracle Agent Playbook* on Gumroad
- AI-generated content variations to avoid repetition
- Reliable posting using OpenClaw's messaging infrastructure

## Usage
Trigger manually:
```
use skill telegram-auto-poster send
```

Schedule via cron (example: every Monday 9 AM):
```
0 9 * * 1 openclaw agents run telegram-auto-poster send --to AgentGunnaAlpha
```
(Or use HEARTBEAT.md to trigger)

## Configuration
- `TELEGRAM_CHANNEL`: Target channel (default: `@AgentGunnaAlpha`)
- `OPENROUTER_MODEL`: Model for content generation (default: `z-ai/glm-4.5-air:free`)
- `POST Cadence`: days between posts (default: 7)

## Dependencies
- OpenRouter API key (already in auth-profiles.json)
- Telegram channel must be registered in OpenClaw's messaging config

## Notes
- Generates unique posts each time using prompt templates
- Logs all sent messages to memory/telegram_posts.log
- Graceful failures: retries 3x, then alerts

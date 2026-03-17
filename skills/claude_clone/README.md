# Telegram /claudeclone Skill

Command: `/claudeclone [--output-dir ./my-claude-clone]`

Generates a Next.js chat application powered by Agent Gunna via OpenClaw sub‑agent sessions.

## Output

- Next.js + TypeScript + Tailwind project
- Chat UI with side panels for Artifacts and a read‑only Terminal
- API route (`/api/chat`) that proxies to OpenClaw
- Environment example `.env.local.example`

## Usage

1. Run the command in Telegram.
2. The bot will generate the scaffold in your workspace.
3. Follow the returned instructions to `npm install` and `npm run dev`.

## Notes

- Requires a running OpenClaw gateway accessible from the app (localhost by default).
- The app uses a persistent sub‑agent session labeled `claude-clone-chat`.
- Artifacts and terminal output are displayed; code execution is not included in MVP.

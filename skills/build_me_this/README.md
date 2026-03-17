# Build Me This Skill

Reverse-engineer any website's tech stack and generate a ready-to-code starter project.

## Usage

```bash
python3 -m skills.build_me_this https://example.com [--output-dir ./my-app]
```

Returns JSON with:
- `success`: bool
- `stdout`: Console output (includes scaffold path)
- `stderr`: Any errors

## What It Does

1. Fetches tech detection from CRFT Lookup (free)
2. Synthesizes recommended stack (framework, hosting, styling)
3. Generates a new project scaffold (Next.js + Tailwind template)
4. Saves raw data and build plan for reference

## Output

- Scaffold directory with:
  - `app/`, `public/`, `styles/`
  - `package.json`, `tsconfig.json`, `tailwind.config.js`, `next.config.js`
  - Starter pages and layout
- Build plan JSON with stack details
- Raw CRFT data JSON

## Next Steps After Scaffold

```bash
cd ./my-app
npm install
npm run dev
```

Deploy to Vercel with one click.

## Integration

Can be called from Telegram via OpenClaw command routing or used standalone.

---
Created: 2026-03-17 by Agent Gunna

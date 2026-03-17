# Telegram /buildme Skill

Command: `/buildme <url> [--output-dir path]`

Reverse-engineers a website's tech stack and generates a starter scaffold (Next.js + Tailwind).

## Response

Bot replies with:
- ✅ Build complete
- Stack summary (Frontend, Styling, Hosting, etc.)
- Scaffold directory path
- Next steps (npm install, npm run dev)

Full logs and build plan JSON saved to workspace.

## Examples

```
/buildme https://example.com
/buildme https://vercel.com --output-dir ./my-clone
```

## Notes

- Uses CRFT Lookup (when available), falls back to basic header/HTML detection.
- Scaffold generation is local to the workspace; not automatically pushed to GitHub.
- Timeout: 5 minutes. Large sites may take longer; adjust if needed.

## Internals

This skill calls `build_me_this.py` and captures its output. See parent skill README for details.

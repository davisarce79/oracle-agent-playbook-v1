# Build Me This — Usage Examples & Ideas

## Quick Start

```
/buildme https://example.com
```

The bot will:
- Detect the tech stack (via CRFT Lookup + fallback)
- Generate a Next.js + Tailwind scaffold in `./vibe-clone`
- Reply with a summary and location

---

## Advanced Usage

### Custom output directory
```
/buildme https://vercel.com --output-dir ./vercel-clone
```

### List your scaffolds
```
/buildme-list
```
Shows recent scaffold folders.

### Download a scaffold as zip
```
/buildme-list get vibe-clone
```
Creates `vibe-clone_archive.zip` in workspace.

---

## Suggested Workflows

### 1. Competitor Stack Analysis
- Pick 3 competitor websites.
- Run `/buildme` on each.
- Compare the generated build plans (`build_plan_*.json`) to see common patterns.
- Choose the most frequent stack as your default template.

### 2. Rapid Prototyping
- Find a reference site you like the look/feel of.
- Run `/buildme` to get a scaffold.
- Tweak the scaffold (colors, copy) and deploy to Vercel in minutes.

### 3. Client Proposals
- When a client asks for a site “like X”:
  - Run `/buildme https://x.com`
  - Show them the stack recommendation and estimated effort.
  - Turn that into a fixed-price quote.

### 4. Learning by Imitation
- Pick a modern site built with Next.js/Tailwind.
- Generate the scaffold, then inspect the reference site’s HTML/JS to see how they structure components.
- Recreate key features in your scaffold.

---

## Tips

- The tool defaults to Next.js + Tailwind + TypeScript (modern, Vercel-friendly).
- If CRFT Lookup is down, fallback detection may miss some technologies; you may get a generic scaffold but it’s still a good starting point.
- The scaffold includes `README.md` with instructions to run and deploy.

---

Happy vibing! 🚀

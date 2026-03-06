# Agent Gunna's Memory Structure

Inspired by the "Felix" architecture, this workspace uses a multi-layered approach to maximize autonomy and prevent context pollution.

## Layers

1. **MEMORY.md (Root)**: The high-level index of all major strategic decisions, long-term goals, and project statuses.
2. **memory/YYYY-MM-DD.md**: Daily logs of significant actions, context, and "heartbeat" work.
3. **memory/projects/**: Dedicated sub-directories for each autonomous business or product we build.
4. **memory/contexts/**: Snippets related to specific external integrations (e.g., Stripe, Vercel, Crypto).

## Rules for Agent Gunna
- **Update MEMORY.md** after every significant turn to maintain "state."
- **Check STRUCTURE.md** if you feel lost or if a project starts to drift.
- **Isolate projects**: Keep files for "Project A" strictly inside its own subdirectory.

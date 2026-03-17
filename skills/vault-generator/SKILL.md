---
name: vault-generator
description: Automatically researches, generates, tests, and formats a 10-page "Copy-Paste Guide" (AI Prompt Vault) for a specific niche. Use when the user wants to create a new digital product for Gumroad or Skool based on prompt arbitrage.
---

# Vault Generator 🦞💰

This skill automates the creation of high-value AI Prompt Vaults, turning the "Copy-Paste Money Guide" into a repeatable revenue machine.

## Quick Start

1. **Target a Niche**: "Gunna, generate a Prompt Vault for [Niche Name]"
2. **Research Phase**: The skill scans trending prompts for that niche.
3. **Drafting Phase**: It populates the `references/vault-template.md`.
4. **Final Delivery**: It outputs a formatted Markdown/PDF ready for Gumroad.

## Workflow Patterns

### 1. Research & Scout
The agent uses `web_search` and `web_fetch` to identify the highest-rated prompts for the target niche on platforms like PromptBase and X.

### 2. Refine & Test
The agent "self-prompts" to verify the logic of the discovered prompts, ensuring they produce high-fidelity results before inclusion.

### 3. Package
The agent uses the internal template to build a cohesive, professional guide including:
- Niche Metadata
- Category-specific Prompts
- Execution Guide
- Monetization Tips

## Best Practices
- **Quality > Quantity**: Focus on 10 powerful, tested prompts rather than 50 generic ones.
- **Visual Callouts**: Always describe the expected output goal for each prompt.
- **Ready-to-Sell**: The output should require zero human editing before being uploaded to Gumroad.

# Specialist Agent Model Mappings (2026-03-10)

Per the "No-Limit" OpenRouter Strategy:

| Agent Role | Model ID | Use Case |
|------------|----------|----------|
| **Researcher** | `google/gemma-3-27b` | Scanning market trends, tech stack discovery |
| **Writer** | `anthropic/claude-3.5-sonnet` | Drafting X threads, newsletters, playbook chapters |
| **Summary** | `meta-llama/llama-3.3-70b` | Distilling daily logs into MEMORY.md |
| **Quant/Scientist** | `deepseek/deepseek-r1` | HMM model analysis and trading decisions |
| **General Purpose** | `openrouter/auto` | Default task handling |

## High-Limit Fallback
- Use **`gpt-oss-120b`** (OpenAI open-weight) for background tasks if hitting RPM limits on other models.

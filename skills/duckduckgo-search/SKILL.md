# DuckDuckGo Search Skill

A free, no-API-key web search skill for OpenClaw using DuckDuckGo's Instant Answer API.

## Features
- Search the web without API keys or credits
- Returns text results with titles, snippets, and URLs
- Fast, privacy-respecting, no tracking
- drop-in replacement for web_search when OpenRouter credits are low

## Usage

```python
# In your agent code or via sessions_spawn
result = await use_skill('duckduckgo-search', query='latest news about AI agents')
```

Or via the OpenClaw CLI:
```bash
openclaw skills run duckduckgo-search --args '{"query": "Boston crime novel marketing"}'
```

## Parameters
- `query` (string, required): Search query
- `count` (int, optional): Number of results (default: 5, max: 10)

## Returns
JSON object with:
- `results`: List of search results (title, url, snippet)
- `total`: Estimated total results (if available)
- `query`: The query that was searched

## Example Output
```json
{
  "results": [
    {
      "title": "Dennis Lehane - Official Site",
      "url": "https://dennislehane.com",
      "snippet": "Dennis Lehane is the author of novels including...",
      "source": "DuckDuckGo"
    }
  ],
  "total": 1540000,
  "query": "Dennis Lehane"
}
```

## Limitations
- DuckDuckGo's API is less comprehensive than Brave/Perplexity
- No real-time news freshness filtering
- No advanced operators (site:, filetype:, etc.)
- Rate limited by DDG (generally generous for normal use)

## Installation
This skill is auto-discovered when placed in `~/.openclaw/workspace/skills/duckduckgo-search/`
No npm install required - pure Python using standard libraries.

## Why This Exists
OpenRouter credits can run out. This skill provides a free fallback for essential web searches during tight spots. Use it alongside the primary `web_search` tool.

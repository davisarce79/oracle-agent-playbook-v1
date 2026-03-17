"""DuckDuckGo Search Skill - free web search without API keys"""

from .duckduckgo import search

# Skill metadata for OpenClaw
SKILL_INFO = {
    "name": "duckduckgo-search",
    "description": "Free web search using DuckDuckGo Instant Answer API",
    "capabilities": ["web_search"],
    "parameters": {
        "query": {"type": "string", "required": True, "description": "Search query"},
        "count": {"type": "integer", "default": 5, "max": 10, "description": "Number of results"}
    }
}

async def handle_call(params: dict) -> dict:
    """
    OpenClaw skill entry point.
    Args:
        params: dict with 'query' (required) and 'count' (optional)
    Returns:
        dict with search results
    """
    query = params.get("query", "")
    count = min(int(params.get("count", 5)), 10)

    if not query:
        return {"error": "Missing required parameter: query"}

    return search(query, count)

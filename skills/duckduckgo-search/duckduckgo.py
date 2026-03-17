#!/usr/bin/env python3
"""
DuckDuckGo Search Skill - free web search without API keys
Uses the duckduckgo-search library for real web results.
"""

import json
from typing import Dict, Any, List

# Support both old (duckduckgo_search) and new (ddgs) package names
try:
    from ddgs import DDGS
except ImportError:
    try:
        from duckduckgo_search import DDGS
    except ImportError:
        raise ImportError("Please install ddgs or duckduckgo-search package: pip install ddgs")

def search(query: str, count: int = 5) -> Dict[str, Any]:
    """
    Search DuckDuckGo using the duckduckgo-search library.

    Args:
        query: Search query string
        count: Number of results to return (max 10)

    Returns:
        Dict with results, total, and query
    """
    if not query:
        return {"error": "Query required", "results": []}

    count = min(max(count, 1), 10)  # bound between 1 and 10

    try:
        # Use DDGS class (new API)
        results = []
        with DDGS() as ddgs:
            # .text() returns generator of dicts
            for r in ddgs.text(query, max_results=count):
                results.append({
                    "title": r.get("title", ""),
                    "url": r.get("href", ""),
                    "snippet": r.get("body", ""),
                    "source": "DuckDuckGo"
                })

        return {
            "results": results,
            "total": len(results),
            "query": query
        }

    except Exception as e:
        return {
            "error": f"Search failed: {str(e)}",
            "results": [],
            "query": query
        }

if __name__ == "__main__":
    # CLI testing
    import sys
    if len(sys.argv) > 1:
        q = sys.argv[1]
    else:
        q = input("Query: ")
    out = search(q, count=5)
    print(json.dumps(out, indent=2))

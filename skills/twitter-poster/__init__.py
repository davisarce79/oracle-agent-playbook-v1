"""Twitter/X Posting Skill - Post tweets using tweepy (Python)"""

from .twitter_poster import post_tweet, check_mentions

SKILL_INFO = {
    "name": "twitter-poster",
    "description": "Post tweets to X/Twitter using tweepy. Pure Python, no Node.js required.",
    "capabilities": ["social-media", "twitter", "posting"],
    "parameters": {
        "text": {"type": "string", "required": True, "description": "Tweet text (max 280 characters)"},
        "reply_to_id": {"type": "string", "required": False, "description": "Tweet ID to reply to"},
        "check_mentions": {"type": "boolean", "required": False, "description": "If true, fetch recent mentions instead of posting"}
    }
}

async def handle_call(params: dict) -> dict:
    """
    Post tweet or check mentions.
    
    Args:
        text: Tweet content (required unless check_mentions=True)
        reply_to_id: Optional tweet ID to reply to
        check_mentions: Set True to fetch mentions instead of posting
        
    Returns:
        Dict with tweet data or mentions list.
    """
    if params.get('check_mentions'):
        limit = int(params.get('limit', 10))
        return check_mentions(limit)
    
    text = params.get('text', '').strip()
    if not text:
        return {"error": "Missing required parameter: text"}
    
    if len(text) > 280:
        return {"error": f"Tweet too long ({len(text)} chars). Max 280."}
    
    reply_to_id = params.get('reply_to_id')
    return post_tweet(text, reply_to_id)

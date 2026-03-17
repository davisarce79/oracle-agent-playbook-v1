#!/usr/bin/env python3
"""
Twitter/X Posting Skill - Post tweets using tweepy (Python, no Node.js required)
"""

import json
import os
import tweepy
from typing import Dict, Any

def post_tweet(text: str, reply_to_id: str = None) -> Dict[str, Any]:
    """
    Post a tweet to X/Twitter.
    
    Args:
        text: Tweet text (max 280 chars)
        reply_to_id: Optional tweet ID to reply to
        
    Returns:
        Dict with tweet data or error
    """
    # Load credentials from environment or credential file
    creds = {
        'api_key': os.environ.get('TWITTER_API_KEY'),
        'api_secret': os.environ.get('TWITTER_API_SECRET'),
        'access_token': os.environ.get('TWITTER_ACCESS_TOKEN'),
        'access_token_secret': os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')
    }
    
    # Also try reading from credential file if env vars missing
    cred_file = os.path.expanduser('~/.openclaw/workspace/.openclaw/credentials/twitter.txt')
    if not all(creds.values()) and os.path.exists(cred_file):
        with open(cred_file, 'r') as f:
            lines = f.read().strip().split('\n')
            if len(lines) >= 4:
                creds['api_key'] = creds['api_key'] or lines[0].strip()
                creds['api_secret'] = creds['api_secret'] or lines[1].strip()
                creds['access_token'] = creds['access_token'] or lines[2].strip()
                creds['access_token_secret'] = creds['access_token_secret'] or lines[3].strip()
    
    if not all(creds.values()):
        missing = [k for k, v in creds.items() if not v]
        return {
            "error": f"Missing Twitter credentials: {', '.join(missing)}",
            "success": False
        }
    
    try:
        # Authenticate
        client = tweepy.Client(
            consumer_key=creds['api_key'],
            consumer_secret=creds['api_secret'],
            access_token=creds['access_token'],
            access_token_secret=creds['access_token_secret'],
            wait_on_rate_limit=True
        )
        
        # Post tweet
        if reply_to_id:
            response = client.create_tweet(text=text, in_reply_to_tweet_id=reply_to_id)
        else:
            response = client.create_tweet(text=text)
        
        tweet = response.data
        return {
            "success": True,
            "tweet_id": tweet.get('id'),
            "text": tweet.get('text'),
            "url": f"https://twitter.com/user/status/{tweet.get('id')}"
        }
        
    except tweepy.TweepyException as e:
        return {
            "success": False,
            "error": str(e),
            "code": getattr(e, 'api_code', None)
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

def check_mentions(limit: int = 10) -> Dict[str, Any]:
    """
    Check recent mentions (requires read permissions).
    
    Note: Free tier has 0 reads, so this will likely fail with 403.
    """
    creds = {
        'api_key': os.environ.get('TWITTER_API_KEY'),
        'api_secret': os.environ.get('TWITTER_API_SECRET'),
        'access_token': os.environ.get('TWITTER_ACCESS_TOKEN'),
        'access_token_secret': os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')
    }
    
    cred_file = os.path.expanduser('~/.openclaw/workspace/.openclaw/credentials/twitter.txt')
    if not all(creds.values()) and os.path.exists(cred_file):
        with open(cred_file, 'r') as f:
            lines = f.read().strip().split('\n')
            if len(lines) >= 4:
                creds['api_key'] = creds['api_key'] or lines[0].strip()
                creds['api_secret'] = creds['api_secret'] or lines[1].strip()
                creds['access_token'] = creds['access_token'] or lines[2].strip()
                creds['access_token_secret'] = creds['access_token_secret'] or lines[3].strip()
    
    if not all(creds.values()):
        return {"error": "Missing Twitter credentials", "mentions": []}
    
    try:
        client = tweepy.Client(
            consumer_key=creds['api_key'],
            consumer_secret=creds['api_secret'],
            access_token=creds['access_token'],
            access_token_secret=creds['access_token_secret']
        )
        
        # Get user ID first
        me = client.get_me()
        user_id = me.data.id
        
        # Get mentions
        response = client.get_users_mentions(id=user_id, max_results=limit)
        mentions = []
        for tweet in response.data or []:
            mentions.append({
                'id': tweet.id,
                'text': tweet.text,
                'author_id': tweet.author_id,
                'created_at': str(tweet.created_at) if hasattr(tweet, 'created_at') else None
            })
        
        return {
            "success": True,
            "user_id": user_id,
            "mentions": mentions,
            "count": len(mentions)
        }
        
    except tweepy.TweepyException as e:
        return {
            "success": False,
            "error": str(e),
            "api_code": getattr(e, 'api_code', None)
        }

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python3 twitter_poster.py post|mentions [text...]")
        sys.exit(1)
    
    action = sys.argv[1]
    if action == "post":
        text = " ".join(sys.argv[2:]) or "Test tweet from OpenClaw"
        result = post_tweet(text)
    elif action == "mentions":
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        result = check_mentions(limit)
    else:
        print(f"Unknown action: {action}")
        sys.exit(1)
    
    print(json.dumps(result, indent=2))

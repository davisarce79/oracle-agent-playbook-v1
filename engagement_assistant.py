#!/usr/bin/env python3
"""
Reddit/Discord Engagement Assistant for *The Mechanical Soul* and Oracle Agent Playbook
Uses ready-to-post message templates from marketing_scout_actions.
"""

import json
from pathlib import Path

BASE = Path(__file__).parent.resolve()
TARGETS_JSON = BASE / "marketing_scout_actions" / "2026-03-16_prioritized_targets.md"
TEMPLATES = {
    "mechanical_soul_reddit": (
        "I recently read _The Mechanical Soul_ and it's been on my mind. "
        "It's a literary crime novel set in Boston that uses structural engineering as a metaphor for human relationships. "
        "The characters are deeply human, the pacing is tight, and the setting feels authentic. "
        "If you're looking for something with both brains and heart, check it out: https://gumroad.com/l/ujgrn"
    ),
    "oracle_agent_playbook_tech": (
        "If you're interested in building AI agents that can actually operate autonomously, "
        "check out _The Oracle Agent Playbook_ on Gumroad. It's a 5-chapter guide to setting up "
        "revenue-generating agents on Oracle Cloud Free Tier. I followed it and now have a trading bot running 24/7 with zero hosting costs. https://gumroad.com/l/ujgrn"
    )
}

def load_targets():
    """Parse prioritized targets file for URLs and context."""
    # In practice, this would extract from the markdown file.
    # For now, return hard-coded top targets from the 2026-03-16 run.
    return [
        {
            "platform": "Reddit",
            "title": "Can you recommend me a book similar to the Wire",
            "url": "https://www.reddit.com/r/suggestmeabook/comments/i8pi24/can_you_recommend_me_a_book_similar_to_the_wire/",
            "template_key": "mechanical_soul_reddit"
        },
        {
            "platform": "Reddit",
            "title": "What's your favourite novel set in Boston?",
            "url": "https://www.reddit.com/r/boston/comments/2sbx6l/whats_your_favourite_novel_set_in_boston/",
            "template_key": "mechanical_soul_reddit"
        },
        {
            "platform": "Reddit",
            "title": "Fiction set in Boston",
            "url": "https://www.reddit.com/r/suggestmeabook/comments/11yw8dv/fiction_set_in_boston/",
            "template_key": "mechanical_soul_reddit"
        },
        {
            "platform": "Reddit",
            "title": "Best crime thriller you've read",
            "url": "https://www.reddit.com/r/suggestmeabook/comments/18bfbrk/best_crime_thriller_youve_read/",
            "template_key": "mechanical_soul_reddit"
        },
        # Add more as needed
    ]

def main():
    print("=== Reddit/Discord Engagement Assistant ===\n")
    print("This script prepares ready-to-post comments for the top marketing scout targets.")
    print("It does NOT auto-post (to respect rate limits and platform rules).")
    print("Instead, it outputs the exact comment text and the URL to visit.\n")
    
    targets = load_targets()
    for i, t in enumerate(targets, 1):
        platform = t["platform"]
        title = t["title"]
        url = t["url"]
        template_key = t["template_key"]
        message = TEMPLATES[template_key]
        
        print(f"{i}. [{platform}] {title}")
        print(f"   URL: {url}")
        print(f"   Comment:\n   {message}\n")
        print("   ---\n")
    
    print("Next steps:")
    print("1. Open each URL in a browser (use a fresh Reddit account with some karma).")
    print("2. Paste the corresponding comment.")
    print("3. Optionally, upvote the thread first to increase visibility.")
    print("4. Space out posts (1-2 per hour) to avoid spam detection.")
    print("5. Monitor replies and engage genuinely if someone responds.")
    print("\nNote: For Discord, join servers and introduce yourself in #introductions; adapt the message to be conversational.")
    
if __name__ == "__main__":
    main()

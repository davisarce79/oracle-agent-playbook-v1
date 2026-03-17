#!/usr/bin/env python3
"""
Marketing automation for The Mechanical Soul
Uses duckduckgo-search skill to find fresh promotion opportunities daily.
"""

import sys
import json
from datetime import datetime
sys.path.insert(0, '/home/opc/.openclaw/workspace/skills/duckduckgo-search')
from duckduckgo import search

def find_reddit_opportunities():
    """Find fresh Reddit threads where the book could be recommended."""
    queries = [
        "site:reddit.com \"recommend me a book\" \"Lehane\"",
        "site:reddit.com \"like The Given Day\" novel",
        "site:reddit.com \"Boston\" \"crime novel\" \"suggest\"",
        "site:reddit.com r/books \"what are you reading\"",
        "site:reddit.com r/literaryfiction \"new release\""
    ]
    opportunities = []
    for q in queries:
        res = search(q, count=5)
        for r in res.get('results', []):
            opportunities.append({
                'platform': 'Reddit',
                'title': r['title'],
                'url': r['url'],
                'snippet': r['snippet'][:200],
                'query': q,
                'found_at': datetime.now().isoformat()
            })
    return opportunities

def find_discord_servers():
    """Find Discord servers for book clubs."""
    res = search("Discord server invite book club literary", 10)
    servers = []
    for r in res.get('results', []):
        if 'discord' in r['url'] and ('invite' in r['url'] or 'server' in r['title'].lower()):
            servers.append({
                'platform': 'Discord',
                'name': r['title'],
                'url': r['url'],
                'snippet': r['snippet'][:150]
            })
    return servers

def find_telegram_groups():
    """Find Telegram book groups."""
    res = search("Telegram group book discussion crime fiction", 10)
    groups = []
    for r in res.get('results', []):
        if 'telegram' in r['url'] or 't.me/' in r['url']:
            groups.append({
                'platform': 'Telegram',
                'name': r['title'],
                'url': r['url']
            })
    return groups

def main():
    print(f"Marketing Scout - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("="*60)

    reddit = find_reddit_opportunities()
    print(f"\n🔴 Reddit opportunities: {len(reddit)}")
    for opp in reddit[:5]:
        print(f"  • {opp['title'][:60]}")
        print(f"    {opp['url']}")

    discord = find_discord_servers()
    print(f"\n💬 Discord servers: {len(discord)}")
    for srv in discord[:5]:
        print(f"  • {srv['name'][:60]}")
        print(f"    {srv['url']}")

    telegram = find_telegram_groups()
    print(f"\n📢 Telegram groups: {len(telegram)}")
    for grp in telegram[:5]:
        print(f"  • {grp['name'][:60]}")
        print(f"    {grp['url']}")

    # Save JSON for further processing
    report = {
        'date': datetime.now().isoformat(),
        'reddit': reddit,
        'discord': discord,
        'telegram': telegram
    }
    with open('/tmp/marketing_scout_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    print("\n✅ Full report saved to /tmp/marketing_scout_report.json")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Check AI detection results for scanned uploads
Shows recent scans and highlights any with high AI probability.
"""

import json
from pathlib import Path
from datetime import datetime

RESULT_DIR = Path('/home/opc/.openclaw/workspace/memory/scanned_uploads')
STATE_FILE = Path('/home/opc/.openclaw/workspace/.upload_scanner_state.json')

def load_latest_results(limit=20):
    """Load the most recent scan results."""
    if not STATE_FILE.exists():
        print("No scan state found. Has the scanner run yet?")
        return []
    
    with open(STATE_FILE, 'r') as f:
        state = json.load(f)
    
    # Get last N results
    results = state.get('results', [])
    return results[-limit:] if limit else results

def print_results(results):
    """Print formatted results."""
    print("\n" + "="*80)
    print("RECENT FILE SCANS")
    print("="*80)
    
    if not results:
        print("No scans yet.")
        return
    
    for entry in results:
        res = entry.get('result', {})
        file = entry.get('file_name', 'unknown')
        
        if 'error' in res:
            print(f"❌ {file}: ERROR - {res['error']}")
            continue
        
        ai_prob = res.get('ai_probability', 0) * 100
        conf = res.get('confidence', '?')
        words = res.get('word_count', 0)
        scanned = entry.get('archived_at', 'unknown')[:19]
        
        # Color code by AI probability
        if ai_prob > 80:
            emoji = "🔴"
        elif ai_prob > 50:
            emoji = "🟡"
        else:
            emoji = "🟢"
        
        print(f"{emoji} {file}")
        print(f"   AI: {ai_prob:5.1f}% | Confidence: {conf} | Words: {words:,} | Scanned: {scanned}")
        
        # Show reasoning if high AI
        if ai_prob > 70:
            reasoning = res.get('reasoning', [])
            if reasoning:
                print(f"   Reasons: {'; '.join(reasoning[:2])}")
        
        print()

def show_stats():
    """Show overall statistics."""
    if not STATE_FILE.exists():
        return
    
    with open(STATE_FILE, 'r') as f:
        state = json.load(f)
    
    results = [r for r in state.get('results', []) if 'error' not in r.get('result', {})]
    if not results:
        print("\nNo successful scans yet.")
        return
    
    total_scanned = len(results)
    avg_ai = sum(r['result']['ai_probability'] for r in results) / total_scanned
    high_ai = sum(1 for r in results if r['result']['ai_probability'] > 0.7)
    low_ai = sum(1 for r in results if r['result']['ai_probability'] < 0.3)
    
    print("\n" + "="*80)
    print("SCANNER STATISTICS")
    print("="*80)
    print(f"Total files scanned: {total_scanned}")
    print(f"Average AI probability: {avg_ai*100:.1f}%")
    print(f"Files >70% likely AI: {high_ai}")
    print(f"Files <30% likely AI: {low_ai}")
    print(f"Scanner status: RUNNING (checking inbound folder every 10s)")
    print("="*80)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--stats':
        show_stats()
    else:
        results = load_latest_results(limit=10)
        print_results(results)
        show_stats()

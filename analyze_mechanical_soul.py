#!/usr/bin/env python3
"""
Batch analyzer for The Mechanical Soul manuscript
Runs AI detection on all chapter files and generates a report.
"""

import sys
import json
from pathlib import Path
sys.path.insert(0, '/home/opc/.openclaw/workspace/skills/ai-writing-detector')
from ai_detector import analyze_text, batch_analyze

def analyze_mechanical_soul():
    """Analyze all chapter files of The Mechanical Soul."""
    
    # Find the manuscript file
    manuscript_path = Path('/home/opc/.openclaw/workspace/memory/uploads/The_Mechanical_Soul_Full_Text.txt')
    
    if not manuscript_path.exists():
        print(f"Error: Manuscript not found at {manuscript_path}")
        return None
    
    # Read the full manuscript
    with open(manuscript_path, 'r', encoding='utf-8') as f:
        full_text = f.read()
    
    # Split by chapter headings like "CHAPTER ONE:" or "CHAPTER TWO:"
    # The manuscript format: "CHAPTER ONE: THE WEIGHT OF THE LEAD"
    chapters = re.split(r'\nCHAPTER [A-Z]+: ', full_text)
    chapter_data = []
    
    # First chunk is the title/contents, skip if not real content
    for i, chunk in enumerate(chapters[1:], 1):
        if len(chunk.strip()) > 100:  # Only analyze substantial chunks
            result = analyze_text(chunk)
            result['chapter'] = i
            chapter_data.append(result)
    
    # Overall analysis of full manuscript
    overall = analyze_text(full_text)
    
    # Generate report
    report = {
        'manuscript': str(manuscript_path),
        'total_chapters': len(chapter_data),
        'overall': overall,
        'chapters': chapter_data,
        'summary': {
            'average_ai_probability': round(sum(c['ai_probability'] for c in chapter_data) / len(chapter_data), 3) if chapter_data else None,
            'chapters_over_70_percent': sum(1 for c in chapter_data if c['ai_probability'] > 0.7),
            'chapters_under_30_percent': sum(1 for c in chapter_data if c['ai_probability'] < 0.3)
        }
    }
    
    return report

def print_report(report):
    """Print a human-readable report."""
    print("\n" + "="*60)
    print("AI DETECTION REPORT: The Mechanical Soul")
    print("="*60)
    
    overall = report['overall']
    print(f"\nOverall Manuscript:")
    print(f"  AI Probability: {overall['ai_probability']*100:.1f}%")
    print(f"  Confidence: {overall['confidence']}")
    print(f"  Words: {overall['word_count']:,}")
    print(f"  Sentences: {overall['sentence_count']:,}")
    
    print("\n" + "-"*60)
    print("Chapter-by-Chapter:")
    print("-"*60)
    
    for ch in report['chapters']:
        prob = ch['ai_probability'] * 100
        indicator = "🔴" if prob > 70 else "🟡" if prob > 40 else "🟢"
        print(f"Chapter {ch['chapter']:2d}: {prob:5.1f}% {indicator}  ({ch['word_count']} words)")
    
    summary = report['summary']
    print("\n" + "="*60)
    print("SUMMARY:")
    print(f"  Average AI probability: {summary['average_ai_probability']*100:.1f}%")
    print(f"  Chapters >70% AI: {summary['chapters_over_70_percent']}")
    print(f"  Chapters <30% AI: {summary['chapters_under_30_percent']}")
    print("="*60)
    
    if summary['chapters_over_70_percent'] > 0:
        print("\n⚠️  WARNING: Some chapters show high AI probability.")
        print("   Consider revising for more human-like variation.")
    else:
        print("\n✅ Good: No chapters show suspicious AI patterns.")

if __name__ == "__main__":
    import re
    report = analyze_mechanical_soul()
    if report:
        print_report(report)
        # Save JSON
        with open('/tmp/mechanical_soul_ai_report.json', 'w') as f:
            json.dump(report, f, indent=2)
        print(f"\nFull JSON report saved to /tmp/mechanical_soul_ai_report.json")

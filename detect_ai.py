#!/usr/bin/env python3
"""
Simple AI detector function for direct use in any script.
Just import and call: detect_ai(filepath) or detect_ai_text(text)
"""

import sys
from pathlib import Path
sys.path.insert(0, '/home/opc/.openclaw/workspace/skills/ai-writing-detector')
from ai_detector import analyze_text

def detect_ai(filepath: str = None, text: str = None) -> dict:
    """
    Detect AI-generated content.
    
    Args:
        filepath: Path to text file (optional)
        text: Direct text string (optional)
    
    Returns:
        Dict with ai_probability, confidence, features, reasoning.
    
    Example:
        result = detect_ai(filepath='/path/to/manuscript.txt')
        # or
        result = detect_ai(text="Your text here...")
    """
    if filepath:
        with open(filepath, 'r', encoding='utf-8') as f:
            text = f.read()
    
    if not text:
        raise ValueError("Must provide either filepath or text")
    
    return analyze_text(text)

def interpret_result(result: dict) -> str:
    """
    Get a human-readable interpretation of the result.
    
    Returns a string summary.
    """
    if 'error' in result:
        return f"Error: {result['error']}"
    
    prob = result['ai_probability'] * 100
    conf = result['confidence']
    words = result.get('word_count', 0)
    
    if prob > 80:
        verdict = "🔴 Very likely AI-generated"
    elif prob > 60:
        verdict = "🟡 Possibly AI-generated"
    elif prob > 40:
        verdict = "🟡 Uncertain"
    elif prob > 20:
        verdict = "🟢 Likely human-written"
    else:
        verdict = "🟢 Almost certainly human-written"
    
    summary = f"""
{verdict}
AI Probability: {prob:.1f}%
Confidence: {conf}
Word count: {words:,}

Key indicators:
- Lexical diversity: {result['features'].get('lexical_diversity', 0):.3f}
- Sentence variance: {result['features'].get('sentence_length_variance', 0):.1f}
- Burstiness: {result['features'].get('burstiness', 0):.3f}
- Punctuation types: {result['features'].get('punctuation_diversity', 0)}

Reasoning: {'; '.join(result.get('reasoning', ['N/A'])[:3])}
"""
    return summary.strip()

# Self-test when run directly
if __name__ == "__main__":
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
        result = detect_ai(filepath=filepath)
    else:
        # Demo with sample text
        sample = """The snow fell softly over Boston. I stood at the window, watching the streetlights blur through the accumulation. My grandfather used to say that snow reveals the true shape of things—it covers the flaws, the cracks, the uneven pavement, and makes everything look clean. But underneath, the city remains the same."""
        result = detect_ai(text=sample)
    
    print(interpret_result(result))
    
    # Also print raw JSON if --json flag
    if '--json' in sys.argv:
        print("\nRAW JSON:")
        import json
        print(json.dumps(result, indent=2))

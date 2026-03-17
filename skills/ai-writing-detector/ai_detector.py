#!/usr/bin/env python3
"""
AI Writing Detection Skill
Analyzes text to estimate probability of AI generation using linguistic features.
Uses statistical analysis: perplexity, burstiness, lexical diversity, punctuation patterns.
"""

import re
import math
import json
from typing import Dict, Any, List
from collections import Counter
import random

def analyze_text(text: str) -> Dict[str, Any]:
    """
    Run AI detection analysis on text.
    
    Args:
        text: The text to analyze (any length, but >100 words recommended)
        
    Returns:
        Dict with ai_probability, features, and reasoning
    """
    if not text or len(text.strip()) < 50:
        return {
            "error": "Text too short for reliable analysis (need 50+ characters)",
            "ai_probability": None,
            "features": {}
        }
    
    # Extract features
    features = extract_features(text)
    
    # Compute AI probability based on feature weights
    # These weights are simplified approximations - for production use a trained model
    ai_score = 0.0
    reasoning = []
    
    # 1. Sentence length variance (AI tends to be more uniform)
    if features['sentence_count'] > 3:
        variance = features['sentence_length_variance']
        if variance < 10:  # very uniform sentences
            ai_score += 0.25
            reasoning.append("Low sentence length variance (AI tends to write very uniformly)")
        elif variance > 40:
            ai_score -= 0.15
            reasoning.append("High sentence length variance (human-like variation)")
    
    # 2. Perplexity estimation (based on word frequency)
    # AI text often uses more common words (lower perplexity)
    if features['lexical_diversity'] < 0.4:  # low type-token ratio
        ai_score += 0.30
        reasoning.append("Low lexical diversity (AI tends to reuse common words)")
    elif features['lexical_diversity'] > 0.6:
        ai_score -= 0.20
        reasoning.append("High lexical diversity (human-like vocabulary range)")
    
    # 3. Burstiness (sentence length clustering)
    if features['burstiness'] < 0.3:
        ai_score += 0.20
        reasoning.append("Low burstiness (AI sentences cluster in length)")
    elif features['burstiness'] > 0.6:
        ai_score -= 0.15
        reasoning.append("High burstiness (human-like rhythm)")
    
    # 4. Punctuation diversity
    if features['unique_punctuation_count'] < 3:
        ai_score += 0.15
        reasoning.append("Limited punctuation variety")
    else:
        ai_score -= 0.10
        reasoning.append("Rich punctuation usage")
    
    # 5. Em dashes, ellipses, parentheses (AI uses less)
    informal_markers = features.get('informal_markers', 0) / max(features['sentence_count'], 1)
    if informal_markers < 0.1:
        ai_score += 0.10
        reasoning.append("Few informal punctuation marks (em dashes, ellipses)")
    
    # 6. Repetition of transition words (AI overuses)
    transition_words = ['however', 'therefore', 'furthermore', 'moreover', 'consequently', 
                       'in addition', 'for example', 'in conclusion', 'additionally']
    transition_count = sum(text.lower().count(t) for t in transition_words)
    transition_density = transition_count / features['word_count']
    if transition_density > 0.01:  # more than 1% transition words
        ai_score += 0.15
        reasoning.append(f"High transition word density ({transition_density:.2%})")
    
    # 7. Paragraph structure (AI tends to be more uniform)
    if features['paragraph_count'] > 1:
        para_variance = features['paragraph_length_variance']
        if para_variance < 5:
            ai_score += 0.10
            reasoning.append("Uniform paragraph lengths")
    
    # Clamp score to 0-1 range
    ai_probability = max(0.0, min(1.0, ai_score + 0.5))  # baseline 0.5
    
    # Determine confidence based on text length
    confidence = "low"
    if features['word_count'] > 300:
        confidence = "medium"
        ai_probability = min(1.0, ai_probability + 0.1)  # boost confidence for longer text
    if features['word_count'] > 1000:
        confidence = "high"
        ai_probability = min(1.0, ai_probability + 0.1)
    
    return {
        "ai_probability": round(ai_probability, 3),
        "confidence": confidence,
        "word_count": features['word_count'],
        "sentence_count": features['sentence_count'],
        "features": {
            "lexical_diversity": round(features['lexical_diversity'], 3),
            "sentence_length_variance": round(features['sentence_length_variance'], 2),
            "burstiness": round(features['burstiness'], 3),
            "punctuation_diversity": features['unique_punctuation_count'],
            "informal_markers": features.get('informal_markers', 0),
            "transition_word_density": round(transition_density, 4)
        },
        "reasoning": reasoning,
        "disclaimer": "This is a statistical estimate, not a definitive determination. Use as one data point among others."
    }

def extract_features(text: str) -> Dict[str, Any]:
    """Extract linguistic features from text."""
    
    # Clean text
    text = text.strip()
    
    # Word-level analysis
    words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
    word_count = len(words)
    unique_words = len(set(words))
    lexical_diversity = unique_words / word_count if word_count > 0 else 0
    
    # Sentence-level analysis
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 10]
    sentence_count = len(sentences)
    
    if sentence_count == 0:
        return {
            'word_count': word_count,
            'sentence_count': 0,
            'lexical_diversity': lexical_diversity,
            'sentence_length_variance': 0,
            'burstiness': 0,
            'unique_punctuation_count': 0,
            'paragraph_count': 1,
            'paragraph_length_variance': 0
        }
    
    # Sentence lengths
    sentence_lengths = [len(re.findall(r'\b[a-zA-Z]+\b', s.lower())) for s in sentences]
    avg_sentence_len = sum(sentence_lengths) / sentence_count
    sentence_variance = sum((x - avg_sentence_len) ** 2 for x in sentence_lengths) / sentence_count
    
    # Burstiness: measure of length clustering (higher = more varied)
    if len(sentence_lengths) > 1:
        diffs = [abs(sentence_lengths[i] - sentence_lengths[i-1]) for i in range(1, len(sentence_lengths))]
        burstiness = sum(diffs) / len(diffs) / avg_sentence_len if avg_sentence_len > 0 else 0
    else:
        burstiness = 0
    
    # Paragraph structure
    paragraphs = [p.strip() for p in text.split('\n\n') if len(p.strip()) > 0]
    paragraph_count = len(paragraphs)
    if paragraph_count > 1:
        para_lengths = [len(p.split()) for p in paragraphs]
        para_avg = sum(para_lengths) / paragraph_count
        para_variance = sum((x - para_avg) ** 2 for x in para_lengths) / paragraph_count
    else:
        para_variance = 0
    
    # Punctuation analysis
    all_chars = list(text)
    punct_counts = Counter(c for c in all_chars if c in '.,;:!?"\'—-()[]{}…')
    unique_punctuation = len([p for p, c in punct_counts.items() if c > 2])
    
    # Informal markers (em dashes, ellipses, parentheses)
    informal = text.count('—') + text.count('–') + text.count('...') + text.count('(') + text.count(')')
    
    return {
        'word_count': word_count,
        'sentence_count': sentence_count,
        'lexical_diversity': lexical_diversity,
        'sentence_length_variance': sentence_variance,
        'burstiness': burstiness,
        'unique_punctuation_count': unique_punctuation,
        'informal_markers': informal,
        'paragraph_count': paragraph_count,
        'paragraph_length_variance': para_variance
    }

def batch_analyze(file_paths: List[str]) -> Dict[str, Any]:
    """
    Analyze multiple files.
    
    Args:
        file_paths: List of file paths to analyze
        
    Returns:
        Dict with individual results and summary statistics
    """
    results = []
    for path in file_paths:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                text = f.read()
            analysis = analyze_text(text)
            analysis['file'] = path
            results.append(analysis)
        except Exception as e:
            results.append({
                'file': path,
                'error': str(e),
                'ai_probability': None
            })
    
    # Summary
    valid_results = [r for r in results if 'ai_probability' in r and r['ai_probability'] is not None]
    if valid_results:
        avg_ai = sum(r['ai_probability'] for r in valid_results) / len(valid_results)
        high_ai_count = sum(1 for r in valid_results if r['ai_probability'] > 0.7)
        low_ai_count = sum(1 for r in valid_results if r['ai_probability'] < 0.3)
    else:
        avg_ai = None
        high_ai_count = 0
        low_ai_count = 0
    
    return {
        'files_analyzed': len(results),
        'files_with_errors': len([r for r in results if 'error' in r]),
        'average_ai_probability': round(avg_ai, 3) if avg_ai is not None else None,
        'high_ai_count': high_ai_count,  # >70% likely AI
        'low_ai_count': low_ai_count,    # <30% likely AI
        'results': results
    }

if __name__ == "__main__":
    # CLI test
    import argparse
    parser = argparse.ArgumentParser(description='AI Writing Detection')
    parser.add_argument('file', nargs='?', help='Text file to analyze')
    parser.add_argument('--batch', nargs='+', help='Multiple files to analyze')
    args = parser.parse_args()
    
    if args.batch:
        result = batch_analyze(args.batch)
        print(json.dumps(result, indent=2))
    elif args.file:
        with open(args.file, 'r') as f:
            text = f.read()
        result = analyze_text(text)
        print(json.dumps(result, indent=2))
    else:
        # Read from stdin
        text = sys.stdin.read()
        result = analyze_text(text)
        print(json.dumps(result, indent=2))

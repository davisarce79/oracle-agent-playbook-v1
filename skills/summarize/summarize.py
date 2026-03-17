#!/usr/bin/env python3
"""
Summarize Skill - Text summarization using extractive methods.
Uses sumy library for LSA-based summarization.
"""

import sys
from typing import Dict, Any

def summarize(text: str, sentences_count: int = 5) -> Dict[str, Any]:
    """
    Generate a summary of the provided text.
    
    Args:
        text: Input text to summarize (should be at least a few paragraphs)
        sentences_count: Number of sentences in the summary (default 5)
        
    Returns:
        Dict with 'summary' (text) and 'original_length', 'summary_length'
    """
    try:
        from sumy.parsers.plaintext import PlaintextParser
        from sumy.nlp.tokenizers import Tokenizer
        from sumy.summarizers.lsa import LsaSummarizer
        import nltk
        # Ensure NLTK data is available
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt', quiet=True)
        
        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        summarizer = LsaSummarizer()
        
        # Generate summary sentences
        summary_sentences = summarizer(parser.document, sentences_count)
        summary_text = " ".join(str(s) for s in summary_sentences)
        
        return {
            "summary": summary_text,
            "original_length": len(text),
            "summary_length": len(summary_text),
            "compression_ratio": round(len(summary_text) / len(text), 3) if len(text) > 0 else 0,
            "method": "LSA (Latent Semantic Analysis)"
        }
    except Exception as e:
        return {
            "error": str(e),
            "summary": "",
            "original_length": len(text),
            "summary_length": 0
        }

if __name__ == "__main__":
    # CLI: read file or stdin
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            text = f.read()
    else:
        text = sys.stdin.read()
    
    result = summarize(text, sentences_count=int(sys.argv[2]) if len(sys.argv) > 2 else 5)
    print(result.get('summary', result))

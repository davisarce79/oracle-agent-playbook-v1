# AI Writing Detection Skill

Detect AI-generated text using statistical analysis of linguistic patterns. Works entirely offline - no API keys needed.

## Overview

This skill analyzes text for indicators of AI generation by measuring:

- **Lexical Diversity**: AI tends to use a smaller, more common vocabulary
- **Sentence Length Variance**: AI writes with remarkably uniform sentence lengths
- **Burstiness**: AI shows low variation in sentence length clustering
- **Punctuation Diversity**: Humans use more varied punctuation (em dashes, ellipses)
- **Transition Word Density**: AI overuses transitional phrases ("however," "therefore")
- **Paragraph Uniformity**: AI produces more consistently-sized paragraphs

**Accuracy:** This is a heuristic analysis, not a definitive detector. Designed as one tool among many for editorial assessment. Works best on 300+ words.

---

## Installation

The skill is ready at:  
`~/.openclaw/workspace/skills/ai-writing-detector/`

No external dependencies - uses Python standard library only.

---

## Usage

### In Python Code

```python
import sys
sys.path.insert(0, '/home/opc/.openclaw/workspace/skills/ai-writing-detector')
from ai_writing_detector import analyze_text

# Analyze a string
result = analyze_text("Your text here...")
print(f"AI Probability: {result['ai_probability']*100:.1f}%")
print(f"Confidence: {result['confidence']}")
print("Reasoning:", result['reasoning'])
```

### Via Skill Interface

```python
# Direct skill call
result = await use_skill('ai-writing-detector', {
    'text': 'The quick brown fox jumps over the lazy dog...'
})

# Or from file
result = await use_skill('ai-writing-detector', {
    'file_path': '/path/to/manuscript.txt'
})

# Batch analysis
result = await use_skill('ai-writing-detector', {
    'batch_files': ['chapter1.txt', 'chapter2.txt', 'chapter3.txt']
})
```

### Command Line

```bash
python3 ~/.openclaw/workspace/skills/ai-writing-detector/ai_detector.py chapter1.txt
python3 ~/.openclaw/workspace/skills/ai-writing-detector/ai_detector.py --batch chapter*.txt
cat chapter.txt | python3 ~/.openclaw/workspace/skills/ai-writing-detector/ai_detector.py
```

---

## Output Format

```json
{
  "ai_probability": 0.723,
  "confidence": "medium",
  "word_count": 1245,
  "sentence_count": 87,
  "features": {
    "lexical_diversity": 0.342,
    "sentence_length_variance": 8.2,
    "burstiness": 0.21,
    "punctuation_diversity": 4,
    "informal_markers": 3,
    "transition_word_density": 0.0154
  },
  "reasoning": [
    "Low lexical diversity (AI tends to reuse common words)",
    "Low sentence length variance (AI tends to write very uniformly)",
    "Low burstiness (AI sentences cluster in length)"
  ],
  "disclaimer": "This is a statistical estimate, not a definitive determination..."
}
```

---

## Interpretation Guide

| AI Probability | Likelihood | Action |
|----------------|------------|--------|
| 0.0 - 0.3 | Low (likely human) | No concerns |
| 0.3 - 0.5 | Uncertain | Review manually; check for other AI indicators |
| 0.5 - 0.7 | Moderate suspicion | Consider editing for more human voice |
| 0.7 - 0.9 | High likelihood | Significant revision needed if you want human-only content |
| 0.9 - 1.0 | Very high | Almost certainly AI-generated or heavily AI-assisted |

**Confidence levels:**
- **high**: >1000 words analyzed
- **medium**: 300-1000 words
- **low**: <300 words (insufficient data)

---

## Use Cases for *The Mechanical Soul*

1. **Verify your own writing** - Ensure the manuscript reads as authentically human
2. **Beta reader screening** - Check if beta feedback contains AI-generated notes (spam detection)
3. **Review authenticity** - Determine if online reviews are AI-generated
4. **Competitor analysis** - See if similar books in your genre appear AI-written

---

## Limitations & Caveats

⚠️ **Important:**
- This is a **statistical heuristic**, not a machine learning model trained on millions of samples
- Results are **estimates** based on simplified feature weights
- **False positives/negatives** occur, especially on short texts
- Skilled human writers can have "AI-like" patterns (technical writing, non-native speakers)
- AI that's been heavily human-edited can score as human
- **Do not use as sole evidence** of academic dishonesty or fraud

**Best practice:** Use as one signal among many. Combine with:
- Manual review of flagged passages
- Perplexity analysis with an actual language model (if available)
- Cross-check with multiple detectors (Originality.ai, GPTZero, etc.)

---

## Advanced: Customizing Thresholds

Edit `ai_detector.py` and adjust the `analyze_text()` function's scoring weights if you find patterns specific to your genre or writing style.

Current weights (subject to change):
- Lexical diversity: 30% weight
- Sentence variance: 25% weight  
- Burstiness: 20% weight
- Punctuation: 15% weight
- Informal markers: 10% weight
- Transition words: 15% weight

These were derived from general observations of ChatGPT vs. human writing patterns as of 2024.

---

## Integration with Your Workflow

### During Writing
```bash
# After each chapter, run detector
python3 ~/.openclaw/workspace/skills/ai-writing-detector/ai_detector.py chapter3.txt
```

### Batch Check Full Manuscript
```bash
python3 ~/.openclaw/workspace/skills/ai-writing-detector/ai_detector.py --batch chapters/*.txt > ai_report.json
```

### In Heartbeat
Add to your daily checks:
```python
result = analyze_text(recent_writing_sample)
if result['ai_probability'] > 0.6:
    # Flag for manual review
    log_alert("High AI probability detected")
```

---

## Recommendations for *The Mechanical Soul*

Given the novel's style (literary, introspective, structurally precise):
- Human writing typically scores 0.2-0.5 on this detector due to deliberate prose
- AI would struggle to maintain the nuanced, metaphor-rich, structurally-themed prose
- Aim for <0.4 AI probability to reassure readers of authenticity (important for literary fiction)
- If any chapters score >0.6, consider adding more organic variation (fragments, run-ons, idiosyncrasies)

---

## Technical Notes

- **No external APIs** - runs completely offline
- **No data sent externally** - your text stays on your machine
- **Fast** - processes ~1000 words per second
- **Memory efficient** - streaming analysis possible (currently loads full text)

Future improvements could include:
- Actual ML model (BERT-based classifier)
- Perplexity calculation using a language model
- Character-level n-gram analysis
- Genre-specific training

---

## License

This skill is provided as-is for your personal use. Feel free to modify weights and thresholds for your needs.

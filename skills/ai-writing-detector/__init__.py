"""AI Writing Detection Skill - Analyze text for AI generation probability"""

from .ai_detector import analyze_text, batch_analyze

# Skill metadata for OpenClaw
SKILL_INFO = {
    "name": "ai-writing-detector",
    "description": "Detect AI-generated writing using statistical analysis of linguistic features (perplexity, burstiness, lexical diversity).",
    "capabilities": ["text-analysis", "ai-detection", "writing-quality"],
    "parameters": {
        "file_path": {"type": "string", "required": False, "description": "Path to text file to analyze"},
        "text": {"type": "string", "required": False, "description": "Direct text to analyze (alternative to file_path)"},
        "batch_files": {"type": "array", "required": False, "description": "List of file paths for batch analysis"}
    }
}

async def handle_call(params: dict) -> dict:
    """
    Analyze text for AI generation.
    
    Either `text` or `file_path` required. Use `batch_files` for multiple files.
    
    Returns:
        Dict with ai_probability (0-1), confidence, features, and reasoning.
    """
    file_path = params.get("file_path")
    text = params.get("text")
    batch_files = params.get("batch_files", [])
    
    # Batch mode
    if batch_files:
        if not isinstance(batch_files, list):
            return {"error": "batch_files must be a list of file paths"}
        return batch_analyze(batch_files)
    
    # Single file mode
    if file_path:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
        except Exception as e:
            return {"error": f"Failed to read file: {str(e)}"}
    
    if not text:
        return {"error": "No text provided (use text or file_path parameter)"}
    
    return analyze_text(text)

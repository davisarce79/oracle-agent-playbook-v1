#!/usr/bin/env python3
"""
Book Marketing Image Generator
Uses Nano Banana Pro (Gemini 3 Pro Image) to create promotional visuals.
"""

import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

def generate_image(
    prompt: str,
    output_dir: str = "~/openclaw/workspace/marketing/images",
    resolution: str = "2K",
    style: str = "book cover, professional, cinematic lighting"
) -> dict:
    """
    Generate an image using Nano Banana Pro (Gemini 3 Pro Image).
    
    Args:
        prompt: Image description (will be enhanced with book marketing context)
        output_dir: Where to save images
        resolution: 1K, 2K, or 4K
        style: Artistic style override
        
    Returns:
        Dict with file path and metadata
    """
    output_dir = os.path.expanduser(output_dir)
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate timestamped filename
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    safe_prompt = "".join(c for c in prompt[:30] if c.isalnum() or c in " _-").rstrip()
    filename = f"{timestamp}-{safe_prompt}.png"
    output_path = os.path.join(output_dir, filename)
    
    # Enhance prompt for book marketing
    full_prompt = f"{prompt}. Style: {style}. High quality, professional book marketing image, no watermarks."
    
    # Build command
    cmd = [
        "uv", "run",
        "/usr/local/lib/node_modules/openclaw/skills/nano-banana-pro/scripts/generate_image.py",
        "--prompt", full_prompt,
        "--filename", output_path,
        "--resolution", resolution
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        
        if result.returncode != 0:
            return {
                "error": f"Generation failed: {result.stderr}",
                "prompt": prompt,
                "output_path": None
            }
        
        # Parse output for MEDIA line
        media_line = None
        for line in result.stdout.split('\n'):
            if line.startswith('MEDIA:'):
                media_line = line
                break
        
        return {
            "success": True,
            "file_path": output_path,
            "media_line": media_line,
            "prompt": prompt,
            "resolution": resolution,
            "stdout": result.stdout[:500]
        }
        
    except subprocess.TimeoutExpired:
        return {"error": "Generation timed out (120s)", "prompt": prompt, "output_path": None}
    except Exception as e:
        return {"error": str(e), "prompt": prompt, "output_path": None}

def generate_book_cover_variants(
    title: str,
    author: str,
    genre: str = "literary crime",
    count: int = 3
) -> list:
    """Generate multiple cover variants for a book."""
    prompts = [
        f"Book cover for '{title}' by {author}. {genre} novel. Dark moody aesthetic, Boston cityscape at night, shadows, minimalist typography placement, professional publishing quality",
        f"Book cover for '{title}' by {author}. {genre} with engineering theme. Blueprint-style elements, load path diagrams, steel and concrete textures, cinematic lighting",
        f"Book cover for '{title}' by {author}. {genre} psychological thriller. Close-up of maintenance tools, precise arrangement, noir atmosphere, high contrast"
    ]
    
    results = []
    for i in range(min(count, len(prompts))):
        result = generate_image(
            prompt=prompts[i],
            resolution="2K",
            style="professional book cover, publishing quality, no text overlay"
        )
        results.append(result)
    
    return results

if __name__ == "__main__":
    # Quick test
    if len(sys.argv) > 1:
        prompt = " ".join(sys.argv[1:])
    else:
        prompt = "The Mechanical Soul book cover: literary crime novel about a hitman who thinks like an engineer, Boston setting, dark moody"
    
    result = generate_image(prompt)
    print(json.dumps(result, indent=2))

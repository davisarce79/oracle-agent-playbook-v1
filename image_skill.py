#!/usr/bin/env python3
"""
Image Description Skill using Moondream
Provides natural language description of any uploaded image.
"""

import sys
from PIL import Image
from moondream import Moondream
import torch

# Load model (cached singleton)
_model = None
_processor = None

def load_model():
    global _model, _processor
    if _model is None:
        print("Loading Moondream model...")
        _model = Moondream.from_pretrained("vikhyatk/moondream-0.5B")
        _model.eval()
        if torch.cuda.is_available():
            _model = _model.cuda()
    return _model

def describe_image(image_path: str, question: str = None) -> str:
    """
    Generate a caption or answer a question about an image.
    If question is None, returns a general description.
    """
    model = load_model()
    image = Image.open(image_path).convert("RGB")
    encoded = model.encode_image(image)
    
    if question:
        answer = model.answer_question(encoded, question)
        return answer
    else:
        # Default caption
        caption = model.caption(encoded)
        return caption

if __name__ == "__main__":
    # Test
    if len(sys.argv) > 1:
        img_path = sys.argv[1]
        desc = describe_image(img_path)
        print("Caption:", desc)
    else:
        print("Usage: python image_skill.py <image_path> [question]")

#!/usr/bin/env python3
"""Generate $GUNNA token logo variations with clean backgrounds."""

import os, json, requests

# Load OpenRouter key
auth_path = '/home/opc/.openclaw/agents/main/agent/auth-profiles.json'
with open(auth_path) as f:
    profiles = json.load(f)
    api_key = profiles['profiles']['openrouter']['key']

def generate_image(prompt: str, model: str = "google/gemini-3.0-flash-exp:free"):
    """Generate an image via Gemini on OpenRouter."""
    resp = requests.post(
        "https://openrouter.ai/api/v1/images/generations",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://openclaw.ai",
            "X-Title": "Agent Gunna"
        },
        json={
            "model": model,
            "prompt": prompt,
            "n": 1,
            "size": "1024x1024"
        },
        timeout=120
    )
    resp.raise_for_status()
    data = resp.json()
    if "error" in data:
        raise RuntimeError(f"OpenRouter error: {data['error']}")
    return data["data"][0]["url"]

# Logo prompts (clean, transparent-friendly)
prompts = [
    "Minimalist logo for crypto token $GUNNA. Abstract geometric red polygons arranged in a hexagonal pattern. Solid black background, clean sharp edges, no grain, no texture. Square composition.",
    "Tech logo: stylized字母 G made of red triangles and squares, cyber style. White background, flat design, crisp edges. No gradients, no noise.",
    "Crypto token emblem: deconstructed cube in red and black, geometric, modern. Transparent background suggested, high contrast. Clean vector-like appearance.",
    "Abstract emblem: five red polygons forming a dynamic shape, speed lines in background muted. Pure black background, matte finish, professional."
]

print("Generating 4 logo variations...")
for i, p in enumerate(prompts, 1):
    try:
        url = generate_image(p)
        print(f"Variation {i}: {url}")
    except Exception as e:
        print(f"Variation {i} failed: {e}")

print("\nDone. Download the images and pick your favorite.")

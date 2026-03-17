#!/usr/bin/env python3
"""Generate clean $GUNNA token logo and save locally."""

import os, json, base64, requests

# Load OpenRouter key
auth_path = '/home/opc/.openclaw/agents/main/agent/auth-profiles.json'
with open(auth_path) as f:
    profiles = json.load(f)
    api_key = profiles['profiles']['openrouter']['key']

# Use Gemini via OpenRouter for image generation
prompt = """Create a minimalist crypto token logo for $GUNNA. 
- Abstract geometric shape: 5 red polygons forming a hexagonal emblem
- Pure white background (for easy transparency later)
- Clean vector-style, sharp edges, no grain, no texture
- Square format, centered
- High contrast, professional"""

resp = requests.post(
    "https://openrouter.ai/api/v1/images/generations",
    headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://openclaw.ai",
        "X-Title": "Agent Gunna"
    },
    json={
        "model": "google/gemini-3.0-flash-exp:free",
        "prompt": prompt,
        "n": 1,
        "size": "512x512"
    },
    timeout=120
)

if resp.status_code == 404:
    print("ERROR: Image generation endpoint not available on this OpenRouter plan.")
    print("Falling back: use current logo as-is, or manually create a 512x512 PNG with white background.")
    exit(1)

resp.raise_for_status()
data = resp.json()
if "error" in data:
    raise RuntimeError(f"OpenRouter error: {data['error']}")

image_url = data["data"][0]["url"]
print("Generated image URL:", image_url)

# Download the image
img_data = requests.get(image_url, timeout=30).content
save_path = '/home/opc/.openclaw/workspace/memory/uploads/gunna_token_logo_clean.png'
with open(save_path, 'wb') as f:
    f.write(img_data)
print(f"Saved to: {save_path}")
print("Ready for pump.fun deployment (white bg, easy to make transparent if needed).")

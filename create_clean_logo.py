#!/usr/bin/env python3
"""Generate clean, minimalist $GUNNA token logo using vector graphics."""

from PIL import Image, ImageDraw
import math

# Create 512x512 white canvas
img = Image.new('RGBA', (512, 512), (255, 255, 255, 255))
draw = ImageDraw.Draw(img)

# Define colors
RED = (220, 20, 60)  # Crimson
BLACK = (20, 20, 20)

# Draw 5 red polygons in a hexagonal pattern
center = 256
radius = 180
hex_points = []
for i in range(6):
    angle = math.radians(60 * i - 30)
    x = center + radius * math.cos(angle)
    y = center + radius * math.sin(angle)
    hex_points.append((x, y))

# Draw the outer hexagon (slightly outlined)
draw.polygon(hex_points, outline=BLACK, width=8)

# Draw 5 inner red triangles/polygons (pentagram-like arrangement)
inner_radius = 120
for i in range(5):
    angle = math.radians(90 + 72 * i)  # start at top
    points = []
    for j in range(3):
        a = math.radians(angle + j * 72 + 36)
        x = center + inner_radius * math.cos(a)
        y = center + inner_radius * math.sin(a)
        points.append((x, y))
    draw.polygon(points, fill=RED, outline=BLACK)

# Optional: small center circle
draw.ellipse([center-20, center-20, center+20, center+20], fill=BLACK)

# Save
out_path = '/home/opc/.openclaw/workspace/memory/uploads/gunna_token_logo_clean.png'
img.save(out_path, 'PNG')
print(f"Saved clean logo: {out_path}")
print("Size: 512x512, white background, sharp vectors. Ready for pump.fun.")

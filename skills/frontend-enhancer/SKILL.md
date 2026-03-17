---
name: frontend-enhancer
description: "A specialized design system for enhancing Next.js applications with premium aesthetics, production-ready components, and high-fidelity animations. Use when the user wants to upgrade UI/UX, add bento-grids, or apply the Hal/OpenClaw design language."
---

# Frontend Enhancer 🦞🎨

This skill transforms basic "wireframe" sites into premium, high-converting digital products.

## Component Library

### 1. The Proactive Button
A highly interactive, accessible button with hover states and micro-interactions.
- **Variants**: primary, secondary, outline, ghost, danger.

### 2. Bento Grid Items
Glassmorphism-based layout components for modern feature showcasing.
- **Props**: icon, title, description, animationDelay.

### 3. Hero Section (Hal-Style)
Large typography, radial glow backgrounds, and pulsing "System Online" indicators.

## Workflow: The Upgrade Loop

### Step 1: Token Audit
Check the current `globals.css` and `tailwind.config.js` for the design tokens provided in `memory/contexts/frontend-enhancer.md`.

### Step 2: Structural Refactor
Move from linear layouts to sophisticated grids (md:cols-2, lg:cols-3).

### Step 3: Polish & Motion
Inject the accessible animation library (fade-in, slide-up, scale) using Tailwind or Framer Motion equivalents.

## Design Constraints
- **Color Palette**: `#0f172a` (Primary BG), `#22d3ee` (Cyan Accent).
- **Mobile First**: Always test at 320px first.
- **Performance**: Zero-clutter, optimized Lucide-React icons only.

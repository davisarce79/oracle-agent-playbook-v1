#!/usr/bin/env python3
"""
Build Me This — Tech Stack Reverse Engineering & Scaffold Generator

Input: URL of a website you want to clone/emulate.
Output: Build specification + starter scaffold.

Workflow:
1. Query CRFT Lookup (free tech detection + Lighthouse)
2. Synthesize recommended stack
3. Generate project structure and starter files
4. Optionally initialize git repo

Usage:
  python3 build_me_this.py https://example.com [--output-dir ./my-project]
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from datetime import datetime

import requests

CRFT_URL = "https://www.crft.studio/lookup"

def fetch_crft_data(target_url: str) -> dict:
    """Query CRFT Lookup and return parsed JSON data. Falls back to basic detection if CRFT unavailable."""
    params = {'url': target_url}
    try:
        resp = requests.get(CRFT_URL, params=params, timeout=15)
        if resp.status_code == 200:
            return resp.json()
        else:
            raise ValueError(f"CRFT returned {resp.status_code}")
    except Exception as e:
        # Fallback: basic header+HTML detection
        print(f"[WARN] CRFT unavailable ({e}). Using fallback detection.", file=sys.stderr)
        return fallback_detection(target_url)

def fallback_detection(target_url: str) -> dict:
    """Basic tech detection via HTTP headers and HTML patterns."""
    import re
    try:
        # Disable SSL verification to avoid cert issues on some hosts
        resp = requests.get(target_url, timeout=15, allow_redirects=True, verify=False)
        headers = resp.headers
        html = resp.text
    except Exception as e:
        raise RuntimeError(f"Fallback fetch failed: {e}")

    tech = []
    # Server header
    server = headers.get('Server', '')
    if server:
        tech.append({'name': server, 'category': 'server'})
    # X-Powered-By
    xpb = headers.get('X-Powered-By', '')
    if xpb:
        tech.append({'name': xpb, 'category': 'framework'})
    # Check HTML meta
    if 'wp-content' in html:
        tech.append({'name': 'WordPress', 'category': 'cms'})
    if 'react' in html.lower() or 'next' in html.lower():
        tech.append({'name': 'React/Next.js', 'category': 'framework'})
    if 'vue' in html.lower():
        tech.append({'name': 'Vue.js', 'category': 'framework'})
    if 'angular' in html.lower():
        tech.append({'name': 'Angular', 'category': 'framework'})
    if 'bootstrap' in html.lower():
        tech.append({'name': 'Bootstrap', 'category': 'css'})
    if 'tailwind' in html.lower():
        tech.append({'name': 'Tailwind CSS', 'category': 'css'})
    if 'shopify' in html.lower():
        tech.append({'name': 'Shopify', 'category': 'ecommerce'})
    if 'cloudflare' in headers.get('Server', '').lower() or 'cloudflare' in headers.get('CF-RAY', '').lower():
        tech.append({'name': 'Cloudflare', 'category': 'cdn'})

    return {
        'technologies': tech,
        'performance': None,
        'meta_tags': None,
        'sitemap': None,
        'source': 'fallback'
    }

def synthesize_stack(crft_data: dict, target_url: str) -> dict:
    """
    Analyze CRFT data and produce a recommended stack + build plan.
    """
    tech = crft_data.get('technologies', [])
    # Normalize keys (CRFT may vary); adapt to actual response structure
    frameworks = []
    cms = None
    hosting = None
    cdn = None
    analytics = []
    language = None

    # Extract common hints
    for t in tech:
        name = t.get('name', '').lower()
        category = t.get('category', '').lower()
        if 'react' in name or 'next' in name or 'vue' in name or 'svelte' in name:
            frameworks.append(name)
        if 'wordpress' in name:
            cms = 'WordPress'
        if 'shopify' in name:
            cms = 'Shopify'
        if 'vercel' in name or 'netlify' in name or 'aws' in name:
            hosting = name
        if 'cloudflare' in name:
            cdn = name
        if 'google analytics' in name or 'gtm' in name:
            analytics.append('Google Analytics')
        if 'node' in name:
            language = 'JavaScript/Node.js'
        if 'python' in name or 'django' in name:
            language = 'Python'
        if 'php' in name:
            language = 'PHP'

    # Heuristic: pick primary frontend framework
    primary_framework = None
    if frameworks:
        # Prefer Next.js over others if present
        for f in frameworks:
            if 'next' in f:
                primary_framework = 'Next.js'
                break
        if not primary_framework:
            primary_framework = frameworks[0].title()

    # If no framework detected, default to a modern vibe
    if not primary_framework:
        primary_framework = 'Next.js (App Router)'
        language = 'TypeScript'

    # Styling: assume Tailwind if not Tailwind already present
    styling = 'Tailwind CSS'
    if any('tailwind' in f.lower() for f in frameworks):
        styling = 'Tailwind CSS (detected)'
    else:
        # Could infer from classes in HTML but not here
        pass

    # Hosting defaults
    if not hosting:
        hosting = 'Vercel (recommended for Next.js)'

    # Build recommendation based on primary stack
    # Safely get performance score
    perf_score = None
    try:
        perf_score = crft_data.get('performance', {}).get('lighthouse', {}).get('categories', {}).get('performance', {}).get('score')
    except Exception:
        perf_score = None

    recommendation = {
        'frontend': primary_framework,
        'styling': styling,
        'language': language or 'TypeScript/JavaScript',
        'hosting': hosting,
        'cms': cms,
        'cdn': cdn,
        'analytics': analytics,
        'performance_target': perf_score
    }

    # Project structure
    tree = {
        'app/': [
            'layout.tsx',
            'page.tsx',
            'components/',
            'lib/'
        ],
        'public/': [
            'images/',
            'favicon.ico'
        ],
        'styles/': [
            'globals.css'
        ],
        'package.json': '',
        'tsconfig.json': '',
        'next.config.js': '',
        'tailwind.config.js': '',
        '.env.local': '',
        'README.md': '',
        '.gitignore': ''
    }

    plan = {
        'stack': recommendation,
        'project_structure': tree,
        'estimated_effort_days': 3,
        'notes': f"Based on analysis of {target_url}. Detected technologies: {', '.join(t.get('name') for t in tech)}"
    }
    return plan

def generate_scaffold(output_dir: Path, plan: dict, target_url: str):
    """Create starter project files according to plan."""
    output_dir.mkdir(parents=True, exist_ok=True)
    tree = plan['project_structure']

    def get_file_content(file_path: str) -> str:
        """Return appropriate starter content for a given file path."""
        filename = Path(file_path).name
        stem = Path(file_path).stem
        suffix = Path(file_path).suffix
        parent = Path(file_path).parent.name

        if file_path == 'package.json':
            return PACKAGE_JSON_NEXTJS if 'Next.js' in plan['stack']['frontend'] else PACKAGE_JSON_GENERIC
        if file_path == 'tsconfig.json':
            return TSCONFIG_JSON
        if file_path == 'next.config.js':
            return NEXT_CONFIG_JS
        if file_path == 'tailwind.config.js':
            return TAILWIND_CONFIG_JS
        if file_path == 'styles/globals.css':
            return GLOBALS_CSS
        if file_path == 'app/page.tsx':
            return PAGE_TSX
        if file_path == 'app/layout.tsx':
            return LAYOUT_TSX
        if file_path == 'README.md':
            return README_TEMPLATE.format(target=target_url, stack=plan['stack']['frontend'], created=datetime.utcnow().isoformat())
        # Default empty
        return ''

    for name, value in tree.items():
        # Case: directory with list of files inside
        if name.endswith('/') and isinstance(value, list):
            dir_path = output_dir / name.rstrip('/')
            dir_path.mkdir(parents=True, exist_ok=True)
            for fname in value:
                file_path = dir_path / fname
                file_path.parent.mkdir(parents=True, exist_ok=True)
                if not file_path.exists():
                    file_path.write_text(get_file_content(f"{name.rstrip('/')}/{fname}"))
        # Case: file at root
        elif isinstance(value, str):
            file_path = output_dir / name
            file_path.parent.mkdir(parents=True, exist_ok=True)
            if not file_path.exists():
                file_path.write_text(value or get_file_content(name))
        # Case: directory (no trailing slash?) but we skip; our tree uses trailing slash for dirs

    print(f"Scaffold generated at: {output_dir}")

# Templates
PACKAGE_JSON_NEXTJS = """{
  "name": "vibe-clone",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint"
  },
  "dependencies": {
    "next": "latest",
    "react": "latest",
    "react-dom": "latest",
    "tailwindcss": "latest",
    "postcss": "latest",
    "autoprefixer": "latest"
  },
  "devDependencies": {
    "@types/node": "latest",
    "@types/react": "latest",
    "@types/react-dom": "latest",
    "typescript": "latest"
  }
}
"""

PACKAGE_JSON_GENERIC = """{
  "name": "vibe-clone",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "vue": "^3.4.0"
  },
  "devDependencies": {
    "vite": "^5.0.0",
    "@vitejs/plugin-vue": "^5.0.0"
  }
}
"""

TSCONFIG_JSON = """{
  "compilerOptions": {
    "target": "ES2017",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [
      {
        "name": "next"
      }
    ],
    "paths": {
      "@/*": ["./*"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
"""

NEXT_CONFIG_JS = """/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
}
module.exports = nextConfig
"""

TAILWIND_CONFIG_JS = """/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
"""

GLOBALS_CSS = """@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  @apply bg-white text-gray-900;
}
"""

PAGE_TSX = """export default function Home() {
  return (
    <main className="min-h-screen p-8">
      <h1 className="text-3xl font-bold">Vibe Clone</h1>
      <p className="mt-4 text-gray-600">
        Built with {process.env.NEXT_PUBLIC_STACK || 'Next.js'} + Tailwind
      </p>
    </main>
  )
}
"""

LAYOUT_TSX = """export const metadata = {
  title: 'Vibe Clone',
  description: 'A vibe-coded clone based on detected stack.',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
"""

README_TEMPLATE = """# {stack} Clone

Inspired by: {target}

This project is an auto-generated starter based on the tech stack detected from the reference site.

## Stack

- {stack}
- Tailwind CSS
- TypeScript
- Vercel deployment (recommended)

## Get Started

1. Install dependencies: `npm install`
2. Run dev server: `npm run dev`
3. Open http://localhost:3000

## Deploy

Push to GitHub and import into Vercel.

Generated by Build Me This on {created}
"""

def main():
    parser = argparse.ArgumentParser(description="Reverse-engineer a website's stack and generate a starter project.")
    parser.add_argument('url', help='Reference website URL to clone')
    parser.add_argument('--output-dir', default='./vibe-clone', help='Output directory for scaffold')
    args = parser.parse_args()

    target_url = args.url
    output_dir = Path(args.output_dir).resolve()

    print(f"Fetching stack data for: {target_url}")
    crft_data = fetch_crft_data(target_url)

    # Save raw data for reference
    raw_out = output_dir.parent / f"crft_raw_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
    with open(raw_out, 'w') as f:
        json.dump(crft_data, f, indent=2)
    print(f"Raw CRFT data saved: {raw_out}")

    print("Synthesizing build plan...")
    plan = synthesize_stack(crft_data, target_url)

    # Save plan
    plan_out = output_dir.parent / f"build_plan_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
    with open(plan_out, 'w') as f:
        json.dump(plan, f, indent=2)
    print(f"Build plan saved: {plan_out}")

    print("Generating scaffold...")
    generate_scaffold(output_dir, plan, target_url)

    print("\n=== Build Summary ===")
    print(json.dumps(plan['stack'], indent=2))
    print(f"\nScaffold at: {output_dir}")
    print("Next: cd into it, run `npm install`, then `npm run dev`")

if __name__ == "__main__":
    main()

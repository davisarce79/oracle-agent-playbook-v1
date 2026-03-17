#!/usr/bin/env python3
"""
Telegram Command Skill: /buildme
Usage in Telegram: /buildme https://example.com [--output-dir ./my-app]

This skill runs the Build Me This stack analyzer and replies with a summary.
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

WORKSPACE = Path('/home/opc/.openclaw/workspace')

def handle_buildme_command(args_list):
    """Parse and execute the /buildme command."""
    parser = argparse.ArgumentParser(prog='/buildme', description='Reverse-engineer a website and generate a starter scaffold.')
    parser.add_argument('url', help='Website URL to clone')
    parser.add_argument('--output-dir', default='./vibe-clone', help='Output directory for scaffold (default: ./vibe-clone)')
    try:
        args = parser.parse_args(args_list)
    except SystemExit:
        return {
            "reply": "Usage: /buildme <url> [--output-dir path]\nExample: /buildme https://example.com --output-dir ./my-clone",
            "success": False
        }

    # Run build_me_this.py
    cmd = [sys.executable, str(WORKSPACE / 'build_me_this.py'), args.url, '--output-dir', args.output_dir]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        output = result.stdout + result.stderr

        if result.returncode != 0:
            return {
                "reply": f"❌ Build failed:\n```\n{output[:2000]}```",
                "success": False
            }

        # Extract summary lines for user-friendly reply
        # The script prints "=== Build Summary ===" and JSON stack info near the end
        summary_lines = []
        for line in output.splitlines():
            if 'Scaffold at:' in line or 'Next:' in line or 'Build Summary' in line:
                summary_lines.append(line)
        summary = '\n'.join(summary_lines) if summary_lines else output[-1000:]

        reply = (
            f"✅ Build complete!\n\n"
            f"Stack: see details below\n"
            f"{summary}\n\n"
            f"Full logs and plan saved in workspace."
        )
        return {
            "reply": reply,
            "success": True,
            "output": output,
            "scaffold_dir": args.output_dir
        }
    except subprocess.TimeoutExpired:
        return {
            "reply": "⏳ Build timed out after 5 minutes. Try again later or use a smaller site.",
            "success": False
        }
    except Exception as e:
        return {
            "reply": f"⚠️ Error: {str(e)}",
            "success": False
        }

# OpenClaw will call this function with the raw command args (list of strings)
def handle(args: list) -> dict:
    """Entry point for OpenClaw command routing."""
    return handle_buildme_command(args)

def main():
    """CLI entry point."""
    result = handle_buildme_command(sys.argv[1:])
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Telegram Command Skill: /claudeclone
Generates a Claude Clone scaffold (Gunna-powered private chat).
Usage: /claudeclone [--output-dir ./my-claude-clone]
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

WORKSPACE = Path('/home/opc/.openclaw/workspace')

def handle_claudeclone_command(args_list):
    parser = argparse.ArgumentParser(prog='/claudeclone', description='Generate a private chat app powered by Agent Gunna.')
    parser.add_argument('url', nargs='?', default='https://claude.ai', help='Reference URL (ignored, just for metadata)')
    parser.add_argument('--output-dir', default='./claude-clone', help='Output directory')
    try:
        args = parser.parse_args(args_list)
    except SystemExit:
        return {
            "reply": "Usage: /claudeclone [url] [--output-dir path]\nGenerates a Next.js chat app that talks to OpenClaw.",
            "success": False
        }

    cmd = [sys.executable, str(WORKSPACE / 'claude_clone.py'), args.url, '--output-dir', args.output_dir]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        output = result.stdout + result.stderr
        if result.returncode != 0:
            return {"reply": f"❌ Build failed:\n```\\n{output[:2000]}```", "success": False}
        return {
            "reply": f"✅ Claude Clone scaffold generated!\\nDirectory: {args.output_dir}\\nNext: cd into it, run `npm install`, then `npm run dev`.",
            "success": True,
            "output": output
        }
    except subprocess.TimeoutExpired:
        return {"reply": "⏳ Build timed out after 5 minutes.", "success": False}
    except Exception as e:
        return {"reply": f"⚠️ Error: {str(e)}", "success": False}

def main():
    result = handle_claudeclone_command(sys.argv[1:])
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()

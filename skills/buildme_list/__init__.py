#!/usr/bin/env python3
"""
Telegram Command Skill: /buildme-list
Lists recent Build Me This scaffolds and can create a zip archive for download.

Usage:
  /buildme-list                     - list recent scaffolds
  /buildme-list get <folder>        - create zip of that scaffold
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

WORKSPACE = Path('/home/opc/.openclaw/workspace')

def list_scaffolds(limit=10):
    """List recent scaffold directories (default pattern: vibe-clone*, plus any dirs with build_plan_*.json)."""
    scaffolds = []
    # Pattern 1: vibe-clone* directories
    for d in WORKSPACE.glob('vibe-clone*'):
        if d.is_dir():
            # Try to find associated build plan
            plan_files = list(d.parent.glob(f"build_plan_*.json"))
            if plan_files:
                plan_time = datetime.fromtimestamp(plan_files[0].stat().st_mtime)
            else:
                plan_time = datetime.fromtimestamp(d.stat().st_mtime)
            scaffolds.append({
                'path': str(d),
                'name': d.name,
                'modified': plan_time.isoformat(),
                'build_plan': str(plan_files[0]) if plan_files else None
            })
    # Also include any dirs that contain a package.json (Next.js projects) but not already listed
    for d in WORKSPACE.iterdir():
        if d.is_dir() and (d / 'package.json').exists():
            if not any(s['path'] == str(d) for s in scaffolds):
                scaffolds.append({
                    'path': str(d),
                    'name': d.name,
                    'modified': datetime.fromtimestamp(d.stat().st_mtime).isoformat(),
                    'build_plan': None
                })
    # Sort by modified descending
    scaffolds.sort(key=lambda x: x['modified'], reverse=True)
    return scaffolds[:limit]

def create_zip(folder_path: str) -> (str, str):
    """Create a zip archive of the scaffold folder. Returns (zip_path, error)."""
    folder = Path(folder_path)
    if not folder.exists() or not folder.is_dir():
        return None, f"Folder not found: {folder_path}"
    zip_name = f"{folder.name}_archive.zip"
    zip_path = WORKSPACE / zip_name
    try:
        # Use zip -r
        subprocess.run(['zip', '-r', str(zip_path), folder.name], cwd=WORKSPACE, check=True, capture_output=True)
        return str(zip_path), None
    except subprocess.CalledProcessError as e:
        return None, f"Zip failed: {e.stderr.decode() if e.stderr else str(e)}"
    except FileNotFoundError:
        return None, "zip command not installed on system"

def handle_list_command(args_list):
    """Handle /buildme-list command."""
    parser = argparse.ArgumentParser(prog='/buildme-list', description='List and retrieve Build Me This scaffolds.')
    parser.add_argument('action', nargs='?', default='list', choices=['list', 'get'], help='list or get')
    parser.add_argument('folder', nargs='?', help='Folder name (from list) to zip')
    try:
        args = parser.parse_args(args_list)
    except SystemExit:
        return {
            "reply": "Usage:\n/buildme-list list\n/buildme-list get <folder_name>",
            "success": False
        }

    if args.action == 'list':
        scaffolds = list_scaffolds()
        if not scaffolds:
            return {"reply": "No scaffolds found yet. Use /buildme <url> to generate one.", "success": False}
        lines = ["Recent Build Me This scaffolds:"]
        for i, s in enumerate(scaffolds, 1):
            lines.append(f"{i}. {s['name']} (modified: {s['modified'][:10]})")
        lines.append("\nTo download a scaffold as zip, use: /buildme-list get <folder_name>")
        return {"reply": "\n".join(lines), "success": True, "scaffolds": scaffolds}

    elif args.action == 'get':
        if not args.folder:
            return {"reply": "Specify a folder name from the list. Example: /buildme-list get vibe-clone", "success": False}
        # Find the folder
        target = WORKSPACE / args.folder
        if not target.exists() or not target.is_dir():
            return {"reply": f"Folder not found: {args.folder}", "success": False}
        zip_path, err = create_zip(args.folder)
        if err:
            return {"reply": f"❌ {err}", "success": False}
        zip_name = Path(zip_path).name if zip_path else args.folder
        return {
            "reply": f"✅ Created zip: {zip_name}\nFile location: {zip_path}\n(You can download via file access or web UI if configured.)",
            "success": True,
            "zip_path": zip_path
        }

def main():
    result = handle_list_command(sys.argv[1:])
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()

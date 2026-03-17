#!/usr/bin/env python3
"""
Automatic File Upload Scanner
Monitors the inbound media directory and automatically scans any new file
with the AI writing detector (if text-based). Logs results for review.
"""

import os
import sys
import time
import json
import hashlib
from pathlib import Path
from datetime import datetime
import logging

# Add skill paths
sys.path.insert(0, '/home/opc/.openclaw/workspace/skills/ai-writing-detector')
sys.path.insert(0, '/home/opc/.openclaw/workspace/skills/duckduckgo-search')

from ai_detector import analyze_text

# Configuration
INBOUND_DIR = Path('/home/opc/.openclaw/media/inbound')
SCANNED_DIR = Path('/home/opc/.openclaw/workspace/memory/scanned_uploads')
LOG_FILE = Path('/home/opc/.openclaw/workspace/logs/upload_scanner.log')
STATE_FILE = Path('/home/opc/.openclaw/workspace/.upload_scanner_state.json')

# Ensure directories exist
SCANNED_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

def calculate_file_hash(filepath: Path) -> str:
    """Calculate SHA256 hash to detect duplicates."""
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def scan_file(filepath: Path) -> dict:
    """Scan a file. If text, run AI detector. If binary, just archive."""
    try:
        file_hash = calculate_file_hash(filepath)
        file_size = filepath.stat().st_size
        
        # Try to read as text for AI detection
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                text = f.read()
            
            # Run AI detector
            result = analyze_text(text)
            result['file_path'] = str(filepath)
            result['file_name'] = filepath.name
            result['scanned_at'] = datetime.now().isoformat()
            result['file_size'] = file_size
            result['file_hash'] = file_hash
            result['file_type'] = 'text'
        except UnicodeDecodeError:
            # Not a text file - return basic info only
            result = {
                'file_path': str(filepath),
                'file_name': filepath.name,
                'scanned_at': datetime.now().isoformat(),
                'file_size': file_size,
                'file_hash': file_hash,
                'file_type': 'binary',
                'ai_probability': None,
                'note': 'Binary file - AI detection skipped'
            }
        
        return result
    except Exception as e:
        return {
            'file_path': str(filepath),
            'file_name': filepath.name,
            'error': str(e),
            'scanned_at': datetime.now().isoformat()
        }

def load_state() -> dict:
    """Load previous scan state to avoid re-scanning."""
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, 'r') as f:
                return json.load(f)
        except Exception:
            return {'scanned_hashes': [], 'results': []}
    return {'scanned_hashes': [], 'results': []}

def save_state(state: dict):
    """Save scan state."""
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

def archive_scanned_file(src: Path, result: dict):
    """Move scanned file to archive with result metadata."""
    # Create a subdirectory by date
    date_dir = SCANNED_DIR / datetime.now().strftime('%Y-%m-%d')
    date_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy file to archive with hash prefix to avoid collisions
    dest = date_dir / f"{result['file_hash'][:8]}_{src.name}"
    import shutil
    shutil.copy2(src, dest)
    
    # Save result JSON alongside
    result_file = dest.with_suffix('.scan.json')
    with open(result_file, 'w') as f:
        json.dump(result, f, indent=2)
    
    logging.info(f"Archived {src.name} → {dest}")

def main_loop():
    """Main scanning loop - runs continuously, checking for new files."""
    logging.info("Upload scanner started")
    state = load_state()
    
    # Track files we've seen in this session
    seen_in_session = set()
    
    try:
        while True:
            # Get all files in inbound directory (non-recursive)
            try:
                files = list(INBOUND_DIR.iterdir())
            except Exception as e:
                logging.error(f"Error reading inbound dir: {e}")
                time.sleep(5)
                continue
            
            for filepath in files:
                if not filepath.is_file():
                    continue
                
                # Skip if already scanned (by hash)
                try:
                    file_hash = calculate_file_hash(filepath)
                except Exception as e:
                    logging.warning(f"Could not hash {filepath.name}: {e}")
                    continue
                
                if file_hash in state['scanned_hashes']:
                    # Already scanned before, but might be new session
                    if filepath.name in seen_in_session:
                        continue
                    seen_in_session.add(filepath.name)
                    logging.debug(f"Skipping already-scanned file: {filepath.name}")
                    continue
                
                # All files are scanned; AI detector will skip binary files automatically
                
                # Scan it!
                logging.info(f"Scanning {filepath.name}...")
                result = scan_file(filepath)
                
                # Log results
                if 'error' in result:
                    logging.error(f"Scan failed for {filepath.name}: {result['error']}")
                else:
                    ai_prob = result.get('ai_probability', 0)
                    conf = result.get('confidence', 'unknown')
                    logging.info(f"Scan complete: {filepath.name} → AI={ai_prob:.1%} ({conf})")
                    
                    # If high AI probability, flag it
                    if ai_prob > 0.8:
                        logging.warning(f"⚠️  HIGH AI PROBABILITY: {filepath.name} ({ai_prob:.1%})")
                        # Could send notification here
                
                # Archive the result
                result_entry = {
                    'file_name': filepath.name,
                    'file_hash': file_hash,
                    'result': result,
                    'archived_at': datetime.now().isoformat()
                }
                state['results'].append(result_entry)
                state['scanned_hashes'].append(file_hash)
                seen_in_session.add(filepath.name)
                
                # Archive the physical file (optional - comment out if you want to keep originals)
                try:
                    archive_scanned_file(filepath, result)
                    # Optionally delete original after archiving
                    # filepath.unlink()
                except Exception as e:
                    logging.error(f"Failed to archive {filepath.name}: {e}")
                
                # Save state after each file
                save_state(state)
            
            # Sleep before next scan
            time.sleep(10)  # Check every 10 seconds
            
    except KeyboardInterrupt:
        logging.info("Scanner stopped by user")
    except Exception as e:
        logging.error(f"Scanner crashed: {e}")
        raise

if __name__ == "__main__":
    main_loop()

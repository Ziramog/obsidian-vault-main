#!/usr/bin/env python3
"""
handoff-archive.py — Archiva handoffs con status:done o cancelled > 7 días.

Uso: python3 handoff-archive.py [--dry-run]
"""

import os
import sys
import shutil
from datetime import datetime, timezone, timedelta

VAULT = "/home/hermes/obsidian-vault"
ART = timedelta(hours=3)
DRY_RUN = "--dry-run" in sys.argv

def parse_frontmatter(filepath):
    fm = {}
    with open(filepath) as f:
        content = f.read()
    if not content.startswith("---"):
        return fm
    parts = content.split("---", 2)
    if len(parts) < 3:
        return fm
    for line in parts[1].strip().split("\n"):
        line = line.strip()
        if ":" in line:
            key, _, val = line.partition(":")
            fm[key.strip()] = val.strip()
    return fm

def find_completed_at(folder_path):
    """Check response.md or events/ for completion timestamp."""
    response_file = os.path.join(folder_path, "response.md")
    if os.path.isfile(response_file):
        fm = parse_frontmatter(response_file)
        completed = fm.get("completed-at", "")
        if completed:
            return completed
    
    # Check events for done event
    events_dir = os.path.join(folder_path, "events")
    if os.path.isdir(events_dir):
        for evt in sorted(os.listdir(events_dir), reverse=True):
            if "done" in evt:
                evt_path = os.path.join(events_dir, evt)
                fm = parse_frontmatter(evt_path)
                timestamp = fm.get("timestamp", "")
                if timestamp:
                    return timestamp
    
    # Fallback: use folder mtime
    mtime = os.path.getmtime(folder_path)
    return datetime.fromtimestamp(mtime).isoformat()

def main():
    now = datetime.now(timezone.utc) - ART
    cutoff = now - timedelta(days=7)
    
    archived = 0
    
    for direction in ["vps-to-local", "local-to-vps"]:
        ho_dir = os.path.join(VAULT, f"Hermes/Handoffs/{direction}")
        archive_dir = os.path.join(VAULT, "Hermes/Handoffs/archive", direction)
        
        if not os.path.isdir(ho_dir):
            continue
        
        for folder in sorted(os.listdir(ho_dir)):
            folder_path = os.path.join(ho_dir, folder)
            request_file = os.path.join(folder_path, "request.md")
            
            if not os.path.isfile(request_file):
                continue
            
            fm = parse_frontmatter(request_file)
            status = fm.get("status", "")
            
            if status not in ("done", "cancelled"):
                continue
            
            # Determine completion time
            completed_str = find_completed_at(folder_path)
            try:
                completed_dt = datetime.fromisoformat(completed_str)
            except (ValueError, TypeError):
                continue
            
            if completed_dt < cutoff:
                dest = os.path.join(archive_dir, folder)
                if DRY_RUN:
                    print(f"[DRY-RUN] Archivaría: {folder} (completado {completed_str[:10]})")
                else:
                    os.makedirs(archive_dir, exist_ok=True)
                    if os.path.exists(dest):
                        shutil.rmtree(dest)
                    shutil.move(folder_path, dest)
                    print(f"📦 Archivado: {folder} → archive/{direction}/")
                archived += 1
    
    if archived == 0:
        print("✅ Nada para archivar.")
    else:
        print(f"\n📦 Total archivados: {archived}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

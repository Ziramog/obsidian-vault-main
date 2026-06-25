#!/usr/bin/env python3
"""
handoff-check.py — Lista handoffs abiertos + detecta escalate-after vencidos.

Uso: python3 handoff-check.py [--all] [--json]
"""

import os
import sys
from datetime import datetime, timezone, timedelta

VAULT = "/home/hermes/obsidian-vault"
ART = timedelta(hours=3)

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

def scan_handoffs(direction="vps-to-local"):
    results = []
    ho_dir = os.path.join(VAULT, f"Hermes/Handoffs/{direction}")
    if not os.path.isdir(ho_dir):
        return results
    
    now = datetime.now(timezone.utc) - ART
    
    for folder in sorted(os.listdir(ho_dir)):
        folder_path = os.path.join(ho_dir, folder)
        request_file = os.path.join(folder_path, "request.md")
        if not os.path.isfile(request_file):
            continue
        
        fm = parse_frontmatter(request_file)
        status = fm.get("status", "?")
        
        if status == "done" or status == "cancelled":
            if "--all" not in sys.argv:
                continue
        
        priority = fm.get("priority", "normal")
        project = fm.get("project", "?")
        created_at = fm.get("created-at", "?")
        
        # Check escalate-after
        escalate = fm.get("escalate-after", "")
        vencido = False
        vencido_h = 0
        if escalate and escalate.endswith("h") and created_at != "?":
            try:
                hours = int(escalate[:-1])
                created_dt = datetime.fromisoformat(created_at)
                deadline = created_dt + timedelta(hours=hours)
                if now > deadline and status == "ready":
                    vencido = True
                    vencido_h = int((now - deadline).total_seconds() / 3600)
            except (ValueError, TypeError):
                pass
        
        results.append({
            "id": folder,
            "status": status,
            "priority": priority,
            "project": project,
            "created": created_at[:16] if created_at != "?" else "?",
            "vencido": vencido,
            "vencido_h": vencido_h,
            "direction": direction,
        })
    
    return results

def main():
    all_results = []
    for d in ["vps-to-local", "local-to-vps"]:
        all_results.extend(scan_handoffs(d))
    
    if "--json" in sys.argv:
        import json
        print(json.dumps(all_results, indent=2))
        return 0
    
    if not all_results:
        print("✅ No hay handoffs activos.")
        return 0
    
    # Counts
    active = [r for r in all_results if r["status"] not in ("done", "cancelled")]
    vencidos = [r for r in all_results if r["vencido"]]
    
    print(f"📋 Handoffs: {len(active)} activos, {len(vencidos)} vencidos\n")
    
    for r in all_results:
        icon = "🔴" if r["priority"] == "high" else ("🟡" if r["priority"] == "normal" else "🟢")
        status_icon = {"ready": "⏳", "done": "✅", "cancelled": "❌", "ack": "👀"}.get(r["status"], "?")
        arrow = "→" if r["direction"] == "vps-to-local" else "←"
        
        vencido_str = f" ⚠️ VENCIDO +{r['vencido_h']}h" if r["vencido"] else ""
        print(f"  {icon} {status_icon} {r['id']} {arrow} {r['project']} [{r['status']}]{vencido_str}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

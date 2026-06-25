#!/usr/bin/env python3
"""
telegram-alert.py — Fase 4: Alertas Telegram para handoffs vencidos y conflictos git.

Verifica:
1. Handoffs priority:high con escalate-after vencido → Telegram
2. Conflictos git (<<<<<<<) en archivos críticos → Telegram

Uso: python3 telegram-alert.py [--dry-run]
Cron: cada 30 min
"""

import os
import sys
import json
import re
import urllib.request
import urllib.parse
from datetime import datetime, timezone, timedelta

VAULT = "/home/hermes/obsidian-vault"
ENV_FILE = "/home/hermes/.hermes/.env"
CHAT_ID = "1479438002"
ART = timedelta(hours=3)  # UTC-3

CRITICAL_FILES = [
    "Hermes/MEMORY.md",
    "Hermes/Briefings/current.md",
    "Hermes/Config/AGENTS.md",
    "Hermes/Config/SOUL.md",
    "Hermes/Config/ARCHITECTURE.md",
]

DRY_RUN = "--dry-run" in sys.argv

# ── Telegram send ──
def get_token():
    with open(ENV_FILE) as f:
        for line in f:
            if line.startswith("TELEGRAM_BOT_TOKEN="):
                return line.split("=", 1)[1].strip()
    return None

def send_telegram(text):
    if DRY_RUN:
        print(f"[DRY-RUN] Telegram: {text[:80]}...")
        return True
    token = get_token()
    if not token:
        print("ERROR: No TELEGRAM_BOT_TOKEN found")
        return False
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = urllib.parse.urlencode({"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}).encode()
    try:
        req = urllib.request.Request(url, data=data)
        resp = urllib.request.urlopen(req, timeout=15)
        result = json.loads(resp.read().decode())
        return result.get("ok", False)
    except Exception as e:
        print(f"Telegram send failed: {e}")
        return False

# ── 1. Handoff checker ──
def parse_frontmatter(filepath):
    """Extract YAML-like frontmatter from markdown file."""
    fm = {}
    with open(filepath) as f:
        content = f.read()
    if not content.startswith("---"):
        return fm
    parts = content.split("---", 2)
    if len(parts) < 3:
        return fm
    fm_text = parts[1]
    for line in fm_text.strip().split("\n"):
        line = line.strip()
        if ":" in line:
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip()
            fm[key] = val
    return fm

def check_handoffs():
    alerts = []
    ho_dir = os.path.join(VAULT, "Hermes/Handoffs/vps-to-local")
    if not os.path.isdir(ho_dir):
        return alerts
    
    now = datetime.now(timezone.utc) - ART
    
    for folder in sorted(os.listdir(ho_dir)):
        folder_path = os.path.join(ho_dir, folder)
        request_file = os.path.join(folder_path, "request.md")
        if not os.path.isfile(request_file):
            continue
        
        fm = parse_frontmatter(request_file)
        status = fm.get("status", "")
        priority = fm.get("priority", "normal")
        
        if status != "ready":
            continue
        if priority != "high":
            continue
        
        escalate_after = fm.get("escalate-after", "")
        created_at = fm.get("created-at", "")
        
        if not escalate_after or not created_at:
            continue
        
        # Parse escalate-after (e.g., "24h", "4h")
        hours = 0
        if escalate_after.endswith("h"):
            try:
                hours = int(escalate_after[:-1])
            except ValueError:
                continue
        
        # Parse created-at
        try:
            created_dt = datetime.fromisoformat(created_at)
        except ValueError:
            continue
        
        deadline = created_dt + timedelta(hours=hours)
        
        if now > deadline:
            age = now - deadline
            age_h = int(age.total_seconds() / 3600)
            alerts.append(f"⚠️ <b>{folder}</b> — handoff priority:high vencido ({age_h}h)\n"
                         f"Proyecto: {fm.get('project', '?')} | Creado: {created_at[:16]}")
    
    return alerts

# ── 2. Git conflict checker ──
def check_git_conflicts():
    alerts = []
    for f in CRITICAL_FILES:
        full_path = os.path.join(VAULT, f)
        if not os.path.isfile(full_path):
            continue
        with open(full_path, errors="ignore") as fh:
            content = fh.read()
        conflict_pattern = re.compile(r'^<<<<<<< ', re.MULTILINE)
        if conflict_pattern.search(content):
            alerts.append(f"🚨 <b>CONFLICTO GIT</b> detectado en <code>{f}</code>\n"
                         f"Revisar y resolver manualmente.")
    return alerts

# ── Main ──
def main():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] telegram-alert.py running...")
    
    ho_alerts = check_handoffs()
    git_alerts = check_git_conflicts()
    all_alerts = ho_alerts + git_alerts
    
    if not all_alerts:
        print("  ✅ Sin alertas.")
        return 0
    
    # Build message
    header = "🤖 <b>Hermes Alert</b>\n"
    body = "\n\n".join(all_alerts)
    message = header + body
    
    if len(message) > 4000:
        message = message[:3900] + "\n\n... (truncado)"
    
    print(f"  📤 Enviando {len(all_alerts)} alertas...")
    ok = send_telegram(message)
    if ok:
        print(f"  ✅ Enviado a Telegram.")
    else:
        print(f"  ❌ Falló el envío.")
    
    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main())

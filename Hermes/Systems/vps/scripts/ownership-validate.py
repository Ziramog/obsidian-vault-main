#!/usr/bin/env python3
"""
ownership-validate.py — Compara archivos modificados vs ownership map.
Detecta escrituras fuera de zona y genera alerta.

Uso: python3 ownership-validate.py [--last-commit] [--json]
  --last-commit: solo verifica el último commit
  Sin flag: verifica working tree vs HEAD
"""

import os
import sys
import subprocess
import json
from datetime import datetime

VAULT = "/home/hermes/obsidian-vault"

# ── Ownership map (from ARCHITECTURE.md V5 Section 11) ──
OWNERSHIP = {
    "brain-vps": [
        "Hermes/MEMORY.md",
        "Hermes/Briefings/current.md",
        "Hermes/Agenda/",
        "Hermes/Sessions/",
        "Hermes/Handoffs/vps-to-local/",
        "Hermes/Daily/",
        "Hermes/Indexes/",
        "Hermes/Reports/",
        "Hermes/Quarantine/",
        "Hermes/Systems/vps/",
        "Hermes/Memory/pending/",
        "Hermes/Memory/archive/",
        "companies/wolfim/intelligence/",
        "companies/ango/intelligence/",
        "companies/construvial/intelligence/",
        "companies/korantis/intelligence/",
    ],
    "Juan": [
        "Hermes/Config/",
        "Hermes/Intelligence/kpis.md",
    ],
    "wolfim-growth": [
        "companies/wolfim/",
    ],
    "ango-commercial": [
        "companies/ango/",
    ],
    "construvial-growth": [
        "companies/construvial/",
    ],
    "korantis-ops": [
        "companies/korantis/",
    ],
    "brain-local": [
        "Hermes/Handoffs/local-to-vps/",
        "Hermes/Systems/local/",
    ],
    "web-builder": [
        "companies/*/projects/",
    ],
    "web-auditor": [
        "companies/*/audit/",
    ],
    "pc-ops": [
        "Hermes/Systems/local/",
    ],
}

# Zonas explícitamente excluidas (auto-generadas, legacy, etc.)
ALWAYS_ALLOWED_PREFIXES = [
    "hq/sessions/",        # session-append cron
    ".git/",
    ".obsidian/",
]

def matches_zone(filepath, zones):
    """Check if filepath is within any of the owner's zones."""
    for zone in zones:
        # Wildcard support
        if "*" in zone:
            import fnmatch
            if fnmatch.fnmatch(filepath, zone):
                return True
            # Also match subpaths of wildcard
            parts = zone.split("/*/")
            if len(parts) == 2:
                if filepath.startswith(parts[0] + "/") and "/" + parts[1] in filepath:
                    return True
        elif filepath.startswith(zone):
            return True
    return False

def get_modified_files(use_last_commit=False):
    """Get list of modified files from git."""
    if use_last_commit:
        result = subprocess.run(
            ["git", "diff", "--name-only", "HEAD~1", "HEAD"],
            capture_output=True, text=True, cwd=VAULT
        )
    else:
        result = subprocess.run(
            ["git", "diff", "--name-only", "HEAD"],
            capture_output=True, text=True, cwd=VAULT
        )
    
    files = [f.strip() for f in result.stdout.split("\n") if f.strip()]
    return files

def is_always_allowed(filepath):
    for prefix in ALWAYS_ALLOWED_PREFIXES:
        if filepath.startswith(prefix):
            return True
    return False

def main():
    use_last = "--last-commit" in sys.argv
    output_json = "--json" in sys.argv
    
    modified = get_modified_files(use_last)
    
    if not modified:
        if output_json:
            print(json.dumps({"status": "clean", "files": [], "violations": []}))
        else:
            print("✅ Sin archivos modificados para auditar.")
        return 0
    
    violations = []
    
    for f in modified:
        if is_always_allowed(f):
            continue
        
        # Find which owners can write here
        allowed_owners = []
        for owner, zones in OWNERSHIP.items():
            if matches_zone(f, zones):
                allowed_owners.append(owner)
        
        if not allowed_owners:
            violations.append({
                "file": f,
                "severity": "high",
                "message": f"⚠️  {f} — NADIE tiene ownership de esta ruta",
            })
        # Note: we don't know WHO wrote it, just that someone did
    
    if output_json:
        print(json.dumps({
            "status": "violations" if violations else "ok",
            "files_checked": len(modified),
            "violations": violations,
        }, indent=2))
    else:
        print(f"📋 {len(modified)} archivos modificados\n")
        
        if violations:
            for v in violations:
                print(v["message"])
            print(f"\n🚨 {len(violations)} violaciones de ownership detectadas.")
        else:
            print("✅ Todos los archivos modificados están en zonas con ownership definido.")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

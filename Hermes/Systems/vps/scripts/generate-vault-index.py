#!/usr/bin/env python3
"""
generate-vault-index.py — Genera Hermes/Indexes/vault-index.md

Lee archivos .md en paths prioritarios, extrae frontmatter si existe,
y produce un índice tabular.

Uso:
  python3 generate-vault-index.py
  python3 generate-vault-index.py --output /path/to/custom/output.md

Dependencias: solo stdlib.
"""

import os
import re
import json
import datetime

VAULT_ROOT = os.path.expanduser("/home/hermes/obsidian-vault")
OUTPUT_PATH = os.path.join(VAULT_ROOT, "Hermes", "Indexes", "vault-index.md")

PATHS = {
    "Hermes/MEMORY.md": {"category": "Maestro", "default_owner": "brain-vps"},
    "Hermes/Briefings/current.md": {"category": "Briefing", "default_owner": "brain-vps"},
    "Hermes/Config/AGENTS.md": {"category": "Config", "default_owner": "Juan"},
    "Hermes/Config/SOUL.md": {"category": "Config", "default_owner": "Juan"},
    "Hermes/Config/ARCHITECTURE.md": {"category": "Config", "default_owner": "Juan"},
}

PROFILE_PATHS = [
    ("Hermes/Profiles/vps/brain-vps.md", "brain-vps", "VPS"),
    ("Hermes/Profiles/vps/wolfim-growth.md", "wolfim-growth", "VPS"),
    ("Hermes/Profiles/vps/ango-commercial.md", "ango-commercial", "VPS"),
    ("Hermes/Profiles/vps/construvial-growth.md", "construvial-growth", "VPS"),
    ("Hermes/Profiles/vps/korantis-ops.md", "korantis-ops", "VPS"),
    ("Hermes/Profiles/local/brain-local.md", "brain-local", "Local"),
    ("Hermes/Profiles/local/web-builder.md", "web-builder", "Local"),
    ("Hermes/Profiles/local/web-auditor.md", "web-auditor", "Local"),
    ("Hermes/Profiles/local/pc-ops.md", "pc-ops", "Local"),
]

COMPANY_README_PATHS = [
    ("companies/wolfim/", "wolfim", "wolfim-growth"),
    ("companies/ango/", "ango", "ango-commercial"),
    ("companies/construvial/", "construvial", "construvial-growth"),
    ("companies/korantis/", "korantis", "korantis-ops"),
]


def extract_frontmatter_field(content: str, field: str) -> str:
    """Extrae un campo de frontmatter YAML entre --- marcadores."""
    m = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if not m:
        return ""
    yaml_block = m.group(1)
    # Busca field: value (sencillo, sin listas anidadas)
    fm = re.search(rf'^{field}:\s*(.+)$', yaml_block, re.MULTILINE)
    if fm:
        return fm.group(1).strip().strip('"').strip("'")
    return ""


def get_file_mtime(path: str) -> str:
    full = os.path.join(VAULT_ROOT, path)
    if not os.path.exists(full):
        return "—"
    ts = os.path.getmtime(full)
    return datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M")


def get_owner_from_file(path: str) -> str:
    full = os.path.join(VAULT_ROOT, path)
    if not os.path.exists(full):
        return "?"
    with open(full, 'r', errors='ignore') as f:
        content = f.read(2000)
    owner = extract_frontmatter_field(content, 'owner')
    return owner if owner else "?"


def get_status_from_file(path: str) -> str:
    full = os.path.join(VAULT_ROOT, path)
    if not os.path.exists(full):
        return "missing"
    with open(full, 'r', errors='ignore') as f:
        content = f.read(2000)
    status = extract_frontmatter_field(content, 'status')
    return status if status else "active"


def generate():
    lines = []
    lines.append("# vault-index.md — Índice del vault")
    lines.append("")
    lines.append(f"> **Generado por:** generate-vault-index.py")
    lines.append(f"> **Última actualización:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"> **Regla:** no se mantiene a mano. Se regenera con el script.")
    lines.append("")

    # Documentos maestros
    lines.append("## Documentos maestros")
    lines.append("")
    lines.append("| Ruta | Owner | Estado | Modificado |")
    lines.append("|---|---|---|---|")
    for rel_path, info in PATHS.items():
        owner = get_owner_from_file(rel_path) or info["default_owner"]
        status = get_status_from_file(rel_path)
        mtime = get_file_mtime(rel_path)
        lines.append(f"| {rel_path} | {owner} | {status} | {mtime} |")
    lines.append("")

    # Empresas
    lines.append("## Empresas")
    lines.append("")
    lines.append("| Ruta | README | Owner | Estado |")
    lines.append("|---|---|---|---|")
    for path, name, default_owner in COMPANY_README_PATHS:
        readme_path = os.path.join(path, "README.md")
        full_readme = os.path.join(VAULT_ROOT, readme_path)
        has_readme = "✅" if os.path.exists(full_readme) else "❌"
        status = get_status_from_file(readme_path) if os.path.exists(full_readme) else "—"
        lines.append(f"| {path} | {has_readme} | {default_owner} | {status} |")
    lines.append("")

    # Profiles
    lines.append("## Profiles")
    lines.append("")
    lines.append("| Ruta | Profile | Host |")
    lines.append("|---|---|---|")
    for path, name, host in PROFILE_PATHS:
        exists = "✅" if os.path.exists(os.path.join(VAULT_ROOT, path)) else "❌"
        lines.append(f"| {path} | {name} | {host} |")
    lines.append("")

    # Skills
    lines.append("## Skills")
    lines.append("")
    skills_dir = os.path.join(VAULT_ROOT, "Hermes/Profiles/skills")
    if os.path.isdir(skills_dir):
        lines.append("| Ruta | Skill |")
        lines.append("|---|---|")
        for f in sorted(os.listdir(skills_dir)):
            if f.endswith(".md"):
                lines.append(f"| Hermes/Profiles/skills/{f} | {f.replace('.md', '')} |")
    lines.append("")

    # Notas
    now = datetime.datetime.now()
    lines.append("## Handoffs abiertos")
    lines.append("")
    for direction in ["vps-to-local", "local-to-vps"]:
        base = os.path.join(VAULT_ROOT, "Hermes/Handoffs", direction)
        if not os.path.isdir(base):
            continue
        items = sorted(os.listdir(base))
        open_handoffs = [d for d in items if d.startswith("HO-")]
        if open_handoffs:
            lines.append(f"### {direction}")
            lines.append("")
            lines.append("| ID | Creado | Antigüedad |")
            lines.append("|---|---|---|")
            for ho_id in open_handoffs:
                req_path = os.path.join(base, ho_id, "request.md")
                if os.path.exists(req_path):
                    mtime_ts = os.path.getmtime(req_path)
                    age = now - datetime.datetime.fromtimestamp(mtime_ts)
                    age_str = f"{int(age.total_seconds() / 3600)}h" if age.total_seconds() < 86400 else f"{int(age.total_seconds() / 86400)}d"
                    lines.append(f"| {ho_id} | {datetime.datetime.fromtimestamp(mtime_ts).strftime('%Y-%m-%d %H:%M')} | {age_str} |")
            lines.append("")

    if not any(os.path.isdir(os.path.join(VAULT_ROOT, "Hermes/Handoffs", d)) for d in ["vps-to-local", "local-to-vps"]):
        lines.append("*(Sin handoffs abiertos)*")
        lines.append("")

    return "\n".join(lines)


if __name__ == "__main__":
    import sys
    output = OUTPUT_PATH
    if len(sys.argv) > 2 and sys.argv[1] == "--output":
        output = sys.argv[2]
    
    content = generate()
    os.makedirs(os.path.dirname(output), exist_ok=True)
    with open(output, 'w') as f:
        f.write(content)
    print(f"✅ vault-index generado: {output}")

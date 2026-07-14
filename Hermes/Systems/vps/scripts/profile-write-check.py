#!/usr/bin/env python3
"""profile-write-check.py — preflight for VPS profile-written vault files.

Checks common issues that block Sync V6 / git diff --check without performing
Git operations. Intended for wolfim-growth, ango-commercial, construvial-growth,
and korantis-ops before closing a task that wrote files for another profile,
brain-local, or Juan.
"""
from __future__ import annotations

import sys
from pathlib import Path

VAULT = Path("/home/hermes/obsidian-vault").resolve()
TEXT_EXTS = {".md", ".txt", ".csv", ".json", ".yaml", ".yml", ".toml"}


def iter_targets(args: list[str]) -> list[Path]:
    if args:
        targets = [Path(a).expanduser() for a in args]
    else:
        targets = [VAULT]
    files: list[Path] = []
    for target in targets:
        if not target.is_absolute():
            target = (Path.cwd() / target).resolve()
        else:
            target = target.resolve()
        if not str(target).startswith(str(VAULT)):
            print(f"ERROR outside_vault path={target}")
            continue
        if target.is_dir():
            for p in target.rglob("*"):
                if ".git" in p.parts:
                    continue
                if p.is_file() and p.suffix.lower() in TEXT_EXTS:
                    files.append(p)
        elif target.is_file():
            files.append(target)
        else:
            print(f"ERROR missing path={target}")
    return sorted(set(files))


def check_file(path: Path) -> list[str]:
    issues: list[str] = []
    try:
        raw = path.read_bytes()
    except Exception as exc:
        return [f"{path}:0: read_error {exc}"]
    if b"\x00" in raw:
        return []
    text = raw.decode("utf-8", errors="replace")
    for idx, line in enumerate(text.splitlines(), start=1):
        if line.endswith(" ") or line.endswith("\t"):
            issues.append(f"{path}:{idx}: trailing whitespace")
        if line.startswith("<<<<<<< ") or line.startswith("=======") or line.startswith(">>>>>>> "):
            issues.append(f"{path}:{idx}: possible git conflict marker")
    return issues


def main() -> int:
    files = iter_targets(sys.argv[1:])
    issues: list[str] = []
    for path in files:
        issues.extend(check_file(path))
    if issues:
        for issue in issues[:200]:
            print(issue)
        if len(issues) > 200:
            print(f"... {len(issues) - 200} more issues")
        print(f"FAIL profile-write-check files={len(files)} issues={len(issues)}")
        return 2
    print(f"OK profile-write-check files={len(files)} issues=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

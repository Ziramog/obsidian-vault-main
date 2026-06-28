#!/usr/bin/env python3
"""Agenda V2 reminder scanner.

Reads today's Agenda V2 markdown, sends due Telegram reminders, and marks them sent.
Intended for cron/no-agent later. Not activated by this script itself.
"""
from __future__ import annotations

import argparse
import datetime as dt
import importlib.util
import json
import os
from pathlib import Path
import sys
import urllib.parse
import urllib.request
from typing import Dict, List, Optional

ART = dt.timezone(dt.timedelta(hours=-3), name="ART")
DEFAULT_VAULT = Path(os.environ.get("HERMES_VAULT", "/home/hermes/obsidian-vault"))
SCRIPT_DIR = Path(__file__).resolve().parent
AGENDA_PY = SCRIPT_DIR / "agenda.py"

spec = importlib.util.spec_from_file_location("agenda", AGENDA_PY)
if spec is None or spec.loader is None:
    raise SystemExit(f"No pude cargar {AGENDA_PY}")
agenda = importlib.util.module_from_spec(spec)
spec.loader.exec_module(agenda)


def now_art() -> dt.datetime:
    return dt.datetime.now(ART)


def parse_due(value: str) -> dt.datetime:
    # Agenda format: YYYY-MM-DD HH:MM, ART assumed.
    naive = dt.datetime.strptime(value.strip(), "%Y-%m-%d %H:%M")
    return naive.replace(tzinfo=ART)


def load_telegram_token(env_path: Path = Path("/home/hermes/.hermes/.env")) -> str:
    if not env_path.exists():
        raise RuntimeError(f"No existe {env_path}")
    for line in env_path.read_text(encoding="utf-8", errors="ignore").splitlines():
        if line.strip().startswith("TELEGRAM_BOT_TOKEN="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise RuntimeError("TELEGRAM_BOT_TOKEN no encontrado")


def send_telegram(text: str, chat_id: str = "1479438002") -> Dict[str, object]:
    token = load_telegram_token()
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = urllib.parse.urlencode({"chat_id": chat_id, "text": text}).encode()
    req = urllib.request.Request(url, data=data)
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode())


def due_tasks(vault: Path, day: dt.date, now: dt.datetime) -> List[Dict[str, str]]:
    path = agenda.agenda_path(vault, day)
    if not path.exists():
        return []
    lines = agenda.read_lines(path)
    tasks = []
    for task in agenda.iter_tasks(lines):
        status = task.get("status", "pending")
        channel = task.get("channel", "telegram")
        reminder = task.get("reminder")
        if not reminder or channel != "telegram":
            continue
        if status not in {"pending", "snoozed"}:
            continue
        try:
            due_at = parse_due(reminder)
        except ValueError:
            continue
        if now >= due_at:
            tasks.append(task)
    return tasks


def mark_sent(vault: Path, day: dt.date, task_ref: str) -> None:
    path = agenda.ensure_agenda(vault, day)
    with agenda.file_lock(path):
        lines = agenda.read_lines(path)
        agenda.set_task_status(
            lines,
            task_ref,
            "sent",
            checkbox_done=False,
            extra_meta={"sent-at": now_art().strftime("%Y-%m-%d %H:%M")},
        )
        agenda.write_lines(path, lines)


def scan(vault: Path, day: dt.date, dry_run: bool = False, chat_id: str = "1479438002") -> str:
    now = now_art()
    tasks = due_tasks(vault, day, now)
    if not tasks:
        return f"No hay recordatorios vencidos para {day.isoformat()} ({now.strftime('%H:%M ART')})."
    outputs = []
    for task in tasks:
        tid = task.get("id", task.get("title", ""))
        text = f"🔔 Recordatorio: {task.get('title')}"
        if task.get("detail"):
            text += f"\n{task['detail']}"
        text += f"\n\nID: {task.get('id', 'sin-id')}"
        if dry_run:
            outputs.append(f"DRY RUN: {text}")
        else:
            result = send_telegram(text, chat_id=chat_id)
            if not result.get("ok"):
                outputs.append(f"ERROR enviando {tid}: {result}")
                continue
            mark_sent(vault, day, tid)
            outputs.append(f"SENT {tid}: {task.get('title')}")
    return "\n".join(outputs)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Agenda V2 reminder scanner")
    p.add_argument("--vault", default=str(DEFAULT_VAULT))
    p.add_argument("--date", default="hoy")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--chat-id", default="1479438002")
    return p


def main(argv: Optional[List[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    day = agenda.parse_date(args.date)
    print(scan(Path(args.vault), day, dry_run=args.dry_run, chat_id=args.chat_id))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Dedicated Telegram Agenda bot poller.

One-shot poller designed to run from cron every minute. Uses a dedicated bot
TOKEN (TELEGRAM_AGENDA_BOT_TOKEN) and reuses Agenda V2 markdown as the single
source of truth.

State lives under Hermes/Systems/vps/state/ so no DB is required.
"""
from __future__ import annotations

import argparse
import contextlib
import datetime as dt
import fcntl
import importlib.util
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
import unicodedata
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

ART = dt.timezone(dt.timedelta(hours=-3), name="ART")
BASE_DIR = Path("/home/hermes/obsidian-vault/Hermes/Systems/vps")
STATE_DIR = BASE_DIR / "state"
STATE_PATH = STATE_DIR / "agenda-bot-state.json"
AUDIO_CACHE_DIR = BASE_DIR / "cache" / "agenda-bot-audio"
DEFAULT_VAULT = Path(os.environ.get("HERMES_VAULT", "/home/hermes/obsidian-vault"))
DEFAULT_TOKEN_ENV = "TELEGRAM_AGENDA_BOT_TOKEN"
AGENDA_PY = BASE_DIR / "scripts" / "agenda.py"
HERMES_REPO = Path("/home/hermes/.hermes/hermes-agent")
if str(HERMES_REPO) not in sys.path:
    sys.path.insert(0, str(HERMES_REPO))

spec = importlib.util.spec_from_file_location("agenda", AGENDA_PY)
if spec is None or spec.loader is None:
    raise SystemExit(f"No pude cargar {AGENDA_PY}")
agenda = importlib.util.module_from_spec(spec)
spec.loader.exec_module(agenda)

from tools.transcription_tools import transcribe_audio  # type: ignore  # noqa: E402

DATE_WORDS = {
    "hoy": "hoy",
    "today": "hoy",
    "mañana": "mañana",
    "manana": "mañana",
    "tomorrow": "mañana",
}
ADD_RE = re.compile(
    r"^(?P<date>hoy|today|mañana|manana|tomorrow)?\s*(?P<time>\d{1,2}(?::\d{2})?)?\s*(?P<title>.+)$",
    re.IGNORECASE,
)
ID_RE = re.compile(r"ag-(?P<date>\d{8})-(?P<seq>\d{3})", re.IGNORECASE)


def now_art() -> dt.datetime:
    return dt.datetime.now(ART)


def load_token(token_env: str = DEFAULT_TOKEN_ENV) -> str:
    token = os.environ.get(token_env, "").strip()
    if token:
        return token
    env_path = Path("/home/hermes/.hermes/.env")
    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8", errors="ignore").splitlines():
            s = line.strip()
            if not s or s.startswith("#") or "=" not in s:
                continue
            k, v = s.split("=", 1)
            if k.strip() == token_env:
                token = v.strip().strip('"').strip("'")
                if token:
                    return token
    raise RuntimeError(
        f"Falta {token_env}. Creá el bot Agenda en BotFather y guardá ese token fuera del vault (.env)."
    )


def allowed_chat_ids() -> set[str]:
    allowed: set[str] = set()
    for key in ("TELEGRAM_ALLOWED_USERS", "TELEGRAM_HOME_CHANNEL"):
        raw = os.environ.get(key, "")
        if not raw:
            continue
        for part in raw.split(","):
            part = part.strip()
            if part and re.fullmatch(r"-?\d+", part):
                allowed.add(part)
    # Fallback to config.yaml top-level TELEGRAM_HOME_CHANNEL when env vars are
    # absent or non-numeric (some installs use TELEGRAM_ALLOWED_USERS for other
    # auth semantics, not chat IDs).
    cfg = Path('/home/hermes/.hermes/config.yaml')
    if cfg.exists():
        for line in cfg.read_text(encoding='utf-8', errors='ignore').splitlines():
            if line.startswith('TELEGRAM_HOME_CHANNEL:'):
                value = line.split(':', 1)[1].strip()
                if re.fullmatch(r"-?\d+", value):
                    allowed.add(value)
                break
    return allowed


def ensure_dirs() -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    AUDIO_CACHE_DIR.mkdir(parents=True, exist_ok=True)


def load_state() -> Dict[str, Any]:
    ensure_dirs()
    if not STATE_PATH.exists():
        return {"offset": 0}
    try:
        return json.loads(STATE_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {"offset": 0}


def save_state(state: Dict[str, Any]) -> None:
    ensure_dirs()
    tmp = STATE_PATH.with_suffix(".tmp")
    tmp.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(STATE_PATH)


def telegram_api(token: str, method: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    url = f"https://api.telegram.org/bot{token}/{method}"
    encoded = None
    if data is not None:
        encoded = urllib.parse.urlencode(data).encode()
    req = urllib.request.Request(url, data=encoded)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())


def get_updates(token: str, offset: int, timeout: int = 0) -> List[Dict[str, Any]]:
    resp = telegram_api(token, "getUpdates", {"offset": offset, "timeout": timeout})
    if not resp.get("ok"):
        raise RuntimeError(f"getUpdates failed: {resp}")
    return resp.get("result", [])


def send_message(token: str, chat_id: str, text: str) -> Dict[str, Any]:
    return telegram_api(token, "sendMessage", {"chat_id": chat_id, "text": text})


def get_file_path(token: str, file_id: str) -> str:
    resp = telegram_api(token, "getFile", {"file_id": file_id})
    if not resp.get("ok"):
        raise RuntimeError(f"getFile failed: {resp}")
    file_path = resp.get("result", {}).get("file_path")
    if not file_path:
        raise RuntimeError("Telegram no devolvió file_path")
    return str(file_path)


def download_file(token: str, file_path: str, suffix: str) -> Path:
    ensure_dirs()
    target = AUDIO_CACHE_DIR / f"{now_art().strftime('%Y%m%d-%H%M%S-%f')}{suffix}"
    url = f"https://api.telegram.org/file/bot{token}/{file_path}"
    with urllib.request.urlopen(url, timeout=60) as resp:
        target.write_bytes(resp.read())
    return target


def date_from_task_id(task_id: str) -> Optional[str]:
    m = ID_RE.search(task_id)
    if not m:
        return None
    raw = m.group("date")
    return f"{raw[0:4]}-{raw[4:6]}-{raw[6:8]}"


def summarize_agenda_output(output: str) -> str:
    lines = [line.rstrip() for line in output.strip().splitlines() if line.strip()]
    if not lines:
        return "Sin cambios."
    if len(lines) <= 12:
        return "\n".join(lines)
    return "\n".join(lines[:12])


def is_open_task(task: Dict[str, str]) -> bool:
    status = task.get("status", "pending")
    checked = task.get("check", " ").lower() == "x"
    return status not in {"done", "cancelled"} and not checked


def open_tasks_for_day(vault: Path, day: dt.date) -> List[Dict[str, str]]:
    path = agenda.agenda_path(vault, day)
    if not path.exists():
        return []
    tasks = [task for task in agenda.iter_tasks(agenda.read_lines(path)) if is_open_task(task)]
    for task in tasks:
        task["date"] = day.isoformat()
    return tasks


def compact_task_line(number: int, task: Dict[str, str]) -> str:
    detail = f" — {task['detail']}" if task.get("detail") else ""
    reminder = f" · 🔔 {task['reminder']}" if task.get("reminder") else ""
    return f"{number}) {task.get('title', 'Tarea')}{detail} · {task.get('id', 'sin-id')}{reminder}"


def agenda_dates(vault: Path) -> List[dt.date]:
    root = vault / "Hermes" / "Agenda"
    dates: List[dt.date] = []
    if not root.exists():
        return dates
    for path in root.glob("*.md"):
        try:
            dates.append(dt.date.fromisoformat(path.stem))
        except ValueError:
            continue
    return sorted(dates)


def save_last_view(chat_id: Optional[str], label: str, tasks: List[Dict[str, str]]) -> None:
    if not chat_id:
        return
    state = load_state()
    views = state.setdefault("last_views", {})
    views[str(chat_id)] = {
        "label": label,
        "at": now_art().isoformat(),
        "refs": [
            {
                "id": task.get("id", ""),
                "date": task.get("date", ""),
                "title": task.get("title", ""),
            }
            for task in tasks
        ],
    }
    save_state(state)


def last_view_tasks(chat_id: Optional[str]) -> List[Dict[str, str]]:
    if not chat_id:
        return []
    state = load_state()
    view = state.get("last_views", {}).get(str(chat_id), {})
    refs = view.get("refs", []) if isinstance(view, dict) else []
    if not isinstance(refs, list):
        return []
    return [ref for ref in refs if isinstance(ref, dict) and (ref.get("id") or ref.get("title"))]


def normalize_match_text(text: str) -> str:
    without_accents = "".join(
        ch for ch in unicodedata.normalize("NFKD", text.lower())
        if not unicodedata.combining(ch)
    )
    return re.sub(r"[^a-z0-9]+", " ", without_accents).strip()


def normalize_add_text(text: str) -> str:
    """Normalize Juan's natural add phrasing before agenda.py parses it."""
    s = re.sub(r"\s+", " ", text.strip())
    m = re.match(
        r"^(?P<prio>urgente|alta|rojo|roja|importante|amarillo|amarilla|verde|backlog|baja)\s+para\s+(?P<date>[^:]{1,80})\s*:\s*(?P<title>.+)$",
        s,
        flags=re.IGNORECASE,
    )
    if not m:
        return text
    prio_raw = agenda.normalize_date_text(m.group("prio"))
    prio = {
        "urgente": "rojo",
        "alta": "rojo",
        "rojo": "rojo",
        "roja": "rojo",
        "importante": "amarillo",
        "amarillo": "amarillo",
        "amarilla": "amarillo",
        "verde": "verde",
        "backlog": "verde",
        "baja": "verde",
    }.get(prio_raw, m.group("prio"))
    return f"{prio} {m.group('date').strip()} {m.group('title').strip()}"


def resolve_short_task_ref(vault: Path, day: dt.date, task_ref: str, tasks: Optional[List[Dict[str, str]]] = None) -> str:
    ref = task_ref.strip().lstrip("#")
    if ID_RE.search(ref) or not re.fullmatch(r"\d+", ref):
        open_tasks = tasks if tasks is not None else open_tasks_for_day(vault, day)
        ref_tokens = normalize_match_text(task_ref).split()
        if ref_tokens:
            for task in open_tasks:
                haystack = normalize_match_text(" ".join([task.get("title", ""), task.get("detail", "")]))
                if all(token in haystack for token in ref_tokens):
                    return task.get("id") or task_ref.strip()
        return task_ref.strip()
    open_tasks = tasks if tasks is not None else open_tasks_for_day(vault, day)
    number = int(ref)
    if number < 1 or number > len(open_tasks):
        return f"__INVALID_SHORT_REF__:{number}:{len(open_tasks)}"
    return open_tasks[number - 1].get("id") or task_ref.strip()


def resolve_action_refs(vault: Path, payload: str, chat_id: Optional[str] = None) -> List[Tuple[str, str]]:
    """Resolve numeric/ID refs using the last visible list first, then today."""
    day = agenda.now_art().date()
    today_tasks = open_tasks_for_day(vault, day)
    refs = re.findall(r"ag-\d{8}-\d{3}|#?\d+", payload, flags=re.IGNORECASE)
    if not refs:
        refs = [payload.strip()]
    resolved_items: List[Tuple[str, str]] = []
    last_refs = last_view_tasks(chat_id)
    for ref in refs:
        clean_ref = ref.strip().lstrip("#")
        resolved_ref = ""
        resolved_date = day.isoformat()
        if last_refs and re.fullmatch(r"\d+", clean_ref):
            number = int(clean_ref)
            if number < 1 or number > len(last_refs):
                raise ValueError(f"No hay tarea {number} en la última lista. Mandá /todo o /hoy para refrescar números.")
            target = last_refs[number - 1]
            resolved_ref = str(target.get("id") or target.get("title") or "")
            resolved_date = str(target.get("date") or day.isoformat())
        if not resolved_ref:
            resolved_ref = resolve_short_task_ref(vault, day, ref, tasks=today_tasks)
            resolved_date = date_from_task_id(resolved_ref) or day.isoformat()
        if resolved_ref.startswith("__INVALID_SHORT_REF__:"):
            _, number, count = resolved_ref.split(":")
            raise ValueError(f"No hay tarea {number}. Hoy hay {count} tareas abiertas. Mandá /hoy para ver números.")
        item = (resolved_date, resolved_ref)
        if item not in resolved_items:
            resolved_items.append(item)
    return resolved_items


def parse_add_text(text: str) -> Tuple[str, Optional[str], str, Optional[str]]:
    s = text.strip()
    s = re.sub(r"^/agendar\s+", "", s, flags=re.IGNORECASE)
    s = re.sub(r"^/add\s+", "", s, flags=re.IGNORECASE)
    s = normalize_add_text(s)
    try:
        batch = agenda.parse_task_batch(s)
    except ValueError as exc:
        raise ValueError(
            "No pude interpretar el texto. Ej: 'rojo mañana 9 llamar a GAMA', 'miércoles que viene 14 pasar a ver ANGO', 'mie 26 10 reunión' o 'mañana: llamar a GAMA, ver ANGO'."
        ) from exc
    if len(batch) != 1:
        raise ValueError("parse_add_text recibió varias tareas; usá cmd_add_batch.")
    date_word, reminder, title, explicit_priority = batch[0]
    if not title:
        raise ValueError("Falta el título de la tarea.")
    return date_word, reminder, title, explicit_priority


def cmd_add_batch(vault: Path, text: str, source: str) -> str:
    s = text.strip()
    s = re.sub(r"^/agendar\s+", "", s, flags=re.IGNORECASE)
    s = re.sub(r"^/add\s+", "", s, flags=re.IGNORECASE)
    s = normalize_add_text(s)
    try:
        batch = agenda.parse_task_batch(s)
    except ValueError as exc:
        raise ValueError(
            "No pude interpretar el texto. Ej: 'mañana 9 llamar a GAMA', 'miércoles que viene 14 pasar a ver ANGO', 'mie 26 10 reunión' o 'mañana: llamar a GAMA, ver ANGO'."
        ) from exc
    outputs: List[str] = []
    paths: List[str] = []
    for date_word, reminder, title, explicit_priority in batch:
        day = agenda.parse_date(date_word)
        args = argparse.Namespace(
            vault=str(vault),
            date=day.isoformat(),
            priority=explicit_priority or agenda.infer_priority(date_word, title),
            title=title,
            detail="",
            reminder=reminder,
            channel="telegram",
            source=source,
            status="pending",
            cmd="add",
        )
        output = agenda.add_task_cmd(args)
        outputs.append(output.splitlines()[0])
        paths.append(str(agenda.agenda_path(vault, day).relative_to(vault)))
    if len(outputs) == 1:
        return f"Listo. {outputs[0]}\nArchivo: {paths[0]}"
    bullets = "\n".join(f"- {line}" for line in outputs)
    unique_paths = sorted(set(paths))
    return f"Listo. Agregué {len(outputs)} tareas:\n{bullets}\nArchivos: {', '.join(unique_paths)}"


def cmd_add(vault: Path, text: str, source: str) -> str:
    return cmd_add_batch(vault, text, source)


def cmd_list(vault: Path, which: str, chat_id: Optional[str] = None) -> str:
    day = agenda.parse_date(which)
    path = agenda.agenda_path(vault, day)
    tasks = open_tasks_for_day(vault, day)
    save_last_view(chat_id, which, tasks)
    if not tasks:
        return f"Agenda {day.isoformat()}: sin tareas abiertas.\nArchivo: {path}"
    grouped: Dict[str, List[str]] = {section: [] for section in agenda.SECTIONS}
    for number, task in enumerate(tasks, start=1):
        section = task.get("section", "")
        if section in grouped:
            grouped[section].append(compact_task_line(number, task))
    out = [f"Agenda {day.isoformat()}", "Cerrar rápido: ok 1 · ok 1 3 5"]
    for section in agenda.SECTIONS:
        out.append(f"\n{section}")
        out.extend(grouped[section] or ["(vacío)"])
    out.append(f"\nArchivo: {path}")
    return "\n".join(out)


def cmd_overview(vault: Path, chat_id: Optional[str] = None) -> str:
    today = agenda.now_art().date()
    tomorrow = today + dt.timedelta(days=1)
    week_end = today + dt.timedelta(days=6)

    overdue: List[Dict[str, str]] = []
    for day in agenda_dates(vault):
        if day < today:
            overdue.extend(open_tasks_for_day(vault, day))

    today_tasks = open_tasks_for_day(vault, today)
    tomorrow_tasks = open_tasks_for_day(vault, tomorrow)
    week_tasks: List[Dict[str, str]] = []
    for offset in range(2, 7):
        week_tasks.extend(open_tasks_for_day(vault, today + dt.timedelta(days=offset)))

    ordered = overdue + today_tasks + tomorrow_tasks + week_tasks
    save_last_view(chat_id, "todo", ordered)

    out = [f"Agenda completa desde {today.isoformat()}", "Cerrar rápido: ok 1 · 5,7 ok"]
    number = 1

    def add_section(title: str, tasks: List[Dict[str, str]], show_date: bool) -> None:
        nonlocal number
        out.append(f"\n{title}")
        if not tasks:
            out.append("(vacío)")
            return
        for task in tasks:
            prefix = f"{task.get('date')} · " if show_date else ""
            line = compact_task_line(number, task)
            out.append(f"{number}) {prefix}{line.split(') ', 1)[1]}")
            number += 1

    add_section("⚠️ Atrasadas", overdue, show_date=True)
    add_section("🔴 Hoy", today_tasks, show_date=False)
    add_section("🟡 Mañana", tomorrow_tasks, show_date=False)
    add_section(f"📅 Esta semana ({(today + dt.timedelta(days=2)).isoformat()} a {week_end.isoformat()})", week_tasks, show_date=True)

    if not ordered:
        out.append("\nSin tareas abiertas en atrasadas, hoy, mañana ni esta semana.")
    return "\n".join(out)


def cmd_focus(vault: Path, which: str = "hoy") -> str:
    day = agenda.parse_date(which)
    return agenda.focus(vault, day)


def cmd_done(vault: Path, task_ref: str) -> str:
    date_str = date_from_task_id(task_ref) or agenda.now_art().date().isoformat()
    day = agenda.parse_date(date_str)
    resolved_ref = resolve_short_task_ref(vault, day, task_ref)
    if resolved_ref.startswith("__INVALID_SHORT_REF__:"):
        _, number, count = resolved_ref.split(":")
        return f"No hay tarea {number}. Hoy hay {count} tareas abiertas. Mandá /hoy para ver números."
    return agenda.done_task(vault, day, resolved_ref)


def cmd_done_many(vault: Path, payload: str, chat_id: Optional[str] = None) -> str:
    try:
        resolved_items = resolve_action_refs(vault, payload, chat_id=chat_id)
    except ValueError as exc:
        return str(exc)
    outputs = [agenda.done_task(vault, agenda.parse_date(item_date), ref).splitlines()[0] for item_date, ref in resolved_items]
    return "Listo ✅ Cerré:\n" + "\n".join(f"- {line.replace('OK done: ', '')}" for line in outputs)


def cmd_move_many(vault: Path, payload: str, target_date: str, chat_id: Optional[str] = None) -> str:
    try:
        resolved_items = resolve_action_refs(vault, payload, chat_id=chat_id)
    except ValueError as exc:
        return str(exc)
    outputs = [agenda.move_task(vault, agenda.parse_date(item_date), ref, target_date).splitlines()[0] for item_date, ref in resolved_items]
    return "Listo ↪️ Moví:\n" + "\n".join(f"- {line.replace('OK move: ', '')}" for line in outputs)


def cmd_snooze(vault: Path, task_ref: str, reminder: str) -> str:
    date_str = date_from_task_id(task_ref) or agenda.now_art().date().isoformat()
    day = agenda.parse_date(date_str)
    return agenda.snooze_task(vault, day, task_ref, reminder)


def cmd_review(vault: Path, which: str = "hoy") -> str:
    day = agenda.parse_date(which)
    return agenda.review(vault, day)


def cmd_week(vault: Path, which: str = "hoy") -> str:
    day = agenda.parse_date(which)
    return agenda.week_summary(vault, day)


def cmd_cancel(vault: Path, task_ref: str, which: str = "hoy") -> str:
    date_str = date_from_task_id(task_ref) or which or agenda.now_art().date().isoformat()
    day = agenda.parse_date(date_str)
    return agenda.cancel_task(vault, day, task_ref)


def cmd_move(vault: Path, task_ref: str, target_date: str, source_date: str = "hoy", reminder: Optional[str] = None) -> str:
    date_str = date_from_task_id(task_ref) or source_date or agenda.now_art().date().isoformat()
    day = agenda.parse_date(date_str)
    return agenda.move_task(vault, day, task_ref, target_date, reminder)


def cmd_priority(vault: Path, task_ref: str, new_priority: str, which: str = "hoy") -> str:
    date_str = date_from_task_id(task_ref) or which or agenda.now_art().date().isoformat()
    day = agenda.parse_date(date_str)
    return agenda.set_task_priority(vault, day, task_ref, new_priority)


def cmd_detail(vault: Path, task_ref: str, which: str = "hoy") -> str:
    date_str = date_from_task_id(task_ref) or which or agenda.now_art().date().isoformat()
    day = agenda.parse_date(date_str)
    return agenda.task_detail(vault, day, task_ref)


def cmd_cleanup(vault: Path, which: str = "hoy") -> str:
    day = agenda.parse_date(which)
    return agenda.cleanup_agenda(vault, day)


def cmd_pending(vault: Path, which: str = "hoy") -> str:
    day = agenda.parse_date(which)
    return agenda.pending_tasks(vault, day)


def cmd_edit(vault: Path, task_ref: str, new_title: str, which: str = "hoy") -> str:
    date_str = date_from_task_id(task_ref) or which or agenda.now_art().date().isoformat()
    day = agenda.parse_date(date_str)
    return agenda.edit_task(vault, day, task_ref, new_title)


def handle_text(vault: Path, text: str, source: str, chat_id: Optional[str] = None) -> str:
    raw = text.strip()
    if not raw:
        return "Mandame una tarea o un comando: /hoy, /mañana, /foco, /hecho, /posponer"
    # Telegram group/private commands may arrive as /comando@BotName.
    # Normalize the first token before dispatching; otherwise commands fall
    # through to cmd_add() and pollute the agenda as tasks.
    if raw.startswith("/"):
        parts = raw.split(maxsplit=1)
        cmd = parts[0].split("@", 1)[0]
        raw = f"{cmd} {parts[1]}".strip() if len(parts) > 1 else cmd
    low = raw.lower()
    if low in {"/start", "/help", "help", "ayuda"}:
        return (
            "Bot Agenda listo.\n"
            "Usos:\n"
            "- mañana 9 llamar a GAMA\n"
            "- miércoles que viene 14 pasar a ver ANGO\n"
            "- mie 26 10 reunión con cliente\n"
            "- martes o miércoles 9 visitar cliente\n"
            "- fin de mes pagar monotributo\n"
            "- recordámelo a las 10 pagar monotributo\n"
            "- pagar seguro después de las 15\n"
            "- pagar seguro a la tarde\n"
            "- mandar presupuesto antes de las 12\n"
            "- mandar mail si no responde recordámelo mañana\n"
            "- seguir propuesta si no llego el viernes pasalo al lunes\n"
            "- mañana: llamar a GAMA, ver ANGO, pasar presupuesto\n"
            "- mañana\\n- llamar a GAMA\\n- ver ANGO\\n- pasar presupuesto\n"
            "- mañana llamar a GAMA y después ver ANGO y también pasar presupuesto\n"
            "- /todo  (atrasadas + hoy + mañana + semana)\n"
            "- /hoy\n"
            "- /mañana\n"
            "- /esta-semana\n"
            "- /pendientes\n"
            "- /revisar\n"
            "- /detalle ag-YYYYMMDD-NNN\n"
            "- /prioridad ag-YYYYMMDD-NNN rojo\n"
            "- /limpiar\n"
            "- /cancelar ag-YYYYMMDD-NNN\n"
            "- /editar ag-YYYYMMDD-NNN nuevo texto de tarea\n"
            "- /mover ag-YYYYMMDD-NNN mañana 11:00\n"
            "- /agendar rojo mañana 9 llamar a GAMA\n"
            "- /foco\n"
            "- ok 1  (cerrar por número de /hoy)\n"
            "- ok 1 3 5  (cerrar varias)\n"
            "- /hecho ag-YYYYMMDD-NNN\n"
            "- /posponer ag-YYYYMMDD-NNN 11:00"
        )
    if low in {"/todo", "todo", "/panorama", "panorama", "ver todo", "listar todo", "agenda completa", "todo agenda", "todo lo de agenda"}:
        return cmd_overview(vault, chat_id=chat_id)
    if low in {"/hoy", "hoy", "agenda hoy", "ver hoy", "mostrar hoy", "mostrame hoy", "listar hoy", "qué tengo hoy", "que tengo hoy"}:
        return cmd_list(vault, "hoy", chat_id=chat_id)
    if low in {"/mañana", "/manana", "mañana", "manana", "agenda mañana", "agenda manana", "ver mañana", "ver manana", "mostrar mañana", "mostrar manana", "mostrame mañana", "mostrame manana", "listar mañana", "listar manana", "qué tengo mañana", "que tengo mañana", "qué tengo manana", "que tengo manana"}:
        return cmd_list(vault, "mañana", chat_id=chat_id)
    if low in {"/esta-semana", "/semana", "esta semana", "semana", "agenda semana", "ver semana", "mostrar semana", "mostrame semana", "qué tengo esta semana", "que tengo esta semana"}:
        return cmd_week(vault, "hoy")
    if low in {"/pendientes", "/pendiente", "pendientes", "pendiente", "dame todo lo pendiente", "dame lo pendiente", "todo lo pendiente", "qué tengo pendiente", "que tengo pendiente"}:
        return cmd_overview(vault, chat_id=chat_id)
    if low in {"/tareas", "tareas", "mis tareas", "qué tengo", "que tengo"}:
        return cmd_overview(vault, chat_id=chat_id)
    if low in {"/revisar", "revisar"}:
        return cmd_review(vault, "hoy")
    if low in {"/limpiar", "limpiar"}:
        return cmd_cleanup(vault, "hoy")
    if low in {"/foco", "foco"}:
        return cmd_focus(vault, "hoy")
    if low in {"ok", "listo", "hecho", "done", "cerrado", "cerrar", "cerra", "cerrá", "x", "✅"}:
        return "Decime qué número cierro. Ej: /todo y después cerrar la 1, ok 1, o 5,7 ok."
    move_suffix_match = re.match(
        r"^(?P<refs>(?:ag-\d{8}-\d{3}|#?\d+)(?:[\s,.;]+(?:ag-\d{8}-\d{3}|#?\d+))*)\s+(?:es\s+)?(?:para|a|al)\s+(?P<date>.+)$",
        raw,
        flags=re.IGNORECASE,
    )
    move_prefix_match = re.match(
        r"^(?:mover|mov[eé]|pasar|pas[aá]lo|pas[aá])\s+(?P<refs>(?:ag-\d{8}-\d{3}|#?\d+)(?:[\s,.;]+(?:ag-\d{8}-\d{3}|#?\d+))*)\s+(?:a|para|al)\s+(?P<date>.+)$",
        raw,
        flags=re.IGNORECASE,
    )
    move_match = move_suffix_match or move_prefix_match
    if move_match:
        return cmd_move_many(vault, move_match.group("refs"), move_match.group("date"), chat_id=chat_id)
    bare_number_match = re.match(r"^(?:la\s+)?(\d+(?:[\s,.;]+\d+)*)$", raw, flags=re.IGNORECASE)
    done_match = re.match(r"^(?:/hecho|hecho|ok|listo|cerrado|cerrar|cerra|cerrá|done|x|✅)\s*(?:la\s+|tarea\s+)?(.+)$", raw, flags=re.IGNORECASE)
    reverse_done_match = re.match(r"^((?:ag-\d{8}-\d{3}|#?\d+)(?:[\s,.;]+(?:ag-\d{8}-\d{3}|#?\d+))*)\s*(?:ok|hecho|listo|cerrado|cerrar|cerra|cerrá|done|x|✅)$", raw, flags=re.IGNORECASE)
    natural_done_match = re.match(r"^(?:ya\s+)?(?:hice|termin[eé]|cerr[eé])\s+(.+)$", raw, flags=re.IGNORECASE)
    suffix_done_match = re.match(r"^(.+?)\s+(?:est[áa]\s+)?(?:hecho|listo|cerrado|terminado)$", raw, flags=re.IGNORECASE)
    compact_done_match = re.match(r"^x\s*(\d+(?:[\s,.;]+\d+)*)$", raw, flags=re.IGNORECASE)
    done_command_match = bare_number_match or reverse_done_match or done_match or natural_done_match or suffix_done_match or compact_done_match
    if done_command_match:
        payload = done_command_match.group(1).strip()
        return cmd_done_many(vault, payload, chat_id=chat_id)
    if low.startswith("/detalle ") or low.startswith("detalle "):
        task_ref = raw.split(maxsplit=1)[1].strip()
        return cmd_detail(vault, task_ref)
    if low.startswith("/prioridad ") or low.startswith("prioridad "):
        payload = raw.split(maxsplit=1)[1].strip()
        parts = payload.split(maxsplit=1)
        if len(parts) < 2:
            return "Uso: /prioridad ag-YYYYMMDD-NNN rojo"
        return cmd_priority(vault, parts[0], parts[1])
    if low.startswith("/cancelar ") or low.startswith("cancelar "):
        task_ref = raw.split(maxsplit=1)[1].strip()
        return cmd_cancel(vault, task_ref)
    if low.startswith("/editar ") or low.startswith("editar "):
        payload = raw.split(maxsplit=1)[1].strip()
        parts = payload.split(maxsplit=1)
        if len(parts) < 2:
            return "Uso: /editar ag-YYYYMMDD-NNN nuevo texto de tarea"
        return cmd_edit(vault, parts[0], parts[1])
    if low.startswith("/mover ") or low.startswith("mover "):
        payload = raw.split(maxsplit=1)[1].strip()
        parts = payload.split()
        if len(parts) < 2:
            return "Uso: /mover ag-YYYYMMDD-NNN mañana 11:00"
        task_ref = parts[0]
        reminder = None
        if len(parts) >= 3 and re.fullmatch(r"\d{1,2}(?::\d{2})?", parts[-1]):
            reminder = parts[-1]
            target_date = " ".join(parts[1:-1]).strip()
        else:
            target_date = " ".join(parts[1:]).strip()
        if not target_date:
            return "Uso: /mover ag-YYYYMMDD-NNN mañana 11:00"
        return cmd_move(vault, task_ref, target_date, reminder=reminder)
    if low.startswith("/posponer ") or low.startswith("posponer "):
        parts = raw.split()
        if len(parts) < 3:
            return "Uso: /posponer ag-YYYYMMDD-NNN 11:00"
        return cmd_snooze(vault, parts[1], parts[2])
    if low.startswith("/agendar ") or low.startswith("/add "):
        return cmd_add(vault, raw, source=source)
    if low.startswith("/"):
        return "Comando no reconocido. No guardé nada. Usá /help para ver comandos válidos."
    if low.startswith("agendar ") or low.startswith("agendá ") or low.startswith("agenda "):
        payload = raw.split(maxsplit=1)[1].strip() if len(raw.split(maxsplit=1)) > 1 else ""
        if not payload:
            return "Uso: agendar mañana 9 llamar a GAMA"
        return cmd_add(vault, payload, source=source)
    return cmd_add(vault, raw, source=source)


def transcribe_voice_file(path: Path) -> str:
    result = transcribe_audio(str(path))
    if not result.get("success"):
        raise RuntimeError(result.get("error") or "Falló la transcripción")
    transcript = str(result.get("transcript") or "").strip()
    if not transcript:
        raise RuntimeError("La transcripción vino vacía")
    return transcript


def process_update(vault: Path, token: str, update: Dict[str, Any], dry_run: bool = False) -> Optional[str]:
    message = update.get("message") or update.get("edited_message")
    if not message:
        return None
    chat_id = str(message.get("chat", {}).get("id", "")).strip()
    allowed = allowed_chat_ids()
    if allowed and chat_id not in allowed:
        return f"SKIP chat_id={chat_id} no autorizado"
    source = "telegram-bot-agenda"
    response_text: Optional[str] = None
    if message.get("text"):
        response_text = handle_text(vault, str(message["text"]), source=source, chat_id=chat_id)
    elif message.get("voice"):
        file_id = message["voice"].get("file_id")
        if not file_id:
            response_text = "No pude leer el audio."
        else:
            try:
                file_path = get_file_path(token, file_id)
                local_path = download_file(token, file_path, ".ogg")
                transcript = transcribe_voice_file(local_path)
                response_text = (
                    f"Transcripción: {transcript}\n\n" +
                    handle_text(vault, transcript, source="telegram-audio", chat_id=chat_id)
                )
            except Exception as exc:
                response_text = f"Error al procesar audio: {exc}\nProbá mandarlo como texto."
    elif message.get("audio"):
        file_id = message["audio"].get("file_id")
        if not file_id:
            response_text = "No pude leer el audio."
        else:
            file_path = get_file_path(token, file_id)
            local_path = download_file(token, file_path, ".mp3")
            transcript = transcribe_voice_file(local_path)
            response_text = (
                f"Transcripción: {transcript}\n\n" +
                handle_text(vault, transcript, source="telegram-audio", chat_id=chat_id)
            )
    else:
        response_text = "Mandame texto o audio."

    if not response_text:
        return None
    if dry_run:
        return f"DRY chat_id={chat_id}: {response_text}"
    send_result = send_message(token, chat_id, response_text)
    ok = bool(send_result.get("ok"))
    return f"chat_id={chat_id} sent={ok} text={response_text.splitlines()[0][:120]}"


def poll_once(vault: Path, token_env: str, dry_run: bool = False, poll_timeout: int = 0) -> str:
    token = load_token(token_env)
    state = load_state()
    offset = int(state.get("offset", 0) or 0)
    updates = get_updates(token, offset, timeout=poll_timeout)
    outputs: List[str] = []
    next_offset = offset
    for upd in updates:
        upd_id = int(upd.get("update_id", 0) or 0)
        next_offset = max(next_offset, upd_id + 1)
        try:
            result = process_update(vault, token, upd, dry_run=dry_run)
            if result:
                outputs.append(result)
        except Exception as exc:
            outputs.append(f"ERROR update_id={upd_id}: {type(exc).__name__}: {exc}")
        if not dry_run:
            latest_state = load_state()
            latest_state["offset"] = next_offset
            save_state(latest_state)
    if not dry_run:
        latest_state = load_state()
        latest_state["offset"] = next_offset
        save_state(latest_state)
    return "\n".join(outputs)


def poll_loop(vault: Path, token_env: str, dry_run: bool = False, poll_timeout: int = 25, sleep_on_error: int = 5) -> int:
    """Run Agenda bot as a resident long-polling process.

    This avoids cron latency. A lock prevents a second resident process from
    colliding with Telegram getUpdates and creating Conflict errors.
    """
    ensure_dirs()
    lock_path = STATE_DIR / "agenda-bot-loop.lock"
    with lock_path.open("w") as lock_file:
        try:
            fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            print("Agenda bot loop already running; exiting.", flush=True)
            return 0
        print(f"{now_art().isoformat()} Agenda bot loop started poll_timeout={poll_timeout}s", flush=True)
        while True:
            try:
                output = poll_once(vault, token_env=token_env, dry_run=dry_run, poll_timeout=poll_timeout)
                if output:
                    print(f"{now_art().isoformat()} {output}", flush=True)
            except KeyboardInterrupt:
                print(f"{now_art().isoformat()} Agenda bot loop stopped", flush=True)
                return 0
            except Exception as exc:
                print(f"{now_art().isoformat()} LOOP ERROR {type(exc).__name__}: {exc}", flush=True)
                time.sleep(sleep_on_error)


def selftest(vault: Path) -> str:
    out = []
    out.append(handle_text(vault, "mañana 9 llamar a GAMA", source="selftest"))
    out.append(handle_text(vault, "/mañana", source="selftest"))
    sample_id = None
    sample_day = agenda.parse_date("mañana")
    for task in agenda.iter_tasks(agenda.read_lines(agenda.agenda_path(vault, sample_day))):
        sample_id = task.get("id")
        break
    if sample_id:
        out.append(handle_text(vault, f"/hecho {sample_id}", source="selftest"))
    return "\n---\n".join(out)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Agenda Telegram bot poller")
    p.add_argument("--vault", default=str(DEFAULT_VAULT))
    p.add_argument("--token-env", default=DEFAULT_TOKEN_ENV)
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--loop", action="store_true", help="Run resident long-polling loop instead of one-shot poll")
    p.add_argument("--poll-timeout", type=int, default=25, help="Telegram long-poll timeout for --loop; use 0 for one-shot")
    p.add_argument("--selftest", action="store_true")
    p.add_argument("--simulate-text", help="Procesa un texto como si viniera del bot, sin Telegram")
    p.add_argument("--simulate-chat-id", default="simulate", help="Chat ID usado para guardar última lista en simulación")
    return p


def main(argv: Optional[List[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    vault = Path(args.vault)
    if args.selftest:
        print(selftest(vault))
        return 0
    if args.simulate_text:
        print(handle_text(vault, args.simulate_text, source="simulate-text", chat_id=args.simulate_chat_id))
        return 0
    if args.loop:
        return poll_loop(vault, token_env=args.token_env, dry_run=args.dry_run, poll_timeout=args.poll_timeout)
    output = poll_once(vault, token_env=args.token_env, dry_run=args.dry_run, poll_timeout=0)
    if output:
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

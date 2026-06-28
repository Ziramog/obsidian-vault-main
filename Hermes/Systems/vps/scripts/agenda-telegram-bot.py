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
import importlib.util
import json
import os
import re
import sys
import urllib.parse
import urllib.request
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


def get_updates(token: str, offset: int) -> List[Dict[str, Any]]:
    resp = telegram_api(token, "getUpdates", {"offset": offset, "timeout": 0})
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


def parse_add_text(text: str) -> Tuple[str, Optional[str], str, Optional[str]]:
    s = text.strip()
    s = re.sub(r"^/agendar\s+", "", s, flags=re.IGNORECASE)
    s = re.sub(r"^/add\s+", "", s, flags=re.IGNORECASE)
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


def cmd_list(vault: Path, which: str) -> str:
    day = agenda.parse_date(which)
    return summarize_agenda_output(agenda.list_agenda(vault, day))


def cmd_focus(vault: Path, which: str = "hoy") -> str:
    day = agenda.parse_date(which)
    return agenda.focus(vault, day)


def cmd_done(vault: Path, task_ref: str) -> str:
    date_str = date_from_task_id(task_ref) or agenda.now_art().date().isoformat()
    day = agenda.parse_date(date_str)
    return agenda.done_task(vault, day, task_ref)


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


def handle_text(vault: Path, text: str, source: str) -> str:
    raw = text.strip()
    if not raw:
        return "Mandame una tarea o un comando: /hoy, /mañana, /foco, /hecho, /posponer"
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
            "- /hecho ag-YYYYMMDD-NNN\n"
            "- /posponer ag-YYYYMMDD-NNN 11:00"
        )
    if low in {"/hoy", "hoy"}:
        return cmd_list(vault, "hoy")
    if low in {"/mañana", "/manana", "mañana", "manana"}:
        return cmd_list(vault, "mañana")
    if low in {"/esta-semana", "/semana", "esta semana", "semana"}:
        return cmd_week(vault, "hoy")
    if low in {"/pendientes", "pendientes"}:
        return cmd_pending(vault, "hoy")
    if low in {"/revisar", "revisar"}:
        return cmd_review(vault, "hoy")
    if low in {"/limpiar", "limpiar"}:
        return cmd_cleanup(vault, "hoy")
    if low in {"/foco", "foco"}:
        return cmd_focus(vault, "hoy")
    if low.startswith("/hecho ") or low.startswith("hecho "):
        task_ref = raw.split(maxsplit=1)[1].strip()
        return cmd_done(vault, task_ref)
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
        response_text = handle_text(vault, str(message["text"]), source=source)
    elif message.get("voice"):
        file_id = message["voice"].get("file_id")
        if not file_id:
            response_text = "No pude leer el audio."
        else:
            file_path = get_file_path(token, file_id)
            local_path = download_file(token, file_path, ".ogg")
            transcript = transcribe_voice_file(local_path)
            response_text = (
                f"Transcripción: {transcript}\n\n" +
                handle_text(vault, transcript, source="telegram-audio")
            )
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
                handle_text(vault, transcript, source="telegram-audio")
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


def poll_once(vault: Path, token_env: str, dry_run: bool = False) -> str:
    token = load_token(token_env)
    state = load_state()
    offset = int(state.get("offset", 0) or 0)
    updates = get_updates(token, offset)
    outputs: List[str] = []
    next_offset = offset
    for upd in updates:
        upd_id = int(upd.get("update_id", 0) or 0)
        next_offset = max(next_offset, upd_id + 1)
        with contextlib.suppress(Exception):
            result = process_update(vault, token, upd, dry_run=dry_run)
            if result:
                outputs.append(result)
        if not dry_run:
            state["offset"] = next_offset
            save_state(state)
    if not dry_run:
        state["offset"] = next_offset
        save_state(state)
    return "\n".join(outputs)


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
    p.add_argument("--selftest", action="store_true")
    p.add_argument("--simulate-text", help="Procesa un texto como si viniera del bot, sin Telegram")
    return p


def main(argv: Optional[List[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    vault = Path(args.vault)
    if args.selftest:
        print(selftest(vault))
        return 0
    if args.simulate_text:
        print(handle_text(vault, args.simulate_text, source="simulate-text"))
        return 0
    output = poll_once(vault, token_env=args.token_env, dry_run=args.dry_run)
    if output:
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

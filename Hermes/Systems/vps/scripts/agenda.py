#!/usr/bin/env python3
"""Agenda V2 CLI/parser for Hermes Obsidian vault.

Source of truth: Hermes/Agenda/YYYY-MM-DD.md
No external dependencies. Designed for VPS, local WSL, and cron usage.
"""
from __future__ import annotations

import argparse
import contextlib
import datetime as dt
import os
import re
import sys
import time
import unicodedata
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

ART = dt.timezone(dt.timedelta(hours=-3), name="ART")
DEFAULT_VAULT = Path(os.environ.get("HERMES_VAULT", "/home/hermes/obsidian-vault"))
PRIORITY_MAP = {
    "red": "🔴 Hoy sí o sí",
    "alta": "🔴 Hoy sí o sí",
    "roja": "🔴 Hoy sí o sí",
    "yellow": "🟡 Importante",
    "media": "🟡 Importante",
    "importante": "🟡 Importante",
    "green": "🟢 Backlog",
    "baja": "🟢 Backlog",
    "backlog": "🟢 Backlog",
}
SECTIONS = ["🔴 Hoy sí o sí", "🟡 Importante", "🟢 Backlog"]
DAYS_ES = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
WEEKDAY_ALIASES = {
    0: ["lunes", "lun", "lu"],
    1: ["martes", "mar", "ma"],
    2: ["miercoles", "miércoles", "mierc", "mie", "mi"],
    3: ["jueves", "jue", "ju"],
    4: ["viernes", "vie", "vi"],
    5: ["sabado", "sábado", "sab", "sa"],
    6: ["domingo", "dom", "do"],
}
MONTH_ALIASES = {
    "ene": 1, "enero": 1,
    "feb": 2, "febrero": 2,
    "mar": 3, "marzo": 3,
    "abr": 4, "abril": 4,
    "may": 5, "mayo": 5,
    "jun": 6, "junio": 6,
    "jul": 7, "julio": 7,
    "ago": 8, "agosto": 8,
    "sep": 9, "sept": 9, "septiembre": 9,
    "oct": 10, "octubre": 10,
    "nov": 11, "noviembre": 11,
    "dic": 12, "diciembre": 12,
}
WEEKDAY_NAME_TO_INDEX = {
    alias: index
    for index, aliases in WEEKDAY_ALIASES.items()
    for alias in aliases
}
TASK_RE = re.compile(r"^- \[(?P<check>[ xX])\] \*\*(?P<title>.*?)\*\*(?: — (?P<detail>.*))?$")
META_RE = re.compile(r"^  - (?P<key>[a-zA-Z0-9_-]+): ?(?P<value>.*)$")
TIME_PREFIX_RE = re.compile(r"^(?P<time>\d{1,2}(?::\d{2})?)\b")
DATE_PREFIX_PATTERNS = [
    re.compile(r"^(?P<date>la\s+semana\s+que\s+viene)\b", re.IGNORECASE),
    re.compile(r"^(?P<date>fin\s+de\s+mes)\b", re.IGNORECASE),
    re.compile(r"^(?P<date>el\s+otro\s+(?:lunes|lun|lu|martes|mar|ma|miercoles|miércoles|mierc|mie|mi|jueves|jue|ju|viernes|vie|vi|sabado|sábado|sab|sa|domingo|dom|do))\b", re.IGNORECASE),
    re.compile(r"^(?P<date>primer\s+(?:lunes|lun|lu|martes|mar|ma|miercoles|miércoles|mierc|mie|mi|jueves|jue|ju|viernes|vie|vi|sabado|sábado|sab|sa|domingo|dom|do)\s+de\s+[a-záéíóú]+)\b", re.IGNORECASE),
    re.compile(r"^(?P<date>(?:lunes|lun|lu|martes|mar|ma|miercoles|miércoles|mierc|mie|mi|jueves|jue|ju|viernes|vie|vi|sabado|sábado|sab|sa|domingo|dom|do)\s+o\s+(?:lunes|lun|lu|martes|mar|ma|miercoles|miércoles|mierc|mie|mi|jueves|jue|ju|viernes|vie|vi|sabado|sábado|sab|sa|domingo|dom|do))\b", re.IGNORECASE),
    re.compile(r"^(?P<date>pasado\s+manana)\b", re.IGNORECASE),
    re.compile(r"^(?P<date>manana|mañana|hoy|today|tomorrow)\b", re.IGNORECASE),
    re.compile(r"^(?P<date>en\s+\d+\s+dias?)\b", re.IGNORECASE),
    re.compile(r"^(?P<date>\d{4}-\d{2}-\d{2})\b"),
    re.compile(r"^(?P<date>\d{1,2}[/-]\d{1,2}(?:[/-]\d{2,4})?)\b"),
    re.compile(r"^(?P<date>(?:lunes|lun|lu|martes|mar|ma|miercoles|miércoles|mierc|mie|mi|jueves|jue|ju|viernes|vie|vi|sabado|sábado|sab|sa|domingo|dom|do)(?:\s+(?:que\s+viene|q\s+viene|proximo|proxima|prox|siguiente))?(?:\s+\d{1,2}(?:\s+de\s+[a-záéíóú]+)?)?)\b", re.IGNORECASE),
]
REMINDER_PREFIX_RE = re.compile(r"^(?:recordamelo|recordámelo|recordar|recordame|recordáme)\s+(?:a\s+)?(?:las\s+)?(?P<time>\d{1,2}(?::\d{2})?)\s+", re.IGNORECASE)
REMINDER_SUFFIX_RE = re.compile(r"(?P<body>.+?)\s+(?:despues|después)\s+de\s+las\s+(?P<time>\d{1,2}(?::\d{2})?)$", re.IGNORECASE)
NATURAL_TIME_SUFFIX_PATTERNS = [
    (re.compile(r"(?P<body>.+?)\s+a\s+la\s+tarde$", re.IGNORECASE), "15:00"),
    (re.compile(r"(?P<body>.+?)\s+despues\s+de\s+comer$", re.IGNORECASE), "15:00"),
    (re.compile(r"(?P<body>.+?)\s+después\s+de\s+comer$", re.IGNORECASE), "15:00"),
    (re.compile(r"(?P<body>.+?)\s+antes\s+de\s+las\s+12$", re.IGNORECASE), "11:30"),
]
PRIORITY_PREFIX_RE = re.compile(r"^(?P<prio>rojo|roja|red|alta|amarillo|amarilla|yellow|importante|verde|green|backlog|baja)\s+", re.IGNORECASE)
PRIORITY_NORMALIZATION = {
    "rojo": "red", "roja": "red", "red": "red", "alta": "red",
    "amarillo": "yellow", "amarilla": "yellow", "yellow": "yellow", "importante": "yellow",
    "verde": "green", "green": "green", "backlog": "green", "baja": "green",
}
CONDITIONAL_REMINDER_PATTERNS = [
    re.compile(r"^(?P<title>.+?)\s+(?:y\s+)?si\s+no\s+responde\s+record(?:a|á)melo\s+(?P<date>mañana|manana|hoy|pasado\s+mañana|la\s+semana\s+que\s+viene)$", re.IGNORECASE),
    re.compile(r"^(?P<title>.+?)\s+si\s+no\s+llego\s+(?P<from_date>[a-záéíóúñ ]+?)\s+pasalo\s+al\s+(?P<date>[a-záéíóúñ ]+)$", re.IGNORECASE),
]


def now_art() -> dt.datetime:
    return dt.datetime.now(ART)


def strip_accents(text: str) -> str:
    return "".join(ch for ch in unicodedata.normalize("NFD", text) if unicodedata.category(ch) != "Mn")


def normalize_date_text(text: str) -> str:
    normalized = strip_accents(text or "").lower().strip()
    normalized = re.sub(r"\s+", " ", normalized)
    return normalized


def days_until_weekday(today: dt.date, weekday: int, force_next_week: bool = False) -> int:
    delta = (weekday - today.weekday()) % 7
    if delta == 0:
        delta = 7
    if force_next_week and delta < 7:
        delta += 7
    return delta


def resolve_day_month(day_num: int, month: Optional[int], today: dt.date) -> dt.date:
    if day_num < 1 or day_num > 31:
        raise ValueError(f"Día inválido: {day_num}")
    candidates: List[dt.date] = []
    years = [today.year, today.year + 1]
    if month is not None:
        for year in years:
            with contextlib.suppress(ValueError):
                candidates.append(dt.date(year, month, day_num))
    else:
        for year in years:
            for month_idx in range(1, 13):
                with contextlib.suppress(ValueError):
                    candidates.append(dt.date(year, month_idx, day_num))
    future = [c for c in sorted(candidates) if c >= today]
    if future:
        return future[0]
    raise ValueError(f"No pude resolver día/mes para {day_num}")


def first_weekday_of_month(year: int, month: int, weekday: int) -> dt.date:
    first = dt.date(year, month, 1)
    delta = (weekday - first.weekday()) % 7
    return first + dt.timedelta(days=delta)


def end_of_month(today: dt.date) -> dt.date:
    if today.month == 12:
        first_next = dt.date(today.year + 1, 1, 1)
    else:
        first_next = dt.date(today.year, today.month + 1, 1)
    return first_next - dt.timedelta(days=1)


def parse_date(value: Optional[str]) -> dt.date:
    today = now_art().date()
    raw = (value or "").strip()
    normalized = normalize_date_text(raw)
    if not normalized or normalized in {"today", "hoy"}:
        return today
    if normalized in {"tomorrow", "manana", "mañana"}:
        return today + dt.timedelta(days=1)
    if normalized == "pasado manana":
        return today + dt.timedelta(days=2)
    if normalized == "la semana que viene":
        days_to_next_monday = days_until_weekday(today, 0, force_next_week=True)
        return today + dt.timedelta(days=days_to_next_monday)
    if normalized == "fin de mes":
        return end_of_month(today)
    rel = re.fullmatch(r"en\s+(\d+)\s+dias?", normalized)
    if rel:
        return today + dt.timedelta(days=int(rel.group(1)))
    try:
        return dt.date.fromisoformat(raw)
    except ValueError:
        pass
    for fmt in ("%d/%m/%Y", "%d-%m-%Y", "%d/%m/%y", "%d-%m-%y"):
        with contextlib.suppress(ValueError):
            parsed = dt.datetime.strptime(raw, fmt).date()
            if parsed < today and parsed.year == today.year:
                with contextlib.suppress(ValueError):
                    parsed = parsed.replace(year=parsed.year + 1)
            return parsed
    short_dm = re.fullmatch(r"(\d{1,2})[/-](\d{1,2})", normalized)
    if short_dm:
        return resolve_day_month(int(short_dm.group(1)), int(short_dm.group(2)), today)
    first_weekday_match = re.fullmatch(r"primer\s+(?P<wd>[a-zñáéíóú]+)\s+de\s+(?P<month>[a-záéíóú]+)", normalized)
    if first_weekday_match:
        weekday = WEEKDAY_NAME_TO_INDEX.get(first_weekday_match.group("wd"))
        month_num = MONTH_ALIASES.get(first_weekday_match.group("month"))
        if weekday is None or month_num is None:
            raise SystemExit(f"Fecha inválida: {value}. No pude resolver primer día del mes.")
        candidate = first_weekday_of_month(today.year, month_num, weekday)
        if candidate < today:
            candidate = first_weekday_of_month(today.year + 1, month_num, weekday)
        return candidate
    other_weekday_match = re.fullmatch(r"el\s+otro\s+(?P<wd>[a-zñáéíóú]+)", normalized)
    if other_weekday_match:
        weekday = WEEKDAY_NAME_TO_INDEX.get(other_weekday_match.group("wd"))
        if weekday is None:
            raise SystemExit(f"Fecha inválida: {value}. Día no reconocido.")
        delta = days_until_weekday(today, weekday, force_next_week=True)
        return today + dt.timedelta(days=delta)
    either_weekday_match = re.fullmatch(r"(?P<wd1>[a-zñáéíóú]+)\s+o\s+(?P<wd2>[a-zñáéíóú]+)", normalized)
    if either_weekday_match:
        weekday1 = WEEKDAY_NAME_TO_INDEX.get(either_weekday_match.group("wd1"))
        weekday2 = WEEKDAY_NAME_TO_INDEX.get(either_weekday_match.group("wd2"))
        if weekday1 is None or weekday2 is None:
            raise SystemExit(f"Fecha inválida: {value}. Día no reconocido.")
        candidates = [
            today + dt.timedelta(days=days_until_weekday(today, weekday1)),
            today + dt.timedelta(days=days_until_weekday(today, weekday2)),
        ]
        return min(candidates)
    weekday_phrase = re.fullmatch(
        r"(?P<wd>[a-zñáéíóú]+)(?:\s+(?P<modifier>que\s+viene|q\s+viene|proximo|proxima|prox|siguiente))?(?:\s+(?P<day>\d{1,2})(?:\s+de\s+(?P<month>[a-záéíóú]+))?)?",
        normalized,
    )
    if weekday_phrase:
        weekday_token = weekday_phrase.group("wd")
        weekday = WEEKDAY_NAME_TO_INDEX.get(weekday_token)
        if weekday is None:
            raise SystemExit(f"Fecha inválida: {value}. Día no reconocido.")
        modifier = weekday_phrase.group("modifier")
        day_part = weekday_phrase.group("day")
        month_name = weekday_phrase.group("month")
        if day_part:
            month_num = MONTH_ALIASES.get(month_name) if month_name else None
            try:
                return resolve_day_month(int(day_part), month_num, today)
            except ValueError as exc:
                raise SystemExit(f"Fecha inválida: {value}. {exc}") from exc
        delta = days_until_weekday(today, weekday, force_next_week=bool(modifier))
        return today + dt.timedelta(days=delta)
    raise SystemExit(
        f"Fecha inválida: {value}. Usá YYYY-MM-DD, hoy, mañana, pasado mañana, en N días, viernes, miércoles que viene, mie 26, 26/7, fin de mes o primer lunes de julio."
    )


def extract_date_time_and_title(text: str) -> Tuple[str, Optional[str], str]:
    s = re.sub(r"\s+", " ", (text or "").strip())
    for cond_pattern in CONDITIONAL_REMINDER_PATTERNS:
        cond_match = cond_pattern.match(s)
        if cond_match:
            title = cond_match.group("title").strip(" ,-:")
            target_date = cond_match.group("date").strip()
            if "from_date" in cond_match.groupdict() and cond_match.group("from_date"):
                from_date = cond_match.group("from_date").strip()
                title = f"{title} (mover si no llego {from_date})"
            return target_date, None, title
    prefix_reminder = REMINDER_PREFIX_RE.match(s)
    if prefix_reminder:
        reminder = prefix_reminder.group("time")
        remainder = s[prefix_reminder.end():].strip(" ,-:")
        if not remainder:
            raise ValueError("Falta el título de la tarea.")
        return "hoy", reminder, remainder
    suffix_reminder = REMINDER_SUFFIX_RE.fullmatch(s)
    if suffix_reminder:
        body = suffix_reminder.group("body").strip()
        date_text, reminder, title = extract_date_time_and_title(body)
        return date_text, suffix_reminder.group("time"), title
    for suffix_pattern, mapped_time in NATURAL_TIME_SUFFIX_PATTERNS:
        suffix_match = suffix_pattern.fullmatch(s)
        if suffix_match:
            body = suffix_match.group("body").strip()
            date_text, _, title = extract_date_time_and_title(body)
            return date_text, mapped_time, title
    for pattern in DATE_PREFIX_PATTERNS:
        match = pattern.match(s)
        if not match:
            continue
        date_text = match.group("date").strip()
        remainder = s[match.end():].strip(" ,-:")
        reminder = None
        normalized_date = normalize_date_text(date_text)
        weekday_num_at_end = re.fullmatch(
            r"(?P<prefix>[a-zñ ]+?(?:que viene|q viene|proximo|proxima|prox|siguiente)?)\s+(?P<num>\d{1,2})",
            normalized_date,
        )
        # Heuristic: in phrases like "miércoles que viene 14 pasar..." the
        # trailing 14 is almost always an hour, not day-of-month. Preserve
        # explicit calendar intent for values > 23 (e.g. "mie 26").
        if weekday_num_at_end and int(weekday_num_at_end.group("num")) <= 23:
            reminder = weekday_num_at_end.group("num")
            date_text = date_text[: date_text.lower().rfind(weekday_num_at_end.group("num"))].strip()
            normalized_date = normalize_date_text(date_text)
        time_match = TIME_PREFIX_RE.match(remainder)
        if time_match:
            reminder = time_match.group("time")
            remainder = remainder[time_match.end():].strip(" ,-:")
        remainder = re.sub(r"^(?:a\.?m\.?|p\.?m\.?)\s*", "", remainder, flags=re.IGNORECASE).strip()
        if not remainder:
            raise ValueError("Falta el título de la tarea.")
        return date_text, reminder, remainder
    time_match = TIME_PREFIX_RE.match(s)
    if time_match:
        reminder = time_match.group("time")
        title = s[time_match.end():].strip(" ,-:")
        title = re.sub(r"^(?:a\.?m\.?|p\.?m\.?)\s*", "", title, flags=re.IGNORECASE).strip()
        if not title:
            raise ValueError("Falta el título de la tarea.")
        return "hoy", reminder, title
    if not s:
        raise ValueError("Falta el texto de la tarea.")
    return "hoy", None, s


def infer_priority(date_text: str, title: str) -> str:
    normalized_title = normalize_date_text(title)
    normalized_date = normalize_date_text(date_text)
    if any(token in normalized_title for token in ["urgente", "ya", "sin falta", "hoy si o si"]):
        return "red"
    if any(token in normalized_title for token in ["cuando pueda", "cuando se pueda", "algun dia", "algún día", "algun dia", "probamos", "probar", "sondear"]):
        return "green"
    if normalized_date in {"hoy", "today", "manana", "mañana", "tomorrow"}:
        return "red"
    if any(token in normalized_date for token in ["esta semana", "la semana que viene", "que viene", "proximo", "proxima", "prox", "siguiente"]):
        return "yellow"
    if re.fullmatch(r"en\s+\d+\s+dias?", normalized_date):
        match = re.search(r"\d+", normalized_date)
        days = int(match.group()) if match else 0
        return "red" if days <= 1 else "yellow"
    return "yellow"


def parse_task_batch(text: str) -> List[Tuple[str, Optional[str], str, Optional[str]]]:
    raw = (text or "").strip()
    if not raw:
        return []
    # Normalize A.M./P.M. spaced variants
    raw = re.sub(r"\b([ap])\s*\.\s+\s*m\s*\.", r"\1.m.", raw, flags=re.IGNORECASE)
    compact = re.sub(r"\s+", " ", raw)

    def _parsed_with_priority(chunk: str, inherited_priority: Optional[str] = None):
        part = chunk.strip()
        prio = inherited_priority
        m = PRIORITY_PREFIX_RE.match(part)
        if m:
            prio = PRIORITY_NORMALIZATION.get(normalize_date_text(m.group("prio")))
            part = part[m.end():].strip()
        date_text, reminder, title = extract_date_time_and_title(part)
        return (date_text, reminder, title, prio)

    prefix_match = re.match(r"^(?P<prefix>[^:]{1,80}):\s*(?P<rest>.+)$", compact)
    if prefix_match:
        prefix = prefix_match.group("prefix").strip()
        rest = prefix_match.group("rest").strip()
        with contextlib.suppress(BaseException):
            parse_date(prefix)
            parts = [p.strip(" -") for p in re.split(r"\s*(?:,|;|\n)\s*", rest) if p.strip(" -")]
            if len(parts) > 1:
                return [_parsed_with_priority(f"{prefix} {part}") for part in parts]
    speech_chunks = [p.strip(" -") for p in re.split(r"\s+y\s+(?:tambien|también)\s+|\s+y\s+despues\s+|\s+y\s+después\s+", compact, flags=re.IGNORECASE) if p.strip(" -")]
    if len(speech_chunks) > 1:
        parsed_chunks: List[Tuple[str, Optional[str], str, Optional[str]]] = []
        inherited_date: Optional[str] = None
        inherited_priority: Optional[str] = None
        for chunk in speech_chunks:
            try:
                parsed = _parsed_with_priority(chunk, inherited_priority)
                if inherited_date and parsed[0] == "hoy" and not any(pattern.match(chunk) for pattern in DATE_PREFIX_PATTERNS):
                    parsed = (inherited_date, parsed[1], parsed[2], parsed[3])
                inherited_date = parsed[0]
                inherited_priority = parsed[3] or inherited_priority
                parsed_chunks.append(parsed)
            except Exception:
                parsed_chunks = []
                break
        if parsed_chunks:
            return parsed_chunks
    lines = [line.strip(" -•*") for line in re.split(r"\n+", raw) if line.strip()]
    if len(lines) > 1:
        tasks: List[Tuple[str, Optional[str], str, Optional[str]]] = []
        inherited_date: Optional[str] = None
        inherited_priority: Optional[str] = None
        for line in lines:
            line = re.sub(r"^\d+[\)\.-]\s*", "", line).strip()
            if not line:
                continue
            try:
                parse_date(line)
                inherited_date = line
                continue
            except SystemExit:
                pass
            explicit_date = any(pattern.match(line) for pattern in DATE_PREFIX_PATTERNS)
            if inherited_date and REMINDER_PREFIX_RE.match(line):
                _, reminder, title = extract_date_time_and_title(line)
                tasks.append((inherited_date, reminder, title, inherited_priority))
                continue
            if inherited_date and not explicit_date:
                tasks.append(_parsed_with_priority(f"{inherited_date} {line}", inherited_priority))
                continue
            try:
                parsed = _parsed_with_priority(line, inherited_priority)
                inherited_date = parsed[0]
                inherited_priority = parsed[3] or inherited_priority
                tasks.append(parsed)
                continue
            except ValueError:
                pass
            tasks.append(_parsed_with_priority(line, inherited_priority))
        return tasks
    sentence_split = [p.strip(" -") for p in re.split(r"\s*;\s*", compact) if p.strip(" -")]
    if len(sentence_split) > 1:
        return [_parsed_with_priority(part) for part in sentence_split]
    return [_parsed_with_priority(raw)]


def parse_reminder(value: Optional[str], base_date: dt.date) -> Optional[str]:
    if not value:
        return None
    value = value.strip()
    if re.fullmatch(r"\d{1,2}:\d{2}", value):
        hh, mm = value.split(":")
        return f"{base_date.isoformat()} {int(hh):02d}:{int(mm):02d}"
    if re.fullmatch(r"\d{1,2}", value):
        return f"{base_date.isoformat()} {int(value):02d}:00"
    if re.fullmatch(r"\d{4}-\d{2}-\d{2} \d{1,2}:\d{2}", value):
        date_part, time_part = value.split()
        hh, mm = time_part.split(":")
        return f"{date_part} {int(hh):02d}:{int(mm):02d}"
    raise SystemExit(f"Reminder inválido: {value}. Usá HH, HH:MM o YYYY-MM-DD HH:MM.")


def agenda_path(vault: Path, day: dt.date) -> Path:
    return vault / "Hermes" / "Agenda" / f"{day.isoformat()}.md"


def session_path(day: dt.date) -> str:
    return f"Hermes/Sessions/{day.isoformat()}.md"


@contextlib.contextmanager
def file_lock(path: Path, timeout: float = 10.0):
    lock = path.with_suffix(path.suffix + ".lock")
    start = time.time()
    while True:
        try:
            fd = os.open(str(lock), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.write(fd, str(os.getpid()).encode())
            os.close(fd)
            break
        except FileExistsError:
            if time.time() - start > timeout:
                raise SystemExit(f"No pude obtener lock: {lock}")
            time.sleep(0.1)
    try:
        yield
    finally:
        with contextlib.suppress(FileNotFoundError):
            lock.unlink()


def agenda_template(day: dt.date, source: str = "cli") -> str:
    weekday = DAYS_ES[day.weekday()]
    return f"""---
type: agenda
date: {day.isoformat()}
owner: brain-vps
status: active
source:
  - {source}
reminders: true
reviewed-at:
summary-status: pending
linked-session: {session_path(day)}
---

# Agenda {day.isoformat()} — {weekday.capitalize()}

## 🎯 Foco del día
> _Sin definir_

## 🔴 Hoy sí o sí

_(vacío)_

## 🟡 Importante

_(vacío)_

## 🟢 Backlog

_(vacío)_

## 🔔 Recordatorios
| Hora | Tarea | Canal | Estado | ID |
|---|---|---|---|---|

## 🧠 Sesión del día
- [[{session_path(day)}]]

## ✅ Cerrado hoy

_(vacío)_

## ➡️ Arrastre sugerido para mañana

_(vacío)_
"""


def ensure_agenda(vault: Path, day: dt.date, source: str = "cli") -> Path:
    path = agenda_path(vault, day)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists() or path.stat().st_size == 0:
        path.write_text(agenda_template(day, source=source), encoding="utf-8")
    return path


def read_lines(path: Path) -> List[str]:
    return path.read_text(encoding="utf-8").splitlines()


def write_lines(path: Path, lines: List[str]) -> None:
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def find_section(lines: List[str], title: str) -> Tuple[int, int]:
    header = f"## {title}"
    start = None
    for i, line in enumerate(lines):
        if line.strip() == header:
            start = i
            break
    if start is None:
        # append missing section before end
        lines.extend(["", header, "", "_(vacío)_"])
        start = len(lines) - 4
    end = len(lines)
    for j in range(start + 1, len(lines)):
        if lines[j].startswith("## "):
            end = j
            break
    return start, end


def remove_empty_marker(lines: List[str], start: int, end: int) -> None:
    for i in range(end - 1, start, -1):
        if lines[i].strip() == "_(vacío)_":
            lines.pop(i)


def next_task_id(lines: List[str], day: dt.date) -> str:
    prefix = f"ag-{day.strftime('%Y%m%d')}-"
    max_n = 0
    for line in lines:
        m = re.search(rf"\b{re.escape(prefix)}(\d{{3}})\b", line)
        if m:
            max_n = max(max_n, int(m.group(1)))
    return f"{prefix}{max_n + 1:03d}"


def normalize_task_key(text: str) -> str:
    return normalize_date_text(re.sub(r"\s+", " ", text or "").strip())


def duplicate_task_id(lines: List[str], title: str, detail: str = "") -> Optional[str]:
    wanted = normalize_task_key(f"{title} {detail}")
    for task in iter_tasks(lines):
        if task.get("status") in {"done", "cancelled"}:
            continue
        hay = normalize_task_key(f"{task.get('title','')} {task.get('detail','')}")
        if hay == wanted:
            return task.get("id")
    return None


def append_task(lines: List[str], day: dt.date, priority: str, title: str, detail: str = "", reminder: Optional[str] = None, channel: str = "telegram", source: str = "cli", status: Optional[str] = None) -> str:
    section = PRIORITY_MAP.get(priority.lower())
    if not section:
        raise SystemExit(f"Prioridad inválida: {priority}. Usá red/yellow/green.")
    existing_id = duplicate_task_id(lines, title, detail)
    if existing_id:
        raise SystemExit(f"Tarea duplicada: {existing_id} — {title}")
    task_id = next_task_id(lines, day)
    if status is None:
        status = "pending" if not reminder else "pending"
    start, end = find_section(lines, section)
    remove_empty_marker(lines, start, end)
    start, end = find_section(lines, section)
    insert_at = end
    while insert_at > start + 1 and lines[insert_at - 1].strip() == "":
        insert_at -= 1
    title_line = f"- [ ] **{title}**" + (f" — {detail}" if detail else "")
    block = [title_line, f"  - id: {task_id}"]
    if reminder:
        block.append(f"  - reminder: {reminder}")
        block.append(f"  - channel: {channel}")
    block.append(f"  - status: {status}")
    block.append(f"  - source: {source}")
    block.append("")
    lines[insert_at:insert_at] = block
    if reminder:
        update_reminders_table(lines)
    return task_id


def iter_tasks(lines: List[str]) -> Iterable[Dict[str, str]]:
    current_section = ""
    current: Optional[Dict[str, str]] = None
    for line in lines:
        if line.startswith("## "):
            current_section = line[3:].strip()
        m = TASK_RE.match(line)
        if m:
            if current:
                yield current
            current = {
                "section": current_section,
                "check": m.group("check"),
                "title": m.group("title"),
                "detail": m.group("detail") or "",
            }
            continue
        mm = META_RE.match(line)
        if current and mm:
            current[mm.group("key")] = mm.group("value")
            continue
        if current and line and not line.startswith("  - ") and not TASK_RE.match(line):
            # keep current until next task/header; markdown noise ignored
            pass
    if current:
        yield current


def format_task(task: Dict[str, str]) -> str:
    check = "✅" if task.get("check", " ").lower() == "x" or task.get("status") == "done" else "☐"
    rid = task.get("id", "sin-id")
    reminder = f" · 🔔 {task['reminder']}" if task.get("reminder") else ""
    status = task.get("status", "pending")
    detail = f" — {task['detail']}" if task.get("detail") else ""
    return f"{check} {rid} [{status}] {task['title']}{detail}{reminder}"


def list_agenda(vault: Path, day: dt.date) -> str:
    path = ensure_agenda(vault, day)
    tasks = [t for t in iter_tasks(read_lines(path)) if t.get("status") not in {"cancelled"}]
    if not tasks:
        return f"Agenda {day.isoformat()}: sin tareas.\nArchivo: {path}"
    grouped: Dict[str, List[str]] = {s: [] for s in SECTIONS}
    for task in tasks:
        if task.get("section") in grouped:
            grouped[task["section"]].append(format_task(task))
    out = [f"Agenda {day.isoformat()}"]
    for section in SECTIONS:
        out.append(f"\n{section}")
        out.extend(grouped[section] or ["(vacío)"])
    out.append(f"\nArchivo: {path}")
    return "\n".join(out)


def locate_task(lines: List[str], task_ref: str) -> Tuple[int, int, Dict[str, str]]:
    """Return task line index, block end index, task dict by ID or title substring."""
    lower_ref = task_ref.lower()
    current_section = ""
    i = 0
    while i < len(lines):
        if lines[i].startswith("## "):
            current_section = lines[i][3:].strip()
            i += 1
            continue
        m = TASK_RE.match(lines[i])
        if not m:
            i += 1
            continue
        block_end = i + 1
        task = {"section": current_section, "check": m.group("check"), "title": m.group("title"), "detail": m.group("detail") or ""}
        while block_end < len(lines) and (lines[block_end].startswith("  - ") or lines[block_end].strip() == ""):
            mm = META_RE.match(lines[block_end])
            if mm:
                task[mm.group("key")] = mm.group("value")
            block_end += 1
            if block_end < len(lines) and TASK_RE.match(lines[block_end]):
                break
        haystack = " ".join([task.get("id", ""), task.get("title", ""), task.get("detail", "")]).lower()
        if lower_ref in haystack:
            return i, block_end, task
        i = block_end
    raise SystemExit(f"No encontré tarea: {task_ref}")


def set_task_status(lines: List[str], task_ref: str, status: str, checkbox_done: bool = False, extra_meta: Optional[Dict[str, str]] = None) -> Dict[str, str]:
    idx, end, task = locate_task(lines, task_ref)
    lines[idx] = re.sub(r"^- \[[ xX]\]", "- [x]" if checkbox_done else "- [ ]", lines[idx])
    status_written = False
    for j in range(idx + 1, end):
        if lines[j].startswith("  - status:"):
            lines[j] = f"  - status: {status}"
            status_written = True
    insert_at = end
    if not status_written:
        lines.insert(insert_at, f"  - status: {status}")
        insert_at += 1
    if extra_meta:
        existing: Dict[str, int] = {}
        for j in range(idx + 1, min(insert_at, len(lines))):
            mm = META_RE.match(lines[j])
            if mm:
                existing[mm.group("key")] = j
        for k, v in extra_meta.items():
            if k in existing:
                lines[existing[k]] = f"  - {k}: {v}"
            else:
                lines.insert(insert_at, f"  - {k}: {v}")
                insert_at += 1
    update_reminders_table(lines)
    task["status"] = status
    return task


def remove_task_block(lines: List[str], task_ref: str) -> Dict[str, str]:
    idx, end, task = locate_task(lines, task_ref)
    del lines[idx:end]
    update_reminders_table(lines)
    return task


def cancel_task(vault: Path, day: dt.date, task_ref: str) -> str:
    path = ensure_agenda(vault, day)
    with file_lock(path):
        lines = read_lines(path)
        task = set_task_status(lines, task_ref, "cancelled", checkbox_done=False, extra_meta={"cancelled-at": now_art().strftime("%Y-%m-%d %H:%M")})
        write_lines(path, lines)
    return f"OK cancel: {task.get('id', task_ref)} — {task.get('title', '')}\nArchivo: {path}"


def move_task(vault: Path, day: dt.date, task_ref: str, target_date: str, reminder: Optional[str] = None) -> str:
    source_path = ensure_agenda(vault, day)
    target_day = parse_date(target_date)
    target_path = ensure_agenda(vault, target_day)
    first, second = sorted([source_path, target_path], key=lambda p: str(p))
    with file_lock(first):
        if second != first:
            with file_lock(second):
                return _move_task_locked(vault, day, target_day, task_ref, reminder)
        return _move_task_locked(vault, day, target_day, task_ref, reminder)


def _move_task_locked(vault: Path, source_day: dt.date, target_day: dt.date, task_ref: str, reminder: Optional[str]) -> str:
    source_path = ensure_agenda(vault, source_day)
    target_path = ensure_agenda(vault, target_day)
    source_lines = read_lines(source_path)
    target_lines = read_lines(target_path)
    _, _, task = locate_task(source_lines, task_ref)
    final_reminder = parse_reminder(reminder, target_day) if reminder else None
    if not final_reminder and task.get("reminder"):
        time_part = task["reminder"].split(" ", 1)[1] if " " in task["reminder"] else task["reminder"]
        final_reminder = parse_reminder(time_part, target_day)
    remove_task_block(source_lines, task_ref)
    priority = next((k for k, v in PRIORITY_MAP.items() if v == task.get("section")), "yellow")
    canonical_priority = priority if priority in {"red", "yellow", "green"} else "yellow"
    try:
        new_id = append_task(
            target_lines,
            target_day,
            canonical_priority,
            task.get("title", "Tarea"),
            task.get("detail", ""),
            final_reminder,
            task.get("channel", "telegram"),
            task.get("source", "cli"),
            task.get("status", "pending") if task.get("status") not in {"done", "cancelled"} else "pending",
        )
    except SystemExit as exc:
        if str(exc).startswith("Tarea duplicada:"):
            write_lines(source_path, source_lines)
            return f"SKIP move duplicate: {exc}\nArchivos: {source_path}, {target_path}"
        raise
    write_lines(source_path, source_lines)
    write_lines(target_path, target_lines)
    return f"OK move: {task.get('id', task_ref)} → {new_id}\nArchivos: {source_path}, {target_path}"


def review(vault: Path, start_day: dt.date, days: int = 7) -> str:
    rows: List[str] = []
    for offset in range(days):
        day = start_day + dt.timedelta(days=offset)
        path = ensure_agenda(vault, day)
        tasks = [t for t in iter_tasks(read_lines(path)) if t.get("status") not in {"done", "cancelled"}]
        for task in tasks:
            if task.get("reminder"):
                rows.append(f"- {task.get('reminder')} · {task.get('title')} · {task.get('status','pending')} · {task.get('id','sin-id')}")
    if not rows:
        return f"Sin recordatorios próximos desde {start_day.isoformat()}."
    return "\n".join([f"Próximos recordatorios desde {start_day.isoformat()}:", *rows])


def week_summary(vault: Path, start_day: dt.date) -> str:
    rows: List[str] = [f"Agenda semana desde {start_day.isoformat()}:"]
    for offset in range(7):
        day = start_day + dt.timedelta(days=offset)
        path = ensure_agenda(vault, day)
        tasks = [t for t in iter_tasks(read_lines(path)) if t.get("status") not in {"done", "cancelled"}]
        count = len(tasks)
        top = tasks[0].get("title") if tasks else "sin tareas"
        rows.append(f"- {day.isoformat()} · {count} abiertas · {top}")
    return "\n".join(rows)


def edit_task(vault: Path, day: dt.date, task_ref: str, new_title: str, new_detail: str = "") -> str:
    path = ensure_agenda(vault, day)
    with file_lock(path):
        lines = read_lines(path)
        idx, _, task = locate_task(lines, task_ref)
        detail = new_detail.strip() or task.get("detail", "")
        lines[idx] = f"- [{'x' if task.get('check',' ').lower() == 'x' else ' '}] **{new_title}**" + (f" — {detail}" if detail else "")
        update_reminders_table(lines)
        write_lines(path, lines)
    return f"OK edit: {task.get('id', task_ref)} — {new_title}\nArchivo: {path}"


def pending_tasks(vault: Path, start_day: dt.date, days: int = 30) -> str:
    rows: List[str] = []
    for offset in range(days):
        day = start_day + dt.timedelta(days=offset)
        path = ensure_agenda(vault, day)
        tasks = [t for t in iter_tasks(read_lines(path)) if t.get("status") not in {"done", "cancelled"} and t.get("check", " ").lower() != "x"]
        for task in tasks:
            reminder = f" · {task.get('reminder')}" if task.get("reminder") else ""
            rows.append(f"- {day.isoformat()} · {task.get('id','sin-id')} · {task.get('title')}{reminder}")
    if not rows:
        return f"Sin tareas pendientes desde {start_day.isoformat()}."
    return "\n".join([f"Pendientes desde {start_day.isoformat()}:", *rows])


def task_detail(vault: Path, day: dt.date, task_ref: str) -> str:
    path = ensure_agenda(vault, day)
    _, _, task = locate_task(read_lines(path), task_ref)
    lines = [
        f"Detalle {task.get('id', task_ref)}:",
        f"- título: {task.get('title','')}",
        f"- detalle: {task.get('detail','') or '(vacío)'}",
        f"- sección: {task.get('section','')}",
        f"- estado: {task.get('status','pending')}",
    ]
    if task.get("reminder"):
        lines.append(f"- reminder: {task['reminder']}")
    if task.get("channel"):
        lines.append(f"- canal: {task['channel']}")
    if task.get("source"):
        lines.append(f"- source: {task['source']}")
    lines.append(f"Archivo: {path}")
    return "\n".join(lines)


def set_task_priority(vault: Path, day: dt.date, task_ref: str, new_priority: str) -> str:
    path = ensure_agenda(vault, day)
    canonical = PRIORITY_NORMALIZATION.get(normalize_date_text(new_priority), new_priority.lower())
    if canonical not in {"red", "yellow", "green"}:
        raise SystemExit("Prioridad inválida. Usá rojo/amarillo/verde.")
    with file_lock(path):
        lines = read_lines(path)
        _, _, task = locate_task(lines, task_ref)
        reminder = task.get("reminder")
        remove_task_block(lines, task_ref)
        new_id = append_task(
            lines,
            day,
            canonical,
            task.get("title", "Tarea"),
            task.get("detail", ""),
            reminder,
            task.get("channel", "telegram"),
            task.get("source", "cli"),
            task.get("status", "pending"),
        )
        write_lines(path, lines)
    return f"OK prioridad: {task.get('id', task_ref)} → {new_id} ({canonical})\nArchivo: {path}"


def cleanup_agenda(vault: Path, day: dt.date) -> str:
    path = ensure_agenda(vault, day)
    with file_lock(path):
        lines = read_lines(path)
        removed = 0
        i = 0
        while i < len(lines):
            m = TASK_RE.match(lines[i])
            if not m:
                i += 1
                continue
            end = i + 1
            task = {"check": m.group("check"), "title": m.group("title"), "detail": m.group("detail") or ""}
            while end < len(lines) and (lines[end].startswith("  - ") or lines[end].strip() == ""):
                mm = META_RE.match(lines[end])
                if mm:
                    task[mm.group("key")] = mm.group("value")
                end += 1
                if end < len(lines) and TASK_RE.match(lines[end]):
                    break
            status = task.get("status", "pending")
            checked_done = task.get("check", " ").lower() == "x"
            if status == "cancelled" or checked_done or status == "done":
                del lines[i:end]
                removed += 1
                continue
            i = end
        update_reminders_table(lines)
        write_lines(path, lines)
    return f"OK limpiar: removí {removed} tareas cerradas/canceladas\nArchivo: {path}"


def done_task(vault: Path, day: dt.date, task_ref: str) -> str:
    path = ensure_agenda(vault, day)
    with file_lock(path):
        lines = read_lines(path)
        task = set_task_status(lines, task_ref, "done", checkbox_done=True, extra_meta={"done-at": now_art().strftime("%Y-%m-%d %H:%M")})
        add_closed_entry(lines, task)
        write_lines(path, lines)
    return f"OK done: {task.get('id', task_ref)} — {task.get('title', '')}\nArchivo: {path}"


def add_closed_entry(lines: List[str], task: Dict[str, str]) -> None:
    start, end = find_section(lines, "✅ Cerrado hoy")
    remove_empty_marker(lines, start, end)
    start, end = find_section(lines, "✅ Cerrado hoy")
    entry = f"- [x] **{task.get('title', 'Tarea')}** — marcado done {now_art().strftime('%H:%M')} ({task.get('id', 'sin-id')})"
    if entry not in lines[start:end]:
        lines.insert(end, entry)


def snooze_task(vault: Path, day: dt.date, task_ref: str, reminder: str) -> str:
    path = ensure_agenda(vault, day)
    new_reminder = parse_reminder(reminder, day)
    with file_lock(path):
        lines = read_lines(path)
        task = set_task_status(lines, task_ref, "snoozed", checkbox_done=False, extra_meta={"reminder": new_reminder or "", "channel": task_channel(lines, task_ref) or "telegram"})
        write_lines(path, lines)
    return f"OK snooze: {task.get('id', task_ref)} → {new_reminder}\nArchivo: {path}"


def task_channel(lines: List[str], task_ref: str) -> Optional[str]:
    try:
        _, _, task = locate_task(lines, task_ref)
        return task.get("channel")
    except SystemExit:
        return None


def update_reminders_table(lines: List[str]) -> None:
    start, end = find_section(lines, "🔔 Recordatorios")
    header = ["## 🔔 Recordatorios", "| Hora | Tarea | Canal | Estado | ID |", "|---|---|---|---|---|"]
    rows = []
    for task in iter_tasks(lines):
        if task.get("reminder"):
            time_part = task["reminder"].split(" ", 1)[1] if " " in task["reminder"] else task["reminder"]
            rows.append(f"| {time_part} | {task.get('title','')} | {task.get('channel','telegram')} | {task.get('status','pending')} | {task.get('id','sin-id')} |")
    lines[start:end] = header + rows + [""]


def add_task_cmd(args: argparse.Namespace) -> str:
    vault = Path(args.vault)
    day = parse_date(args.date)
    reminder = parse_reminder(args.reminder, day)
    path = ensure_agenda(vault, day, source=args.source)
    with file_lock(path):
        lines = read_lines(path)
        try:
            tid = append_task(lines, day, args.priority, args.title, args.detail or "", reminder, args.channel, args.source, args.status)
        except SystemExit as exc:
            if str(exc).startswith("Tarea duplicada:"):
                return f"SKIP duplicate: {exc}\nArchivo: {path}"
            raise
        write_lines(path, lines)
    return f"OK add: {tid} — {args.title}\nArchivo: {path}"


def focus(vault: Path, day: dt.date) -> str:
    path = ensure_agenda(vault, day)
    tasks = [t for t in iter_tasks(read_lines(path)) if t.get("status") not in {"done", "cancelled"} and t.get("check", " ").lower() != "x"]
    for section in SECTIONS:
        for task in tasks:
            if task.get("section") == section:
                return f"🎯 Foco {day.isoformat()}: {task.get('title')} ({task.get('id','sin-id')})\nArchivo: {path}"
    return f"🎯 Foco {day.isoformat()}: sin tareas abiertas.\nArchivo: {path}"


def reminders(vault: Path, day: dt.date) -> str:
    path = ensure_agenda(vault, day)
    items = [t for t in iter_tasks(read_lines(path)) if t.get("reminder")]
    if not items:
        return f"Sin recordatorios para {day.isoformat()}.\nArchivo: {path}"
    lines = [f"Recordatorios {day.isoformat()}:"]
    lines.extend(f"- {t.get('reminder')} · {t.get('title')} · {t.get('status','pending')} · {t.get('id','sin-id')}" for t in items)
    lines.append(f"Archivo: {path}")
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Hermes Agenda V2 CLI")
    p.add_argument("--vault", default=str(DEFAULT_VAULT), help="Path al obsidian-vault")
    sub = p.add_subparsers(dest="cmd", required=True)

    for name in ["today", "tomorrow", "list", "ensure", "focus", "reminders", "review", "week", "pending", "detail", "cleanup"]:
        sp = sub.add_parser(name)
        if name in {"list", "ensure", "focus", "reminders", "review", "week", "pending", "detail", "cleanup"}:
            sp.add_argument("--date", default="hoy")

    add = sub.add_parser("add")
    add.add_argument("--date", default="hoy")
    add.add_argument("--priority", default="yellow")
    add.add_argument("--title", required=True)
    add.add_argument("--detail", default="")
    add.add_argument("--reminder")
    add.add_argument("--channel", default="telegram")
    add.add_argument("--source", default="cli")
    add.add_argument("--status", choices=["pending", "scheduled", "sent", "done", "cancelled", "snoozed"], default=None)

    done = sub.add_parser("done")
    done.add_argument("task_ref")
    done.add_argument("--date", default="hoy")

    snooze = sub.add_parser("snooze")
    snooze.add_argument("task_ref")
    snooze.add_argument("reminder")
    snooze.add_argument("--date", default="hoy")

    cancel = sub.add_parser("cancel")
    cancel.add_argument("task_ref")
    cancel.add_argument("--date", default="hoy")

    move = sub.add_parser("move")
    move.add_argument("task_ref")
    move.add_argument("target_date")
    move.add_argument("--date", default="hoy")
    move.add_argument("--reminder")

    priority = sub.add_parser("priority")
    priority.add_argument("task_ref")
    priority.add_argument("new_priority")
    priority.add_argument("--date", default="hoy")

    detail = sub.add_parser("detail")
    detail.add_argument("task_ref")
    detail.add_argument("--date", default="hoy")

    edit = sub.add_parser("edit")
    edit.add_argument("task_ref")
    edit.add_argument("new_title")
    edit.add_argument("--date", default="hoy")
    edit.add_argument("--detail", default="")
    return p


def main(argv: Optional[List[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    vault = Path(args.vault)
    if args.cmd == "today":
        print(list_agenda(vault, now_art().date()))
    elif args.cmd == "tomorrow":
        print(list_agenda(vault, now_art().date() + dt.timedelta(days=1)))
    elif args.cmd == "list":
        print(list_agenda(vault, parse_date(args.date)))
    elif args.cmd == "ensure":
        day = parse_date(args.date)
        print(ensure_agenda(vault, day))
    elif args.cmd == "add":
        print(add_task_cmd(args))
    elif args.cmd == "done":
        print(done_task(vault, parse_date(args.date), args.task_ref))
    elif args.cmd == "snooze":
        print(snooze_task(vault, parse_date(args.date), args.task_ref, args.reminder))
    elif args.cmd == "cancel":
        print(cancel_task(vault, parse_date(args.date), args.task_ref))
    elif args.cmd == "move":
        print(move_task(vault, parse_date(args.date), args.task_ref, args.target_date, args.reminder))
    elif args.cmd == "priority":
        print(set_task_priority(vault, parse_date(args.date), args.task_ref, args.new_priority))
    elif args.cmd == "detail":
        print(task_detail(vault, parse_date(args.date), args.task_ref))
    elif args.cmd == "edit":
        print(edit_task(vault, parse_date(args.date), args.task_ref, args.new_title, args.detail))
    elif args.cmd == "focus":
        print(focus(vault, parse_date(args.date)))
    elif args.cmd == "reminders":
        print(reminders(vault, parse_date(args.date)))
    elif args.cmd == "review":
        print(review(vault, parse_date(args.date)))
    elif args.cmd == "week":
        print(week_summary(vault, parse_date(args.date)))
    elif args.cmd == "pending":
        print(pending_tasks(vault, parse_date(args.date)))
    elif args.cmd == "cleanup":
        print(cleanup_agenda(vault, parse_date(args.date)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

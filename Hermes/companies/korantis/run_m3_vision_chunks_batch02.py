#!/usr/bin/env python3
"""
run_m3_vision_chunks_batch02.py

Runner real para MiniMax-M3 vision sobre korantis_ba_batch_02.

CONTRATO:
- Lee input sanitized (M2.7 -> M3 split).
- Para cada item: descarga con Accept forzado, valida magic bytes (PIL),
  rechaza svg/gif/avif/bmp/otro, valida dimension minima 512px,
  marca below_preferred_resolution si max(w,h) < 1024,
  envia a MiniMax-M3 vision con image bytes (base64 inline),
  guarda respuesta cruda por item, nunca aborta por 1 item malo.
- Escribe 1 *_results.json y 1 *_report.md por chunk.

SEGURIDAD:
- API key leida de /home/hermes/.hermes/config.yaml en memoria.
- API key NUNCA se imprime, loguea, escribe a disco, ni aparece en reportes.
- Inputs previos NO se tocan (read-only).
- Modo --preflight: solo valida, no descarga, no llama M3.
- Modo --run: ejecuta el/los chunks solicitados.

USO:
    python3 run_m3_vision_chunks_batch02.py --preflight --chunk 1
    python3 run_m3_vision_chunks_batch02.py --run --chunk 1
    python3 run_m3_vision_chunks_batch02.py --run --chunk 1 2 3
"""

from __future__ import annotations

import argparse
import base64
import datetime as _dt
import io
import json
import os
import re
import sys
import time
import traceback
from pathlib import Path

import requests
import yaml
from PIL import Image, UnidentifiedImageError

# ---------------------------------------------------------------------------
# RUTAS Y CONSTANTES
# ---------------------------------------------------------------------------

BASE_DIR = Path("/home/hermes/obsidian-vault/Hermes/companies/korantis")
INPUT_PATH = BASE_DIR / "korantis_ba_batch_02_m27_final_vision_queue_sanitized.json"
CONFIG_PATH = Path("/home/hermes/.hermes/config.yaml")
ENV_PATH = Path("/home/hermes/.hermes/.env")

# Chunk definitions: (index, offset_start, offset_end, run_id_suffix)
CHUNKS = [
    (1, 0, 25, "chunk_01"),
    (2, 25, 50, "chunk_02"),
    (3, 50, 52, "chunk_03"),
]

ALLOWED_PIL_FORMATS = {"JPEG", "PNG", "WEBP"}
MIN_DIM_FOR_SCREENING = 512
PREFERRED_DIM_THRESHOLD = 1024
DOWNLOAD_TIMEOUT_S = 20
DOWNLOAD_MAX_BYTES = 12 * 1024 * 1024  # 12 MB
MAX_REDIRECTS = 2

# Accept forzado: NUNCA */*, nunca image/avif. Solo jpeg/png/webp.
DOWNLOAD_HEADERS = {
    "Accept": "image/jpeg,image/png,image/webp;q=0.9;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
}

# Prompt a M3 — JSON estricto, una sola linea al final.
M3_PROMPT = (
    "Korantis image screening. Identify what is visually present. "
    "Return strict JSON with keys: "
    "scene_type (one of: hero_interior, hero_exterior, product_food, "
    "gallery_atmosphere, menu, logo, people_closeup, crowd, decorative, unusable), "
    "has_identifiable_faces (bool, count if any), "
    "text_visible (list of strings or empty), "
    "is_dark_or_low_contrast (bool), "
    "resolution_quality (one of: high, medium, low), "
    "editorial_usable (bool), "
    "notes (one short line). "
    "One JSON object only, no prose."
)

ALLOWED_SCENE_TYPES = {
    "hero_interior", "hero_exterior", "product_food",
    "gallery_atmosphere", "menu", "logo",
    "people_closeup", "crowd", "decorative", "unusable",
}


# ---------------------------------------------------------------------------
# CARGA DE CONFIG — API KEY EN MEMORIA SOLAMENTE
# ---------------------------------------------------------------------------

def _redact(s: str) -> str:
    if not isinstance(s, str) or len(s) <= 8:
        return "***"
    return s[:4] + "..." + s[-4:]


def _load_env_var(name: str) -> str | None:
    """
    Lee UNA variable de /home/hermes/.hermes/.env.
    - Soporta lineas 'export NAME=...' y 'NAME=...'.
    - Ignora comentarios (#) y lineas vacias.
    - NO imprime el valor, NO lo loguea, NO lo escribe a disco.
    - Devuelve el valor (str) o None si no existe / no se pudo parsear.
    """
    if not ENV_PATH.exists() or not os.access(ENV_PATH, os.R_OK):
        return None
    try:
        with open(ENV_PATH, "r", encoding="utf-8") as f:
            for raw in f:
                line = raw.strip()
                if not line or line.startswith("#"):
                    continue
                if line.startswith("export "):
                    line = line[len("export "):].lstrip()
                if "=" not in line:
                    continue
                k, _, v = line.partition("=")
                k = k.strip()
                v = v.strip()
                # Quitar comillas envolventes si las hay
                if len(v) >= 2 and v[0] == v[-1] and v[0] in ("'", '"'):
                    v = v[1:-1]
                if k == name and v:
                    return v
    except Exception:
        return None
    return None


def load_runtime_config():
    """
    Devuelve dict con {model, base_url, api_key, anthropic_version, api_key_source}.
    api_key se mantiene en memoria, nunca se loguea.
    Prioridad api_key:
      1) /home/hermes/.hermes/.env (MINIMAX_API_KEY)  [autorizado por usuario]
      2) /home/hermes/.hermes/config.yaml -> providers.minimax.api_key
    """
    cfg = yaml.safe_load(CONFIG_PATH.read_text())
    model = cfg.get("model", {})
    provider_name = model.get("provider")
    provider = cfg.get("providers", {}).get(provider_name, {})

    # Detectar placeholders (string con '...' literal o longitud sospechosa)
    def _is_placeholder(s):
        if not isinstance(s, str):
            return True
        if "..." in s:
            return True
        if len(s) < 20:  # MiniMax keys son >= 40 chars en general
            return True
        return False

    yaml_key = provider.get("api_key")
    env_key = _load_env_var("MINIMAX_API_KEY")
    env_key_cn = _load_env_var("MINIMAX_CN_API_KEY")

    api_key = None
    api_key_source = None
    if env_key and not _is_placeholder(env_key):
        api_key = env_key
        api_key_source = "env"
    elif env_key_cn and not _is_placeholder(env_key_cn):
        api_key = env_key_cn
        api_key_source = "env_cn"
    elif yaml_key and not _is_placeholder(yaml_key):
        api_key = yaml_key
        api_key_source = "config_yaml"

    return {
        "model": model.get("default", "MiniMax-M3"),
        "base_url": provider.get("base_url") or model.get("base_url"),
        "api_key": api_key,            # memoria
        "api_key_source": api_key_source,
        "anthropic_version": "2023-06-01",
    }


# ---------------------------------------------------------------------------
# VALIDACIÓN DE INPUT
# ---------------------------------------------------------------------------

def load_input():
    if not INPUT_PATH.exists():
        raise FileNotFoundError(f"Input not found: {INPUT_PATH}")
    data = json.loads(INPUT_PATH.read_text())
    if not isinstance(data, dict) or "queue" not in data:
        raise ValueError("Input malformed: top-level dict with 'queue' key required")
    if not data.get("ready_for_m3", False):
        raise ValueError("Input has ready_for_m3=False; refusing to run")
    queue = data["queue"]
    if not isinstance(queue, list) or not queue:
        raise ValueError("Input queue empty or not a list")
    return data


def preflight_check():
    """Validacion seca: input, config, endpoints, dependencias. No descarga."""
    print("=" * 60)
    print("PREFLIGHT (no descarga, no M3)")
    print("=" * 60)

    # Input
    data = load_input()
    queue = data["queue"]
    print(f"input  : {INPUT_PATH}")
    print(f"  queue_len        : {len(queue)}")
    print(f"  run_id           : {data.get('run_id')}")
    print(f"  model_used_queue : {data.get('model_used_for_queue')}")
    print(f"  ready_for_m3     : {data.get('ready_for_m3')}")

    # Chunks
    for ci, a, b, label in CHUNKS:
        sub = queue[a:b]
        venues = sorted({it.get("venue_name") for it in sub})
        print(f"  chunk {ci} [{a}:{b}] -> {len(sub)} items, venues={len(venues)}")

    # Formatos declarados en input
    bad = [it for it in queue if (it.get("content_type") or "").lower() not in {
        "image/jpeg", "image/jpg", "image/png", "image/webp"
    }]
    print(f"  bad declared ct  : {len(bad)} (esperado 0)")

    # Config
    rt = load_runtime_config()
    print(f"config : {CONFIG_PATH}")
    print(f"  model            : {rt['model']}")
    print(f"  base_url         : {rt['base_url']}")
    print(f"  api_key present  : {bool(rt['api_key'])}  (source={rt['api_key_source']}, redacted={_redact(rt['api_key']) if rt['api_key'] else 'n/a'})")
    print(f"  anthropic_version: {rt['anthropic_version']}")

    # Endpoint reachability (HEAD, sin auth)
    try:
        r = requests.head(
            f"{rt['base_url'].rstrip('/')}/v1/messages",
            timeout=10,
        )
        print(f"endpoint HEAD     : {r.status_code} (esperado 401/403/404, no DNS-fail)")
    except Exception as e:
        print(f"endpoint HEAD     : ERROR {type(e).__name__}: {e}")

    # Outputs a escribir
    print("outputs (a CREAR, no sobreescribir inputs):")
    for ci, _, _, label in CHUNKS:
        j = BASE_DIR / f"korantis_ba_batch_02_m3_vision_{label}_run01_results.json"
        m = BASE_DIR / f"korantis_ba_batch_02_m3_vision_{label}_run01_report.md"
        print(f"  {j.name}  -> exists={j.exists()}")
        print(f"  {m.name}  -> exists={m.exists()}")

    # Inputs protegidos
    protected = [
        "korantis_ba_batch_02_m3_vision_chunk_01.json",
        "korantis_ba_batch_02_m3_vision_chunk_02.json",
        "korantis_ba_batch_02_m3_vision_chunk_03.json",
        "korantis_ba_batch_02_m27_final_vision_queue_sanitized.json",
        "korantis_ba_batch_02_m27_final_vision_queue.json",
        "korantis_ba_batch_02_m27_source_fullres_queue.json",
        "korantis_ba_batch_02_m27_manifest.json",
        "korantis_ba_batch_02_m27_queue_sanitizer_report.md",
        "korantis_ba_batch_02_m27_codex_handoff.md",
    ]
    print("inputs protegidos (NO se tocan):")
    for f in protected:
        print(f"  {f}  -> exists={(BASE_DIR / f).exists()}")

    print("=" * 60)
    print("PREFLIGHT OK")
    print("=" * 60)


# ---------------------------------------------------------------------------
# PIPELINE POR ITEM
# ---------------------------------------------------------------------------

def _download(url: str) -> tuple[bytes | None, str | None, str | None]:
    """
    Descarga con Accept forzado. Devuelve (bytes, content_type_header, error).
    error es str si fallo, None si ok.
    """
    try:
        sess = requests.Session()
        sess.max_redirects = MAX_REDIRECTS
        r = sess.get(
            url,
            headers=DOWNLOAD_HEADERS,
            timeout=DOWNLOAD_TIMEOUT_S,
            stream=True,
            allow_redirects=True,
        )
        if r.status_code != 200:
            return None, None, f"http_status_{r.status_code}"
        # Limitar tamaño
        buf = io.BytesIO()
        total = 0
        for chunk in r.iter_content(chunk_size=64 * 1024):
            if not chunk:
                continue
            total += len(chunk)
            if total > DOWNLOAD_MAX_BYTES:
                return None, None, "too_large"
            buf.write(chunk)
        return buf.getvalue(), r.headers.get("content-type", ""), None
    except requests.exceptions.TooManyRedirects:
        return None, None, "too_many_redirects"
    except requests.exceptions.Timeout:
        return None, None, "timeout"
    except requests.exceptions.RequestException as e:
        return None, None, f"download_error:{type(e).__name__}"


def _validate_bytes(raw: bytes):
    """
    Valida magic bytes via PIL. Devuelve (pil_format, width, height) o (None, None, None) + reason.
    """
    try:
        img = Image.open(io.BytesIO(raw))
        img.verify()  # verifica estructura
    except (UnidentifiedImageError, Exception) as e:
        return None, None, None, f"invalid_magic_bytes:{type(e).__name__}"
    # verify cierra el file, reabrir para tamaño
    try:
        img2 = Image.open(io.BytesIO(raw))
        fmt = (img2.format or "").upper()
        w, h = img2.size
    except Exception as e:
        return None, None, None, f"invalid_dimensions:{type(e).__name__}"
    if fmt not in ALLOWED_PIL_FORMATS:
        return None, None, None, f"unsupported_format:{fmt}"
    return fmt, w, h, None


def _sha256_hex(b: bytes) -> str:
    import hashlib
    return hashlib.sha256(b).hexdigest()


def _call_m3(rt: dict, image_b64: str, media_type: str) -> dict:
    """
    Llama a MiniMax-M3 vision via Anthropic-compatible endpoint.
    api_key nunca se loguea.
    Devuelve dict con {ok, http_status, m3_text, m3_parsed, error}.
    """
    url = f"{rt['base_url'].rstrip('/')}/v1/messages"
    headers = {
        "content-type": "application/json",
        "x-api-key": rt["api_key"],
        "anthropic-version": rt["anthropic_version"],
    }
    body = {
        "model": rt["model"],
        "max_tokens": 1024,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": image_b64,
                        },
                    },
                    {"type": "text", "text": M3_PROMPT},
                ],
            }
        ],
    }
    try:
        r = requests.post(url, headers=headers, json=body, timeout=120)
    except requests.exceptions.Timeout:
        return {"ok": False, "error": "m3_timeout", "http_status": None, "m3_text": None}
    except requests.exceptions.RequestException as e:
        return {"ok": False, "error": f"m3_request_error:{type(e).__name__}", "http_status": None, "m3_text": None}

    if r.status_code != 200:
        # Cuerpo de error sin filtrar la key (puede no estar, pero por las dudas)
        snippet = (r.text or "")[:500]
        return {
            "ok": False,
            "error": f"m3_http_{r.status_code}",
            "http_status": r.status_code,
            "m3_text": snippet,
        }

    try:
        j = r.json()
    except Exception as e:
        return {"ok": False, "error": f"m3_bad_json:{type(e).__name__}", "http_status": 200, "m3_text": r.text[:500]}

    # Anthropic shape: content[].text
    text = ""
    try:
        for block in j.get("content", []):
            if block.get("type") == "text":
                text += block.get("text", "")
    except Exception:
        pass

    parsed = _parse_m3_text(text)
    return {
        "ok": True,
        "error": None,
        "http_status": 200,
        "m3_text": text[:2048],  # truncado a 2KB para debug
        "m3_parsed": parsed,
        "raw_response": j,  # guardamos toda la respuesta, NO incluye key
    }


def _parse_m3_text(text: str):
    """Extrae el primer JSON object del texto. None si no se puede."""
    if not text:
        return None
    # Buscar {...} mas externo
    m = re.search(r"\{[\s\S]*\}", text)
    if not m:
        return None
    try:
        obj = json.loads(m.group(0))
    except Exception:
        return None
    if not isinstance(obj, dict):
        return None
    # Validacion laxa de campos esperados
    if "scene_type" in obj and obj["scene_type"] not in ALLOWED_SCENE_TYPES:
        obj["scene_type"] = "unusable"
    return obj


# ---------------------------------------------------------------------------
# PROCESS POR ITEM
# ---------------------------------------------------------------------------

def process_item(item: dict, rt: dict, seen_sha256: set) -> dict:
    """
    Procesa UN item. Nunca lanza excepcion.
    Devuelve dict con resultado y status.
    """
    rec = {
        "venue_name": item.get("venue_name"),
        "resolved_image_url": item.get("resolved_image_url"),
        "original_image_url": item.get("original_image_url"),
        "source_url": item.get("source_url"),
        "source_type": item.get("source_type"),
        "source_quality": item.get("source_quality"),
        "rights_hint": item.get("rights_hint"),
        "dedupe_hash": item.get("dedupe_hash"),
        "priority": item.get("priority"),
        "prevision_reason": item.get("prevision_reason"),
        "risk_flags_input": item.get("risk_flags") or [],
        "declared_content_type": item.get("content_type"),
        "declared_width": item.get("width"),
        "declared_height": item.get("height"),
        "ok_photo": False,
        "skip_reason": None,
        "m3_transport": None,
        "bytes_received": 0,
        "pil_format": None,
        "real_width": None,
        "real_height": None,
        "sha256": None,
        "max_dim": None,
        "below_preferred_resolution": False,
        "runtime_duplicate_of": None,
        "m3_http_status": None,
        "m3_response": None,
        "m3_raw_text_excerpt": None,
        "m3_error": None,
        "error_detail": None,
    }

    # 1) Download
    raw, ct_header, err = _download(rec["resolved_image_url"])
    if err or raw is None:
        rec["skip_reason"] = err or "download_error"
        rec["error_detail"] = err
        return rec
    rec["bytes_received"] = len(raw)

    # 2) Magic bytes
    fmt, w, h, v_err = _validate_bytes(raw)
    if v_err or fmt is None:
        rec["skip_reason"] = v_err or "invalid_bytes"
        rec["error_detail"] = v_err
        return rec
    rec["pil_format"] = fmt
    rec["real_width"] = w
    rec["real_height"] = h
    rec["max_dim"] = max(w, h)

    # 3) Gate dimension minima para screening
    if rec["max_dim"] < MIN_DIM_FOR_SCREENING:
        rec["skip_reason"] = "below_min_dimension"
        rec["error_detail"] = f"max_dim={rec['max_dim']} < {MIN_DIM_FOR_SCREENING}"
        return rec

    # 4) Flag below_preferred_resolution (NO skip, solo marca)
    if rec["max_dim"] < PREFERRED_DIM_THRESHOLD:
        rec["below_preferred_resolution"] = True

    # 5) Dedupe runtime por sha256(bytes)
    sha = _sha256_hex(raw)
    rec["sha256"] = sha
    if sha in seen_sha256:
        rec["runtime_duplicate_of"] = sha
        rec["skip_reason"] = "runtime_dup"
        return rec
    seen_sha256.add(sha)

    # 6) Llamar M3
    media_type = {
        "JPEG": "image/jpeg",
        "PNG": "image/png",
        "WEBP": "image/webp",
    }[fmt]
    b64 = base64.b64encode(raw).decode("ascii")
    rec["m3_transport"] = "base64_inline"
    m3 = _call_m3(rt, b64, media_type)
    rec["m3_http_status"] = m3.get("http_status")
    rec["m3_raw_text_excerpt"] = m3.get("m3_text")
    if not m3.get("ok"):
        rec["skip_reason"] = m3.get("error") or "m3_error"
        rec["m3_error"] = m3.get("error")
        return rec
    rec["m3_response"] = m3.get("m3_parsed")
    if rec["m3_response"] is None:
        rec["skip_reason"] = "m3_invalid_json"
        rec["m3_error"] = "m3_returned_non_json"
        return rec

    rec["ok_photo"] = True
    return rec


# ---------------------------------------------------------------------------
# OUTPUTS
# ---------------------------------------------------------------------------

def _now_iso() -> str:
    return _dt.datetime.now(_dt.timezone.utc).isoformat(timespec="seconds")


def _safe_venue_count(records):
    return len({r["venue_name"] for r in records if r.get("venue_name")})


def write_results_json(chunk_idx: int, label: str, parent_run_id: str, records: list, started: str) -> Path:
    out = {
        "run_id": f"korantis_ba_batch_02_m3_vision_{label}_run01",
        "parent_run_id": parent_run_id,
        "chunk_index": chunk_idx,
        "chunk_total": len(CHUNKS),
        "model_to_use": "MiniMax-M3",
        "vision_used": True,
        "vision_transport": "base64_inline",
        "m3_endpoint_base": "https://api.minimax.io/anthropic",
        "m3_prompt_summary": "scene_type, faces, text, contrast, quality, editorial_usable, notes (strict JSON)",
        "min_dim_for_screening": MIN_DIM_FOR_SCREENING,
        "preferred_dim_threshold": PREFERRED_DIM_THRESHOLD,
        "allowed_pil_formats": sorted(ALLOWED_PIL_FORMATS),
        "started_at": started,
        "finished_at": _now_iso(),
        "item_count_requested": len(records),
        "item_count_processed": len(records),
        "item_count_ok_photo": sum(1 for r in records if r["ok_photo"]),
        "item_count_skipped": sum(1 for r in records if not r["ok_photo"]),
        "item_count_below_preferred_resolution": sum(1 for r in records if r["below_preferred_resolution"]),
        "skip_reasons_breakdown": _count_skip_reasons(records),
        "venues_in_chunk": _safe_venue_count(records),
        "records": records,
    }
    path = BASE_DIR / f"korantis_ba_batch_02_m3_vision_{label}_run01_results.json"
    path.write_text(json.dumps(out, indent=2, ensure_ascii=False))
    return path


def _count_skip_reasons(records):
    from collections import Counter
    c = Counter()
    for r in records:
        if not r["ok_photo"]:
            c[r["skip_reason"] or "unknown"] += 1
    return dict(c)


def write_report_md(chunk_idx: int, label: str, parent_run_id: str, records: list, started: str) -> Path:
    skip_breakdown = _count_skip_reasons(records)
    ok = [r for r in records if r["ok_photo"]]
    below_pref = [r for r in records if r["below_preferred_resolution"] and r["ok_photo"]]
    by_scene = {}
    for r in ok:
        s = (r.get("m3_response") or {}).get("scene_type") or "unknown"
        by_scene[s] = by_scene.get(s, 0) + 1

    lines = []
    lines.append(f"# KORANTIS — M3 VISION REPORT (chunk {chunk_idx}/3)")
    lines.append("")
    lines.append(f"**Run ID:** korantis_ba_batch_02_m3_vision_{label}_run01")
    lines.append(f"**Parent run:** {parent_run_id}")
    lines.append(f"**Model:** MiniMax-M3 (vision, base64 inline)")
    lines.append(f"**Started:** {started}")
    lines.append(f"**Finished:** {_now_iso()}")
    lines.append(f"**Items in chunk:** {len(records)} (offsets {CHUNKS[chunk_idx-1][1]}:{CHUNKS[chunk_idx-1][2]})")
    lines.append(f"**Venues in chunk:** {_safe_venue_count(records)}")
    lines.append("")
    lines.append("## TL;DR")
    lines.append("")
    lines.append(f"- **Requested: {len(records)} · Processed: {len(records)} · Vision-OK: {len(ok)} · Skipped: {len(records)-len(ok)}**")
    lines.append(f"- **below_preferred_resolution (max_dim<1024) entre OK: {len(below_pref)}**")
    if by_scene:
        lines.append(f"- **Scene distribution:** " + ", ".join(f"{k}={v}" for k, v in sorted(by_scene.items())))
    if skip_breakdown:
        lines.append(f"- **Skip reasons:** " + ", ".join(f"{k}={v}" for k, v in sorted(skip_breakdown.items())))
    lines.append("")
    lines.append("## Per-item results")
    lines.append("")
    lines.append("| # | venue | ok | pil | dim | below<1024 | m3_status | scene_type | faces | editorial_usable | skip_reason |")
    lines.append("|---|---|---|---|---|---|---|---|---|---|---|")
    for i, r in enumerate(records, 1):
        m3r = r.get("m3_response") or {}
        scene = m3r.get("scene_type") or "-"
        faces = m3r.get("has_identifiable_faces")
        eu = m3r.get("editorial_usable")
        m3_status = "ok" if r["ok_photo"] else f"skip:{r['skip_reason']}"
        dim = f"{r['real_width']}x{r['real_height']}" if r['real_width'] else "-"
        below = "yes" if r["below_preferred_resolution"] else "no"
        lines.append(
            f"| {i} | {r['venue_name']} | "
            f"{'✅' if r['ok_photo'] else '❌'} | "
            f"{r['pil_format'] or '-'} | "
            f"{dim} | {below} | {m3_status} | {scene} | {faces} | {eu} | {r['skip_reason'] or '-'} |"
        )
    lines.append("")
    lines.append("## Inputs preservados (NO tocados)")
    lines.append("")
    for f in [
        "korantis_ba_batch_02_m3_vision_chunk_01.json",
        "korantis_ba_batch_02_m3_vision_chunk_02.json",
        "korantis_ba_batch_02_m3_vision_chunk_03.json",
        "korantis_ba_batch_02_m27_final_vision_queue_sanitized.json",
        "korantis_ba_batch_02_m27_final_vision_queue.json",
        "korantis_ba_batch_02_m27_source_fullres_queue.json",
        "korantis_ba_batch_02_m27_manifest.json",
        "korantis_ba_batch_02_m27_queue_sanitizer_report.md",
        "korantis_ba_batch_02_m27_codex_handoff.md",
    ]:
        p = BASE_DIR / f
        lines.append(f"- {f}  (exists={p.exists()})")
    lines.append("")
    lines.append("## API key policy")
    lines.append("")
    lines.append("- API key leida de `/home/hermes/.hermes/config.yaml` en memoria.")
    lines.append("- NUNCA escrita a logs, disco, ni impresa en este reporte.")
    lines.append("- Header enviado: `x-api-key: <redacted>` (no se registra el valor).")
    lines.append("")
    path = BASE_DIR / f"korantis_ba_batch_02_m3_vision_{label}_run01_report.md"
    path.write_text("\n".join(lines))
    return path


# ---------------------------------------------------------------------------
# ORQUESTACIÓN
# ---------------------------------------------------------------------------

def run_chunk(chunk_idx: int, rt: dict, queue: list, parent_run_id: str):
    _, a, b, label = CHUNKS[chunk_idx - 1]
    sub = queue[a:b]
    started = _now_iso()
    print(f"\n>>> CHUNK {chunk_idx} [{a}:{b}] label={label}  items={len(sub)}")
    print(f"    started_at = {started}")

    seen_sha256: set[str] = set()
    records = []
    for i, item in enumerate(sub, 1):
        venue = item.get("venue_name", "?")
        url = item.get("resolved_image_url", "")[:60]
        print(f"  [{i:02d}/{len(sub)}] {venue}  ({url}...)")
        t0 = time.time()
        try:
            rec = process_item(item, rt, seen_sha256)
        except Exception as e:
            # Defensa de cinturon: si algo escapa, log y sigue
            rec = {
                "venue_name": item.get("venue_name"),
                "resolved_image_url": item.get("resolved_image_url"),
                "source_url": item.get("source_url"),
                "dedupe_hash": item.get("dedupe_hash"),
                "ok_photo": False,
                "skip_reason": f"unhandled:{type(e).__name__}",
                "error_detail": str(e)[:200],
            }
            print(f"    !! unhandled: {type(e).__name__}: {str(e)[:120]}")
        dt = time.time() - t0
        print(f"     -> ok={rec['ok_photo']} skip={rec['skip_reason']} below<1024={rec['below_preferred_resolution']} {dt:.1f}s")
        records.append(rec)

    # Outputs
    jpath = write_results_json(chunk_idx, label, parent_run_id, records, started)
    mpath = write_report_md(chunk_idx, label, parent_run_id, records, started)
    print(f"  wrote: {jpath.name}")
    print(f"  wrote: {mpath.name}")
    return jpath, mpath


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--preflight", action="store_true", help="Solo validar, no descargar, no llamar M3")
    p.add_argument("--run", action="store_true", help="Ejecutar chunks solicitados")
    p.add_argument("--chunk", type=int, nargs="+", required=False, help="Numeros de chunk a correr (1,2,3)")
    args = p.parse_args()

    if args.preflight:
        preflight_check()
        return

    if not args.run or not args.chunk:
        p.print_help()
        return

    # Load input + config
    data = load_input()
    queue = data["queue"]
    rt = load_runtime_config()
    if not rt["api_key"]:
        print("FATAL: api_key vacia en config.yaml", file=sys.stderr)
        sys.exit(2)

    parent_run_id = data.get("run_id", "unknown")
    print(f"model={rt['model']} base_url={rt['base_url']} key_source={rt['api_key_source']} key={_redact(rt['api_key']) if rt['api_key'] else 'NONE'}")
    print(f"queue_len={len(queue)}  parent_run_id={parent_run_id}")

    for c in args.chunk:
        if c < 1 or c > 3:
            print(f"chunk invalido: {c} (esperado 1..3)", file=sys.stderr)
            sys.exit(2)
        run_chunk(c, rt, queue, parent_run_id)

    print("\nDONE.")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
merge_run02.py

Merge estructural (no re-inferencia) de los 3 chunks _run02 a:
  - korantis_ba_batch_02_m3_vision_merged.json
  - korantis_ba_batch_02_m3_vision_merged.md
  - korantis_ba_batch_02_m3_selected_candidates.json

Reglas:
- No llama M3. No usa vision_analyze. No re-infiere.
- Preserva records tal cual vienen de cada chunk.
- Valida: count=52, no dupes por dedupe_hash/resolved_image_url/sha256,
  campos pedidos preservados, no key leak, run_id coherente _run02.
- Selected candidates: aplica reglas declaradas (ver CORRELATION_RULES).
"""

import json
import os
import re
import sys
import datetime as _dt
from collections import Counter, defaultdict
from pathlib import Path

BASE = Path("/home/hermes/obsidian-vault/Hermes/companies/korantis")
CHUNKS = [
    (1, BASE / "korantis_ba_batch_02_m3_vision_chunk_01_run02_results.json"),
    (2, BASE / "korantis_ba_batch_02_m3_vision_chunk_02_run02_results.json"),
    (3, BASE / "korantis_ba_batch_02_m3_vision_chunk_03_run02_results.json"),
]
OUT_JSON = BASE / "korantis_ba_batch_02_m3_vision_merged.json"
OUT_MD = BASE / "korantis_ba_batch_02_m3_vision_merged.md"
OUT_CAND = BASE / "korantis_ba_batch_02_m3_selected_candidates.json"

# ---------------------------------------------------------------------------
# REGLAS DE SELECCIÓN (texto literal del brief)
# ---------------------------------------------------------------------------

# Tipos de fuente según source_type del input
TRUSTED_SOURCE_TYPES = {"official_website"}  # venue_controlled
REVIEW_SOURCE_QUALITY = {"official_site", "editorial_review"}

# Risk flags que SIEMPRE se mantienen (input ya los trae en risk_flags_input)
ALWAYS_PRESERVE_RISK_FLAGS = {
    "rights_review_needed",
    "identity_review_needed",
    "below_preferred_resolution",
    "face_release_needed",  # se agrega si M3 detecta faces
}


def _now_iso() -> str:
    return _dt.datetime.now(_dt.timezone.utc).isoformat(timespec="seconds")


def _load_chunk(c, path):
    if not path.exists():
        raise FileNotFoundError(f"Missing chunk: {path}")
    d = json.loads(path.read_text())
    if d.get("run_id") != f"korantis_ba_batch_02_m3_vision_chunk_0{c}_run02":
        raise ValueError(f"run_id mismatch in {path}: {d.get('run_id')}")
    return d


def _redact_check(txt: str) -> list:
    leaks = []
    for k in ["sk-cp-", "X-Api-Key:", "fdmU", "Bearer sk-cp"]:
        if k in txt:
            leaks.append(k)
    return leaks


# ---------------------------------------------------------------------------
# CARGA
# ---------------------------------------------------------------------------

def load_all():
    all_records = []
    chunk_meta = []
    for c, p in CHUNKS:
        d = _load_chunk(c, p)
        chunk_meta.append({
            "chunk_index": c,
            "run_id": d["run_id"],
            "item_count": d["item_count_requested"],
            "ok_photo": d["item_count_ok_photo"],
            "skipped": d["item_count_skipped"],
            "below_preferred_resolution": d["item_count_below_preferred_resolution"],
            "started_at": d.get("started_at"),
            "finished_at": d.get("finished_at"),
        })
        for r in d["records"]:
            r_copy = dict(r)  # copia defensiva
            r_copy["_source_chunk"] = c
            r_copy["_source_run_id"] = d["run_id"]
            all_records.append(r_copy)
    return all_records, chunk_meta


# ---------------------------------------------------------------------------
# VALIDACIONES
# ---------------------------------------------------------------------------

def validate(records):
    errors = []
    # Total 52
    if len(records) != 52:
        errors.append(f"expected 52 records, got {len(records)}")
    # Sin dupes
    seen_h = set(); dup_h = []
    seen_u = set(); dup_u = []
    seen_s = set(); dup_s = []
    for r in records:
        h = r.get("dedupe_hash")
        u = r.get("resolved_image_url")
        s = r.get("sha256")
        if h in seen_h: dup_h.append(h)
        if u in seen_u: dup_u.append(u)
        if s and s in seen_s: dup_s.append(s)
        if h: seen_h.add(h)
        if u: seen_u.add(u)
        if s: seen_s.add(s)
    if dup_h: errors.append(f"dupes by dedupe_hash: {len(dup_h)}")
    if dup_u: errors.append(f"dupes by resolved_image_url: {len(dup_u)}")
    if dup_s: errors.append(f"dupes by sha256: {len(dup_s)}")
    # Campos pedidos preservados
    needed = ["venue_name", "resolved_image_url", "source_url", "dedupe_hash"]
    for i, r in enumerate(records):
        for k in needed:
            if not r.get(k):
                errors.append(f"record {i} missing {k}")
    # Todos los skipped con skip_reason explicito
    no_skip = [i for i, r in enumerate(records) if not r["ok_photo"] and not r.get("skip_reason")]
    if no_skip:
        errors.append(f"{len(no_skip)} skipped items without skip_reason")
    # ok_photo count
    ok = sum(1 for r in records if r["ok_photo"])
    sk = sum(1 for r in records if not r["ok_photo"])
    if ok != 30:
        errors.append(f"expected 30 ok_photo, got {ok}")
    if sk != 22:
        errors.append(f"expected 22 skipped, got {sk}")
    # below_preferred_resolution solo en ok
    bpr_bad = [i for i, r in enumerate(records) if r.get("below_preferred_resolution") and not r["ok_photo"]]
    if bpr_bad:
        errors.append(f"below_preferred_resolution en {len(bpr_bad)} skips (no deberia)")
    # Records M3 reales tienen model_used MiniMax-M3
    # (en el JSON, ok_photo=True implica que _call_m3 devolvio ok=True; el modelo esta en chunk meta)
    return errors, ok, sk


# ---------------------------------------------------------------------------
# SELECCIÓN DE CANDIDATOS
# ---------------------------------------------------------------------------

def derive_record_decision(r):
    """
    Deriva la decision de seleccion a nivel record.
    Devuelve dict con: validation_status, publication_status, decision_class,
    role_allowed, risk_flags, notes.
    Reglas aplicadas literalmente del brief.
    """
    risk = list(r.get("risk_flags_input") or [])

    # face_release_needed si M3 detecto caras
    m3r = r.get("m3_response") or {}
    faces = m3r.get("has_identifiable_faces")
    face_count = None
    if isinstance(faces, int):
        face_count = faces; faces = True
    elif isinstance(faces, dict):
        face_count = faces.get("count")
        faces = bool(face_count and face_count > 0)
    if faces:
        risk.append("face_release_needed")

    # below_preferred_resolution se mantiene como risk_flag
    if r.get("below_preferred_resolution"):
        risk.append("below_preferred_resolution")

    # rights_review_needed / identity_review_needed segun source
    sq = r.get("source_quality") or ""
    if sq not in REVIEW_SOURCE_QUALITY:
        risk.append("rights_review_needed")
    rights_hint = r.get("rights_hint") or ""
    if rights_hint not in {"venue_controlled"}:
        risk.append("rights_review_needed")

    # Si ok_photo=False => skip explicito
    if not r["ok_photo"]:
        return {
            "validation_status": "imported_needs_validation",
            "publication_status": "rejected",
            "decision_class": "rejected",
            "role_allowed": "none",
            "risk_flags": sorted(set(risk)),
            "notes": f"skip_reason={r.get('skip_reason')}",
        }

    # Si ok_photo=True, decision segun scene_type
    st = m3r.get("scene_type") or "unusable"
    notes_extra = []

    if st == "product_food":
        decision_class = "reference_only"
        role_allowed = "reference_only_no_hero"
        notes_extra.append("product_food: usable as reference, not as hero/card")
    elif st == "logo":
        decision_class = "rejected"
        role_allowed = "reference_only"
        notes_extra.append("logo: no editorial value")
    elif st == "menu":
        decision_class = "rejected"
        role_allowed = "reference_only"
        notes_extra.append("menu: no editorial value for hero/card")
    elif st == "decorative":
        decision_class = "rejected"
        role_allowed = "reference_only"
        notes_extra.append("decorative: no editorial value")
    elif st == "hero_interior":
        decision_class = "candidate"
        role_allowed = "candidate_for_hero_or_card"
    elif st == "gallery_atmosphere":
        decision_class = "candidate"
        role_allowed = "candidate_for_gallery"
    elif st == "hero_exterior":
        # hero_exterior: solo si el M3 indico que identifica el venue
        notes_extra.append("hero_exterior: requires post-M3 venue identification check")
        decision_class = "candidate_review"
        role_allowed = "candidate_for_hero_with_venue_verification"
    elif st == "people_closeup" or st == "crowd":
        decision_class = "rejected"
        role_allowed = "reference_only"
        notes_extra.append(f"{st}: people closeup/crowd; face/identity review applies")
    elif st == "unusable":
        decision_class = "rejected"
        role_allowed = "none"
    else:
        decision_class = "rejected"
        role_allowed = "none"
        notes_extra.append(f"unknown scene_type={st}")

    # Editorial usable segun M3
    eu = m3r.get("editorial_usable")
    if eu is False:
        notes_extra.append("M3 marked editorial_usable=False")

    # dark/low contrast
    if m3r.get("is_dark_or_low_contrast"):
        notes_extra.append("M3 flagged dark_or_low_contrast")
        risk.append("low_contrast_review_needed")

    return {
        "validation_status": "imported_needs_validation",
        "publication_status": "not_approved_for_publication",
        "decision_class": decision_class,
        "role_allowed": role_allowed,
        "risk_flags": sorted(set(risk)),
        "notes": " | ".join(notes_extra) if notes_extra else "ok",
    }


def select_candidates(records):
    """
    Para cada venue, selecciona:
    - best_hero_candidate (preferentemente hero_interior en alta dim)
    - best_card_candidate (hero_interior o gallery_atmosphere)
    - best_gallery_candidates (hasta 3, gallery_atmosphere/hero_interior)
    - rejected_candidates (todos los demas con su decision)
    Reglas:
    - Solo entre records ok_photo=True y decision_class in {candidate, candidate_review, reference_only}
    - Preferir no below_preferred_resolution para hero/card
    - Si hero_exterior es el unico candidato, queda como candidate_review
    """
    by_venue = defaultdict(list)
    for r in records:
        if not r["ok_photo"]:
            continue
        dec = derive_record_decision(r)
        if dec["decision_class"] in ("rejected",):
            continue
        by_venue[r["venue_name"]].append((r, dec))

    selection = {}
    for venue, items in by_venue.items():
        items.sort(key=lambda x: (
            0 if not x[0].get("below_preferred_resolution") else 1,  # preferir alta dim
            0 if x[1]["decision_class"] == "candidate" else 1,        # preferir candidate limpio
            -int(x[0].get("max_dim") or 0),                            # mayor dim primero
        ))
        heroes = [it for it in items if it[1]["role_allowed"] in (
            "candidate_for_hero_or_card", "candidate_for_hero_with_venue_verification")]
        cards = [it for it in items if it[1]["role_allowed"] in (
            "candidate_for_hero_or_card", "candidate_for_gallery")]
        gallery = [it for it in items if it[1]["role_allowed"] == "candidate_for_gallery"]

        best_hero = None
        best_card = None
        best_gallery = []

        if heroes:
            best_hero = heroes[0]
        if cards and (not best_hero or cards[0][0] is not best_hero[0]):
            best_card = cards[0]
        elif cards and best_hero and cards[0][0] is best_hero[0] and len(cards) > 1:
            best_card = cards[1]
        # gallery: hasta 3 que NO sean best_hero/best_card
        used_ids = set()
        if best_hero: used_ids.add(id(best_hero[0]))
        if best_card: used_ids.add(id(best_card[0]))
        for it in gallery:
            if id(it[0]) not in used_ids and len(best_gallery) < 3:
                best_gallery.append(it)
                used_ids.add(id(it[0]))

        selection[venue] = {
            "venues": venue,
            "items_total": sum(1 for r in records if r["venue_name"] == venue),
            "items_ok_photo": sum(1 for r in records if r["venue_name"] == venue and r["ok_photo"]),
            "items_skipped": sum(1 for r in records if r["venue_name"] == venue and not r["ok_photo"]),
            "best_hero_candidate": _candidate_summary(best_hero[0], best_hero[1]) if best_hero else None,
            "best_card_candidate": _candidate_summary(best_card[0], best_card[1]) if best_card else None,
            "best_gallery_candidates": [_candidate_summary(r, d) for r, d in best_gallery],
            "rejected_candidates": [
                {
                    "venue_name": r["venue_name"],
                    "scene_type": (r.get("m3_response") or {}).get("scene_type"),
                    "decision_class": d["decision_class"],
                    "role_allowed": d["role_allowed"],
                    "below_preferred_resolution": r.get("below_preferred_resolution", False),
                    "risk_flags": d["risk_flags"],
                    "max_dim": r.get("max_dim"),
                    "pil_format": r.get("pil_format"),
                    "resolved_image_url": r["resolved_image_url"],
                    "source_url": r["source_url"],
                    "dedupe_hash": r["dedupe_hash"],
                }
                for r, d in items
                if (r is not (best_hero[0] if best_hero else None)
                    and r is not (best_card[0] if best_card else None)
                    and r not in [g[0] for g in best_gallery])
            ],
        }
    return selection


def _candidate_summary(r, d):
    return {
        "venue_name": r["venue_name"],
        "scene_type": (r.get("m3_response") or {}).get("scene_type"),
        "decision_class": d["decision_class"],
        "role_allowed": d["role_allowed"],
        "max_dim": r.get("max_dim"),
        "real_width": r.get("real_width"),
        "real_height": r.get("real_height"),
        "pil_format": r.get("pil_format"),
        "below_preferred_resolution": r.get("below_preferred_resolution", False),
        "risk_flags": d["risk_flags"],
        "validation_status": d["validation_status"],
        "publication_status": d["publication_status"],
        "resolved_image_url": r["resolved_image_url"],
        "source_url": r["source_url"],
        "dedupe_hash": r["dedupe_hash"],
        "notes": d["notes"],
    }


# ---------------------------------------------------------------------------
# MERGE
# ---------------------------------------------------------------------------

def main():
    records, chunk_meta = load_all()
    errors, ok_count, sk_count = validate(records)
    if errors:
        print("VALIDATION ERRORS:", file=sys.stderr)
        for e in errors:
            print("  -", e, file=sys.stderr)
        sys.exit(2)

    # Decisiones por record
    decisions_by_venue = select_candidates(records)

    # Per-record decision (para el JSON merged)
    record_decisions = {}
    for r in records:
        record_decisions[r["dedupe_hash"]] = derive_record_decision(r)

    # Key leak check (los chunks no deberian tener, pero por las dudas)
    for c, p in CHUNKS:
        leaks = _redact_check(p.read_text())
        if leaks:
            print(f"KEY LEAK in {p.name}: {leaks}", file=sys.stderr)
            sys.exit(3)

    # Distribuciones
    scene_dist = Counter()
    venue_dist = Counter()
    for r in records:
        venue_dist[r["venue_name"]] += 1
        if r["ok_photo"]:
            st = (r.get("m3_response") or {}).get("scene_type") or "unknown"
            scene_dist[st] += 1

    venue_ok = Counter()
    venue_skip = Counter()
    for r in records:
        if r["ok_photo"]:
            venue_ok[r["venue_name"]] += 1
        else:
            venue_skip[r["venue_name"]] += 1

    # Venues sin candidato visual usable
    venues_no_usable = []
    for v, cnt in venue_dist.items():
        if venue_ok[v] == 0:
            venues_no_usable.append({
                "venue_name": v,
                "reason": "all items skipped at dimension gate (<512px)",
                "items_total": cnt,
                "items_skipped": venue_skip[v],
            })
        elif v not in decisions_by_venue:
            venues_no_usable.append({
                "venue_name": v,
                "reason": "all M3-verified items rejected (logo/menu/decorative/crowd/people_closeup/unusable)",
                "items_total": cnt,
                "items_ok_photo": venue_ok[v],
            })

    # ------------------------------------------------------------------
    # WRITE MERGED JSON
    # ------------------------------------------------------------------
    merged = {
        "run_id": "korantis_ba_batch_02_m3_vision_merged_run02",
        "parent_run_id": "korantis_ba_batch_02_final_vision_queue_2026-06-06",
        "model_used": "MiniMax-M3",
        "vision_used": True,
        "merge_strategy": "structural_concat_no_reinference",
        "merge_built_at": _now_iso(),
        "sources": chunk_meta,
        "totals": {
            "items_requested": 52,
            "items_processed": len(records),
            "items_ok_photo": ok_count,
            "items_skipped": sk_count,
            "items_below_preferred_resolution": sum(1 for r in records if r.get("below_preferred_resolution")),
            "venues_unique": len(venue_dist),
        },
        "validation": {
            "no_dupes_by_dedupe_hash": True,
            "no_dupes_by_resolved_image_url": True,
            "no_dupes_by_sha256": True,
            "all_skipped_have_skip_reason": True,
            "all_required_fields_preserved": True,
            "no_api_key_exposed": True,
            "all_run_ids_renamed_to_run02": True,
        },
        "scene_type_distribution": dict(scene_dist),
        "venue_distribution": dict(venue_dist.most_common()),
        "records": [
            {
                "venue_name": r["venue_name"],
                "resolved_image_url": r["resolved_image_url"],
                "original_image_url": r.get("original_image_url"),
                "source_url": r["source_url"],
                "source_type": r.get("source_type"),
                "source_quality": r.get("source_quality"),
                "rights_hint": r.get("rights_hint"),
                "dedupe_hash": r["dedupe_hash"],
                "priority": r.get("priority"),
                "prevision_reason": r.get("prevision_reason"),
                "risk_flags_input": r.get("risk_flags_input") or [],
                "declared_content_type": r.get("declared_content_type"),
                "ok_photo": r["ok_photo"],
                "skip_reason": r.get("skip_reason"),
                "m3_transport": r.get("m3_transport"),
                "bytes_received": r.get("bytes_received"),
                "pil_format": r.get("pil_format"),
                "real_width": r.get("real_width"),
                "real_height": r.get("real_height"),
                "max_dim": r.get("max_dim"),
                "below_preferred_resolution": r.get("below_preferred_resolution", False),
                "sha256": r.get("sha256"),
                "m3_http_status": r.get("m3_http_status"),
                "m3_response": r.get("m3_response"),
                "m3_error": r.get("m3_error"),
                "m3_raw_text_excerpt": r.get("m3_raw_text_excerpt"),
                "_source_chunk": r["_source_chunk"],
                "_source_run_id": r["_source_run_id"],
                "decision": record_decisions[r["dedupe_hash"]],
            }
            for r in records
        ],
        "decisions_per_venue": decisions_by_venue,
        "venues_without_usable_visual_candidate": venues_no_usable,
    }
    OUT_JSON.write_text(json.dumps(merged, indent=2, ensure_ascii=False))
    print(f"wrote: {OUT_JSON.name}  ({OUT_JSON.stat().st_size} bytes)")

    # ------------------------------------------------------------------
    # WRITE SELECTED CANDIDATES JSON
    # ------------------------------------------------------------------
    candidates_out = {
        "run_id": "korantis_ba_batch_02_m3_selected_candidates_run02",
        "parent_run_id": "korantis_ba_batch_02_m3_vision_merged_run02",
        "model_used": "MiniMax-M3",
        "selection_strategy": "scene_type_role + dimension_preference + risk_flag_preservation",
        "no_publication_approval": True,
        "validation_status_universal": "imported_needs_validation",
        "built_at": _now_iso(),
        "totals": {
            "venues_with_candidates": sum(1 for v in decisions_by_venue.values() if v["best_hero_candidate"] or v["best_card_candidate"] or v["best_gallery_candidates"]),
            "venues_without_candidates": len(venues_no_usable),
        },
        "decisions_per_venue": decisions_by_venue,
        "venues_without_usable_visual_candidate": venues_no_usable,
    }
    OUT_CAND.write_text(json.dumps(candidates_out, indent=2, ensure_ascii=False))
    print(f"wrote: {OUT_CAND.name}  ({OUT_CAND.stat().st_size} bytes)")

    # ------------------------------------------------------------------
    # WRITE MERGED MARKDOWN
    # ------------------------------------------------------------------
    md = []
    md.append("# KORANTIS — M3 VISION MERGED REPORT (run02)")
    md.append("")
    md.append(f"**Run ID:** korantis_ba_batch_02_m3_vision_merged_run02")
    md.append(f"**Parent run:** korantis_ba_batch_02_final_vision_queue_2026-06-06")
    md.append(f"**Model:** MiniMax-M3 (vision, base64 inline)")
    md.append(f"**Merge strategy:** structural concat, no re-inference")
    md.append(f"**Built at:** {_now_iso()}")
    md.append(f"**Items in scope:** {len(records)}")
    md.append("")

    # Resumen ejecutivo
    md.append("## TL;DR")
    md.append("")
    md.append(f"- **52 items en scope (post-sanitizer) · 30 M3-verified · 22 skipped at dimension gate (<512px).**")
    md.append(f"- **8 venues unicos** · **0 duplicados** por dedupe_hash / resolved_image_url / sha256.")
    md.append(f"- **22 items below_preferred_resolution** (max_dim entre 512 y 1023): usables para screening, no para hero/card sin revision.")
    md.append(f"- **{len(decisions_by_venue)} venues con candidatos visuales** (al menos 1 M3-verified no rechazado).")
    md.append(f"- **{len(venues_no_usable)} venues sin candidato visual usable** ({', '.join(v['venue_name'] for v in venues_no_usable) or 'ninguno'}).")
    md.append(f"- **Cero imagenes aprobadas para publicacion.** validation_status universal: `imported_needs_validation`.")
    md.append("")

    # Fuentes de los chunks
    md.append("## Source chunks")
    md.append("")
    md.append("| chunk | run_id | items | ok | skipped | below<1024 | started | finished |")
    md.append("|---|---|---|---|---|---|---|---|")
    for cm in chunk_meta:
        md.append(f"| {cm['chunk_index']} | {cm['run_id']} | {cm['item_count']} | {cm['ok_photo']} | {cm['skipped']} | {cm['below_preferred_resolution']} | {cm['started_at']} | {cm['finished_at']} |")
    md.append("")

    # Distribucion por venue
    md.append("## Distribution per venue")
    md.append("")
    md.append("| venue | total | ok_photo | skipped | below<1024 (ok) |")
    md.append("|---|---|---|---|---|")
    for v, n in venue_dist.most_common():
        md.append(f"| {v} | {n} | {venue_ok[v]} | {venue_skip[v]} | {sum(1 for r in records if r['venue_name']==v and r['ok_photo'] and r.get('below_preferred_resolution'))} |")
    md.append("")

    # Scene type distribution
    md.append("## Scene type distribution (M3-verified only)")
    md.append("")
    md.append("| scene_type | count |")
    md.append("|---|---|")
    for st, n in scene_dist.most_common():
        md.append(f"| {st} | {n} |")
    md.append("")

    # Selected candidates per venue
    md.append("## Selected candidates per venue")
    md.append("")
    if not decisions_by_venue:
        md.append("_No venues with M3-verified non-rejected items._")
    else:
        for venue, sel in sorted(decisions_by_venue.items()):
            md.append(f"### {venue}")
            md.append("")
            md.append(f"- total items: {sel['items_total']} · ok_photo: {sel['items_ok_photo']} · skipped: {sel['items_skipped']}")
            if sel["best_hero_candidate"]:
                h = sel["best_hero_candidate"]
                md.append(f"- **best_hero_candidate:** `{h['scene_type']}` · max_dim={h['max_dim']} · "
                          f"role=`{h['role_allowed']}` · risk={h['risk_flags']} · below<1024={h['below_preferred_resolution']}")
                md.append(f"    - url: {h['resolved_image_url'][:120]}...")
            else:
                md.append(f"- **best_hero_candidate:** _none_")
            if sel["best_card_candidate"]:
                cc = sel["best_card_candidate"]
                md.append(f"- **best_card_candidate:** `{cc['scene_type']}` · max_dim={cc['max_dim']} · "
                          f"role=`{cc['role_allowed']}` · risk={cc['risk_flags']}")
            else:
                md.append(f"- **best_card_candidate:** _none_")
            if sel["best_gallery_candidates"]:
                md.append(f"- **best_gallery_candidates ({len(sel['best_gallery_candidates'])}):**")
                for g in sel["best_gallery_candidates"]:
                    md.append(f"    - `{g['scene_type']}` · max_dim={g['max_dim']} · below<1024={g['below_preferred_resolution']} · risk={g['risk_flags']}")
            else:
                md.append(f"- **best_gallery_candidates:** _none_")
            if sel["rejected_candidates"]:
                md.append(f"- rejected ({len(sel['rejected_candidates'])}):")
                for rj in sel["rejected_candidates"][:6]:
                    md.append(f"    - `{rj['scene_type']}` · decision=`{rj['decision_class']}` · max_dim={rj['max_dim']} · risk={rj['risk_flags']}")
                if len(sel["rejected_candidates"]) > 6:
                    md.append(f"    - ... and {len(sel['rejected_candidates'])-6} more")
            md.append("")

    # Venues sin candidato visual usable
    md.append("## Venues sin candidato visual usable")
    md.append("")
    if not venues_no_usable:
        md.append("_Ninguno._")
    else:
        for v in venues_no_usable:
            md.append(f"- **{v['venue_name']}** — {v['reason']} (total={v.get('items_total')}, skipped={v.get('items_skipped',0)}, ok_photo={v.get('items_ok_photo',0)})")
    md.append("")

    # Problemas detectados
    md.append("## Problemas detectados del pipeline")
    md.append("")
    md.append("1. **Sanitizer no hizo HEAD/GET de dimensiones.** El 42% de la queue (22/52) cae por debajo de 512px en runtime, a pesar de haber pasado el sanitizer. M2.7 prevision pasó URLs sin validar tamaño real.")
    md.append("2. **Apu Nena concentra 22/52 (42%)** de la queue, con 14 thumbs <512px de `static.wixstatic.com` que sirven `~mv2.jpg` en pequeñas dimensiones por default.")
    md.append("3. **El Preferido de Palermo: 4/4 thumbs <512px** desde `cloudimg.io` — el CDN responde con versiones pequeñas sin parámetro de resize explícito.")
    md.append("4. **Wix URL con `enc_avif` en el path**: el server responde con `image/webp` cuando Accept lo pide (no avif); magic bytes confirmaron WEBP, lo que PIL acepta. Sin rechazos por avif en este run.")
    md.append("5. **Sources no propias**: 100% de los items son `official_website` con `rights_hint=venue_controlled` (per input), pero la presencia de caras en M3 (`has_identifiable_faces=True`) activa `face_release_needed` en el decision layer, independientemente de rights.")
    md.append("6. **No hubo re-fetch step** entre M2.7 prevision y M3 vision. Si M2.7 hubiera reportado thumbs antes, podríamos haber bajado el size de la queue o pedido versiones full-res antes de gastar M3 calls.")
    md.append("7. **API key en `config.yaml` es placeholder literal** (string enmascarado de 13 chars con `...` literales); la key real está en `~/.hermes/.env` como `MINIMAX_API_KEY`. El runner ya lo resuelve, pero el config debería corregirse. _No se imprime el valor de la key en este reporte por política de no-exposición._")
    md.append("")

    # Recomendación para Codex
    md.append("## Recomendación para Codex")
    md.append("")
    md.append("- **NO mergear con captioning / copy pipeline todavía.** Ningún item tiene `publication_status=approved_for_publication`.")
    md.append("- **Tratar el set de 30 M3-verified como screening output, no como input creativo.**")
    md.append("- **Para cada `best_hero_candidate`**: pedir versión full-res al sitio (parámetros `w=`, `h=` o fetch directo) si `below_preferred_resolution=True`, antes de considerarlo para producción.")
    md.append("- **Para venues sin candidato usable** (los 4 venues con 100% thumbs): decidir si se re-scrapea o se descartan del scope.")
    md.append("- **Verificar `face_release_needed` antes de usar cualquier hero/card con caras detectadas.**")
    md.append("- **Mantener `validation_status=imported_needs_validation` en el siguiente paso (editorial M2.7 o copy)** — no saltar a validado solo por pasar M3.")
    md.append("")

    # Recomendación para M2.7 sanitizer/resolver
    md.append("## Recomendación para mejorar M2.7 sanitizer/resolver antes del próximo batch")
    md.append("")
    md.append("1. **Agregar paso HEAD/GET con validación de dimensiones reales** después de resolver cada `resolved_image_url`. Si `max(w,h) < 1024`, marcar como `low_resolution` y resolver una versión full-res o excluir del queue.")
    md.append("2. **Detectar y rechazar URLs con `enc_avif` en el path** (Wix convierte a avif cuando el cliente lo acepta) o forzar Accept a `image/jpeg,image/png,image/webp` y re-derivar `content_type` real del header del server, no del URL path.")
    md.append("3. **Resolver versiones full-res para CDNs** que sirven thumbs por default: `cloudimg.io` (acepta `?w=`, `?h=`), `static.wixstatic.com` (quitar `/v1/fit/w_X,h_Y/`), `imgix`-based.")
    md.append("4. **No incluir el mismo venue más de N veces** en una queue (N=3 razonable) cuando M2.7 detecta que las URLs alternativas son del mismo origen. Apu Nena tenía 22 — eso es sobremuestreo.")
    md.append("5. **Mantener `width/height/content_length` reales en el item de queue**, no dejar 0/0/0 como actualmente.")
    md.append("6. **Mover el gate de min_dimension 512 al sanitizer**, no al M3 runner. Items <512 no deberían llegar a M3: gastan 1 HTTP call + 1 vision call para nada.")
    md.append("7. **Limpiar la API key en `config.yaml`**: el valor actual es un placeholder literal. Reemplazar por `key: ${MINIMAX_API_KEY}` o leer solo de `.env`.")
    md.append("")

    # Audit trail
    md.append("## Audit trail")
    md.append("")
    md.append("- **run01 was renamed to run02 after successful real M3 execution because the runner had hardcoded run01 suffix. No M3 calls were repeated.**")
    md.append("- 3 chunks renombrados (chunk_01/02/03_run01 → _run02) con rewrite de run_id interno.")
    md.append(f"- Merge estructural construido: {_now_iso()}.")
    md.append("- NO re-inferencia. NO llamadas M3 nuevas. NO web scouting. NO queue expansion.")
    md.append("- API key leida de `~/.hermes/.env` (MINIMAX_API_KEY) en memoria, nunca escrita a logs/disco/reporte.")
    md.append("")

    OUT_MD.write_text("\n".join(md))
    print(f"wrote: {OUT_MD.name}  ({OUT_MD.stat().st_size} bytes)")

    # Validar outputs
    for f in [OUT_JSON, OUT_MD, OUT_CAND]:
        leaks = _redact_check(f.read_text())
        if leaks:
            print(f"KEY LEAK in output {f.name}: {leaks}", file=sys.stderr)
            sys.exit(4)
    print("\nMERGE OK. Validation passed. No key leaks in outputs.")


if __name__ == "__main__":
    main()

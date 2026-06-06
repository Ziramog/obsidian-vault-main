# KORANTIS — M3 VISION REPORT (chunk 3/3)

**Run ID:** korantis_ba_batch_02_m3_vision_chunk_03_run02
**Parent run:** korantis_ba_batch_02_final_vision_queue_2026-06-06
**Model:** MiniMax-M3 (vision, base64 inline)
**Started:** 2026-06-06T21:47:17+00:00
**Finished:** 2026-06-06T21:47:44+00:00
**Items in chunk:** 2 (offsets 50:52)
**Venues in chunk:** 1

## TL;DR

- **Requested: 2 · Processed: 2 · Vision-OK: 2 · Skipped: 0**
- **below_preferred_resolution (max_dim<1024) entre OK: 2**
- **Scene distribution:** product_food=2

## Per-item results

| # | venue | ok | pil | dim | below<1024 | m3_status | scene_type | faces | editorial_usable | skip_reason |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Apu Nena | ✅ | WEBP | 480x720 | yes | ok | product_food | False | True | - |
| 2 | Apu Nena | ✅ | WEBP | 480x720 | yes | ok | product_food | False | True | - |

## Inputs preservados (NO tocados)

- korantis_ba_batch_02_m3_vision_chunk_01.json  (exists=True)
- korantis_ba_batch_02_m3_vision_chunk_02.json  (exists=True)
- korantis_ba_batch_02_m3_vision_chunk_03.json  (exists=True)
- korantis_ba_batch_02_m27_final_vision_queue_sanitized.json  (exists=True)
- korantis_ba_batch_02_m27_final_vision_queue.json  (exists=True)
- korantis_ba_batch_02_m27_source_fullres_queue.json  (exists=True)
- korantis_ba_batch_02_m27_manifest.json  (exists=True)
- korantis_ba_batch_02_m27_queue_sanitizer_report.md  (exists=True)
- korantis_ba_batch_02_m27_codex_handoff.md  (exists=True)

## API key policy

- API key leida de `/home/hermes/.hermes/config.yaml` en memoria.
- NUNCA escrita a logs, disco, ni impresa en este reporte.
- Header enviado: `x-api-key: <redacted>` (no se registra el valor).


---

## Audit trail

- **run01 was renamed to run02 after successful real M3 execution because the runner had hardcoded run01 suffix. No M3 calls were repeated.**
- Rename + run_id rewrite: 2026-06-06T21:48 UTC (manual, no re-execution).
- Vision content of each record was NOT modified; only the run_id, filename, and this audit note changed.

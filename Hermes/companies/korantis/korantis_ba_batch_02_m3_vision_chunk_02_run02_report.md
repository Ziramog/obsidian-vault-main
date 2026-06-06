# KORANTIS — M3 VISION REPORT (chunk 2/3)

**Run ID:** korantis_ba_batch_02_m3_vision_chunk_02_run02
**Parent run:** korantis_ba_batch_02_final_vision_queue_2026-06-06
**Model:** MiniMax-M3 (vision, base64 inline)
**Started:** 2026-06-06T21:45:58+00:00
**Finished:** 2026-06-06T21:47:17+00:00
**Items in chunk:** 25 (offsets 25:50)
**Venues in chunk:** 3

## TL;DR

- **Requested: 25 · Processed: 25 · Vision-OK: 7 · Skipped: 18**
- **below_preferred_resolution (max_dim<1024) entre OK: 7**
- **Scene distribution:** crowd=1, product_food=6
- **Skip reasons:** below_min_dimension=18

## Per-item results

| # | venue | ok | pil | dim | below<1024 | m3_status | scene_type | faces | editorial_usable | skip_reason |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Florería Atlántico | ✅ | JPEG | 620x400 | yes | ok | crowd | True | True | - |
| 2 | El Preferido de Palermo | ❌ | WEBP | 500x500 | no | skip:below_min_dimension | - | None | None | below_min_dimension |
| 3 | El Preferido de Palermo | ❌ | WEBP | 500x500 | no | skip:below_min_dimension | - | None | None | below_min_dimension |
| 4 | El Preferido de Palermo | ❌ | WEBP | 500x500 | no | skip:below_min_dimension | - | None | None | below_min_dimension |
| 5 | El Preferido de Palermo | ❌ | WEBP | 500x500 | no | skip:below_min_dimension | - | None | None | below_min_dimension |
| 6 | Apu Nena | ❌ | WEBP | 20x20 | no | skip:below_min_dimension | - | None | None | below_min_dimension |
| 7 | Apu Nena | ❌ | WEBP | 20x20 | no | skip:below_min_dimension | - | None | None | below_min_dimension |
| 8 | Apu Nena | ❌ | WEBP | 20x20 | no | skip:below_min_dimension | - | None | None | below_min_dimension |
| 9 | Apu Nena | ❌ | WEBP | 147x83 | no | skip:below_min_dimension | - | None | None | below_min_dimension |
| 10 | Apu Nena | ❌ | WEBP | 123x184 | no | skip:below_min_dimension | - | None | None | below_min_dimension |
| 11 | Apu Nena | ❌ | WEBP | 300x300 | no | skip:below_min_dimension | - | None | None | below_min_dimension |
| 12 | Apu Nena | ❌ | WEBP | 300x300 | no | skip:below_min_dimension | - | None | None | below_min_dimension |
| 13 | Apu Nena | ❌ | WEBP | 300x300 | no | skip:below_min_dimension | - | None | None | below_min_dimension |
| 14 | Apu Nena | ❌ | WEBP | 300x300 | no | skip:below_min_dimension | - | None | None | below_min_dimension |
| 15 | Apu Nena | ❌ | WEBP | 300x300 | no | skip:below_min_dimension | - | None | None | below_min_dimension |
| 16 | Apu Nena | ❌ | WEBP | 300x300 | no | skip:below_min_dimension | - | None | None | below_min_dimension |
| 17 | Apu Nena | ❌ | WEBP | 300x300 | no | skip:below_min_dimension | - | None | None | below_min_dimension |
| 18 | Apu Nena | ❌ | WEBP | 300x300 | no | skip:below_min_dimension | - | None | None | below_min_dimension |
| 19 | Apu Nena | ❌ | WEBP | 300x300 | no | skip:below_min_dimension | - | None | None | below_min_dimension |
| 20 | Apu Nena | ✅ | WEBP | 480x720 | yes | ok | product_food | False | True | - |
| 21 | Apu Nena | ✅ | WEBP | 480x720 | yes | ok | product_food | False | True | - |
| 22 | Apu Nena | ✅ | WEBP | 480x720 | yes | ok | product_food | False | True | - |
| 23 | Apu Nena | ✅ | WEBP | 479x853 | yes | ok | product_food | False | True | - |
| 24 | Apu Nena | ✅ | WEBP | 480x720 | yes | ok | product_food | False | True | - |
| 25 | Apu Nena | ✅ | WEBP | 480x718 | yes | ok | product_food | False | True | - |

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

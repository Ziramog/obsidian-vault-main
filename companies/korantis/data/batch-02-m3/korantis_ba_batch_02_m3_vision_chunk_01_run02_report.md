# KORANTIS — M3 VISION REPORT (chunk 1/3)

**Run ID:** korantis_ba_batch_02_m3_vision_chunk_01_run02
**Parent run:** korantis_ba_batch_02_final_vision_queue_2026-06-06
**Model:** MiniMax-M3 (vision, base64 inline)
**Started:** 2026-06-06T21:36:32+00:00
**Finished:** 2026-06-06T21:40:33+00:00
**Items in chunk:** 25 (offsets 0:25)
**Venues in chunk:** 6

## TL;DR

- **Requested: 25 · Processed: 25 · Vision-OK: 21 · Skipped: 4**
- **below_preferred_resolution (max_dim<1024) entre OK: 13**
- **Scene distribution:** decorative=1, gallery_atmosphere=2, hero_exterior=1, hero_interior=6, logo=1, product_food=10
- **Skip reasons:** below_min_dimension=4

## Per-item results

| # | venue | ok | pil | dim | below<1024 | m3_status | scene_type | faces | editorial_usable | skip_reason |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Mishiguene | ❌ | PNG | 192x45 | no | skip:below_min_dimension | - | None | None | below_min_dimension |
| 2 | Mishiguene | ❌ | PNG | 1x1 | no | skip:below_min_dimension | - | None | None | below_min_dimension |
| 3 | Mishiguene | ✅ | JPEG | 1024x683 | no | ok | logo | False | True | - |
| 4 | Mishiguene | ✅ | JPEG | 682x1024 | no | ok | product_food | False | True | - |
| 5 | Mishiguene | ✅ | JPEG | 683x1024 | no | ok | product_food | False | True | - |
| 6 | Mishiguene | ✅ | JPEG | 1024x683 | no | ok | product_food | False | True | - |
| 7 | Mishiguene | ✅ | JPEG | 2500x1667 | no | ok | product_food | False | True | - |
| 8 | Verne Club | ✅ | JPEG | 920x600 | yes | ok | gallery_atmosphere | False | True | - |
| 9 | Verne Club | ✅ | JPEG | 920x600 | yes | ok | hero_interior | True | True | - |
| 10 | Verne Club | ✅ | JPEG | 920x600 | yes | ok | hero_interior | False | True | - |
| 11 | Verne Club | ✅ | JPEG | 1591x1037 | no | ok | product_food | False | True | - |
| 12 | Verne Club | ✅ | JPEG | 920x600 | yes | ok | hero_interior | True | True | - |
| 13 | Verne Club | ❌ | JPEG | 276x180 | no | skip:below_min_dimension | - | None | None | below_min_dimension |
| 14 | Verne Club | ✅ | JPEG | 920x600 | yes | ok | hero_interior | False | False | - |
| 15 | Verne Club | ✅ | JPEG | 920x600 | yes | ok | product_food | False | True | - |
| 16 | Gran Bar Danzon | ✅ | JPEG | 937x765 | yes | ok | decorative | False | True | - |
| 17 | Gran Bar Danzon | ✅ | JPEG | 950x950 | yes | ok | gallery_atmosphere | False | True | - |
| 18 | Gran Bar Danzon | ✅ | PNG | 996x996 | yes | ok | product_food | False | True | - |
| 19 | Oporto Almacén | ✅ | JPEG | 1500x1000 | no | ok | hero_interior | False | True | - |
| 20 | Oporto Almacén | ✅ | JPEG | 600x800 | yes | ok | product_food | False | True | - |
| 21 | Oporto Almacén | ✅ | JPEG | 600x800 | yes | ok | product_food | False | True | - |
| 22 | La Biela | ❌ | WEBP | 103x105 | no | skip:below_min_dimension | - | None | None | below_min_dimension |
| 23 | La Biela | ✅ | WEBP | 1240x619 | no | ok | hero_exterior | True | False | - |
| 24 | Florería Atlántico | ✅ | JPEG | 620x400 | yes | ok | product_food | False | True | - |
| 25 | Florería Atlántico | ✅ | JPEG | 620x400 | yes | ok | hero_interior | False | True | - |

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
- Original M3 execution: 2026-06-06T21:36:32+00:00 (21 ok_photo of 25 items, 4 below_min_dimension skipped).
- Rename + run_id rewrite: 2026-06-06T21:43 UTC (manual, no re-execution).
- Vision content of each record was NOT modified; only the run_id, filename, and this audit note changed.

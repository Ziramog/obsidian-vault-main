# Korantis BA Batch 02 — M3 Vision Run Kit

Status: PREPARATION ONLY. No M3 inference has been executed in this environment.
This kit contains the sanitized queue, chunk splits, prompts, and merge spec
to be run in a real MiniMax-M3 environment.

## Important — do not skip

This environment has no M3 vision-call tool, cannot download 52 images
reliably, and has no DB / Cloudinary access. Running a real M3 batch from
here would either fail silently or produce fabricated-looking outputs.
Everything in this directory is *preparation*. The actual vision run
must happen elsewhere.

## Files in this directory

### Input (already produced)
| File | What it is |
|---|---|
| `korantis_ba_batch_02_m27_final_vision_queue.json` | Original M2.7 queue (75 items, contains SVG) |
| `korantis_ba_batch_02_m27_final_vision_queue_sanitized.json` | Sanitized queue (52 items, jpeg/png only). **Use this as M3 input.** |
| `korantis_ba_batch_02_m27_queue_sanitizer_report.md` | Sanitizer report — what was rejected and why |

### Chunks (already produced, ready to feed to M3)
| File | Items | Offset |
|---|---|---|
| `korantis_ba_batch_02_m3_vision_chunk_01.json` | 25 | 0–24 |
| `korantis_ba_batch_02_m3_vision_chunk_02.json` | 25 | 25–49 |
| `korantis_ba_batch_02_m3_vision_chunk_03.json` | 2 | 50–51 |

### Prompts (copy-paste into real M3 environment)
| File | Use it for |
|---|---|
| `M3_CHUNK_01_PROMPT.txt` | Running M3 on chunk 01 |
| `M3_CHUNK_02_PROMPT.txt` | Running M3 on chunk 02 |
| `M3_CHUNK_03_PROMPT.txt` | Running M3 on chunk 03 |
| `MERGE_PROMPT.txt` | Merging the 3 chunk outputs after all are validated |

### Scripts
| File | What it does |
|---|---|
| `split_m3_chunks.py` | Re-splits the sanitized queue into chunks. Idempotent. |

## How to run a chunk (in a real M3 environment)

1. Open the chunk file to confirm it has 25/25/2 items and all entries
   have allowed content types (jpeg/jpg/png/webp).
2. Copy the contents of the matching `M3_CHUNK_xx_PROMPT.txt` into your
   M3 environment, with the chunk JSON attached as the input file.
3. Run the chunk.
4. The M3 environment must produce exactly two files:
   - `korantis_ba_batch_02_m3_vision_chunk_NN.json`
   - `korantis_ba_batch_02_m3_vision_chunk_NN.md`
5. Save them in this same directory.
6. Sanity check the output JSON:
   - `model_used == "MiniMax-M3"` on every vision entry.
   - Items attempted = 25 / 25 / 2.
   - No item is missing or duplicated vs. the chunk input (by
     `dedupe_hash`).

## How to run the merge

Only after all 3 chunks are saved and sanity-checked:

1. Open `MERGE_PROMPT.txt`.
2. Run it against the 3 chunk JSONs.
3. The merge step does NOT re-run M3. It concatenates queues, validates
   the schema, and reports counts. It is structural, not inferential.
4. Expected output files:
   - `korantis_ba_batch_02_m3_vision_merged.json`
   - `korantis_ba_batch_02_m3_vision_merged.md`

## Output naming convention

Always:

  korantis_ba_batch_02_m3_vision_<stage>_<NN?>.<ext>

Stages:
  - `chunk_01`, `chunk_02`, `chunk_03` (per-chunk M3 run)
  - `merged` (post-merge consolidation)

Do not invent different prefixes. If you need a re-run, append
`_retry1`, `_retry2`, etc. Never overwrite a previously-validated
chunk — rename it to `_superseded` first.

## Hard rules (every chunk + the merge)

- No publish.
- No DB writes.
- No Cloudinary upload.
- Vision ONLY in the chunk stage. Merge is structural, not inferential.
- If a single image fails (SVG, missing, unreachable, wrong type), skip
  it and report. Do not abort the whole batch for one bad image.
- Do not mix models. Every vision entry must declare
  `model_used: "MiniMax-M3"`.

## Sanitizer summary (for context)

- Original: 75 items
- Removed: 23 (all SVG, by URL or content type)
- Sanitized: 52 items (jpeg + png only)
- Flagged (kept, unknown dimensions): 52 — width/height were 0/0 in
  the source queue. Not rejected; the rule only fires when both dims
  are known AND both < 1024. If you want strict resolution gating,
  re-run the sanitizer with explicit `min(width, height) >= 1024`
  as an unknown-dims rejector. Not done here — would gut the batch.

## File paths (absolute)

- Source queue:    /home/hermes/obsidian-vault/Hermes/companies/korantis/korantis_ba_batch_02_m27_final_vision_queue.json
- Sanitized queue: /home/hermes/obsidian-vault/Hermes/companies/korantis/korantis_ba_batch_02_m27_final_vision_queue_sanitized.json
- Sanitizer report:/home/hermes/obsidian-vault/Hermes/companies/korantis/korantis_ba_batch_02_m27_queue_sanitizer_report.md
- Chunks:          /home/hermes/obsidian-vault/Hermes/companies/korantis/korantis_ba_batch_02_m3_vision_chunk_{01,02,03}.json
- Prompts:         /home/hermes/obsidian-vault/Hermes/companies/korantis/M3_CHUNK_{01,02,03}_PROMPT.txt
- Merge prompt:    /home/hermes/obsidian-vault/Hermes/companies/korantis/MERGE_PROMPT.txt
- Splitter:        /home/hermes/.hermes/tmp/split_m3_chunks.py

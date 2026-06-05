# Korantis Model Split — Phase B execution (current M3 session)

**Date:** 2026-06-05 16:09 ART
**Active model:** MiniMax-M3
**Phase A provenance:** VERIFIED via session_search (session id 20260605_121851_accc65 had explicit system note switching to M2.7 at start)
**Phase A file:** UNCHANGED — original at /home/hermes/obsidian-vault/Hermes/Sessions/2026-06-05-korantis-model-split-phaseA.json

## Phase B execution

| # | Venue | File | Resolution | Vision call | Result |
|---|-------|------|------------|-------------|--------|
| 1 | Ninina | og:image | 767x767 | ❌ EXCLUDED (pre-vision resolution gate) | reference_only_thumb |
| 2 | Ninina | IMG_9549 width=165 | 165x165 | ❌ EXCLUDED (pre-vision resolution gate) | reference_only_thumb |
| 3 | Ninina | LolaMoraP | 1066x1066 | ✅ | product_context (NOT interior) |
| 4 | Verne | sillones | 2048x1474 | ✅ | hero_candidate (interior ✅) |
| 5 | Verne | VERNE_Verano26 | 1014x1024 | ✅ | reference_only (marketing collage) |
| 6 | Verne | Verne_otono-26 | 767x1024 | ✅ | reference_only (marketing collage) |
| 7 | Mishiguene | LA8A1489 | 1536x1024 | ✅ | product_context (NOT interior) |
| 8 | Mishiguene | LA8A5280 | 1536x1024 | ✅ | product_context (NOT interior) |
| 9 | Mishiguene | LA8A1536 | 1365x2048 | ✅ | product_context (NOT interior) |

**Summary:** 9 in queue → 7 passed resolution gate → 7 vision calls → 1 hero, 4 product, 2 reference, 0 gallery seating/atmosphere, 0 rejected.

## Why this matters

The Phase A vision_queue was over-confident. The URL/filename heuristic labeled too many things as "interior_possible" that turned out to be product shots (Mishiguene) or marketing collages (Verne seasonal). M3 vision corrected every wrong call.

**Net result for the split test:**
- M2.7 did text/web scouting (cheap) for 5 venues
- M3 vision was called 7 times (vs 42 if every prevision candidate was vision-analyzed, vs 9 if no resolution gate)
- Resolution gate saved 2 unnecessary vision calls
- Real interior found: 1/9 (Verne sillones)
- Real product found: 4/9 (Ninina 1 + Mishiguene 3)
- Marketing collage: 2/9 (Verne seasonal)

**Honest verdict on the split:** The split saved 35 vision calls (83.3%) but found only 1 real interior. The bottleneck is NOT vision cost — it's **source quality**. 4 of 5 venues have no real interior photography on their official sites. Editorial sourcing (Michelin/50Best) is the real unlock.

## Files exported

- /home/hermes/obsidian-vault/companies/korantis/scraping-outputs/korantis_model_split_combined_provisional_2026-06-05.json
- /home/hermes/obsidian-vault/Hermes/Sessions/2026-06-05-korantis-model-split-combined-provisional.json
- /home/hermes/obsidian-vault/companies/korantis/scraping-outputs/korantis_model_split_phaseB_m3_vision_2026-06-05.json
- /home/hermes/obsidian-vault/Hermes/Sessions/2026-06-05-korantis-model-split-phaseB.json

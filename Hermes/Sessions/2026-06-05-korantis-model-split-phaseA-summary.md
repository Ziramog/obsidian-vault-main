# Korantis Model Split Test — Phase A (M2.7 Text Scout)

**Date:** 2026-06-05
**Model used:** MiniMax-M2.7
**Vision used:** NO (per brief)

## Test Venues (5/5 processed)

| Venue | Website | Img candidates | Vision queue |
|---|---|---|---|
| Ninina | ✓ ninina.com | 27 | 3 |
| Don Julio | ✓ parrilladonjulio.com | 0 ⚠ | 0 |
| Verne Club | ✓ vernecocktailclub.com | 10 | 3 |
| Milion | ✓ milion.com.ar | 0 ⚠ | 0 |
| Mishiguene | ✓ mishiguenerestaurant.com | 5 | 3 |

## Key findings

- **5/5 official websites found** (all via direct domain knowledge + search)
- **5/5 phone numbers found**
- **5/5 price hints** (Michelin + editorial positioning)
- **2 menu links**, **1 reservation link**, **2 WhatsApp links**
- **42 prevision image candidates total → 9 in reduced vision queue** (3 max/venue)

## Gaps that need Phase B sourcing

- **Don Julio**: official site is 5KB landing. Editorial sourcing needed.
- **Milion**: official site has only product-card PNGs. Editorial sourcing needed.
- **Ninina**: 27 candidates = high; many are likely product, not interior.

## Phase B — NOT EXECUTED

Per brief: "If Hermes cannot actually switch model inside one run, stop after Phase A and output the vision_queue for a second M3-only run."

Hermes is currently on M2.7 (model switch happened at session start via system context). Mid-run model switch to M3 is not supported. Phase B is ready to run in a second session with M3 active, using the 9-image vision_queue output.

## Efficiency estimate

If full M3 pipeline would have analyzed all 42 prevision candidates, the split reduces vision calls to 9 (~78% reduction) and moves the cheap text/web scouting to M2.7. Real savings depend on M3 token cost vs M2.7 and the M3 calls avoided.

## Full output

See `korantis_model_split_test_m27_text_scout_2026-06-05.json` in this folder.

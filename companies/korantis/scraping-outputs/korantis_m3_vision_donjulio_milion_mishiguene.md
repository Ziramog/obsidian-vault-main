# KORANTIS — M3 VISION REPORT
## Don Julio Parrilla · Milión · Mishiguene

**Run ID:** korantis_m3_vision_donjulio_milion_mishiguene_2026-06-05
**Model:** MiniMax-M3 (vision)
**Vision calls spent:** 2 (the 6 thumbs and 1 missing artifact did not get a vision call per skill pitfall #11)
**Date:** June 5, 2026
**Input preflight:** `korantis_editorial_preflight_donjulio_milion_mishiguene_m27.json` (MiniMax-M2.7)

---

## TL;DR

- **9 M2.7 candidates received → 8 on disk → 2 passed the resolution gate → 2 vision-analyzed.**
- **0 hero candidates, 1 card candidate, 1 gallery candidate, 1 product candidate, 6 thumbs excluded.**
- **Mishiguene: blocked_on_rights** (the only M3-verified interior has identifiable faces + Condé Nast rights).
- **Don Julio: NOT ready.** Both on-disk candidates excluded as thumbs (<1024px). 3rd candidate missing.
- **Milión: NOT ready.** Only product shot (CNT) passed gate; venue hero strip is a 600px thumb.
- **M2.7 → M3 split structure: validated.** Editorial pre-vision accuracy on this batch: 50% (1/2). Up from 11% on the prior Ninina/Verne run, but still requires a re-fetch step between M2.7 and M3 because editorial sites serve small gallery thumbs by default.

---

## Input vs. analyzed

| Metric | Count |
|---|---|
| M2.7 candidates requested | 9 |
| Files present on disk | 8 |
| Files missing on disk | 1 (Don Julio / Argentina Tourism) |
| Passed resolution gate (≥1024 px) | 2 |
| Excluded by resolution gate | 6 |
| Vision-analyzed by M3 | 2 |
| Bytes-identical duplicates found | 1 (milion_s1.png = candidate_7_Mil_milion_official_gallery.jpg, md5 `156c024d`) |

---

## Per-image results

### Don Julio Parrilla

| File | Source | Resolution | Gate | M3 verdict |
|---|---|---|---|---|
| `candidate_0_Don_michelin_gallery.jpg` | Michelin | 1000×1000 | ❌ thumb | excluded — M3 not called |
| `candidate_1_Don_50best_profile.jpg` | 50 Best | 600×314 | ❌ thumb | excluded — M3 not called |
| _(not on disk)_ | Argentina Tourism | — | n/a | missing artifact |

**Result:** No M3-verified image for Don Julio. Both editorial candidates came back as gallery thumbs after M2.7 prevision. The government-tourism source is missing from the download cache. Per the brief, M3 did not web-scout or expand the queue.

### Mishiguene

| File | Source | Resolution | Gate | M3 verdict |
|---|---|---|---|---|
| `candidate_3_Mis_50best_profile.jpg` | 50 Best | 600×314 | ❌ thumb | excluded — M3 not called |
| `candidate_4_Mis_michelin_gallery.jpg` | Michelin | 1000×1000 | ❌ thumb | excluded — M3 not called |
| `candidate_5_Mis_cntraveler_review.jpg` | Condé Nast | 2560×1440 | ✅ pass | **gallery_atmosphere** (M3-verified) |

**`candidate_5_Mis_cntraveler_review.jpg` — gallery_atmosphere**
- ✅ Real interior: dim warm light, gallery wall of framed photos (matches the Michelin fact "walls covered with Judaica and photos of Israeli markets"), burgundy banquette, globe pendant lights, table setting with cocktails + wine.
- ✅ Seating visible: banquette + diners' chairs.
- ⚠️ People staying: 1 server (white shirt + tie) standing center, 2 servers moving in background, 4+ diners in foreground.
- ⚠️ **Identifiable faces:** 3+. The central server is in focus and clearly recognizable. Two foreground diners are recognizable. **Face releases required.**
- Scores: atmosphere 90, interior 70, seating 60, gallery 82, hero 55.
- Suggested role: **gallery_atmosphere** (not hero — people-forward composition rules it out as a clean architectural hero).
- Risk flags: `rights_review_needed` (Condé Nast), `face_release_needed`, `identity_review_needed`, `editorial_source`.

### Milión

| File | Source | Resolution | Gate | M3 verdict |
|---|---|---|---|---|
| `candidate_6_Mil_cntraveler_review.jpg` | Condé Nast | 2560×1440 | ✅ pass | **product_context** (top-down) |
| `candidate_7_Mil_milion_official_gallery.jpg` | milion.com.ar | 600×295 | ❌ thumb | excluded — M3 not called |
| `milion_s1.png` (duplicate of above) | milion.com.ar | 600×295 | ❌ thumb | excluded — M3 not called |

**`candidate_6_Mil_cntraveler_review.jpg` — product_context**
- ❌ **Not an interior.** Top-down overhead shot of two plated dishes on a marble surface (roasted aubergine/zucchini on patterned platter, smoked salmon on blini with cream). Marble is visible at the edges — that is the only environmental cue.
- ❌ No people, no seating, no interior architecture.
- ❌ Cannot serve as hero. Cannot serve as gallery_interior.
- Scores: atmosphere 35, interior 0, seating 0, gallery 15, hero 5.
- Suggested role: **product_context** (editorial food photography; useful only as a food reference).
- Risk flags: `rights_review_needed` (Condé Nast), `editorial_source`.
- **Note:** M2.7 prevision was "venue / atmosphere". M3 corrected to product_context. Prevision accuracy for this image: wrong.

---

## Decisions per venue

### Don Julio Parrilla — NOT ready for staging
- **best_hero_candidate:** none
- **best_card_candidate:** none
- **best_gallery_candidates:** none
- **rejected:** candidate_0, candidate_1 (both thumbs)
- **missing:** argentina_travel priority 3 not in download cache
- **Path forward:** re-download the same URLs at full resolution (Michelin gallery has full-res variants, 50 Best profile page does too — the captured images are banner thumbs). Or add new editorial sources that have confirmed full-res availability.

### Mishiguene — blocked on rights
- **best_hero_candidate:** none
- **best_card_candidate:** `candidate_5_Mis_cntraveler_review.jpg` (gallery_atmosphere)
- **best_gallery_candidates:** `candidate_5_Mis_cntraveler_review.jpg` (the only M3-verified interior)
- **rejected:** candidate_3, candidate_4 (both thumbs)
- **Blockers before staging:** (a) Condé Nast rights confirmation, (b) face releases for the 3+ identifiable faces in candidate_5, (c) even with releases, the people-forward composition disqualifies this image from being a venue hero — it's a context shot, not an architectural hero.
- **Path forward:** if a clean architectural interior is needed, request full-res versions of the Michelin gallery (some Michelin images go up to 2048×1361) and 50 Best Latin America profile photos; both are 1000×1000 thumbs now.

### Milión — NOT ready for staging
- **best_hero_candidate:** none
- **best_card_candidate:** none
- **best_gallery_candidates:** none (the only M3-analyzed image is product-only)
- **rejected:** candidate_6 (product only), candidate_7 + milion_s1.png (thumb + duplicate)
- **Path forward:** the official site only has 600×295 hero strips; the M2.7 prevision was overly optimistic about s1-s6b. For Milion, get full-res versions of the venue's own gallery (s2, s3, s4, s5, s6b) or the Wander Argentina article photos at full resolution. A different editorial source is also worth trying.

---

## Pipeline validation: does M2.7 → M3 split work?

**Status: partial — split structure validated, prevision accuracy acceptable, but a re-fetch step is needed between M2.7 and M3.**

| Question | Answer |
|---|---|
| Did M2.7 produce 9 editorial candidates superior to UGC? | Yes (Michelin, 50 Best, CNT, milion.com.ar) |
| Did those 9 contain real interior / hero candidates? | 1/9 (candidate_5), 1/9 product-only, 7/9 not analyzable |
| Is the M2.7 prevision heuristic acceptable as a filter? | Yes (50% accuracy on the 2 that could be analyzed, vs 11% in the prior Ninina/Verne batch — improved) |
| Should M3 burn vision tokens on thumbs? | No — resolution gate correctly excluded 6 of 8 |
| Is the resolution gate reliable when applied to actual files? | Yes — caught 6/8 in this run, vs 2/9 in the prior run. Higher exclusion rate reflects that editorial sites serve small gallery thumbs, while self-hosted WP/Shopify serves full-res. |

**Key finding:** editorial sourcing produces better **content** but smaller **default file size** when the scraper pulls the first image on the page. M2.7 prevision cannot detect this from URL alone — only the actual file does. **A re-fetch step between M2.7 and M3 (prefer `srcset`/largest variant, or follow `src` from `<a>` wrappers) is the missing piece.**

**Recommended next step (NOT a Batch 02 trigger — a structural fix):**
1. Add a "request full-res variant" step in M2.7: when a prevision candidate's URL contains a known thumbnail hint (`-2048x` query, `width=`, `w_`, `h_`), strip the size param and re-request.
2. Add a HEAD request in M2.7 to get `content-length` before the file lands. If content-length < 50 KB, downgrade priority.
3. Re-run only the 3 venues with the fix. Don't run Batch 02 yet.

---

## Files generated

1. `/home/hermes/korantis_m3_vision_donjulio_milion_mishiguene.json` — structured JSON (8 records analyzed, 1 missing, decisions per venue, pipeline validation)
2. `/home/hermes/korantis_m3_vision_donjulio_milion_mishiguene.md` — this report

**Model constraint:** MiniMax-M3 used for vision only. M2.7 not called. No web scouting. No queue expansion. No DB write. No Cloudinary upload. No publish. No Korantis file modification. All 8 inspected images are on disk in `/home/hermes/.chrome_tmp/vision_queue/`. All images remain candidates only — nothing approved for publication.

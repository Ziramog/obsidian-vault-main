# Korantis

> **Status:** New company — early validation phase (no clients yet, no revenue)

## What is it?

Korantis is a curated venue discovery product for Buenos Aires. The hypothesis: there's a gap between generic Maps/Yelp listings and high-end editorial guides (Michelin, 50 Best). Korantis sits in the middle — discovery with curation, but the visual and contextual depth that editorial offers.

The product isn't published yet. We are in evidence-collection mode: gathering web + visual evidence on candidate venues so a later validation pipeline can decide which to feature, and so we can produce a strong initial dataset of 25+ venues.

## Domain

- `korantis.com` (per user) — NOT yet wired up. (Note: AGENTS.md says "Corantis.com" — this is a typo/legacy. Real domain is `korantis.com`.)
- Status: domain not deployed. Mockups in progress at VPS port 8080+ (IP 194.163.161.99), synced via GitHub.

## What we've done so far

### Soft Scout Batch 01 (2026-06-05) — 25 venues, isolated scout test

We ran an isolated web+visual evidence scout on 25 BA venues to validate the pipeline and produce a first dataset. Result: `data/korantis_ba_hermes_soft_scout_batch_01_2026-06-05.json` (177.8 KB).

**Coverage:**
- 13/25 with official websites
- 10/25 with official hubs (Linktree/IG/FB)
- 8/25 with explicit reservation links
- 4/25 with menu PDFs
- 4/25 with WhatsApp
- 10/25 with phone
- 20/25 with price hints
- **56 image candidates total** (42 `needs_validation`, 14 `reference_only`, 0 `usable_candidate`)
- 19/25 with possible interior images

**Top HERO candidates identified (vision-verified):**
- 🥇 Ninina bakery interior — no people, 0 release issues
- 🥇 Verne Club speakeasy (Difford's editorial)
- 🥇 Milion Recoleta mansion bar — staircase + wingback chairs
- 🥇 Oporto Almacén — salon-pb + entrepiso (Núñez, industrial)
- 🥇 Gran Bar Danzon — wine bar with famous Enomatic dispensers
- 🥇 Don Julio Parrilla — iconic parilla + wine cellar
- 🥇 Niño Gordo — red Chinese lantern ceiling (signature)
- 🥇 Uptown — life-size NYC subway car interior

**Open issues (next batch):**
- 19 venues recommend `browser_render` retry (Michelin/IG/50 Best JS galleries)
- 3 venues recommend `residential_proxy` retry (Tres Monos, Reliquia, Mishiguene TA)
- 25/25 marked `manual_review_needed=true` (mainly for facial release + UGC source)

### Scraping Transport Diagnostic (2026-06-05)

We tested 5 transports (curl, curl+headers, chrome headless, playwright, curl_cffi) on 5 problem URLs to find the best default strategy.

**Result:** Simple `curl` is the right default for 80% of cases. Chrome is escalation only.

📄 `data/scraping_transport_diagnostic.json` + `.md`

## Active policies

### Scraping transport policy (registered 2026-06-05)

1. **No Playwright/Chrome by default.** Use `simple curl` for official websites, Michelin, 50 Best, and editorial.
2. **Escalate to `google-chrome --headless` ONLY IF** `curl` returns:
   - <500 bytes of content, OR
   - No `<title>` detected, OR
   - `meaningful_text_detected: false`, OR
   - 0 images on a visually-important source (Michelin/50 Best gallery page)
3. **TripAdvisor:** if `curl` returns 403, mark as `requires curl_cffi/residential_proxy`. Do NOT retry with Playwright/Chrome.
4. **Instagram:** never use as image source. Profile/@handle confirmation only via Google search snippets. If content is needed, route to Apify or similar.
5. **Chrome/Playwright env:** always `TMPDIR=/home/hermes/.chrome_tmp` before invoking.
6. **No residential proxy** unless source is critical and blocked.

### Data hygiene policy

- Every fact in scout JSON must have `source_url`. No source = no fact.
- Confidence values 0-1 only.
- Image candidates: max 8 per venue. Vision-analyze all of them.
- Reject logos, icons, payment methods, maps, menu screenshots as usable images.
- IG post images = reference_only at best, never usable.
- Manual review flagged for: facial release, UGC source, ambiguous match, failed important source.

## Next actions

1. `pip install curl_cffi` to unlock TripAdvisor + Instagram profile checks
2. Re-run scout for 3 venues with `residential_proxy` recommendation
3. Request press kits from Las Lilas, Julia, Reliquia, Verne, Gran Bar Danzon (caliber justifies outreach)
4. Validate the 42 `needs_validation` images: rights + duplicates + size
5. Korantis domain go-live (when ready)

## Files

### Scout artifacts
- `data/korantis_ba_hermes_soft_scout_batch_01_2026-06-05.json` — main 25-venue JSON (177.8 KB)
- `data/korantis_ba_scout_test_10_2026-06-05.json` — earlier 10-venue strict run (39 KB)
- `data/korantis_ba_soft_scout_test_10_2026-06-05.json` — earlier 10-venue soft run (74 KB)

### Transport diagnostic
- `data/scraping_transport_diagnostic.json` — 25 transport tests
- `data/scraping_transport_diagnostic.md` — report

### Working memory
- `companies/korantis/scraping-policy.md` — registered policy
- `companies/korantis/run-log-2026-06-05.md` — today's session log

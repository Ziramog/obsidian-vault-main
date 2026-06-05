# Korantis — Scraping Transport Policy

**Registered:** 2026-06-05
**Source:** Diagnostic test (5 transports × 5 URLs = 25 tests). Full report in `data/scraping_transport_diagnostic.md`.
**Applies to:** All Korantis scout batches (and any other VPS-resident web extraction work).

---

## TL;DR

Use **`curl` plain as default**. Escalate to **`google-chrome --headless`** only when curl fails the gating tests. Never retry TripAdvisor or Instagram with anything other than `curl_cffi` + residential proxy.

---

## Rules

### 1. Default transport: `simple curl`
- No special headers needed for 80% of cases.
- Successful on: official websites, Michelin, 50 Best, editorial pages, frommer's, malevamag, etc.
- Speed: <2s per request.
- Example: `curl -s -L --max-time 20 -w "\n__HTTP_STATUS__%{http_code}" <url>`

### 2. Do NOT use Playwright/Chrome by default
- Speed penalty ~6-13s per request vs curl.
- Not needed for 4/5 of the URLs we tested.
- Reserve for: cases where curl genuinely returns <500 bytes and the URL is known JS-heavy.

### 3. Escalate to `google-chrome --headless=new` ONLY IF `curl` returns:
- `<500 bytes` of body content, OR
- No `<title>` tag detected, OR
- `meaningful_text_detected: false` (i.e. body is a JS shell, not rendered HTML), OR
- `0 image_urls_found` on a source that is **visually important** (Michelin gallery, 50 Best hero, official site homepage)

Required chrome flags:
```
google-chrome --headless=new --no-sandbox --disable-gpu \
  --user-data-dir=/home/hermes/.chrome_tmp/chrome_<unique_id> \
  --disable-features=ProcessSingleton --no-zygote --no-first-run \
  --user-agent="Mozilla/5.0 ..." \
  --virtual-time-budget=8000 \
  --dump-dom <url>
```

### 4. **Mandatory env var** for any Chrome/Playwright invocation:
```
export TMPDIR=/home/hermes/.chrome_tmp
```
Without it, both Chrome and Playwright fail with `EACCES: permission denied, mkdtemp '/tmp/playwright-artifacts-...'` (the /tmp dir is permission-locked on this VPS).

### 5. **TripAdvisor handling:**
- If `curl` returns HTTP 403, **mark as `requires curl_cffi/residential_proxy`** in `fetch_diagnostics.retry_recommendation`.
- Do NOT retry with Playwright/Chrome (will also fail — same Cloudflare/Akamai block).
- Acceptable workarounds (in order of preference):
  1. Install `curl_cffi` (30s, `pip install curl_cffi`) — TLS fingerprint spoofing unblocks most TA pages.
  2. Residential proxy pool (~$10/mo) — full unblock.
  3. Backup: Google search snippet `[venue name] tripadvisor` for handle + rating only. No images.

### 6. **Instagram handling:**
- **Never use IG post images as image candidates** (per the original scout policy).
- IG profile pages: do NOT scrape directly (Meta blocks VPS IPs entirely).
- For @handle confirmation: use Google search snippet `[venue name] instagram`.
- For IG content (if ever needed): use Apify or similar third-party. Out of scope for current scout batches.

### 7. **No residential proxy** unless:
- Source is critical (e.g. image rights to the venue we want to feature), AND
- It's blocked by every cheaper transport (curl + chrome + curl_cffi), AND
- The cost ($10-50/mo) is justified by a real downstream revenue path (not just completeness).

---

## Decision tree (per URL)

```
START: For each URL in scout batch
│
├── Try simple curl (Transport A)
│   │
│   ├── HTTP 200 + body > 500 bytes + title + at least 1 img?
│   │   └─ YES → Use this. Done. (80% of cases)
│   │   └─ NO (no img but has text) → Use this for text facts; mark "0 images, visual escalation needed" if source is visually important.
│   │
│   ├── HTTP 200 + body < 500 bytes OR no title?
│   │   └─ YES → Escalate to google-chrome (Transport C, with TMPDIR fix).
│   │
│   ├── HTTP 403 + URL is TripAdvisor / Cloudflare-protected?
│   │   └─ YES → Mark `retry_recommendation: residential_proxy` and STOP. Do not retry.
│   │
│   ├── HTTP 403 + URL is Instagram?
│   │   └─ YES → Mark `unsafe_or_rejected_findings` with type "social". STOP. Do not retry.
│   │
│   ├── HTTP 5xx or timeout?
│   │   └─ Mark as transient failure. Retry once after 60s. If still fails: mark as `unknown_status` + `manual_check`.
│   │
│   └── DNS error / connection refused?
│       └─ Mark as `dns_error` or `blocked`. Likely dead site. Manual verify.
│
└── If escalated to chrome:
    │
    ├── Chrome succeeds with >500 bytes?
    │   └─ YES → Use this. Done.
    │
    ├── Chrome still blocked (TA, IG)?
    │   └─ Mark `residential_proxy` and STOP.
    │
    └── Chrome timeout or crash?
        └─ Mark `manual_check` and STOP. Don't burn more cycles.
```

---

## Cost matrix

| Transport | Cost | Time | When |
|---|---|---|---|
| `curl` plain | $0 | <2s | Default |
| `curl` + browser headers | $0 | <2s | When plain curl returns <500 bytes (same as above usually) |
| `google-chrome headless` | $0 | ~8s | When curl returns <500 bytes AND source is visually important |
| `playwright` | $0 | ~13s | Same as Chrome, but with finer control. Reserved for complex multi-step flows. |
| `curl_cffi` (NOT installed) | $0 to install | <2s | When TA/IG need unlocking |
| Residential proxy (Bright Data, Webshare) | $10-50/mo | <2s | Last resort, for sources that block curl_cffi too |

---

## Reference

- Diagnostic run: 25 tests, 17 successful.
- Discovery: many "js_required" classifications in earlier scout runs were wrong — `curl` plain was sufficient.
- Chrome on this VPS is slow due to TMPDIR/ProcessSingleton quirks. Set `TMPDIR=/home/hermes/.chrome_tmp` and `--user-data-dir=` per invocation.
- Playwright same TMPDIR issue. Same fix.

Files:
- `data/scraping_transport_diagnostic.json` — raw test results
- `data/scraping_transport_diagnostic.md` — narrative report
- `companies/korantis/scraping-policy.md` — this file

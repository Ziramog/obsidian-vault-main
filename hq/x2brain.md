# X2Brain System — Complete Architecture, Design & Implementation Blueprint
> *From zero-dollar start to autonomous cognitive infrastructure*

---

## ASSESSMENT OF ORIGINAL DOCUMENT

The original XBrain spec has strong conceptual clarity but several critical gaps that would stall real implementation:

| Gap | Problem | Fix Applied Below |
|---|---|---|
| **No concrete Twitter ingestion plan** | X API is not free anymore | Three free-tier fallback methods defined |
| **No LLM budget strategy** | Assumes paid APIs | Full free-tier LLM routing mapped |
| **Hermes integration is vague** | No actual agent roles or prompts defined | Agent role specs + prompt templates included |
| **Obsidian sync is hand-wavy** | Two options listed but no setup steps | Full Git-based sync pipeline with scripts |
| **No phased implementation** | Jumps from concept to "future" | 4-week sprint plan with deliverables |
| **No error handling / fallback logic** | Fragile in practice | Resilience patterns per layer |
| **Vector store undefined** | "Semantic memory" without tooling | ChromaDB (free, local) integrated |

---

## 1. SYSTEM IDENTITY

**X2Brain** is a **personal intelligence extraction engine**.

It does not save content. It converts information into structured knowledge and surfaces it as decision intelligence — automatically, daily, at zero cost.

```
INFORMATION → SIGNAL → KNOWLEDGE → DECISION → FEEDBACK LOOP
```

---

## 2. FULL STACK (Zero Dollar Budget)

### Core Infrastructure
| Layer | Tool | Cost | Why |
|---|---|---|---|
| Agent runtime | Hermes (already on VPS) | $0 | Already deployed |
| LLM | Groq API (free tier) | $0 | 30 RPM, fast inference |
| LLM fallback | Mistral API (free tier) | $0 | Le Platforme free plan |
| LLM fallback 2 | Ollama on VPS (mistral:7b) | $0 | Fully offline if needed |
| Vector DB | ChromaDB (local on VPS) | $0 | Persistent semantic memory |
| Metadata DB | SQLite | $0 | Zero setup, zero infra |
| Knowledge UI | Obsidian (local, free) | $0 | Markdown-native |
| Sync layer | Git + GitHub (private repo) | $0 | Version-controlled vault |
| Notifications | Telegram Bot API | $0 | Unlimited messages |
| X Data (primary) | twitter-scraper-python + Nitter | $0 | Scrape without API key |
| X Data (fallback) | IFTTT free tier → RSS bookmarks | $0 | Append-only log |
| X Data (manual) | Browser export script | $0 | Copy-paste JSON dump |
| Scheduling | VPS cron | $0 | Native Linux |

### LLM Routing Logic (Priority Order)
```
Request → Try Groq (fast, free) →
  [fail/rate limit] → Try Mistral API →
    [fail] → Try Ollama local →
      [fail] → Queue for retry
```

---

## 3. ARCHITECTURE — DETAILED SYSTEM MAP

```
╔══════════════════════════════════════════════════════════════════╗
║                         DATA SOURCES                            ║
║   [Likes]  [Bookmarks]  [Own Tweets]  [Tracked Accounts]        ║
╚══════════════╦═══════════════════════════════════════════════════╝
               ↓
╔══════════════╩═══════════════════════════════════════════════════╗
║                      INGESTION LAYER                            ║
║  twitter-scraper / Nitter RSS / Manual JSON import              ║
║  → Dedup check (SQLite)                                         ║
║  → Thread reconstruction                                        ║
║  → Normalize to TweetRecord schema                              ║
╚══════════════╦═══════════════════════════════════════════════════╝
               ↓
╔══════════════╩═══════════════════════════════════════════════════╗
║                    HERMES AGENT PIPELINE                        ║
║                                                                 ║
║  [Role: Cleaner]    → remove noise, fix encoding                ║
║  [Role: Classifier] → type + domain + value_score              ║
║  [Role: Compressor] → RAW → PRINCIPLE → APPLICATION            ║
║  [Role: Linker]     → semantic similarity → related notes       ║
║  [Role: Writer]     → generate Obsidian .md note               ║
║  [Role: Strategist] → daily brief + action items               ║
╚══════════════╦═══════════════════════════════════════════════════╝
               ↓
╔══════════════╩═══════════════════════════════════════════════════╗
║                      STORAGE LAYER                              ║
║  SQLite (metadata + scores + dedup)                             ║
║  ChromaDB (embeddings for semantic search)                      ║
║  Git Vault (Obsidian .md files)                                 ║
╚══════════════╦═══════════════════════════════════════════════════╝
               ↓
╔══════════════╩═══════════════════════════════════════════════════╗
║                      OUTPUT LAYER                               ║
║  Git push → GitHub → Local pull → Obsidian auto-refresh         ║
║  Telegram Bot → Daily report at configured time                  ║
╚══════════════════════════════════════════════════════════════════╝
```

---

## 4. DATA SCHEMAS

### TweetRecord (Internal Schema)
```python
{
  "id": "tweet_1234567890",
  "text": "Full reconstructed text (thread-joined)",
  "author": "@handle",
  "author_followers": 12400,
  "timestamp": "2025-04-25T14:32:00Z",
  "type": "bookmarked",          # liked | bookmarked | own | tracked
  "engagement": {
    "likes": 340,
    "reposts": 88,
    "replies": 12
  },
  "thread": ["tweet_id1", "tweet_id2"],  # thread chain
  "raw_url": "https://x.com/...",
  "processed": false
}
```

### KnowledgeNote (Obsidian Output Schema)
```markdown
---
id: 20250425-1432-vwap-execution-edge
type: insight
domain: trading
source_account: "@tradingwolf"
source_date: 2025-04-25
ingested_date: 2025-04-25
value_score: 0.87
tags: [trading, execution, vwap, edge]
related: [[20250312-1100-order-flow-basics]]
status: active
---

## VWAP Execution Edge

### Principle
[One-sentence crystallization of the core idea]

### Why It Matters
[Context: why this is relevant now]

### Application
- [ ] Action 1
- [ ] Action 2

### Source
> [Compressed quote — not raw tweet]

### Review
*Validate on: [date+trigger]*
```

### SQLite Schema
```sql
CREATE TABLE tweets (
  id TEXT PRIMARY KEY,
  author TEXT,
  timestamp TEXT,
  type TEXT,
  value_score REAL,
  processed INTEGER DEFAULT 0,
  note_path TEXT,
  ingested_at TEXT
);

CREATE TABLE accounts (
  handle TEXT PRIMARY KEY,
  signal_score REAL,
  total_ingested INTEGER,
  avg_value_score REAL,
  last_seen TEXT
);

CREATE TABLE daily_reports (
  date TEXT PRIMARY KEY,
  telegram_sent INTEGER DEFAULT 0,
  insights_count INTEGER,
  actions_count INTEGER
);
```

---

## 5. HERMES AGENT ROLES — PROMPTS & LOGIC

### Role 1: Cleaner
```python
SYSTEM = """
You are a data cleaner. Given raw tweet text:
1. Remove URLs, @mentions noise, hashtag spam
2. Reconstruct thread into coherent prose
3. Fix broken formatting
4. Output: clean_text (string only, no commentary)
"""
```

### Role 2: Classifier
```python
SYSTEM = """
You are a content classifier. Analyze the tweet and output ONLY valid JSON:
{
  "type": "insight|framework|tactic|signal|noise",
  "domain": "trading|business|ai|philosophy|content|other",
  "value_score": 0.0-1.0,
  "reasoning": "one sentence"
}
Rules:
- noise score < 0.3: motivational fluff, generic advice, self-promotion
- tactic 0.3-0.6: actionable but common
- insight 0.6-0.85: original angle, strong signal
- framework 0.85-1.0: reusable mental model with wide application
"""
```

### Role 3: Compressor
```python
SYSTEM = """
You compress content into structured knowledge. Given clean tweet text, output ONLY valid JSON:
{
  "title": "3-6 word descriptive title (kebab-case)",
  "principle": "One sentence — the core transferable idea",
  "why_it_matters": "2-3 sentences of context",
  "applications": ["action 1", "action 2", "action 3"],
  "keywords": ["kw1", "kw2", "kw3"],
  "compressed_quote": "Best 1-sentence representation of original"
}
Never invent information not present in the source.
"""
```

### Role 4: Linker
```python
# Uses ChromaDB to find semantically related existing notes
def find_related_notes(principle: str, top_k: int = 3) -> list[str]:
    results = chroma_collection.query(
        query_texts=[principle],
        n_results=top_k,
        include=["metadatas", "distances"]
    )
    # Return note IDs with similarity > 0.75
    return [r["id"] for r in results if r["distance"] < 0.25]
```

### Role 5: Strategist (Daily Brief Generator)
```python
SYSTEM = """
You are a strategic intelligence analyst.
Given a JSON list of today's processed insights, generate a daily brief in this EXACT format:

🔴 HIGH SIGNAL
[Top 2-3 ideas that demand attention today]

🔁 PATTERNS
[Recurring themes across multiple signals]

⚡ ACTIONS
[Concrete things to do or test — numbered list]

🧪 VALIDATE
[Hypotheses to track over next 7 days]

🗑️ IGNORE
[What was filtered out and why — one line]

🔍 RESEARCH GAPS
[Questions raised that need deeper investigation]

Keep total length under 400 words. Be surgical, not comprehensive.
"""
```

---

## 6. INGESTION METHODS (Free Tier, Ranked by Reliability)

### Method A — twitter-scraper-python (Primary, No API Key)
```bash
pip install twitter-scraper-python
```
```python
from twitter_scraper import get_tweets

def ingest_bookmarks(username: str, pages: int = 5):
    # Note: requires session cookies for bookmarks
    # Export cookies from browser using EditThisCookie extension
    tweets = get_tweets(username, pages=pages)
    return [normalize(t) for t in tweets]
```

### Method B — Nitter RSS (Reliable for Tracked Accounts)
```python
import feedparser

NITTER_INSTANCES = [
    "https://nitter.poast.org",
    "https://nitter.privacydev.net",
    "https://nitter.1d4.us"
]

def fetch_account_feed(handle: str) -> list:
    for instance in NITTER_INSTANCES:
        try:
            feed = feedparser.parse(f"{instance}/{handle}/rss")
            if feed.entries:
                return [normalize_rss(e) for e in feed.entries]
        except:
            continue
    return []
```

### Method C — Manual JSON Export (Fallback, Bookmarks)
```
Workflow:
1. Open X in browser
2. Run bookmarks-exporter userscript (GitHub: nicholasgasior/tweet-bookmarks-export)
3. Save output to: /wolfim/x2brain/inbox/manual_import.json
4. Run: python ingest.py --source manual_import.json
```

### Thread Reconstruction
```python
def reconstruct_thread(tweet_ids: list[str], fetcher) -> str:
    """Join thread tweets into single coherent text block."""
    parts = []
    for tid in tweet_ids:
        tweet = fetcher.get_tweet(tid)
        if tweet:
            parts.append(tweet["text"])
    return "\n\n---\n\n".join(parts)
```

---

## 7. OBSIDIAN VAULT STRUCTURE

```
obsidian-vault/
├── .obsidian/               # Obsidian config (committed to Git)
│   └── plugins/
│       └── dataview/        # Dataview plugin config
├── Inbox/                   # Auto-written by Hermes (unreviewed)
├── Insights/                # Validated, high-score notes
│   ├── trading/
│   ├── business/
│   ├── ai/
│   └── philosophy/
├── Frameworks/              # Reusable mental models
├── Playbooks/               # Step-by-step execution guides
├── Signals/                 # Time-sensitive signals (archive after 30d)
├── Accounts/                # One note per tracked account (signal score)
├── Daily Reports/           # Auto-generated briefs from Telegram
│   └── 2025/
│       └── 2025-04-25.md
└── Meta/
    ├── Stats.md             # Auto-updated dashboard
    └── Backlog.md           # Ideas flagged for research
```

### Dataview Dashboard (Meta/Stats.md)
```dataview
TABLE value_score, domain, type, ingested_date
FROM "Insights"
WHERE value_score >= 0.75
SORT ingested_date DESC
LIMIT 20
```

---

## 8. GIT SYNC PIPELINE

### VPS Side (Hermes writes notes)
```bash
# /wolfim/x2brain/sync.sh
#!/bin/bash
cd /wolfim/x2brain/obsidian-vault
git add -A
git commit -m "auto: $(date +%Y-%m-%d-%H%M) — ${1:-batch}"
git push origin main
```

```python
# Called at end of each processing batch in Hermes
import subprocess

def push_vault(message: str = "batch"):
    result = subprocess.run(
        ["/wolfim/x2brain/sync.sh", message],
        capture_output=True, text=True
    )
    return result.returncode == 0
```

### Local Machine (Windows, Auto-Pull)
```powershell
# Task Scheduler: runs every 15 minutes
# pull_vault.ps1
Set-Location "C:\Users\Truzt\ObsidianVault\x2brain"
git pull origin main
```

Or use **Obsidian Git plugin** (free, community plugin):
- Set auto-pull interval: 15 minutes
- Auto-commit on file change: disabled (VPS is source of truth for auto-notes)

### GitHub Private Repo Setup
```bash
# On VPS, one-time setup
cd /wolfim/x2brain
git init
git remote add origin https://github.com/YOUR_USERNAME/x2brain-vault.git
git branch -M main
git push -u origin main

# Store token in .netrc for passwordless push
echo "machine github.com login YOUR_USERNAME password YOUR_TOKEN" > ~/.netrc
chmod 600 ~/.netrc
```

---

## 9. TELEGRAM BOT SETUP

### Create Bot (one-time)
```
1. Open Telegram → @BotFather
2. /newbot → name: X2Brain → username: x2brain_yourname_bot
3. Save the token
4. Get your chat_id: message @userinfobot
```

### Send Daily Report
```python
import httpx
from datetime import date

TELEGRAM_TOKEN = "YOUR_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"

async def send_report(report_text: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": report_text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload)
    return response.json()
```

### Cron Schedule (VPS)
```bash
# crontab -e
# Daily brief at 8:00 AM Argentina time (UTC-3)
0 11 * * * /usr/bin/python3 /wolfim/x2brain/run_daily_brief.py >> /wolfim/logs/x2brain.log 2>&1

# Ingestion runs every 4 hours
0 */4 * * * /usr/bin/python3 /wolfim/x2brain/run_ingestion.py >> /wolfim/logs/x2brain.log 2>&1
```

---

## 10. COMPLETE FILE STRUCTURE (VPS)

```
/wolfim/x2brain/
├── config.py                # ALL config variables centralized
├── main.py                  # Entry point / orchestrator
├── run_ingestion.py         # Cron target: ingestion cycle
├── run_daily_brief.py       # Cron target: Telegram report
├── sync.sh                  # Git push script
│
├── ingestion/
│   ├── __init__.py
│   ├── scrapers.py          # twitter-scraper + nitter RSS
│   ├── manual_import.py     # JSON file importer
│   └── thread_builder.py    # Thread reconstruction logic
│
├── processing/
│   ├── __init__.py
│   ├── cleaner.py
│   ├── classifier.py
│   ├── compressor.py
│   ├── linker.py            # ChromaDB similarity
│   └── note_writer.py       # Markdown generator
│
├── storage/
│   ├── __init__.py
│   ├── sqlite_store.py      # Metadata, dedup, scores
│   └── vector_store.py      # ChromaDB wrapper
│
├── output/
│   ├── __init__.py
│   ├── telegram_bot.py
│   └── report_builder.py    # Strategist role
│
├── obsidian-vault/          # Git repo (synced to GitHub)
│   └── [vault structure above]
│
├── inbox/                   # Drop zone for manual imports
├── logs/
│   └── x2brain.log
└── data/
    ├── x2brain.db           # SQLite
    └── chroma/              # ChromaDB persistent storage
```

### config.py
```python
# /wolfim/x2brain/config.py

# LLM
GROQ_API_KEY = "your_key"
MISTRAL_API_KEY = "your_key"
OLLAMA_URL = "http://localhost:11434"
LLM_MODEL_GROQ = "llama3-8b-8192"
LLM_MODEL_MISTRAL = "mistral-small-latest"
LLM_MODEL_OLLAMA = "mistral"

# Telegram
TELEGRAM_TOKEN = "your_bot_token"
TELEGRAM_CHAT_ID = "your_chat_id"
REPORT_HOUR_UTC = 11  # 8 AM Argentina

# Filtering
VALUE_SCORE_THRESHOLD = 0.60
MIN_ENGAGEMENT_SIGNAL = 50  # min likes to consider

# Twitter Tracked Accounts
TRACKED_ACCOUNTS = [
    "@handle1",
    "@handle2",
]

# Paths
VAULT_PATH = "/wolfim/x2brain/obsidian-vault"
DB_PATH = "/wolfim/x2brain/data/x2brain.db"
CHROMA_PATH = "/wolfim/x2brain/data/chroma"
INBOX_PATH = "/wolfim/x2brain/inbox"
LOG_PATH = "/wolfim/x2brain/logs/x2brain.log"

# GitHub
GITHUB_REMOTE = "origin"
GITHUB_BRANCH = "main"
```

---

## 11. IMPLEMENTATION SPRINT — 4 WEEKS

### Week 1 — Foundation
**Goal: Pipeline works end-to-end with manual import**

| Day | Task |
|---|---|
| 1 | Set up `/wolfim/x2brain/` folder structure, `config.py`, SQLite schema |
| 2 | Install deps: `chromadb`, `feedparser`, `httpx`, `groq`, `mistral` |
| 3 | Build `manual_import.py` — import JSON bookmarks export |
| 4 | Build `cleaner.py` + `classifier.py` with Groq |
| 5 | Build `note_writer.py` → generates `.md` in vault |
| 6 | Set up GitHub private repo + Git sync script |
| 7 | Test full loop: manual import → note in Obsidian |

**Week 1 Success Metric:** 10 notes generated automatically from manual import

---

### Week 2 — Automation
**Goal: Automated ingestion + Telegram daily brief**

| Day | Task |
|---|---|
| 8 | Build `nitter RSS` scraper for 3 tracked accounts |
| 9 | Build `compressor.py` + `vector_store.py` (ChromaDB) |
| 10 | Build `linker.py` — semantic similarity via ChromaDB |
| 11 | Build `report_builder.py` (Strategist role) |
| 12 | Build `telegram_bot.py` + test send |
| 13 | Set up cron jobs — ingestion + daily brief |
| 14 | Run full automated cycle for 2 days, fix bugs |

**Week 2 Success Metric:** Daily brief arrives on Telegram at 8 AM with ≥5 insights

---

### Week 3 — Intelligence Quality
**Goal: Improve signal quality + vault usability**

| Day | Task |
|---|---|
| 15 | Add `accounts.py` — score tracked accounts by output quality |
| 16 | Add deduplication (hash + vector similarity check) |
| 17 | Build Dataview dashboards in Obsidian |
| 18 | Add `thread_builder.py` — treat threads as one unit |
| 19 | Tune value_score thresholds based on real output |
| 20 | Add domain-specific classifier tuning (trading focus) |
| 21 | Review 100 auto-generated notes — adjust prompts |

**Week 3 Success Metric:** <10% junk notes in vault; patterns visible in Obsidian

---

### Week 4 — Resilience & Expansion
**Goal: System is stable, self-monitoring, and ready for Phase 2**

| Day | Task |
|---|---|
| 22 | Add LLM fallback routing (Groq → Mistral → Ollama) |
| 23 | Add retry queue for failed processing jobs |
| 24 | Add `validate` flag system — track applied insights |
| 25 | Health check endpoint + daily system status alert |
| 26 | Document all prompts + create prompt versioning |
| 27 | Add `/inbox` Telegram command for ad-hoc tweet analysis |
| 28 | Full system review + 30-day plan |

**Week 4 Success Metric:** System runs 7 days unattended with <2 manual fixes

---

## 12. FUTURE PHASES

### Phase 2 — Decision Engine (Month 2-3)

**Account Signal Scoring**
```python
# Rank accounts by quality of insights they produce
# Updated weekly from value_score averages in SQLite
def update_account_scores():
    scores = db.query("""
        SELECT author, AVG(value_score), COUNT(*)
        FROM tweets WHERE processed = 1
        GROUP BY author
    """)
    # Promote high-scorers → more frequent tracking
    # Demote low-scorers → reduce pull frequency
```

**Pattern Detection**
```python
# Weekly cross-note analysis
# Find recurring themes in ChromaDB clusters
# Generate: "This week's dominant signal: X"
```

**Action Tracker**
```markdown
# In Obsidian: Playbooks/Action-Tracker.md
| Insight | Source | Applied | Result | Score |
|---------|--------|---------|--------|-------|
| VWAP edge note | @trader | 2025-04-25 | +2.3% | ✅ |
```

---

### Phase 3 — Cognitive Amplifier (Month 3-5)

**Cross-Domain Synthesis**
```
New trading insight detected →
  Query ChromaDB: "similar ideas in business domain" →
  Find: pricing psychology note from 3 months ago →
  Hermes: "These connect because: [synthesis]" →
  Generate new note: cross-domain framework
```

**Obsidian Telegram Query Interface**
```
You → Telegram: "What do I know about order flow?"
Bot → ChromaDB similarity search →
Bot → Returns top 5 related notes with links
```

**Weekly Pattern Report (Separate from Daily)**
```
Every Sunday 9 AM:
- Top 5 signals of the week
- Emerging themes
- Cross-domain connections
- Account quality changes
- Recommended focus areas for coming week
```

---

### Phase 4 — Autonomous Strategist (Month 5+)

**Self-Improving Threshold System**
```python
# Reflection agent runs weekly
# Analyzes: which insights did you actually use?
# Input: action_tracker data + value_score history
# Output: updated classification thresholds

def reflection_cycle():
    applied_insights = db.get_applied_insights()
    avg_score_of_used = mean([i.value_score for i in applied_insights])
    # If avg_score_of_used is 0.72, raise threshold to 0.68
    # System learns what *you* actually find valuable
    update_config("VALUE_SCORE_THRESHOLD", avg_score_of_used - 0.04)
```

**Market Narrative Alignment (Trading Specific)**
```
Hermes tracks:
- Dominant narrative on X this week
- Contrarian signals
- Sentiment shift moments

Output: "Narrative map" in Obsidian/Signals/
```

**WOLFIM Integration Opportunity**
```
X2Brain surfaces: AI automation trend growing in SMB space
→ Auto-generates: draft blog post outline for WOLFIM content
→ Auto-creates: WOLFIM/Content-Pipeline/drafts/ai-automation-sme.md
→ Telegram alert: "New content opportunity detected"
```

---

## 13. RESILIENCE & OPERATIONAL PATTERNS

### Error Handling Per Layer
```python
# All processing jobs use this pattern
def safe_process(tweet: dict) -> Optional[KnowledgeNote]:
    try:
        cleaned = cleaner.clean(tweet)
        classification = classifier.classify(cleaned)

        if classification["value_score"] < VALUE_SCORE_THRESHOLD:
            db.mark_as_noise(tweet["id"])
            return None

        compressed = compressor.compress(cleaned)
        links = linker.find_related(compressed["principle"])
        note = note_writer.write(compressed, classification, links)
        db.mark_as_processed(tweet["id"], note.path)
        return note

    except LLMRateLimitError:
        db.queue_for_retry(tweet["id"])
        return None
    except Exception as e:
        log.error(f"Failed {tweet['id']}: {e}")
        db.mark_as_failed(tweet["id"])
        return None
```

### Health Monitoring
```bash
# Daily health check via Telegram (runs before main report)
# Checks:
# - Last successful ingestion timestamp
# - SQLite size
# - ChromaDB entry count  
# - Git sync status
# - LLM API response time
```

---

## 14. INSTALLATION COMMANDS (VPS)

```bash
# On your VPS
cd /wolfim
mkdir x2brain && cd x2brain

# Python environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install \
  chromadb \
  feedparser \
  httpx \
  groq \
  mistral \
  python-telegram-bot \
  sentence-transformers \
  sqlite-utils \
  python-dateutil \
  pydantic

# Initialize SQLite
python3 -c "from storage.sqlite_store import init_db; init_db()"

# Initialize ChromaDB
python3 -c "from storage.vector_store import init_chroma; init_chroma()"

# Initialize Git vault
cd obsidian-vault
git init
git remote add origin https://github.com/YOUR_HANDLE/x2brain-vault.git

# Test Telegram
python3 -c "from output.telegram_bot import send_report; import asyncio; asyncio.run(send_report('X2Brain online ✅'))"
```

---

## 15. FIRST ACTION CHECKLIST

```
□ Create /wolfim/x2brain/ on VPS
□ Set up config.py with your actual keys
□ Get Groq API key (free at console.groq.com)
□ Get Mistral API key (free at console.mistral.ai)
□ Create Telegram bot via @BotFather
□ Create private GitHub repo: x2brain-vault
□ Export your X bookmarks manually (first test batch)
□ Run manual import → see first note appear in Obsidian
□ Install Obsidian Git plugin on local machine
□ Set first cron job for daily brief
```

---

## FINAL ARCHITECTURE PRINCIPLE

> Store nothing you haven't compressed.  
> Compress nothing you won't use.  
> Report nothing you can't act on.

The system's value is not in how much it captures.  
It's in how precisely it converts information into **your next move**.

---

*x2brain.md — Truzt / WOLFIM Intelligence Infrastructure*  
*Version 1.0 — Start date: [your date here]*

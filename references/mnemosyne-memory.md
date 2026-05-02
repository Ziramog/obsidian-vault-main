---
title: mnemosyne-memory
type: tool
created: 2026-05-02
tags: [memory, sqlite, local, hermes, infrastructure]
confidence: medium
sources: [https://mnemosyne.site/]
status: saved
---

# Mnemosyne — Native Memory for Hermes Agent

## What
Zero-dependency, sub-millisecond memory system for AI agents. Built on SQLite + sqlite-vec + FTS5. 100% local, no API keys, no cloud.

- **Version:** v1.11.0 (PyPI)
- **Install:** `pip install mnemosyne-memory`
- **Repository:** github.com/AxDSan/mnemosyne

## Architecture: BEAM (Bilevel Episodic-Associative Memory)

| Layer | Purpose | Scope |
|---|---|---|
| Working Memory | Hot, recent context | Session (auto-injected) |
| Episodic Memory | Long-term storage | Persistent (sqlite-vec + FTS5) |
| Scratchpad | Temp reasoning workspace | Session (cleared) |

## Core API

```python
from mnemosyne import remember, recall

remember("User prefers dark mode", importance=0.9, scope="global")
results = recall("user preferences")
```

## Benchmarks (vs Honcho/Zep/Mem0)

| Operation | Mnemosyne | competitors |
|---|---|---|
| Write | 0.81ms | 45-85ms |
| Read | 0.076ms | 38-62ms |
| Search | 1.2ms | 52-78ms |
| Cold Start | 0ms | 300-800ms |

Speed advantage: 43-500x faster.

## Comparison

| Feature | Mnemosyne | Honcho | Zep | Mem0 |
|---|---|---|---|---|
| Cost | Free | $$$ | $$$ | Freemium |
| Hosting | Local | Cloud | Cloud | Cloud |
| Privacy | 100% local | External API | External API | External API |
| Offline | ✓ | ✗ | ✗ | ✗ |
| Setup | pip install | Docker + keys | Docker + Postgres | API key |

## When to Use

**Use now:**
- SOUL.md + MEMORY.md + wiki need unification
- session_search is too slow or irrelevant
- Want one SQLite file = full agent memory

**Not needed yet:**
- Currently in survival mode (outreach > infrastructure)
- Hermes already has session_search + persistent wiki

## Priority for Juan's stack

🟡 **Medium** — Revisit when in scale mode, cash flow positive.

## Installation

```bash
pip install mnemosyne-memory
pip install mnemosyne-memory[all]  # + dense retrieval + local LLM
python -m mnemosyne.install         # as Hermes MemoryProvider
```

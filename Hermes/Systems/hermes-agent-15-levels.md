# 15 Levels of Hermes Agent — Referencia

> Fuente: Artículo viral de YanXbt (@IBuzovskyi) — 423K views, Jun 2026
> Medium: https://nitingavhane.medium.com/15-levels-of-hermes-agent-from-chatbot-to-24-7-autonomous-system-da15c3c204f6
> Tweet: https://x.com/IBuzovskyi/status/2068629714776756339
> Guardado: 2026-07-01

---

## Fase 1: Basics (Levels 1–3)

| Nivel | Nombre | Qué es |
|---|---|---|
| **1** | One-shot prompts | Typing a prompt, getting a response. Using Hermes as a chatbot. Basic stuff. |
| **2** | Direct access to specialists | Connecting to specific tools/APIs directly |
| **3** | One front door | One front door coordinating multiple specialists. Hermes becomes an orchestrator routing to different capabilities. |

> *"Levels 1-3 = fancy chatbot."*

---

## Fase 2: Infrastructure (Levels 4–7)

| Nivel | Nombre | Qué es |
|---|---|---|
| **4** | VPS + persistent agent | Hermes lives on a server, runs 24/7 without your laptop open |
| **5** | Messaging gateway | Connected to Telegram/Discord/WhatsApp — you talk to it from anywhere |
| **6** | Cron jobs + scheduled tasks | Hermes runs tasks on schedule without you asking |
| **7** | Memory + learning loop | Persistent memory across sessions. Remembers context, preferences, patterns. Starts feeling like a team member that learns. |

> *"The magic happens in the shift from Levels 1-3 to Levels 4-7. Once you hit 5-7, it feels like having a tireless team member, or even a mini department, that learns from every task."* — Michael Guo

> Levels 3-4 require real infrastructure knowledge: Docker, VPS, SSH, the control room structure. Don't skip Level 1.

---

## Fase 3: Autonomy (Levels 8–15)

| Nivel | Nombre | Qué es |
|---|---|---|
| **8** | Multiple profiles | Specialized agents for one job each. A Scout, a Coder, an Ops agent — each with its own personality, memory, skills. |
| **9** | Orchestrated team | An orchestrator routing work through specialist agents |
| **10** | Skills system | Agent creates and reuses procedural memory. Self-evolving skills. |
| **11** | Handoffs + async work | Work flows between agents asynchronously via handoffs |
| **12** | Automated team | Cron/events fire jobs, orchestrator routes through task bus, team handles work without you |
| **13** | Self-improvement | Agent improves its own skills over time (GEPA optimization) |
| **14** | Full business automation | Agent runs business processes end-to-end |
| **15** | 24/7 autonomous system | The system runs your business without you. It gets better over time. |

> *"Hermes runs without you. The system gets better over time."*

---

## Dónde estamos nosotros (2026-07-01)

Nuestro setup: brain-vps (VPS Contabo) + brain-local (PC Juan) + profiles empresariales.

| Feature | Estado | Level |
|---|---|---|
| One-shot prompts | ✅ | 1 |
| Direct tool access | ✅ | 2 |
| Orchestrator routing | ✅ | 3 |
| VPS 24/7 | ✅ | 4 |
| Telegram gateway | ✅ | 5 |
| Cron jobs (agenda, backups) | ✅ | 6 |
| Memory + learning loop (MEMORY.md, patterns.md) | ✅ | 7 |
| Multiple profiles (wolfim-growth, ango-commercial, etc.) | ✅ | 8 |
| Orchestrated team (brain-vps coordina) | ✅ | 9 |
| Skills system | ⚠️ Parcial | 10 |
| Handoffs async (vps-to-local) | ✅ | 11 |
| Automated team (cron → profiles) | ⚠️ Parcial | 12 |
| Self-improvement (GEPA) | ❌ | 13 |
| Full business automation | ❌ | 14 |
| 24/7 autonomous system | ❌ | 15 |

**Veredicto: Level 8-12 consolidado. Gap principal en Levels 10, 12 y 13.**

---

## Qué falta para subir

### Level 10 — Skills auto-evolutivos
- Que los profiles generen skills automáticamente cuando resuelven problemas nuevos
- Que los skills se mejoren solos con cada uso
- Ya tenemos el mecanismo (skill_manage), pero no está automatizado

### Level 12 — Automated team completo
- Cron → orchestrator → profiles → resultado sin intervención de Juan
- Ya funciona para backups y agenda
- Falta para: pipeline comercial, outreach, reporting automático

### Level 13 — GEPA / Self-improvement
- Que el sistema evalúe su propio rendimiento
- Que ajuste SOUL.md, patterns.md, skills basándose en resultados
- Que identifique qué funciona y qué no, y corrija solo

---

## Referencias adicionales

- [Shann³ — 4 Levels of Hermes Agent setup](https://x.com/shannholmberg/status/2056410242330874349)
- [Michael Guo — Response to the 15 levels](https://x.com/Michaelzsguo/status/2067980808200003875)
- [Akshay Pachaar — Hermes Agent Crash Course (YouTube)](https://www.youtube.com/watch?v=bNp6YcKBLgY)
- [Hermes Agent Docs — Profiles](https://hermes-agent.nousresearch.com/docs/user-guide/profiles)
- [Hermes Agent Docs — Skills](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills)
- [Hermes Agent Docs — Learning Path](https://hermes-agent.nousresearch.com/docs/getting-started/learning-path)

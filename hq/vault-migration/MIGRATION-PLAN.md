---
type: migration
created: 2026-05-02
status: pending
---

# Obsidian Vault Migration Plan

## Target Structure

```
obsidian-vault/
├── 00-Intake/                          ← Hermes writes here only
├── 01-Companies/
│   ├── wolfim/
│   │   ├── co-wolfim.md                ← Company note (master)
│   │   ├── campaigns/
│   │   ├── clients/
│   │   └── finance/
│   └── ango/
│       ├── co-ango.md
│       ├── campaigns/
│       ├── my-roles.md                 ← Juan's responsibilities
│       └── finance/
├── 02-Projects/
│   └── proj-[name].md
├── 03-Systems/
│   └── sys-[name].md
├── 04-Intelligence/
│   ├── insights/
│   ├── decisions/
│   └── reviews/
├── 05-Thinking/
│   ├── research/res-[topic].md
│   ├── tools/tool-[name].md
│   ├── skills/skill-[name].md
│   └── ideas/idea-[name].md
├── 06-Finance/
├── 07-Meta/
│   ├── system-map.md
│   ├── principles.md
│   └── changelog.md
└── *99-Archive/*
```

---

## Inventory

### Se crea (0 archivos → existe)

| Carpeta / archivo | Nota |
|---|---|
| `00-Intake/` | |
| `01-Companies/ango/` | |
| `03-Systems/` | |
| `04-Intelligence/` | |
| `04-Intelligence/insights/` | |
| `04-Intelligence/decisions/` | |
| `04-Intelligence/reviews/` | |
| `05-Thinking/` | |
| `05-Thinking/research/` | |
| `05-Thinking/tools/` | |
| `05-Thinking/skills/` | |
| `05-Thinking/ideas/` | |
| `06-Finance/` | |
| `07-Meta/` | |
| `07-Meta/system-map.md` | |
| `07-Meta/principles.md` | |
| `07-Meta/changelog.md` | |
| `99-Archive/` | |

### Se mueve y renombra

| Origen | Destino |
|---|---|
| `wolfim/README.md` + `wolfim/BRAND.md` | `01-Companies/wolfim/co-wolfim.md` |
| `wolfim/finances/revenue-tracker.md` | `01-Companies/wolfim/finance/` |
| `wolfim/google-ads/` | `01-Companies/wolfim/campaigns/` |
| `wolfim/projects/webagency.md` | `02-Projects/proj-webagency.md` |
| `wolfim/projects/portfolio-servicios.md` | `02-Projects/` |
| `gpt/LOOP-outreach.md` | `03-Systems/sys-outreach.md` |
| `gpt/WHATSAPP-BRIDGE-PLAN.md` | `03-Systems/sys-whatsapp-bridge.md` |

### Se archiva (mover a 99-Archive/)

- `companies/` (vacío tras migrar)
- `sessions/` (redundante con hq/sessions)
- `gpt/` (vacío tras migrar)
- `analyses/`, `finances/`, `inbox/` (vacíos)
- Untitled canvas/base en raíz
- `projects/wolfim/outreach-base.md` → `01-Companies/wolfim/campaigns/`

### Se borra

- Todo lo que quede vacío en origen tras mover

---

## Pendiente por definir

- [ ] `01-Companies/ango/` — ¿qué industria/servicios hace Ango? Necesito esto para la estructura interna correcta
- [ ] `01-Companies/wolfim/co-wolfim.md` — ¿Juan lo arma o lo hacemos juntos?

# MEMORY.md — Estado de negocio
# Master: vault/Hermes/MEMORY.md (GitHub synced → PC + Android)
# Escrito por Hermes al cerrar sesión. Una sola fuente de verdad.

---
## Última actualización
2026-05-10 20:50 | Informe UX Conforti enviado. Luis Farias en viaje — vuelve julio, agendar follow-up. MEMORY actualizado.

---

## Semáforo
🔴 Crítico — Gap: –$475/mes | $425 ingresados / $900 gastos

---

## Estructura vault
```
Hermes/
├── Clients/          — 1 índice por cliente (Franco-Roma, Luis-Farias, Ann...)
├── Leads/            — Prospectos fríos (117 concesionarias + manuales)
├── Pipeline/         — Leads en conversación activa
├── Daily/            — Resúmenes diarios
├── Sessions/         — Sesiones de trabajo
├── projects/         — Mockups y proyectos web
└── MEMORY.md         — Este archivo
```

---

## Pipeline activo

| Lead | Empresa | Valor | Estado | Próxima acción |
|---|---|---|---|---|
| Franco Roma | Roggero & Roma | $400 + $25/mes | ✅ Cerrado — $200 adelantados 02/05 | **Cobrar $200 restantes** |
| Luis Farias | Farias & Asociados | $300 + $50/mes | ⏳ En viaje — vuelve julio, retomar seguimiento | **Follow-up julio 2026 cuando vuelva** |
| Ann | Documental de cine | — | 🟡 Pitch enviado | Seguimiento (Juan) |
| Comforti Propiedades | — | — | Sin contactar | Integrar a outreach |
| Rivas Inmuebles | — | — | Sin contactar | Integrar a outreach |
| Gamma | — | — | Sin contactar | Integrar a outreach |

**117 leads concesionarias** en Supabase → `concesionarias_autos` — outreach en curso (200 mensajes enviados, 2-3 tibios, 0 cierres). Próxima sesión: diagnóstico de respuestas.

---

## Checkpoints China (octubre 2026)
- Julio: $400/mes
- Agosto: $700/mes
- Septiembre: $1.000/mes (2+ fuentes activas)

---

## USD cobrados
| Mes | Ingreso | Gasto | Gap |
|---|---|---|---|
| Abril 2026 | $400 | $900 | –$500 |
| Mayo 2026 | $425 | en curso | –$475 |

**Ingresos mayo:** Franco Roma $200 + Construvial $225

---

## Última acción comprometida
- ✅ Follow-up Luis Farias — enviado 10/05 20:27 (pregunta abierta, no push)
- Follow-up Franco Roma — cobrar $200 restantes (pendiente)
- Juan escanea QR WA (pendiente 8+ días)
- Revisión semanal — esta noche dom 10/05

---

## Daemon outreach — estado técnico
- **outreach-daemon**: Running ✅ (pid variable — verificar con `pm2 list`)
- **Bug timezone**: FIXED
- **Bug EACCES state.json**: FIXED
- **Bug Baileys 401 loop**: FIXED
- **⚠️ WA desconectado**: Número requiere re-autenticación (QR scan pendiente)
- **DataImpulse sin crédito** (mayo 2026): proxy 823 bloqueado desde VPS. Sin Maps scraping hasta nuevo crédito o alternativa.
- **Regiones + verticales**: Neuquén + Vaca Muerta = Oil & Gas. San Juan + Catamarca = Mining.
- **Leads disponibles**: 1,433 en JSON + 117 en Supabase `concesionarias_autos`
- **QR files**: `/home/hermes/data/baileys-connect/qr.txt` y `/home/hermes/workspace/projects/outreach-connect-daemon/direct-qr.png`

---

## Cron jobs — fixes aplicados 2026-05-05 + root cause fix 2026-05-06
- ✅ Bug `repeat` job `5fea8d5dad57` — `"5/999999"` → objeto JSON
- ✅ Morning Report `bd62f9437fa4` — deliver `local` → `origin` (Telegram)
- ✅ Hermes Auto-Solve — migrado a `no_agent` mode
- 🔴 ROOT CAUSE: model_dump crash en run_agent.py línea 8890 — MiniMax SDK devuelve dict-subclass con model_dump() roto
- ✅ Fix en run_agent.py: hasattr(model_dump) and not isinstance(dict) primero
- ⚠️ FIX PENDIENTE: Juan debe restart hermes-agent para pick up fix de run_agent.py (`hermes update && hermes gateway restart`)
- 10 cron jobs aún fallando — requieren restart del gateway

---

## Viaje San Juan — Mining Expo 6-8 Mayo 2026
- Hotel: **Hotel Media Agua** (localidad Media Agua, ruta 20, ~30-40km de San Juan Capital)
- Fechas: noches del 6 y 7 de mayo
- Estadio del Bicentenario — San Juan Capital
- ⚠️ Casi todo ocupado por la expo

---

## Modo
Ejecución

---

## LLM Stack — modelos disponibles

| Provider | Modelos | Costo |
|---|---|---|
| MiniMax (default) | minimax-2.7, minimax-2.5, deepseek-v4-pro | $10/mes (infinito) |
| OpenCode Go | glm-5, qwen3.5-plus, kimi-k2.5, deepseek-v4-pro, minimax-m2.5, etc. | $5/mes |
| Bedrock | llama3-8b, nova-lite, kimi-k2 | gratis |

LiteLLM corriendo en localhost:4000 con 16 modelos configurados.
Para cambiar modelo durante sesión: `/model opencode/qwen3.5-plus` o el que quieras.

---

## Companies

### Wolfim — Operativa
- Sector: Software SaaS (WhatsApp outreach para inmobiliarias)
- Dueño: Juan Manuel Gomariz
- Activa: cliente Franco Roma ($400 + $25/mes) + Luis Farias (PDF enviado)
- Outreach: daemon WA activo, leads inmobiliarias en Supabase
- vault: `/home/hermes/obsidian-vault/companies/wolfim/`
- workspace: `/home/hermes/workspace/companies/wolfim/`

### Ango — Metalúrgica del Padre
- Sector: Metalurgia / Industrial
- Dueño: Padre de Juan
- Estado: arrancando — estructura creada 2026-05-09
- Necesidad: digitalización comercial, outreach a empresas industriales
- vault: `/home/hermes/obsidian-vault/companies/ango/`
- workspace: `/home/hermes/workspace/companies/ango/`
- **Pendiente:** definir productos, mercado objetivo, leads

### Construvial — Constructora del Amigo
- Sector: Construcción / Obra civil
- Dueño: Amigo de Juan
- Estado: arrancando — estructura creada 2026-05-09
- Necesidad: digitalización comercial, outreach a desarrollistas y gobierno
- vault: `/home/hermes/obsidian-vault/companies/construvial/`
- workspace: `/home/hermes/workspace/companies/construvial/`
- **Pendiente:** definir productos, mercado objetivo, leads

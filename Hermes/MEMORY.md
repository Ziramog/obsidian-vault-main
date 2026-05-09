# MEMORY.md — Estado de negocio
# Master: vault/Hermes/MEMORY.md (GitHub synced → PC + Android)
# Escrito por Hermes al cerrar sesión. Una sola fuente de verdad.

---
## Última actualización
2026-05-08 20:00 | Cron session. Sin ingresos nuevos en mayo. Luis Farias: 8+ días sin respuesta. Franco Roma: $200 pendientes de cobro. WA desautenticado 8+ días. ~10 cron jobs pendientes restart. Sin actividad comercial humana desde 28/04. Semáforo 🔴 Crítico (-$700/mes). Revisión semanal domingo 11/05.

---

## Semáforo
🔴 Crítico — Gap: –$700/mes | $200 ingresados / $900 gastos

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
| Luis Farias | Farias & Asociados | $300 + $50/mes | PDF enviado — **sin respuesta 8+ días** | **Follow-up urgente** |
| Ann | Documental de cine | — | 🟡 Pitch enviado | Seguimiento (Juan) |
| Comforti Propiedades | — | — | Sin contactar | Integrar a outreach |
| Rivas Inmuebles | — | — | Sin contactar | Integrar a outreach |
| Gamma | — | — | Sin contactar | Integrar a outreach |

**117 leads concesionarias** en Supabase → `concesionarias_autos` — outreach pendiente.

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
| Mayo 2026 | $200 | en curso | –$700 |

---

## Última acción comprometida
- Follow-up Luis Farias (pendiente 10+ días — crítico)
- Follow-up Franco Roma — cobrar $200 restantes (urgente)
- Juan escanea QR WA — pendiente 8+ días
- Juan ejecuta `hermes update && hermes gateway restart` — pendiente
- Revisión semanal domingo 11/05

---

## Daemon outreach — estado técnico
- **outreach-daemon**: Running ✅ (pid variable — verificar con `pm2 list`)
- **Bug timezone**: FIXED
- **Bug EACCES state.json**: FIXED
- **Bug Baileys 401 loop**: FIXED
- **⚠️ WA desconectado**: Número requiere re-autenticación (QR scan pendiente)
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

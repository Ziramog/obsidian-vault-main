# MEMORY.md — Estado de negocio
# Master: vault/Hermes/MEMORY.md (GitHub synced → PC + Android)
# Escrito por Hermes al cerrar sesión. Una sola fuente de verdad.

---
## Última actualización
2026-05-05 | Sesión cron: auto-solve — daemon estabilizado, WA necesita re-autenticación

## Semáforo
🔴 Crítico — Gap: –$700/mes | $200 ingresados / $900 gastos

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
| Franco Roma | Roggero & Roma | $400 + $25/mes | ✅ Cerrado — $200 adelantados | Mantenimiento $25/mes |
| Luis Farias | Farias & Asociados | $300 + $50/mes | PDF enviado — evalúa esta semana | Follow-up (Juan) |
| Ann | Documental de cine | — | 🟡 Pitch enviado — esperando respuesta | Seguimiento (Juan) |
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
- Follow-up Luis Farias (pendiente 5 días)
- Follow-up Franco Roma — cobrar $200 restantes
- Outreach a 117+ leads de concesionarias (WA necesita re-autenticación primero)

## Daemon outreach — estado técnico
- **outreach-daemon**: Running ✅ (pid 421522, restart 0, 99MB RAM)
- **Bug timezone**: FIXED — `isBusinessHours()` ahora usa Intl API (Argentina correcta)
- **Bug EACCES state.json**: FIXED — permisos 666
- **Bug Baileys 401 loop**: FIXED — ahora pide QR fresco en vez de colgar
- **Bug ecosystem.config**: FIXED — cwd/args/exec_mode corregidos
- **⚠️ WA desconectado**: Número de WhatsApp requiere re-autenticación (QR scan)
- **Leads disponibles**: 293 + 140 + 1.000 = 1.433 leads en archivos JSON

---

## Modo
Ejecución

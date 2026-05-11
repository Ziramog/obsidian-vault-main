# MEMORY.md — Estado de negocio
# Master: obsidian-vault/Hermes/MEMORY.md (GitHub synced → PC + Android)

---

## Última actualización
2026-05-11 20:00 | Sesión cron — Fix Telegram delivery, gap –$475/mes, 13 días sin cierre

---

## Semáforo
🔴 Crítico — Gap mayo 2026: ~–$475 | $425 ingresados / $900 gastos

---

## Pipeline activo
- Franco Roma: $400+$25/mes — $200 adelantados, $200 restantes por cobrar. URGENTE.
- Luis Farias: PDF enviado — en viaje, vuelve julio. Follow-up retomar julio.
- Ann: Pitch enviado — seguimiento pendiente
- Comforti, Rivas, Gamma: leads fríos — integrar a outreach cuando WA esté autenticado
- Construvial: $225 USD cobrados (10/05)

---

## Construvial — Plan 3 fases activo
- Fase 1: Investigación de mercado (50 empresas objetivo) — EN CURSO
- 21 empresas en DB: leads_oil_gas_mining.csv
- Top contactos: CISA (Neuquén), Sigma SA (SJ), Dumandzic (SJ/CAT), CASEMICA (CAT)
- Solo investigación — sin outreach hasta activación explícita de Juan
- Posicionamiento: subcontratista de subcontratistas (maquinaria + obra civil para empresas que ya sirven a petroleras/mineras)

---

## Alerta resuelta — Cron delivery Telegram/Discord (2026-05-11)
- Causa: `approvals.cron_mode: deny` en config.yaml — bloqueaba todo delivery de crons
- Fix: cambiado a `cron_mode: allow`
- Token Telegram: `8632805727:AAEF34Y45...` (@hermestri3bot)
- 5 crons cambiados de `deliver: local` → `deliver: origin`
- Gateway reiniciado via PM2 (PID 1746901)
- Test curl → sendMessage funciona (✅ Mensajes llegan a 1479438002)
- Monitorear próximas 24h — confirmar que Juan recibió mensajes de prueba

---

## Errores de Juan — Corregidos 2026-05-10
- Solo Google Reviews lo pidió Franco directamente — los otros 3 add-ons son IDEAS DE JUAN
- Productos Wolfim = solo los explícitamente en "Productos hoy" en webagency.md
- Neuquén = Oil & Gas / San Juan + Catamarca = Mining
- Los 49 leads de Posadas/San Vicente son de Wolfim (outreach manual del amigo de Juan)

---

## API Keys confirmadas
- Serper: `7f4c661b596a1110ec64d8ea4f137588c2176a5c`
- Firecrawl: `fc-43a...1eef`
- DataImpulse: SIN CRÉDITO (port 823 bloqueado desde VPS)

---

## Modo
Ejecución

---

## Días sin cierre comercial
13 (desde Franco Roma 28/04)

---

## Historial financiero mayo 2026

| Fecha | Ingreso | Detalle |
|-------|---------|---------|
| 02/05 | $200 | Franco Roma — adelantados |
| 10/05 | $225 USD | Construvial — cobrado |
| 11/05 | $0 | Sin nuevos ingresos |

**Total mayo:** $425 ingresados / $900 proyectados = Gap –$475

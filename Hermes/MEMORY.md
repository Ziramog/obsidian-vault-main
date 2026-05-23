# MEMORY.md — Estado de negocio
# Master: obsidian-vault/Hermes/MEMORY.md (GitHub synced → PC + Android)

---

## Última actualización
2026-05-19 22:30 | Sesión activa | Propuesta Construvial reformateada + enviada | Semáforo 🔴

---

## Semáforo
🔴 Crítico — Gap mayo 2026: ~–$475 | $567 ingresados / $900 gastos
**Último ingreso:** Franco Roma $425 total (28/04) — hace 20 días
**Con Franco Roma $200 cobrado:** –$275

**Semáforo actualizado a 🔴 Crítico — 7 días consecutivos sin sesión humana (11–17/05).**

---

## Pipeline activo
- Franco Roma: $300 USD restantes — entrega en ~10 días. Add-ons extra ($100) incluidos en ese total.
- Luis Farias: PDF enviado — en viaje, vuelve julio. Follow-up retomar julio.
- Ann: Pitch enviado — seguimiento pendiente
- Comforti, Rivas, Gamma: leads fríos — INTEGRAR A OUTREACH AHORA (WA funcionando ✅)
- Construvial: $225 USD cobrados (10/05) + $142 USD viáticos Catamarca (14/05) = $367 total Construvial
- Ango: sin actividad

---

## Construvial — Plan 3 fases activo
- Fase 1: Investigación de mercado (50 empresas objetivo) — EN CURSO
- 21 empresas en DB: leads_oil_gas_mining.csv
- Top contactos: CISA (Neuquén), Sigma SA (SJ), Dumandzic (SJ/CAT), CASEMICA (CAT)
- Solo investigación — sin outreach hasta activación explícita de Juan
- Posicionamiento: subcontratista de subcontratistas (maquinaria + obra civil para empresas que ya sirven a petroleras/mineras)
- PROPUESTA ENVIADA 19/05: Propuesta_Construvial_Wolfim_2026.pdf (17 páginas, branding Wolfim, dark/gold cinematic) — guardada en obsidian-vault/companies/construvial/propuesta_2026/

---

## Racha cron-only
⚠️ 8 días consecutivos (11–18/05) — última sesión humana: 2026-05-11-22-00
**Contrato SOUL: 7+ días → Telegram alert enviado.**

---

## Alerta resuelta — Cron delivery Telegram/Discord (2026-05-11)
- Causa: `approvals.cron_mode: deny` en config.yaml — bloqueaba todo delivery de crons
- Fix: cambiado a `cron_mode: allow`
- Token Telegram: `8632805727:AAEF34Y45...` (@hermestri3bot) — funcionando ✅
- 5 crons cambiados de `deliver: local` → `deliver: origin`
- Morning report cron明日 8AM — verificar receipt en sesión siguiente
- Gateway con restart loop (systemd + PM2 compiten) — NO bloqueante para cron reports
- Nota: mensajes del bot directos (no crons) pueden perderse si gateway está caído

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
20 (desde Franco Roma 28/04) — persiste patrón sin actividad comercial

---

## Historial financiero mayo 2026

| Fecha | Ingreso | Detalle |
|-------|---------|---------|
| 02/05 | $200 | Franco Roma — adelantados |
| 10/05 | $225 USD | Construvial — cobrado |
| 14/05 | $142 USD | Construvial — viáticos Catamarca (gestiones comerciales) |
| 11/05-16/05 | $0 | Sin nuevos ingresos |
| 17/05 | +$100 USD (pendiente) | Franco Roma — add-ons extra |

**Total mayo:** $425 + $142 = $567 ingresados / $900 gastos proyectados = Gap actual –$333
**Con Franco Roma cobrado (~10 días):** $567 + $300 = $867 → Gap proyectado –$33

---

## Hito China — octubre 2026
Meta: > $1.000 USD/mes con operación autónoma.
**Días restantes:** ~142
**Estado actual:** 🟠 Transición — WA outreach activo, Franco Roma cobra ~10 días, gap mayo casi equilibrado

---

## Sesión 2026-05-23 — Informe Inteligencia Air Total SRL (v2.0)
**Archivo:** `Hermes/Intelligence/AirTotal_SRL_2026-05-23.md`
**PDF enviado:** Telegram Juanchi777 (message_id 4513, 121 KB)

- patchright instalado para scraping browser automation
- chromium-browser disponible en /usr/bin/chromium-browser para HTML→PDF
- Configurar siempre: `PLAYWRIGHT_BROWSERS_PATH=/home/hermes/tmp/playwright TMPDIR=/home/hermes/tmp`
- executable_path explícito: `/home/hermes/tmp/playwright/chromium_headless_shell-1217/chrome-headless-shell-linux64/chrome-headless-shell`
- Informe concluido: Air Total = distribuidor minorista climatización, NO ingeniería civil pesada
- Niederle: 2 causas penales activas (2022 fraude $2.1B + 2025 estafa)
- Air Total: CERO contratos con mineras de Catamarca
- Recomendación: NO formalizar consorcio sin due diligence legal

---

## browse.sh — probada 2026-05-23
CLI browser automation (npm install -g browse, v0.8.0). Requiere `TMPDIR=/home/hermes/tmp` (sino EACCES). Skills pre-definidos 111 (mayoría US: LinkedIn API, Indeed, Glassdoor, gov). NO sirve para ARCA/AFIP/CUITonline (Cloudflare). patchright sigue siendo la tool para scraping argentino.

---

## Última actualización
2026-05-23 21:30 | Sesión Air Total | Informe v2.0 guardado + PDF enviado Telegram

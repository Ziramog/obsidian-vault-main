# MEMORY.md — Estado de negocio
# Master: obsidian-vault/Hermes/MEMORY.md (GitHub synced → PC + Android)

---

## Última actualización
2026-05-11 08:30 | Sesión — fix cron_mode deny→allow, gateway reiniciado PM2

---

## Semáforo
🔴 Crítico — Gap mayo 2026: ~–$475 | $425 ingresados / $900 gastos

---

## Pipeline activo
- Franco Roma: $400+$25/mes — 50% recibido, frontend en desarrollo. Add-ons para pronta implementación (1 pedido Franco + 3 ideas Juan)
- Luis Farias: PDF enviado — sin respuesta 10+ días. Vuelve julio.
- Ann: Pitch enviado — seguimiento Juan
- Comforti, Rivas, Gamma: leads fríos — integrar a outreach cuando WA esté autenticado

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
- Gateway reiniciado via PM2 (PID 1746901)
- Monitorear próximas 24h — si vuelven a fallar, revisar `allowed_chats` en Telegram config

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

## 2026-05-11 — Fix Telegram cron delivery

**Problema:** Cron reports no llegaban a Telegram hace ~10 días. Dos causas:
1. 5 crons con `deliver: local` (guardaban output a archivo, no enviaban a Telegram)
2. Token Telegram `8644817415:AAFHV8fx...` daba 401 Unauthorized (revocado/inválido)

**Solución aplicada:**
- 5 crons cambiados de `deliver: local` → `deliver: origin` (Morning Report 8AM, Health Check x2, Hermes Daily Update 6AM, Morning Report Test 11AM)
- Token Telegram actualizado a `8632805727:AAEF34Y45...` (@hermestri3bot — bot nuevo creado x Juan)
- Gateway restart vía PM2/systemd
- Test curl → sendMessage funciona (✅ Mensajes llegan a 1479438002)
- morning-report.py confirmado funcional (envía directo, no depende del gateway)

**Juan debe confirmar:** ¿le llegaron los mensajes de prueba a Telegram?

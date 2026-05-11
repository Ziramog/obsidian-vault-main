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
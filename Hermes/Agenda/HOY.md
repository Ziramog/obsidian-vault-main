---
owner: brain-vps
date: 2026-08-31
updated-at: 2026-08-31T10:03:46-03:00
summary-status: active
source: cron-campaign
---

# Agenda 2026-08-31

## 🔴 Arrastre / requiere confirmación de Juan

- [ ] **Actualizar KPIs formales** — ingresos cobrados del mes, gastos fijos, gap mensual, objetivo vigente. Vencido desde 2026-06-25.
- [ ] **Decidir Web Viejas** — reabastecer leads nuevos o pausar canal y hacer follow-up humano. La cola actual no genera contactos nuevos.
- [ ] **Hacer follow-up humano** — Luis Farias primero; después Conforti, RIVAS y Ann.
- [ ] **Revisar handoff Wolfim Motors Demo `HO-2026-08-03-002`** — high, vencido, sin response visible.
- [ ] **Cerrar/actualizar handoffs ANGO vencidos** — `HO-2026-07-16-001`, `HO-2026-07-22-001`, `HO-2026-07-24-001`, `HO-2026-07-27-001`.
- [ ] **Triage Hermes update/gateway** — `hermes --version` al cierre previo seguía 46 commits behind; gateway activo pero con conflicto Telegram polling.
- [ ] **Revisar backup offsite Roggero & Roma** — backup local OK, subida Google Drive falló con WARN en arrastre previo.
- [ ] **Limpiar memoria persistente bloqueada `hermes_env`** — pendiente por drift de memoria.

## ✅ Cerrado hoy

- [x] **`cron_campaign.py` ejecutado 10:03 ART:** exit code 0; stdout: `✅ Todos los leads han sido enviados. No hay más pendientes.`
- [x] **Tracker Web Viejas verificado 10:03 ART:** 121 leads fuente; 107 registros: 97 `sent`, 10 `bounced`, 0 `failed`; 0 pendientes componibles; 19 no componibles.
- [x] **Check replies Gmail 14:02 ART:** `himalaya envelope list -s 10` revisado; delta 18 mensajes desde id 69719 a 69737; 0 respuestas nuevas a campaña `Noté algo en la web de...`.

## 🟡 Atención operativa

- Semáforo financiero no confirmable: `kpis.md` sigue incompleto/vencido.
- Briefing vigente vencido: no cambiar prioridades sin Juan.
- Web Viejas necesita inventario nuevo o follow-up/cierre humano; seguir corriendo cron sin leads es ruido operativo.

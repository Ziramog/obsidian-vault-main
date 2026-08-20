---
owner: brain-vps
date: 2026-08-20
updated-at: 2026-08-20T10:01:07-03:00
---

# HOY

- [x] Ejecutar `python3 /home/hermes/workspace/scraping/cron_campaign.py`
  - Resultado: `✅ Todos los leads han sido enviados. No hay más pendientes.`
  - Verificación tracker: 107 registros totales, 97 `sent`, 10 `bounced`, 0 pendientes.
- [x] Ejecutar `check-replies`
  - Resultado: `Sin novedades`.
  - Verificación real: `himalaya envelope list -s 10` mostró top IDs `69151, 69150, 69149, 69148, 69146, 69145, 69147, 69144, 69143, 69142`; delta desde top ID previo `69133` = **18 emails nuevos** (`69134`–`69151`). Cross-check real contra `campaign_tracker.csv` (97 recipients enviados / 83 business domains) no detectó matches exactos de remitente, overlaps de dominio + `Re:` ni asuntos con el prefijo de campaña.

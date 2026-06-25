# Cron del VPS — documentación

> Documentar aquí los cron jobs del sistema. No modificar los crons sin tener un reemplazo activo funcionando primero.

## System crontab (crontab -l)

```
# Vault sync a GitHub cada 15 min
*/15 * * * * cd /home/hermes/obsidian-vault && git add -A && git diff --cached --quiet || (git commit -m "auto-sync $(date +\%Y-\%m-\%d\ \%H:\%M)" && git push) 2>/dev/null

# Health check 4 AM Argentina (7 AM UTC)
0 7 * * * /home/hermes/scripts/hermes-health-check.py >> /home/hermes/.hermes/logs/health.log 2>&1

# Backup Roggero & Roma — Saturdays 10am
0 10 * * 6 cd /home/hermes/roggero_backup && set -a && source .env_roggero && set +a && bash scripts/backup.sh >> /home/hermes/roggero_backup/logs/backup_cron.log 2>&1
```

### Detalle

| Línea | Función | Frecuencia | Crítico | Notas |
|---|---|---|---|---|
| 1 | Sync vault a GitHub | cada 15 min | ✅ Sí | Agente nunca toca git. El cron es independiente. |
| 2 | Health check + auto-recovery | 7am daily | ✅ Sí | Envía alerta a Telegram si hay problemas. |
| 3 | Backup Roggero & Roma | Sáb 10am | ⚠️ Medio | Cliente externo, backup semanal. |

## Hermes cron jobs activos (jobs relevantes)

| Job ID | Nombre | Schedule | Notas |
|---|---|---|---|
| e38de9d79984 | Daily Email Summary | 13:00 daily | Repasa inbox de Gmail. |
| c8d3387aa5b3 | Hermes daily update | 9:00 daily | `hermes update && hermes gateway start` |
| 53a5bb507d02 | Daily Session Summary | 20:00 daily | Escribe resumen de sesión al vault. |
| 5fea8d5dad57 | Session End-of-Day | 23:55 daily | Procesa sesión del día. |
| d5538f25b5ca | Hermes Daily Health Check | 4:00 daily | Versión corregida del health check. |
| bd62f9437fa4 | Morning Report 8AM | 11:00 daily | Reporte matutino a Telegram. |
| db02776dd86f | Supabase Keep-Alive | Lun/Jue 6:00 | Evita sleep de Supabase. |
| 87243a0ab3ac | check-replies | 10/14/18 lun-vie | Revisa respuestas de email outreach. |
| 81cf14ebb0ac | wolfim-campaign | 10:00 daily | Ejecuta campaña de outreach email. |

## Hermes cron jobs ELIMINADOS

| Job ID | Nombre | Razón | Fecha |
|---|---|---|---|
| ca40b29010be | Hermes Memory Backup | Redundante con system crontab. Gastaba ~2K tokens/tick. | 2026-06-24 |

## Historial de cambios

| Fecha | Cambio | Autor |
|---|---|---|
| 2026-06-24 | Documentación inicial de cron existentes | brain-vps |
| 2026-06-24 | Eliminado Hermes Memory Backup (ca40b29010be) por redundante | brain-vps |

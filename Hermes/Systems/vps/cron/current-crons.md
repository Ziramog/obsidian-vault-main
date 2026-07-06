# Cron Jobs Activos — VPS

> **Zona horaria:** America/Argentina/Buenos_Aires (UTC-3, ART)
> **Última verificación:** 2026-07-06
> **Host:** Contabo VPS (194.163.161.99)
> **Fase 4:** Scripts de alertas, archivo y validación agregados

---

## User crontab (`crontab -l` — usuario hermes)

| Schedule | Hora (ART) | Comando | Descripción | Fase |
|---|---|---|---|---|
| `0 7 * * *` | 07:00 diario | `/home/hermes/scripts/hermes-health-check.py` | Health check del sistema Hermes | Pre-V5 |
| `*/15 * * * *` | Cada 15 min | `cd /home/hermes/obsidian-vault && git pull --rebase --autostash origin main && git add -A && git diff --cached --quiet \|\| (git commit -m "auto-sync [vps]" && git push)` | Sync del vault a GitHub | Pre-V5 |
| `0 10 * * 6` | 10:00 sábados | `cd /home/hermes/roggero_backup && . ./.env_roggero && bash scripts/backup.sh` | Backup Roggero & Roma | Pre-V5 |
| `*/30 * * * *` | Cada 30 min (+300s) | `sleep 300 && python3 /home/hermes/scripts/telegram-alert.py` | **NUEVO F4:** Handoffs vencidos + conflictos git → Telegram | Fase 4 |
| `15 4 * * *` | 04:15 diario | `python3 /home/hermes/scripts/handoff-archive.py` | **NUEVO F4:** Archiva handoffs done/cancelled > 7 días | Fase 4 |
| `*/15 * * * *` | Cada 15 min (+120s) | `cd /home/hermes/obsidian-vault && python3 Hermes/Systems/vps/scripts/ownership-validate.py --last-commit` | **NUEVO F4:** Valida escrituras dentro de zonas de ownership | Fase 4 |

---

## Root crontab (`sudo crontab -l`)

| Schedule | Hora (ART) | Comando | Descripción |
|---|---|---|---|
| `#DISABLED_F4 0 11 * * *` | desactivado | `/wolfim/crawler/trigger-scan.sh` | Wolfim daily crawl scan |
| `#DISABLED_F4 0 12 * * 0` | desactivado | `SUPABASE_SERVICE_KEY=... python3 /wolfim/link_validator.py` | Link validation (solo `link_status=none`) |
| `#DISABLED_F4 */30 * * * *` | desactivado | `/home/hermes/scripts/session-append.sh` | Session recording (mecánico, 0 LLM) |

---

## Detalles por cron

### Vault sync (`*/15`)
- **Función:** Mantiene el vault sincronizado con GitHub como medio de coordinación VPS ↔ PC local.
- **Log:** `/var/log/vault-sync.log`
- **Mecanismo:** Pull con rebase → add all → commit si hay cambios → push.

### Health check (`0 7`)
- **Función:** Diagnóstico matutino del sistema Hermes.
- **Log:** `/home/hermes/.hermes/logs/health.log`

### Roggero & Roma backup (`0 10 * * 6`)
- **Función:** Backup semanal del sitio Roggero & Roma.
- **Log:** `/home/hermes/roggero_backup/logs/backup_cron.log`

### Telegram alerts (`*/30` — Fase 4)
- **Función:** Detecta handoffs `priority:high` con `escalate-after` vencido y envía Telegram a Juan. También detecta conflictos git (`<<<<<<<`) en archivos críticos.
- **Log:** `/var/log/hermes-alerts.log`
- **Script:** `/home/hermes/scripts/telegram-alert.py`
- **Chat:** Juanchi777 (1479438002)

### Handoff archive (`15 4` — Fase 4)
- **Función:** Archiva handoffs con `status: done` o `cancelled` con más de 7 días de antigüedad. Los mueve a `Hermes/Handoffs/archive/`.
- **Log:** `/var/log/hermes-handoff-archive.log`
- **Script:** `/home/hermes/scripts/handoff-archive.py`

### Ownership validate (`*/15` — Fase 4)
- **Función:** Compara archivos modificados en el último commit contra el mapa de ownership (Sección 11 de ARCHITECTURE.md V5). Detecta escrituras fuera de zona.
- **Log:** `/var/log/hermes-ownership.log`
- **Script:** `/home/hermes/obsidian-vault/Hermes/Systems/vps/scripts/ownership-validate.py`

### Wolfim crawler (`0 11`)
- **Función:** Dispara el scan diario de crawling de Wolfim.
- **Script:** `/wolfim/crawler/trigger-scan.sh`

### Link validation (`0 12 * * 0`)
- **Función:** Validación semanal de links en leads de Wolfim. Procesa solo entradas con `link_status=none`.
- **Log:** `/var/log/wolfim-links.log`
- **Requiere:** SUPABASE_SERVICE_KEY, SERPER_API_KEY, WOLFIM_GGL_KEY, OPENAI_API_KEY (tomados de `/wolfim/sales/.env`)

### Session recording (`*/30`)
- **Función:** Apéndice mecánico de sesión cada 30 min a `hq/sessions/YYYY-MM-DD.md`. Sin LLM.
- **Log:** `/var/log/session-recording.log`
- **Script:** `/home/hermes/scripts/session-append.sh`
- **Nota:** Este cron escribe en `hq/sessions/`, no en `Hermes/Sessions/`. Las sesiones narrativas de Hermes van en `Hermes/Sessions/` por separado.

---

## Scripts de Fase 4 — Resumen

| Script | Ruta vault | Ruta producción | Cron |
|---|---|---|---|
| `telegram-alert.py` | `Hermes/Systems/vps/scripts/` | `/home/hermes/scripts/` | `*/30 * * * *` |
| `handoff-check.py` | `Hermes/Systems/vps/scripts/` | `/home/hermes/scripts/` | Manual / bajo demanda |
| `handoff-archive.py` | `Hermes/Systems/vps/scripts/` | `/home/hermes/scripts/` | `15 4 * * *` |
| `ownership-validate.py` | `Hermes/Systems/vps/scripts/` | `/home/hermes/scripts/` | `*/15 * * * *` |

---

## Crons eliminados

| Nombre | Fecha baja | Motivo |
|---|---|---|
| Hermes Memory Backup (ca40b29010be) | 2026-06-24 | Redundante con system crontab. Era LLM-driven git push cada 15 min (~2K tokens/tick). |

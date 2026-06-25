# Cron Jobs Activos — VPS

> **Zona horaria:** America/Argentina/Buenos_Aires (UTC-3, ART)
> **Última verificación:** 2026-06-25
> **Host:** Contabo VPS (194.163.161.99)

---

## User crontab (`crontab -l` — usuario hermes)

| Schedule | Hora (ART) | Comando | Descripción |
|---|---|---|---|
| `0 7 * * *` | 07:00 diario | `/home/hermes/scripts/hermes-health-check.py` | Health check del sistema Hermes |
| `*/15 * * * *` | Cada 15 min | `cd /home/hermes/obsidian-vault && git pull --rebase --autostash origin main && git add -A && git diff --cached --quiet \|\| (git commit -m "auto-sync [vps]" && git push)` | Sync del vault a GitHub |
| `0 10 * * 6` | 10:00 sábados | `cd /home/hermes/roggero_backup && source .env_roggero && bash scripts/backup.sh` | Backup Roggero & Roma |

---

## Root crontab (`sudo crontab -l`)

| Schedule | Hora (ART) | Comando | Descripción |
|---|---|---|---|
| `0 11 * * *` | 11:00 diario | `/wolfim/crawler/trigger-scan.sh` | Wolfim daily crawl scan |
| `0 12 * * 0` | 12:00 domingos | `SUPABASE_SERVICE_KEY=... python3 /wolfim/link_validator.py` | Link validation (solo `link_status=none`) |
| `*/30 * * * *` | Cada 30 min | `/home/hermes/scripts/session-append.sh` | Session recording (mecánico, 0 LLM) |

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

## Crons eliminados

| Nombre | Fecha baja | Motivo |
|---|---|---|
| Hermes Memory Backup (ca40b29010be) | 2026-06-24 | Redundante con system crontab. Era LLM-driven git push cada 15 min (~2K tokens/tick). |

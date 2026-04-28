# Caída del VPS — 27/04/2026 (incidente resuelto)

> Incident date: 27/04/2026. Resolved same day. Full details in `/home/hermes/Transfer-files/caida_vps_27_04.md`

## Resumen

El VPS 194.163.161.99 se reinició por OOM Killer (Out of Memory). Causa raíz: falta de memoria + ataques SSH bruteforce.

## Causas

| Tipo | Detalle |
|---|---|
| OOM Node | 28GB VM / 6GB RSS — outreach-api/daemon |
| OOM Python | 8GB / 7.2GB RSS — wolfim-cron-alerts |
| Script perdido | `/tmp/start_api.sh` borrado → 820+ restart loops |
| SSH bruteforce | 5 IPs intentando acceso |

## Fixes aplicados

- Swap 2GB ya existía
- PM2 memory limits: 300M (outreach-daemon), 200M (wolfim-*)
- Swappiness = 10
- Fail2ban instalado
- Script `/root/start_api.sh` recreado

## Estado actual

✅ VPS estable, ~7GB RAM disponible, Fail2ban activo

## Ver también

- `hq/sessions/2026-04-28.md` — seguimiento del incidente
- `/home/hermes/Transfer-files/caida_vps_27_04.md` — documento técnico completo

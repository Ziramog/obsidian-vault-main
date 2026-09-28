# Preflight del VPS aplicado al request.md

- **Fecha:** 2026-09-27 ~21:05 -04:00
- **Actor:** brain-local (PC local)
- **Origen:** auditoría de brain-vps sobre `vmi3131751` (100.124.132.48)

## Qué cambió

Se reescribieron los pasos 2, 3, 5 y 6 del §1 de `request.md` y se agregó el **§5
Preflight del VPS — correcciones al plan**, con los 4 hallazgos reales del servidor
más el atajo de `tailscale serve`.

## Hallazgos que pisan el handover original

| # | Hallazgo | Corrección aplicada |
|---|---|---|
| 1 | `HERMES_HOME=/root/.hermes` es falso; corre como `hermes` | `/home/hermes/.hermes` |
| 2 | Node v26.7.0 viene del toolchain de Hermes (sin nvm/volta) | fijar Node 20 por NodeSource y arreglar el PATH del PM2 de `hermes` |
| 3 | No hay startup propio de `hermes`; `dump.pm2` de root vacío | systemd user + linger (o unit como `hermes`) antes de dar por bueno "sobrevive reboot" |
| 4 | Gateway `:8642` responde `401 Invalid gateway API key` | la key la pasa el director por fuera del vault (en la PC local el nombre es `API_SERVER_KEY`) |
| ✔ | `tailscale serve` ya apunta a `127.0.0.1:3000` | Paso 6 saltable |

## Decisiones tomadas

- **Path de deploy:** `/home/hermes/hermes-pwa` en lugar de `/opt/hermes-pwa`
  (mismo usuario dueño de PM2 y `HERMES_HOME`, sin sudo, sin archivos root-owned).

## Estado

Handoff sigue `ready` / `blocked-on: decision-de-juan` (A/B/C para el working tree
de `hermes-pwa`). Nada escrito en el VPS todavía.

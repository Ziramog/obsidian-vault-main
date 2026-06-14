---
title: Hermes Desktop (Windows) ↔ VPS via Tailscale
type: setup
status: funcionando
created: 2026-06-14
updated: 2026-06-14
fuente: sesión 2026-06-14
tags: [hermes, desktop, vps, tailscale, remote, windows, infra]
---

# Hermes Desktop (Windows) ↔ VPS via Tailscale

Objetivo: correr el cliente Electron de Hermes Desktop en Windows, pero mantener el agente, memoria, sesiones y ejecución de comandos en el VPS Linux. **No instalar Hermes en Windows. Sin puertos públicos.**

## Arquitectura (resumen)

Windows corre el cliente Hermes Desktop Electron. El Desktop habla HTTP contra un proceso `hermes dashboard` corriendo en el VPS y bindeado a la IP de Tailscale. El tráfico queda dentro de la tailnet. El dashboard lee `~/.hermes/.env` para credenciales basic-auth y activa el gate automáticamente cuando está bindeado a una IP no-loopback. El usuario se loguea en Desktop con esas credenciales, el session token se firma con un secret estable, y desde ahí Desktop se comporta igual que una instalación local — mismas sesiones, misma MEMORY.md, misma ejecución (corre en el VPS).

## Estado al cierre (14/06/2026) — FUNCIONANDO

- [x] Tailscale daemon instalado y activo en VPS (IP `100.124.132.48` registrada, tailnet `ingjuangomariz@`)
- [x] Cliente Tailscale activo en Windows (`desktop-qu8nhdi`, IP `100.96.176.100`)
- [x] Conexión directa Windows↔VPS verificada (tx 32MB rx 1.3MB acumulados)
- [x] Unit `tailscaled.service` arreglado (tenía un `EOF` huérfano que rompía TUN mode → userspace forzado)
- [x] Credenciales basic-auth generadas y guardadas en `~/.hermes/.env` (modo 600)
- [x] Servicio systemd `hermes-dashboard.service` creado, habilitado y activo
- [x] Bind a `100.124.132.48:9119` verificado con `ss -ltn`
- [x] `/api/status` responde con `auth_required: true, auth_providers: ['basic']` y `gateway_running: true`
- [x] Test end-to-end: Desktop en Windows abrió sesión contra el VPS y cargó MEMORY.md
- [x] `hermes-gateway.service` (Telegram) — `enabled` para arrancar en boot
- [x] Bloque "API Keys confirmadas" removido de MEMORY.md (vault + CLI)
- [x] `keys-status.md` creado en `/home/hermes/.hermes/private/` (modo 600, NO inyectado al system prompt)
- [x] `~/.hermes/memories/MEMORY.md` ahora es symlink al del vault (single source of truth)
- [x] Script `~/bin/hermes-tui` para abrir TUI con un comando (vía SSH desde Windows)
- [x] Vault sincronizado a GitHub (commits `7f1ec67` y `f78e37f`)

## Documentos en esta carpeta

| Archivo | Para qué |
|---|---|
| [setup.md](setup.md) | Paso a paso completo de lo que se hizo (orden de comandos) |
| [troubleshooting.md](troubleshooting.md) | Qué hacer si rompe (conexiones, auth, dashboard caído, etc.) |
| [files-changed.md](files-changed.md) | Diff completo de archivos tocados (qué había → qué hay) |

## TL;DR para el día a día

- **Conectar desde Windows:** abrir Hermes Desktop → Settings → Gateway → Remote URL: `http://100.124.132.48:9119` → Sign in (`juang` / password en `~/.hermes/.env`)
- **Alternativa TUI por SSH:** configurar `~/.ssh/config` con el host `hermes-vps` y alias en PowerShell → `hermes-vps` (instrucciones detalladas en `setup.md` § "Lado Windows")
- **Si algo no anda:** ver `troubleshooting.md`
- **Si querés entender qué cambió:** ver `files-changed.md`

## Credenciales (referencia)

- **Username del dashboard:** `juang`
- **Password:** vive en `~/.hermes/.env` (variable `HERMES_DASHBOARD_BASIC_AUTH_PASSWORD`)
- **Secret de sesión:** vive en `~/.hermes/.env` (variable `HERMES_DASHBOARD_BASIC_AUTH_SECRET`, 32 bytes base64, estable)
- **Backend URL:** `http://100.124.132.48:9119`

> ⚠️ **No commitear el `.env` a git nunca.** El archivo está en `~/.hermes/.env`, modo 600, solo el usuario `hermes` lo lee.

## Servicios systemd (persistencia)

| Servicio | Tipo | Enabled | Linger | Reinicia en reboot |
|---|---|---|---|---|
| `tailscaled.service` | system | sí | n/a | ✅ |
| `hermes-dashboard.service` | system | sí | n/a | ✅ |
| `hermes-gateway.service` | user | sí | sí | ✅ |

`linger=yes` está activo para el usuario `hermes` (`loginctl show-user hermes | grep Linger`), por eso el gateway user-service arranca aunque no haya sesión SSH abierta.

## Tailnet (3 nodos registrados)

```
100.124.132.48   vmi3131751          (VPS)        ← este
100.96.176.100   desktop-qu8nhdi     (Windows)    ← Juan
100.67.21.94     juans-s22-ultra     (Android)    ← offline hace 40 días
```

## Referencias

- Documentación oficial: https://hermes-agent.nousresearch.com/docs/user-guide/desktop (sección "Connecting to a remote backend")
- Skill interna: `~/.hermes/skills/hermes/hermes-vps-ops/references/hermes-desktop-remote-backend.md`
- [[SOUL]] — principios y criterios de decisión
- [[AGENTS]] — arquitectura de carpetas VPS/vault
- `~/.hermes/AGENTS.md` (master) — versión VPS de AGENTS

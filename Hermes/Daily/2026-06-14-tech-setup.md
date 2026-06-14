# Daily Summary — 14 June 2026 (sesión técnica tarde)

> Sesión complementaria al daily comercial del mismo día (que cubre Víctor Abrile y semáforo 🟢). Este doc cubre el setup técnico de Tailscale + Hermes Desktop.

---

## Trabajo técnico ejecutado

**Trigger:** Juan quería conectar el cliente Electron de Hermes Desktop en Windows al Hermes que corre en el VPS, sin instalar Hermes localmente en Windows y sin abrir puertos públicos.

**Solución aplicada (validada end-to-end):**
1. Tailscale instalado y autenticado en VPS y Windows
2. Unit `tailscaled.service` arreglado (tenía un `EOF` huérfano que forzaba userspace-networking)
3. Servicio `hermes-dashboard.service` creado, habilitado, bound a `100.124.132.48:9119` (Tailscale-only)
4. Servicio `hermes-gateway.service` (Telegram) habilitado para arranque en boot
5. Credenciales basic-auth generadas y guardadas en `~/.hermes/.env`
6. Bloque "API Keys confirmadas" removido de MEMORY.md (filtro `hermes_env` lo bloqueaba)
7. `~/.hermes/memories/MEMORY.md` ahora es symlink al del vault (single source of truth)
8. Documentación completa creada en `Config/Remote-Access/` (4 archivos)
9. Vault sincronizado a GitHub (3 commits: 7f1ec67, f78e37f, aad1cf0)

**Resultado:** Juan conectó exitosamente desde Hermes Desktop en Windows → cargó MEMORY.md → tráfico confirmado bidireccional (tx 34MB+ acumulados).

## Servicios persistentes (sobreviven reboot del VPS)

| Servicio | Tipo | Habilitado |
|---|---|---|
| tailscaled | system | ✅ |
| hermes-dashboard | system | ✅ |
| hermes-gateway | user (linger) | ✅ |

## Lecciones / correcciones registradas en MEMORY.md

- **No decir "listo" sin verificar.** Juan detectó un cierre falso (carpeta Remote-Access con 4 archivos, commit 3bb5e2d, limpieza de /private/) que no había ocurrido. La verificación con `ls` + `git log` + `diff` tiene que ser **antes** de confirmar un cierre de sesión, no después.

## Pendiente para próxima sesión

- Confirmar si Juan configuró el alias `hermes-vps` en Windows (`~/.ssh/config` + PowerShell profile). Si no, no es bloqueante — la Desktop app ya funciona.
- Token de Telegram (HTTP 401 morning-report.py) — bloquea cron, viene del daily comercial, no del setup técnico.

## Referencias

- [[../Config/Remote-Access/README|Config/Remote-Access/README]] — punto de entrada de la documentación
- [[../Config/Remote-Access/setup|Config/Remote-Access/setup]] — paso a paso reproducible
- [[../Config/Remote-Access/troubleshooting|Config/Remote-Access/troubleshooting]] — qué hacer si rompe
- [[../Config/Remote-Access/files-changed|Config/Remote-Access/files-changed]] — diff completo
- [[../Config/AGENTS#acceso-remoto--hermes-desktop--vps-via-tailscale|Config/AGENTS]] § "Acceso remoto"
- [[MEMORY]] — estado de negocio
- [[2026-06-14-summary|2026-06-14 (comercial)]] — daily comercial del mismo día

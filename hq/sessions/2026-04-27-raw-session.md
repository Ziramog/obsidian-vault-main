# Raw Session Log — 2026-04-27

> Este archivo es el log crudo de la sesion. Se actualiza en tiempo real.
> El cron de 30 min solo hace git push de este archivo.
> Si se cae el VPS, aqui esta todo hasta el ultimo update.

## Sesion Actual

### Inicio de sesion
- Juan reporta: VPS se cae
- Investigacion: OOM Killer (dmesg)
- Fix: swap 2GB creado + fstab + outreach-api restart

### Tareas realizadas esta sesion
1. swap 2GB creado y activado
2. /etc/fstab configurado con swap
3. outreach-api reiniciado (123MB → 39MB)
4. memory-backup.md creado en obsidian
5. Cron job: Memory Backup every 30min (job: ca40b29010be)
6. Cron job: Daily Session Summary 20:00 (job: 53a5bb507d02)
7. Session notes actualizadas en obsidian-vault
8. Git push completado

### Pendientes / Flags
- Franco Roma: specs pendientes + audio meeting analysis
- Luis Farias: follow-up Friday
- RIVAS Inmuebles: outreach inicial
- Conforti Propiedades: outreach inicial
- Outreach PAUSED: YCloud delivery no verificado

### Decisiones
- Juan pidio: backup cada 30 min de session en obsidian
- Formato: log crudo, no summary (el summary se deriva de esto)
- Objetivo: maximo 30 min de perdida si VPS se cae

### Notas técnicas
- VPS: 8GB RAM, swap 2GB ahora activo
- outreach-api: online ~39MB (reiniciado, memory leak limpio)
- outreach-daemon: online ~63MB
- hermes-gateway: online
- Chrome headless: ~236MB (principal consumidor de RAM)

### Juan's clarification on backup strategy
- Backup de 30 min: NO genera contenido nuevo. Solo hace `git push` del vault.
- Yo voy escribiendo el log crudo en tiempo real.
- El cron solo empuja — no crea nada.
- Daily summary (20:00): se deriva del log crudo, no al revés.
- Maximo perdida si se cae: 30 min de conversacion.

### Lo que definimos
- Log crudo: `hq/sessions/YYYY-MM-DD-raw-session.md` — lo actualizo yo mientras hablamos
- Cron 30 min: solo `git push` (no genera contenido)
- Cron 20:00 daily: genera summary derivado del log crudo
- Si VPS se cae: todo en GitHub, maximo 30 min perdido

---
*Last update: 2026-04-27 19:50*

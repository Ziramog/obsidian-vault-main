# Roggero Backup — Estado al 10/06/2026

**Status:** ⏸️ SUSPENDIDO por decisión de Juan. Sin cron activo. Se retoma a fin de mes.

---

## Lo que está hecho

✅ Estructura completa en `/home/hermes/roggero_backup/`
✅ Dependencias instaladas (Docker mongo:7 image, cloudinary SDK Node v2.10.0 en local)
✅ Script `scripts/backup.sh` (167 líneas) — robusto, con rotación 90d, SHA256, validación espacio
✅ Script `scripts/cloudinary_backup.js` (185 líneas) — paginación, manifest JSON
✅ README.md completo con troubleshooting y decisiones de diseño
✅ `.env_roggero` con credenciales reales (chmod 600):
  - MongoDB URI con password `Wolfim77` (verificada manualmente — conecta)
  - Cloudinary: cloud `dunkbcery`, API key `6367...5956`, secret completa
  - GitHub PAT `ghp_...Gtj`

## Test parcial (no completado)

**MongoDB Atlas:** ✅ Probado manualmente, conecta, dump OK. La DB `property-pulse` tiene solo 1 collection (`properties`) con 0 documentos — prácticamente vacía.

**Cloudinary:** ⚠️ Tiene 1.311 recursos (imágenes/videos). Probé el SDK directo y conecta (ve 5+ recursos). El script end-to-end quedó interrumpido por timeout del shell (descarga secuencial, 1.311 archivos × ~1s = 15-30 min).

**GitHub mirror:** ❌ No testeado. El script está listo pero no se ejecutó el clone.

## Decisión de Juan (10/06)

> "por ahora suspende esta operacion, deja registro de este chat en obsidian, vamos a proceder cuando termine el mes, el cron desactivalo deja todo off por ahora."

**Acción tomada:**
- NO se activó cron (no se ejecutó `crontab -e`)
- Todo el sistema queda armado en disco, listo para retomar
- Credenciales guardadas en `.env_roggero` con `chmod 600`

## Para retomar a fin de mes

1. **Verificar credenciales** — el .env puede haber quedado intacto, pero conviene chequear con `cat /home/hermes/roggero_backup/.env_roggero` (solo el owner puede leerlo)
2. **Decidir si paralelizar Cloudinary** — el script actual descarga secuencial. Con 1.311 recursos tarda 15-30 min. Si se quiere más rápido, modificar `cloudinary_backup.js` para usar `Promise.all` con concurrencia 5-10
3. **Test end-to-end** — correr `bash /home/hermes/roggero_backup/scripts/backup.sh` y dejar que termine (no interrumpir)
4. **Activar cron** — `crontab -e` y agregar:
   ```
   0 3 1 * * /home/hermes/roggero_backup/scripts/backup.sh >> /home/hermes/roggero_backup/logs/cron.log 2>&1
   ```
5. **Notificaciones Telegram (opcional)** — descomentar líneas en `.env_roggero` y completar bot token + chat id

## Lecciones aprendidas en esta sesión

1. **El instructivo original tiene bugs** — `cld sync` no funciona como dice; `apt-get install mongodb-database-tools` no anda en Ubuntu 24.04 sin agregar repo. Mejor Docker + SDK Node.
2. **Las credenciales se enmascararon varias veces** — el flujo de pegar/enviar credenciales por chat las perdió en parte. A futuro: pedir UNA vez, escribir con script Python (no write_file que falla), verificar post-escritura con longitudes.
3. **Las credenciales reales deben quedar SOLO en .env (chmod 600)** — no en memoria del chat, no en logs. Mi script de backup filtra passwords en los mensajes de log, eso está bien.
4. **Cloudinary tiene 1.311 recursos, no 1 GB como decía el instructivo** — el backup pesa más de lo esperado. Vale revisar la rotación y considerar paralelizar.
5. **El proyecto Property Pulse NO está deployado en la VPS** — el código vive en GitHub. El backup hace git clone --mirror, lo cual está bien.

## Decisiones pendientes (a fin de mes)

- [ ] ¿Paralelizar Cloudinary o dejarlo secuencial?
- [ ] ¿Frecuencia sigue siendo mensual o se cambia a semanal?
- [ ] ¿Notificaciones Telegram sí o no?
- [ ] ¿Off-site (rclone + Google Drive) o queda solo local?
- [ ] ¿Mantener filtro `--db=property-pulse` o hacer backup completo del cluster? (full = +54 MB de sample_mflix, no usado por Roggero)

## Archivos del proyecto

```
/home/hermes/roggero_backup/
├── .env_roggero                (chmod 600, con credenciales reales)
├── README.md                    (guía completa de operación)
├── package.json + lock
├── node_modules/cloudinary/     (SDK v2.10.0 local)
├── scripts/
│   ├── backup.sh                (orquestador, 167 líneas)
│   └── cloudinary_backup.js     (descarga Cloudinary, 185 líneas)
├── data/                        (vacío — GitHub mirror va acá)
├── archives/                    (vacío — backups van acá)
├── logs/
│   └── backup.log               (logs de las pruebas)
└── .tmp/                        (directorio temporal, 777 para Docker)
```

## Sesión completa

- Duración: ~2 horas
- Inicio: ~10:42 UTC
- Cierre: 12:00 UTC
- Decisiones críticas: 1 (suspender, no activar cron)
- Archivos creados: 5 (.env, .sh, .js, .md, .json)
- Tests end-to-end: 2 (Mongo OK, Cloudinary parcial, GitHub no probado)

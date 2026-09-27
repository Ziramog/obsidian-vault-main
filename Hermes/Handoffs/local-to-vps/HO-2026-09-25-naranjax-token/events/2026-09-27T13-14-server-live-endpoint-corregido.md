---
type: event
handoff: HO-2026-09-25-naranjax-token
by: brain-local
at: 2026-09-27T13:14:00-04:00
kind: verification + correction
status: blocked-on-vps
---

# Event: server Naranjax levantado y endpoint corregido

## Hecho

Juan autorizó avanzar con Naranjax. El server estaba caído (nada escuchando en :3001,
consecuencia del apagado sucio del 27/09 05:23). Reiniciado desde `C:/Projects/Naranjax`
con `node server.mjs` (PID 7740). El `.env` ya tenía el token nuevo, así que el reinicio
manual que pedía el request quedó resuelto: el proceso vivo es el que lee el token actual.

## Probes ejecutados (sin exponer el valor del token)

| Request | Resultado |
|---|---|
| `GET /api/totals?month=2026-06` sin token | 401 |
| `GET /api/totals?month=2026-06&token=basura` | 401 `{"error":"Token inválido o faltante."}` |
| `GET /api/totals?month=2026-06&token=$NARANJAX_API_TOKEN` | 200, total 2226132.72 |
| `GET /api/totals?month=2026-07` con token | 200, total 1645395.37 |
| `GET /api/totals?month=2026-05` con token | 200, total 1626952.20 |
| `GET /api/totals?month=2026-08` y `2026-09` con token | 200, total 0 ("No hay movimientos") |
| `GET http://truzt:3001/api/totals` (hostname Tailscale, sin token) | 401 → red OK, es auth |

Bind del server: `app.listen(PORT, "0.0.0.0")` → escucha en todas las interfaces, Tailscale incluida.

## CORRECCIÓN — la URL del request estaba mal

El request apunta a `http://100.124.132.48:3001`. Esa IP **es el VPS**
(`vmi3131751`, linux, active), no la PC. `tailscale status` desde la PC:

- PC (esta máquina): `100.105.0.23` hostname `truzt`
- VPS: `100.124.132.48` hostname `vmi3131751`

Con la URL original, brain-vps se estaría consulteando a sí mismo en :3001 → nunca iba a
funcionar. **URL correcta: `http://100.105.0.23:3001/api/totals?month=YYYY-MM&token=$NARANJAX_API_TOKEN`**
(verificada desde la PC contra su propia IP Tailscale: 200 con el total de 2026-06).
Alternativa por MagicDNS: `http://truzt:3001/...` (responde, probado).

## Segundo hallazgo — el cron mensual va a escribir ceros

No hay resúmenes cargados después de julio. `GET /api/summaries` lista 7 PDFs, el último
(`resumen-tarjeta-naranja-1785246765.pdf`) subido el 28/07. Agosto y septiembre devuelven
`total: 0`. Si el cron de brain-vps corre hoy contra `2026-09`, escribe 0 en `kpis.md` y
contamina el semáforo financiero. Hace falta que Juan suba los resúmenes de agosto y
septiembre (POST `/api/parse-pdf`) antes del primer consumo real.

## Pendiente

1. brain-vps: usar la URL corregida y configurar el cron mensual → `kpis.md`.
2. Juan: subir resúmenes de agosto/septiembre (bloqueante para que el cron tenga datos).
3. El proceso corre como job en background de esta sesión (PID 7740). Si la PC se reinicia
   vuelve a caerse: no hay servicio ni tarea programada que lo levante. Evaluar Task Scheduler
   tipo `HermesVaultSyncLocal` si se quiere 24/7.

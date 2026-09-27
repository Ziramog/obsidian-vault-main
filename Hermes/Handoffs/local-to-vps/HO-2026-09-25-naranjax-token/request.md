# HO-2026-09-25 Naranjax API Token

**From:** brain-local
**To:** brain-vps
**Status:** ready
**Created:** 2026-09-25T02:30:00Z
**Updated:** 2026-09-27T13:14:00-04:00 (ver `events/2026-09-27T13-14-server-live-endpoint-corregido.md`)
**Priority:** high

## Contexto

Endpoint `/api/totals` de Naranjax listo para consumo desde VPS vía Tailscale.

## Credencial

- **Variable:** `NARANJAX_API_TOKEN`
- **Ubicación archivo:** `C:/Projects/Naranjax/.env` (leer directamente desde la PC local)
- **Endpoint:** `http://100.105.0.23:3001/api/totals?month=YYYY-MM&token=$NARANJAX_API_TOKEN`
  - ⚠️ CORREGIDO 2026-09-27: la URL original (`100.124.132.48`) era la IP Tailscale **del VPS**, no de la PC. Desde esa IP brain-vps se consultaba a sí mismo en :3001. La PC es `truzt` = `100.105.0.23`. Alternativa por MagicDNS: `http://truzt:3001/...`

## Acción requerida

1. Copiar el valor de `NARANJAX_API_TOKEN` desde el archivo `.env` de Naranjax a env var del VPS
2. Configurar cron consumer mensual → `kpis.md`
3. Probe de verificación: 401 sin token, 200 con token (sin imprimir valor en logs)

## Formato de respuesta del endpoint

```json
{
  "month": "2026-09",
  "total": 2226132.72,
  "categories": { "supermercado": 562680.01, ... },
  "transactionCount": 160
}
```

## Notas

- El servidor de Naranjax actualmente corre con token viejo. Se necesita reinicio manual del proceso node (kill PID 6796 + `npm run server`) para que tome el token nuevo del `.env`. Pendiente aprobación de Juan.
- Este handoff es solo transferencia de credencial, no requiere respuesta una vez configurado el cron.

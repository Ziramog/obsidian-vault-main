# Session 2026-06-02 15:30

## Contexto
22 días sin sesión humana. Juan vuelve. Semáforo 🔴 Crítico.

## Decisiones tomadas
1. **Cristina Welldone SRL → DESCARTADA** (Juan la llamó farsante, no cerró)
2. **Franco Roma → HOY pasa a producción** → cobra $200 finales al validar
3. **Outreach automático → SKIP** (sesión WA muerta, teléfonos mascarados, PM2 vacío)
4. **Cambio modelo: minimax-2.7 → MiniMax-M3** (config.yaml actualizado)

## Diagnóstico ejecutado
- `pm2 list` → vacío
- Procesos zombie fuera de PM2: PID 2281900 (outreach-daemon), 2350582 (wolfim-api)
- `baileys-connect/` → sin `creds.json`, solo `qr.txt` raw PNG → sesión WhatsApp muerta
- `state.json` teléfonos: `+549****8601` (mascarados por RLS Supabase) → 0% delivery
- `outreach-api` port 3001 → DOWN (Connection refused)
- Leads Comforti/Rivas/Gamma: plantillas vacías, sin teléfono/email/contacto

## Acciones comprometidas
| Acción | Responsable | Estado |
|--------|-------------|--------|
| Confirmar link sitio Franco Roma en producción | Juan | ⏳ |
| Validar sitio + cobrar $200 | Juan/Hermes | Bloqueado |
| Scavenging Comforti/Rivas/Gamma | Juan/Hermes | ⏳ Esperando datos |

## Bloqueos
- Outreach automático no recuperable sin: credenciales WhatsApp + teléfonos reales (no RLS-mascarados) + re-registro en PM2
- Leads "fríos" no atacables: faltan datos básicos (teléfono, ciudad, nombre contacto)

## Próxima sesión
1. Link Franco Roma → validar
2. Scavenging o ciudad+nombre para Comforti/Rivas/Gamma
3. Meta concreta de junio antes 15/06

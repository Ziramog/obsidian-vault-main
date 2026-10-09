# Telegram multiplexer — recarga de token por perfil (PC local)

**Ámbito:** gateway local de la PC de Juan (perfil `default` como multiplexer; PID actual en
`%LOCALAPPDATA%\hermes\gateway_state.json`).

## Regla dura

Comentar o eliminar `TELEGRAM_BOT_TOKEN` en el `.env` de un perfil servido por el multiplexer
**NO da de baja el adapter Telegram en caliente**. El adapter ya arrancado sigue polleando con
el token que cargó al start.

- El re-scan por cambio de `config/.env` (`[MULTIPLEX] Re-scanned profile '<x>' ...`) sólo
  **agrega/actualiza** adapters; **no** mata uno en curso.
- El estado real se ve en `gateway_state.json` → `platforms["<perfil>:telegram"].state`.
  Si dice `connected` con `updated_at` fresco, el poller está vivo aunque el `.env` ya no
  tenga el token.
- Log engañoso: `(0 adapter(s) connected)` en la línea de re-scan NO significa "adapter
  desmontado".

## Cómo dar de baja un adapter Telegram de un perfil

1. Comentar/borrar la línea en `profiles/<perfil>/.env`.
2. **Reiniciar el gateway** (obligatorio):
   ```bash
   hermes -p default gateway --accept-hooks restart
   ```
3. Verificar:
   ```bash
   python3 -c "import json;d=json.load(open('gateway_state.json'));print(d['pid']);[print(k,v['state']) for k,v in d['platforms'].items()]"
   # y en logs/gateway.log buscar: "Profile '<perfil>': skipping telegram - no bot credential"
   ```

## Diagnóstico rápido de un poller duplicado (conflict en otro host)

- `gateway_state.json` → qué `<perfil>:telegram` está `connected` y con qué `writer_pid`.
- `netstat -ano | grep 149.154.166.110` → sockets al API de Telegram por PID del gateway.
- Sonda: `curl -s "https://api.telegram.org/bot<TOK>/getUpdates?timeout=1&offset=-1"` desde
  el host sospechoso. `"ok":true` = no había otro cliente; `Conflict` = hay un poller vivo.
  (Una sonda con el mismo token puede terminar el poll del otro cliente — usarla con cuidado.)
- **Nunca** imprimir el token en logs/vault; referenciar `[credencial: TELEGRAM_BOT_TOKEN]`.

## Nota de seguridad (residual)

El gateway escucha el api_server en `0.0.0.0:8642` (no loopback) con terminal backend `local`.
El propio gateway lo advierte: trabajo despachado por ese endpoint corre como el usuario del
host con acceso total a terminal/archivos. Firewallear a LAN/tailnet confiable o pasar a
backend sandboxeado.

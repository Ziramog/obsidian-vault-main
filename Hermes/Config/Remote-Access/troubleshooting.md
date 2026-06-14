---
title: Troubleshooting — Hermes Desktop ↔ VPS
type: troubleshooting
status: vivo
created: 2026-06-14
tags: [hermes, desktop, vps, tailscale, troubleshooting]
---

# Troubleshooting — Hermes Desktop ↔ VPS

## Tabla rápida de fallas

| Síntoma | Diagnóstico probable | Fix |
|---|---|---|
| Desktop dice "Connection refused" | Dashboard caído o Tailscale caído en VPS | `sudo systemctl status hermes-dashboard tailscaled` |
| Desktop dice "401 Invalid credentials" | Password mal copiada o el .env no se cargó | Ver abajo § "Auth falla" |
| Desktop dice "timeout" al conectar | Tailscale no conecta desde Windows, o IP cambió | Ver abajo § "Tailscale" |
| Dashboard carga pero MEMORY.md no aparece | Filtro de secrets borró el bloque, o MEMORY.md se borró | Ver abajo § "MEMORY no carga" |
| Gateway Telegram no responde | `hermes-gateway` no levantó después de reboot | `systemctl --user status hermes-gateway` |
| Sign-in no aparece (pide token) | El dashboard no detectó auth provider activo | Ver `.env` que tenga las 3 variables |
| Sesión se pierde en cada reboot del VPS | Falta `HERMES_DASHBOARD_BASIC_AUTH_SECRET` | Agregar a `.env` y reiniciar dashboard |
| `tailscale status` muestra VPS como "offline" | Tailscale daemon se cayó o perdió credenciales | `sudo systemctl restart tailscaled` |

---

## Auth falla (401 / "Invalid credentials")

**Diagnóstico:**
```bash
# En el VPS, en SSH:
sudo systemctl status hermes-dashboard
# ¿el proceso cargó las env vars? Verificá:
sudo systemctl show hermes-dashboard -p Environment
# Tiene que listar HERMES_DASHBOARD_BASIC_AUTH_USERNAME y _PASSWORD
```

**Fix:**
1. Verificá que el .env tenga las 3 variables (`USERNAME`, `PASSWORD`, `SECRET`):
   ```bash
   grep HERMES_DASHBOARD /home/hermes/.hermes/.env
   ```
2. Si falta alguna, agregala y reiniciá el servicio:
   ```bash
   sudo systemctl restart hermes-dashboard
   ```
3. Si el password tiene caracteres especiales, asegurate de que esté entre comillas en el .env.

**Confirmá el gate activo desde el VPS:**
```bash
curl -s http://100.124.132.48:9119/api/status | python3 -m json.tool
# auth_required debe ser true, auth_providers debe incluir "basic"
```

---

## Tailscale caído o IP cambió

**Diagnóstico desde Windows (PowerShell):**
```powershell
tailscale status
# ¿Aparece vmi3131751 con IP 100.124.132.48?
ping 100.124.132.48
# ¿Responde?
```

**Diagnóstico desde VPS:**
```bash
sudo tailscale status
ip -4 addr show tailscale0
# ¿La IP 100.124.132.48 aparece en tailscale0?
```

**Fix si el daemon del VPS se cayó:**
```bash
sudo systemctl restart tailscaled
sleep 5
tailscale status
# Si la IP cambió (raro pero posible tras re-auth), actualizá:
# 1) el unit de hermes-dashboard
# 2) el README y setup.md de este vault
# 3) el Remote URL en Desktop
```

**Fix si Tailscale arrancó en userspace mode (sin interfaz tailscale0):**
```bash
# Verificá que el unit NO tenga --tun=userspace-networking:
sudo cat /etc/systemd/system/tailscaled.service
# Si lo tiene, sacalo y reiniciá:
sudo systemctl daemon-reload
sudo systemctl restart tailscaled
```

**Fix si Tailscale en Windows está "offline":**
```powershell
# Re-autenticá:
tailscale up
# Si te da link, abrilo en el browser.
# Si sigue sin conectar, abrí la app gráfica de Tailscale desde el menú inicio.
```

---

## Dashboard caído

**Diagnóstico:**
```bash
sudo systemctl status hermes-dashboard
# Si dice "inactive (dead)":
sudo journalctl -u hermes-dashboard --no-pager -n 30
```

**Fix:**
```bash
sudo systemctl restart hermes-dashboard
sleep 5
sudo systemctl status hermes-dashboard
ss -ltn | grep 9119
```

**Si el proceso arranca pero muere inmediatamente:**
- Probablemente `.env` no se carga o hay un error de auth
- Mirá el log: `tail -50 /home/hermes/.hermes/logs/*.log | grep dashboard`
- O corré manual para ver el error:
  ```bash
  cd /home/hermes
  /home/hermes/.local/bin/hermes dashboard --no-open --host 100.124.132.48 --port 9119
  ```

---

## MEMORY no carga en Desktop

**Síntoma:** Desktop conecta, ves "1 active session" pero cuando me preguntás algo personal (Wolfim, Ango, Construvial, leads) no respondo con el contexto correcto.

**Diagnóstico:**
1. Verificá que `~/.hermes/memories/MEMORY.md` existe y es symlink al vault:
   ```bash
   ls -la /home/hermes/.hermes/memories/MEMORY.md
   # Debería apuntar a /home/hermes/obsidian-vault/Hermes/MEMORY.md
   ```
2. Verificá que el archivo del vault NO tenga el header `## API Keys confirmadas` ni valores de keys (filtro `hermes_env` lo borra):
   ```bash
   grep -n 'API Keys confirmadas\|7f4c661b' /home/hermes/obsidian-vault/Hermes/MEMORY.md
   # No debería matchear nada
   ```
3. Verificá que `USER.md` esté cargado en system prompt — eso lo confirmás en la respuesta de la IA (si dice tu nombre, contexto, etc).

**Fix:**
- Si `MEMORY.md` es symlink roto: `ln -sf /home/hermes/obsidian-vault/Hermes/MEMORY.md /home/hermes/.hermes/memories/MEMORY.md`
- Si tiene keys: moverlas a `~/.hermes/private/keys-status.md` (ver `files-changed.md` § "MEMORY.md")

---

## Gateway Telegram no responde

**Diagnóstico (como usuario hermes):**
```bash
sudo -u hermes XDG_RUNTIME_DIR=/run/user/1000 systemctl --user status hermes-gateway
# Si dice "inactive (dead)":
sudo -u hermes XDG_RUNTIME_DIR=/run/user/1000 systemctl --user restart hermes-gateway
```

**Verificar linger:**
```bash
loginctl show-user hermes | grep Linger
# Debe decir Linger=yes
# Si dice no:
sudo loginctl enable-linger hermes
```

**Si el proceso muere repetidamente:**
```bash
# Ver logs:
sudo -u hermes XDG_RUNTIME_DIR=/run/user/1000 journalctl --user -u hermes-gateway --no-pager -n 50
```

---

## Sesión se pierde en cada reboot del VPS

**Causa:** falta `HERMES_DASHBOARD_BASIC_AUTH_SECRET` en el `.env`. Sin esta variable, el dashboard genera un secret aleatorio nuevo en cada arranque → invalida todos los tokens de sesión.

**Fix:**
```bash
# Generar secret estable:
SECRET=$(openssl rand -base64 32)
# Agregarlo al .env (si no está):
echo "HERMES_DASHBOARD_BASIC_AUTH_SECRET=$SECRET" >> /home/hermes/.hermes/.env
chmod 600 /home/hermes/.hermes/.env
# Reiniciar dashboard:
sudo systemctl restart hermes-dashboard
```

---

## Bind a Tailscale falla ("could not bind on any address")

**Síntoma:** al arrancar el dashboard, sale:
```
ERROR: could not bind on any address out of [('100.124.132.48', 9119)]
```

**Causa:** Tailscale está en userspace-networking (sin interfaz `tailscale0` con la IP).

**Diagnóstico:**
```bash
ip -4 addr show | grep '100\.'
# Si no aparece, Tailscale está en userspace
ip link show tailscale0 2>&1
# Si dice "does not exist", TUN mode no está activo
```

**Fix:** ver § "Tailscale en userspace" arriba.

---

## Reset nuclear (último recurso)

Si nada funciona:

```bash
# 1. Reiniciá los 3 servicios en orden:
sudo systemctl restart tailscaled
sleep 3
sudo systemctl restart hermes-dashboard
sudo -u hermes XDG_RUNTIME_DIR=/run/user/1000 systemctl --user restart hermes-gateway

# 2. Verificá estado:
sudo systemctl status tailscaled hermes-dashboard
sudo -u hermes XDG_RUNTIME_DIR=/run/user/1000 systemctl --user status hermes-gateway

# 3. Verificá conectividad:
ss -ltn | grep 9119
sudo tailscale status
ip -4 addr show tailscale0

# 4. Desde Windows:
#    tailscale status
#    ping 100.124.132.48
#    curl http://100.124.132.48:9119/api/status
```

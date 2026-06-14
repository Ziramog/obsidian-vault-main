---
title: Setup — Hermes Desktop ↔ VPS paso a paso
type: setup
status: validado
created: 2026-06-14
tags: [hermes, desktop, vps, tailscale, setup, howto]
---

# Setup — Hermes Desktop ↔ VPS (paso a paso ejecutado)

Documenta el orden EXACTO de comandos que se ejecutaron el 14/06/2026 para dejar la conexión andando. Útil para reproducir en otro VPS, o para entender qué hace cada pieza.

## Pre-requisitos

- VPS Linux con systemd (probado en Contabo Ubuntu 24.04, IP pública `194.163.161.99`)
- Cuenta de Tailscale creada (gratis hasta 100 nodos)
- Tailscale instalado y logueado en Windows
- SSH al VPS funcional
- `hermes` (Hermes Agent v0.16.0+) instalado en el VPS

## Pasos

### 1. Diagnosticar estado inicial

```bash
# ¿Qué corre, qué escucha?
ss -ltn
ps -ef | grep '[h]ermes'
which hermes && hermes --version

# ¿Tailscale instalado?
which tailscale
sudo systemctl status tailscaled  # probablemente inactivo
```

### 2. Diagnosticar si MEMORY.md estaba bloqueada por filtro

```bash
# ¿El filtro 'hermes_env' está bloqueando MEMORY.md?
grep -n 'API Keys confirmadas' /home/hermes/.hermes/memories/MEMORY.md
# Si matchea, ese header + las keys reales están haciendo que el filtro
# borre toda la sección del system prompt. Remover antes de seguir.
```

### 3. Levantar Tailscale en el VPS

```bash
# Backup del unit si ya existe (probablemente esté roto)
sudo cp /etc/systemd/system/tailscaled.service /etc/systemd/system/tailscaled.service.bak.$(date +%Y%m%d_%H%M%S)

# Verificar el unit — si tiene --tun=userspace-networking o un 'EOF' huérfano, está mal
sudo cat /etc/systemd/system/tailscaled.service

# Reescribir limpio:
sudo tee /etc/systemd/system/tailscaled.service > /dev/null <<'EOF'
[Unit]
Description=Tailscale
After=network.target

[Service]
Type=simple
ExecStart=/usr/local/bin/tailscaled
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

# Activar y autenticar
sudo systemctl daemon-reload
sudo systemctl enable --now tailscaled
sudo tailscale up    # abre link en browser, autorizar
sudo tailscale ip -4 # ANOTAR esta IP (ej: 100.124.132.48)
```

**Verificación crítica:**
```bash
ip -4 addr show tailscale0
# DEBE mostrar: inet 100.124.132.48/32 scope global tailscale0
# Si no aparece, TUN no se activó (usar userspace workaround → ver troubleshooting)
```

### 4. Generar credenciales del dashboard

```bash
# Backup del .env antes de tocar
cp /home/hermes/.hermes/.env /home/hermes/.hermes/.env.bak.$(date +%Y%m%d_%H%M%S)

# Generar credenciales (elegir username, password, secret)
USERNAME="juang"
PASSWORD=*** rand -base64 18 | tr -d '=+/' | head -c 20)
SECRET=*** rand -base64 32)

cat >> /home/hermes/.hermes/.env <<EOF

# --- Hermes Dashboard (Tailscale-only) ---
HERMES_DASHBOARD_BASIC_AUTH_USERNAME=$USERN...hmod 600 /home/hermes/.hermes/.env
```

### 5. Crear el servicio systemd del dashboard

```bash
sudo tee /etc/systemd/system/hermes-dashboard.service > /dev/null <<'EOF'
[Unit]
Description=Hermes Agent Dashboard (Tailscale)
After=network-online.target tailscaled.service
Wants=network-online.target

[Service]
Type=simple
User=hermes
WorkingDirectory=/home/hermes
EnvironmentFile=/home/hermes/.hermes/.env
ExecStart=/home/hermes/.local/bin/hermes dashboard --no-open --host 100.124.132.48 --port 9119
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable --now hermes-dashboard
sleep 5

# Verificación
sudo systemctl status hermes-dashboard
ss -ltn | grep 9119
# DEBE mostrar: LISTEN 0 2048 100.124.132.48:9119

# Health check
curl -s http://100.124.132.48:9119/api/status
# DEBE devolver JSON con auth_required: true, auth_providers: ["basic"]
```

### 6. Habilitar gateway de Telegram (user systemd)

```bash
sudo -u hermes XDG_RUNTIME_DIR=/run/user/1000 systemctl --user enable hermes-gateway
loginctl show-user hermes | grep Linger  # DEBE decir yes
# Si dice no:
sudo loginctl enable-linger hermes
```

### 7. Limpiar MEMORY.md (sacar bloque de keys)

```bash
# Backup
cp /home/hermes/.hermes/memories/MEMORY.md /home/hermes/.hermes/memories/MEMORY.md.bak.$(date +%Y%m%d_%H%M%S)

# Identificar líneas del bloque problemático
grep -n 'API Keys confirmadas' /home/hermes/.hermes/memories/MEMORY.md

# Borrar bloque (ajustá los números según tu archivo)
sed -i '107,115d' /home/hermes/.hermes/memories/MEMORY.md

# Insertar nota referencial (después de la línea 106)
sed -i '106a\
## Credenciales y API keys\
- Estado operativo: `~/.hermes/private/keys-status.md` (modo 600, NO inyectado en system prompt).\
- Valores reales: `~/.hermes/.env` (modo 600).\
- Por seguridad, este archivo nunca lista valores de keys.\
' /home/hermes/.hermes/memories/MEMORY.md

# Crear archivo privado de tracking (sin secrets)
mkdir -p /home/hermes/.hermes/private
cat > /home/hermes/.hermes/private/keys-status.md <<'EOF'
# API Keys — Estado (privado)
# Ubicación: ~/.hermes/private/keys-status.md
# Permisos: 0600

## Estado (snapshot)

| Servicio | Estado | Notas |
|---|---|---|
| Serper | Activa | valor en ~/.hermes/.env |
| Firecrawl | Activa | valor en ~/.hermes/.env |
| DataImpulse | SIN CRÉDITO | port 823 bloqueado desde VPS |
| MiniMax API | Activa | valor en ~/.hermes/.env |

## Regla
Valores reales: solo en ~/.hermes/.env (0600).
EOF
chmod 600 /home/hermes/.hermes/private/keys-status.md
```

### 8. Symlink MEMORY.md CLI → vault

```bash
cp /home/hermes/.hermes/memories/MEMORY.md /home/hermes/.hermes/memories/MEMORY.md.bak.prelink
rm /home/hermes/.hermes/memories/MEMORY.md
ln -s /home/hermes/obsidian-vault/Hermes/MEMORY.md /home/hermes/.hermes/memories/MEMORY.md
ls -la /home/hermes/.hermes/memories/MEMORY.md
# DEBE mostrar: ... -> /home/hermes/obsidian-vault/Hermes/MEMORY.md
```

### 9. Commit a GitHub (sync PC + Android)

```bash
cd /home/hermes/obsidian-vault
git add -A
git -c user.email="hermes@vps" -c user.name="Hermes" commit -m "chore: remove API keys from MEMORY.md, link to keys-status.md"
git push
```

### 10. Lado Windows — Configurar SSH + alias

**Editar `C:\Users\TU_USUARIO\.ssh\config`:**
```
Host hermes-vps
    HostName 100.124.132.48
    User hermes
    IdentityFile ~/.ssh/id_ed25519
    ServerAliveInterval 60
    ServerAliveCountMax 3
```

**Agregar a PowerShell profile (`notepad $PROFILE`):**
```powershell
function hermes-vps { ssh -t hermes-vps 'hermes-tui' }
function hermes-vps-cmd { param([string]$cmd) ssh -t hermes-vps "hermes -z '$cmd'" }
```

**Uso:**
```powershell
PS> ssh hermes-vps 'whoami; hostname'
hermes
vmi3131751

PS> hermes-vps
# Abre la TUI de Hermes contra el VPS
```

### 11. Lado Windows — Configurar Hermes Desktop

1. Instalar Hermes Desktop en Windows (instrucciones en la doc oficial)
2. Abrir la app → Settings → Gateway → Remote gateway
3. Remote URL: `http://100.124.132.48:9119`
4. Click "Sign in" → usuario `juang` → password (de `~/.hermes/.env`)
5. Save and reconnect

**Test final:** mandar un mensaje a Hermes y verificar que reconoce tu contexto.

## Comandos de verificación rápida

```bash
# ¿Todo arriba?
sudo systemctl is-active tailscaled hermes-dashboard
sudo -u hermes XDG_RUNTIME_DIR=/run/user/1000 systemctl --user is-active hermes-gateway

# ¿Conectividad?
sudo tailscale status
ss -ltn | grep 9119
curl -s http://100.124.132.48:9119/api/status | python3 -m json.tool
```

#!/usr/bin/env bash
# antigravity-cli.sh — maneja el CLI headless de Antigravity (language_server.exe agentapi)
# Verificado 2026-09-28 sobre Antigravity 2.15.1 (host: PC de Juan, MSYS/git-bash).
#
# Uso:
#   ./antigravity-cli.sh discover                       # muestra puerto gRPC, csrf y proyectos
#   ./antigravity-cli.sh new --project hermes-pwa --model flash_lite --prompt "hola"
#   ./antigravity-cli.sh new --project hermes-pwa --prompt-file /c/.../prompt.md --title "Fase 1"
#   ./antigravity-cli.sh read <conversationId>          # imprime la respuesta del agente
#
# Reglas del descubrimiento (todas verificadas):
#  1. El LS corre como `language_server.exe --standalone --override_ide_name antigravity ...`
#     y escucha en DOS puertos 127.0.0.1 (el que responde con error RPC gRPC es el bueno; el otro
#     contesta "error reading server preface: EOF" porque es HTTP/1.1).
#  2. ANTIGRAVITY_CSRF_TOKEN sale de la línea de comandos del propio LS (`--csrf_token <uuid>`).
#     Sin él: `Unauthenticated ... missing CSRF token`.
#  3. ANTIGRAVITY_PROJECT_ID es OBLIGATORIO y NO se resuelve desde el cwd: correr el CLI dentro
#     del repo sin esa variable falla con `project_id is required when providing project_env_config`.
#     El proyecto define el workspace del agente (folderUri + defaultBranch del JSON).
#     Los ids viven en ~/.gemini/config/projects/<uuid>.json.
#  4. La conversación queda en ~/.gemini/antigravity/conversations/<id>.db (SQLite, tabla `steps`),
#     así que la respuesta se lee sin GUI. `read` hace eso.
set -uo pipefail

AG="${ANTIGRAVITY_EXE:-/c/Users/ingju/AppData/Local/Programs/antigravity/resources/bin/language_server.exe}"
PROJDIR="$HOME/.gemini/config/projects"
CONVDIR="$HOME/.gemini/antigravity/conversations"
PY="${PY:-python}"
# MSYS: python nativo no entiende /c/... → traducir siempre las rutas que le pasamos
winpath() { cygpath -w "$1" 2>/dev/null || printf '%s' "$1"; }

# ---------- descubrimiento ----------
ls_cmdline() {
  powershell.exe -NoProfile -Command \
    "Get-CimInstance Win32_Process | Where-Object { \$_.Name -eq 'language_server.exe' -and \$_.CommandLine -match '--standalone' } | Select-Object -First 1 -ExpandProperty CommandLine" \
    2>/dev/null | tr -d '\r'
}

ls_pid() {
  powershell.exe -NoProfile -Command \
    "(Get-CimInstance Win32_Process | Where-Object { \$_.Name -eq 'language_server.exe' -and \$_.CommandLine -match '--standalone' } | Select-Object -First 1).ProcessId" \
    2>/dev/null | tr -d '\r'
}

find_port() { # $1 = pid ; imprime el puerto gRPC (o nada)
  local pid="$1" p
  for p in $(netstat.exe -ano 2>/dev/null | grep "LISTENING" | grep -E " $pid\$" | awk '{print $2}' | sed 's/.*://' | sort -u); do
    out=$(ANTIGRAVITY_LS_ADDRESS="http://127.0.0.1:$p" ANTIGRAVITY_CSRF_TOKEN="${TOKEN:-}" \
          timeout 25 "$AG" agentapi get-conversation-metadata 00000000-0000-0000-0000-000000000000 2>&1)
    case "$out" in
      *"server preface"*) : ;;                        # HTTP/1.1, no es el API gRPC
      *Unauthenticated*)  echo "$p"; return 0 ;;      # gRPC correcto (falta token, ya lo tenemos)
      *)                  echo "$p"; return 0 ;;
    esac
  done
  return 1
}

cmd_discover() {
  local cmd pid port token
  cmd=$(ls_cmdline); pid=$(ls_pid)
  token=$(printf '%s' "$cmd" | grep -oE -- '--csrf_token[= ]+[0-9a-f-]{36}' | grep -oE '[0-9a-f-]{36}' | head -1)
  TOKEN="$token"; port=$(find_port "$pid")
  echo "LS pid      : $pid"
  echo "csrf token  : ${token:0:8}… (oculto)"
  echo "gRPC port   : ${port:-NO ENCONTRADO}"
  echo "exe         : $AG"
  echo "proyectos   :"
  for f in "$PROJDIR"/*.json; do
    [ -f "$f" ] || continue
    n=$($PY -c "import json,sys;d=json.load(open(sys.argv[1]));print(d.get('name'),'|',d.get('id'),'|',json.dumps(d.get('projectResources',{}))[:120])" "$f" 2>/dev/null)
    echo "  - $n"
  done
}

# project id a partir de un nombre o de una carpeta
resolve_project() { # $1 = nombre o uuid
  local want="$1" f id
  if [[ "$want" =~ ^[0-9a-f-]{36}$ ]]; then echo "$want"; return 0; fi
  for f in "$PROJDIR"/*.json; do
    [ -f "$f" ] || continue
    id=$($PY -c "import json,sys;d=json.load(open(sys.argv[1]));print(d['id'] if d.get('name','').lower()==sys.argv[2].lower() else '')" "$f" "$want" 2>/dev/null)
    [ -n "$id" ] && { echo "$id"; return 0; }
  done
  # segundo intento: por carpeta (URL-encoded)
  local enc; enc=$(printf '%s' "$want" | sed 's|^/c/|file:///c%3A/|; s|/|%2F|g')
  grep -l "$enc" "$PROJDIR"/*.json 2>/dev/null | while read -r f; do
    $PY -c "import json,sys;print(json.load(open(sys.argv[1]))['id'])" "$f"; break
  done
}

# ---------- corrida ----------
cmd_new() {
  local project="" model="flash_lite" title="" prompt="" pfile=""
  while [ $# -gt 0 ]; do
    case "$1" in
      --project) project="$2"; shift 2 ;;
      --model)   model="$2"; shift 2 ;;
      --title)   title="$2"; shift 2 ;;
      --prompt)  prompt="$2"; shift 2 ;;
      --prompt-file) pfile="$2"; shift 2 ;;
      *) echo "arg desconocido: $1" >&2; return 2 ;;
    esac
  done
  [ -n "$pfile" ] && prompt=$(cat "$pfile")
  [ -z "$prompt" ] && { echo "falta --prompt o --prompt-file" >&2; return 2; }
  [ -z "$project" ] && { echo "falta --project (nombre o uuid)" >&2; return 2; }

  local cmd pid token port
  cmd=$(ls_cmdline); pid=$(ls_pid)
  token=$(printf '%s' "$cmd" | grep -oE -- '--csrf_token[= ]+[0-9a-f-]{36}' | grep -oE '[0-9a-f-]{36}' | head -1)
  TOKEN="$token"; port=$(find_port "$pid")
  [ -z "$port" ] && { echo "no encontré el puerto gRPC del LS" >&2; return 1; }

  local id; id=$(resolve_project "$project")
  [ -z "$id" ] && { echo "no resolví el project id de '$project'" >&2; return 1; }

  ANTIGRAVITY_LS_ADDRESS="http://127.0.0.1:$port" ANTIGRAVITY_CSRF_TOKEN="$token" ANTIGRAVITY_PROJECT_ID="$id" \
    timeout 120 "$AG" agentapi new-conversation ${title:+--title="$title"} --model="$model" "$prompt"
}

# ---------- lectura ----------
cmd_read() {
  local id="$1" tries="${2:-20}"
  $PY - "$CONVDIR/$id.db" "$tries" <<'PY'
import os,re,sqlite3,sys,time,shutil,glob
db, tries = sys.argv[1], int(sys.argv[2])
if not os.path.exists(db):
    print("no existe", db); sys.exit(1)
tmp = os.path.join(os.environ.get("TMPDIR","/tmp"), "agread"); os.makedirs(tmp, exist_ok=True)
for ext in ("", "-wal", "-shm"):
    if os.path.exists(db+ext): shutil.copy(db+ext, tmp)
copy = os.path.join(tmp, os.path.basename(db))
last = None
for _ in range(tries):
    try:
        c = sqlite3.connect(copy)
        rows = list(c.execute("select idx,step_type,status,step_payload from steps order by idx"))
        c.close()
    except Exception as e:
        print("err", e); sys.exit(1)
    sig = [(r[0], r[2], len(r[3] or b"")) for r in rows]
    if sig == last: break
    last = sig; time.sleep(3)
def strings(blob):
    if isinstance(blob, str): blob = blob.encode("utf8", "ignore")
    return [t.decode("utf8","ignore") for t in re.findall(rb"[ -~]{8,}", blob or b"")]
for idx, st, status, payload in rows:
    txt = [t for t in strings(payload) if not re.match(r"^(bot-|[0-9a-f]{32})", t)]
    print(f"--- step {idx} type={st} status={status} ({len(payload or b'')} b) ---")
    for t in txt[-6:]:
        print("   ", t[:300])
PY
}

case "${1:-}" in
  discover) cmd_discover ;;
  new) shift; cmd_new "$@" ;;
  read) shift; cmd_read "$@" ;;
  *) sed -n '3,20p' "$0" ;;
esac

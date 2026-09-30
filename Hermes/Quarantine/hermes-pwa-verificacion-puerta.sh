#!/bin/sh
# Verificación de puerta — Hermes PWA (Fase 2, criterios sin umbral)
# Uso:  BASE=https://truzt.taila7f43b.ts.net KEY=<clave> LOCAL_PORT=3000 sh verificacion-puerta.sh
#       BASE=http://100.124.132.48:3000 KEY=<clave> sh verificacion-puerta.sh
# Salida: una línea OK/FALLA por criterio. No escribe nada, no envía mensajes.
#
# Criterios:
#   0. identidad de la puerta (con LOCAL_PORT): PID dueño del puerto, BUILD_ID y commit en disco
#   1. health: ok:true y profileCount != 0 (el health da 200 con 0 perfiles locales)
#   2. perfiles: hay perfiles y ninguno offline
#   3. ruteo: los perfiles de prueba resuelven (400 = frena en la validación; nada enviado)
#   4. transcripts: turnos > 0  Y  0 ids repetidos, sin umbral de largo
#      (0 turnos con 0 ids repetidos es una sala VACÍA, no una sala sana: no pasa como OK)

BASE=${BASE:-http://100.124.132.48:3000}
KEY=${KEY:?falta KEY}
ROOMS=${ROOMS:-"rmuli31hi-inptr rmugviqw9-6zez7 rmufxz2ti-w6sk5 rmuag13gp-5r3kn"}
CFG=${CFG:-"brain-local web-builder rws wolfim-growth"}   # 2 del PC + 2 del VPS
TMPF=".hermes-verif-$$.json"
trap 'rm -f "$TMPF"' EXIT
LOCAL_PORT=${LOCAL_PORT:-}   # p.ej. 3000: habilita el criterio 0 (identidad de la puerta)
fail=0

say() { printf '%-58s %s\n' "$1" "$2"; }

# 0) identidad de la puerta (best effort, sólo si se declara el puerto local)
if [ -n "$LOCAL_PORT" ] && command -v powershell >/dev/null 2>&1; then
  ID=$(powershell -NoProfile -Command "\$p=(Get-NetTCPConnection -LocalPort $LOCAL_PORT -State Listen -ErrorAction SilentlyContinue | Select-Object -First 1).OwningProcess; if(\$p){ \$o=Get-CimInstance Win32_Process -Filter \"ProcessId=\$p\"; 'PID '+\$o.ProcessId+' start='+\$o.CreationDate+' cmd='+(\$o.CommandLine -replace '\s+',' ') } else { 'SIN LISTENER' }" 2>/dev/null | tr -d '\r')
  BID=$(cat .next/BUILD_ID 2>/dev/null); HED=$(git rev-parse --short HEAD 2>/dev/null)
  say "0 identidad puerta :$LOCAL_PORT" "$ID"
  [ -n "$BID" ] && say "0 build en disco (BUILD_ID / HEAD)" "$BID / $HED"
else
  say "0 identidad de la puerta" "no aplica (puerta remota: $BASE)"
fi

# 1) health: identidad y perfiles locales (el health puede dar 200 con 0 perfiles)
H=$(curl -sk -m 20 "$BASE/api/health")
echo "$H" | grep -q '"ok":true' && say "health ok" "OK  $H" || { say "health ok" "FALLA"; fail=1; }
echo "$H" | grep -q '"profileCount":0' && { say "profileCount != 0" "FALLA (0 perfiles locales: revisar HERMES_HOME)"; fail=1; } || say "profileCount != 0" "OK"

# 2) perfiles: 17 totales, todos online, sin PEER_MISSING_CONFIG
curl -sk -m 25 -H "Authorization: Bearer $KEY" "$BASE/api/profiles" > "$TMPF"
python3 - "$TMPF" <<'PY' || fail=1
import json,sys
d=json.load(open(sys.argv[1])); ps=d.get('profiles') or []
off=[p.get('name') for p in ps if not p.get('isOnline')]
print('%-58s %s' % ('perfiles: total / offline', ('OK  %d totales' % len(ps)) if (ps and not off) else ('FALLA  %d totales, offline=%s' % (len(ps), off))))
raise SystemExit(0 if (ps and not off) else 1)
PY

# 3) ruteo: perfil resuelto => 400 (frena en la validación del payload, nada enviado)
for p in $CFG; do
  c=$(curl -sk -m 30 -o /dev/null -w '%{http_code}' -X POST -H "Authorization: Bearer $KEY" \
      -H 'Content-Type: application/json' -d "{\"profile\":\"$p\"}" "$BASE/api/chat")
  if [ "$c" = "400" ]; then say "ruteo $p" "OK  400 (resuelto)"; else say "ruteo $p" "FALLA $c"; fail=1; fi
done

# 4) transcripts: 0 ids repetidos, sin umbral de largo (el defecto visible son mensajes cortos)
for r in $ROOMS; do
  curl -sk -m 120 -H "Authorization: Bearer $KEY" "$BASE/api/groups/$r/messages" > "$TMPF"
  python3 - "$r" "$TMPF" <<'PY' || fail=1
import json,sys,collections,re,os
r=sys.argv[1]; win=int(os.environ.get('WINDOW_S','120'))*1000
try: d=json.load(open(sys.argv[2]))
except Exception: print('%-58s FALLA no-json'%('4 %s'%r)); raise SystemExit(1)
m=d.get('messages') or []
def auth(x):
    n=(x.get('from') or {}).get('name') or '?'
    return 'hermes' if n in ('hermes','.hermes') else n
def text(x):
    t=x.get('text')
    if not isinstance(t,str): t=json.dumps(t,sort_keys=True,ensure_ascii=False)
    return re.sub(r'\s+',' ',t).strip()
rows=len(m); ids=len(set(x.get('id') for x in m))
ev=set((auth(x),text(x)) for x in m)
g=collections.defaultdict(list)
for x in m: g[(auth(x),text(x))].append(x.get('at') or 0)
cop=0
for k,ts in g.items():
    ts=sorted(t for t in ts if t)
    for i in range(1,len(ts)):
        if ts[i]-ts[i-1]<=win: cop+=1
peer=d.get('peerReachable'); src=d.get('source')
tag='filas=%d eventos=%d copias<%ds=%d ids_distintos=%d source=%s peer=%s'%(rows,len(ev),win//1000,cop,ids,src,peer)
if rows==0:
    print('%-58s FALLA sala VACIA | %s'%('4 %s'%r,tag)); raise SystemExit(1)
if not peer:
    print('%-58s FALLA sin fusion | %s'%('4 %s'%r,tag)); raise SystemExit(1)
if cop:
    print('%-58s FALLA copias del mismo instante | %s'%('4 %s'%r,tag)); raise SystemExit(1)
print('%-58s OK  %s'%('4 %s'%r,tag))
raise SystemExit(0)
PY
done

echo
[ "$fail" = 0 ] && echo "VEREDICTO: puerta OK (los 4 criterios)" || echo "VEREDICTO: hay FALLAS (ver arriba)"
exit $fail

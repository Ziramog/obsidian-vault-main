#!/bin/sh
# Verificación de puerta — Hermes PWA (Fase 2, criterios sin umbral)
# Uso:  BASE=https://truzt.taila7f43b.ts.net KEY=<clave> sh verificacion-puerta.sh
#       BASE=http://100.124.132.48:3000 KEY=<clave> sh verificacion-puerta.sh
# Salida: una línea OK/FALLA por criterio. No escribe nada, no envía mensajes.

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
import json,sys,collections
r=sys.argv[1]
try: d=json.load(open(sys.argv[2]))
except Exception as e: print('%-58s FALLA no-json'%('ids repetidos %s'%r)); raise SystemExit(1)
m=d.get('messages') or []
c=collections.Counter(x.get('id') for x in m)
dup=sum(1 for v in c.values() if v>1); extra=sum(v-1 for v in c.values() if v>1)
ok = (dup==0)
print('%-58s %s' % ('ids repetidos %s'%r, ('OK  %d turnos, 0 repetidos, source=%s'%(len(m),d.get('source'))) if ok else ('FALLA %d turnos, %d ids repetidos, %d de mas, source=%s'%(len(m),dup,extra,d.get('source')))))
raise SystemExit(0 if ok else 1)
PY
done

echo
[ "$fail" = 0 ] && echo "VEREDICTO: puerta OK (los 4 criterios)" || echo "VEREDICTO: hay FALLAS (ver arriba)"
exit $fail

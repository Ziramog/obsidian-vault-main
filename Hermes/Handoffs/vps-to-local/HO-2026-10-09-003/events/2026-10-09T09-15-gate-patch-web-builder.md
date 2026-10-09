---
event: parche-propuesto
handoff: HO-2026-10-09-003
at: 2026-10-09T09:15:00-03:00
by: web-builder
status: verificado en memoria contra HEAD d682961e — NO aplicado, espera decisión de brain-local
adjunto: events/agenda-bot-gate.patch (sha256 ec5f4af844f0a96290ad5b51e87d5ca825f9435800c389cdeef87a2f64c039a6)
---

# Parche del gate S4 + fix del regex de fechas — verificado, sin aplicar

Sin tokens ni secrets. El fuente vivo no se tocó; el vault real sólo se montó en
lectura (una vez, sólo casos query, checksum idéntico).

## Por qué existe

1. La implementación en HEAD (`b8cd4813`) pasa la matriz literal del request pero
   deja el **default en `cmd_add`**: 10 de 16 entradas fuera de la lista crean
   tarea (ver `2026-10-09T09-06-acceptance-web-builder.md`).
2. La corrección de @web-auditor es correcta y la reproduje: con el gate invertido
   *solo*, se pierden altas legítimas porque `_DATE_TOKEN_RE` de HEAD casa
   `a\s+las\s+\d` con `\b` final, así que `a las 10`, `a las 12`, `a las 15`,
   `3/11`, `antes de las 12`, `después de las 15` y `a la tarde` son **False**.
   El fix del regex es requisito del gate, no un extra.

Tabla cruda `_DATE_TOKEN_RE` (HEAD → parche): `a las 9` True→True; `a las 10`,
`a las 12`, `a las 15`, `3/11`, `3/11 14:30 reunión`, `después de las 15`,
`antes de las 12`, `a la tarde`, `a la noche`, `en 3 días` → **False→True**;
`fin de mes`, `mañana 9 llamar a GAMA`, `miércoles que viene 14 …` True→True.

## Qué hace el parche (128 líneas de diff, 3 hunks funcionales + 1 defensivo)

1. `_DATE_TOKEN_RE`: `a las \d{1,2}`, `\d{1,2}[:/]\d{1,2}`, `antes|después de
   las N`, `a la tarde/noche/mañana`, `en N días`, `día N`.
2. Gate invertido en `handle_text`: `_is_help_query` → `_is_query_cue` (cue
   interrogativo ancorado: qué/tenés/tengo algo/mostrame/dame/listar) →
   `_has_task_signal` (token de fecha) → pedir precisión. `cmd_add` deja de ser
   el default.
3. **Defensivo (hallazgo nuevo, no estaba en la matriz):** `agenda.py` señala los
   errores de usuario con `raise SystemExit` y el bot no los captura en ningún
   lado. `poll_once` sólo atrapa `Exception`, así que **un solo mensaje inválido
   mata el `poll_loop` residente**. Reproducido, 7 de 11 sondeos:

   ```text
   LEAK  '/detalle ag-20260101-999'            -> SystemExit: No encontré tarea: ag-20260101-999
   LEAK  '/detalle 99'                         -> SystemExit: No encontré tarea: 99
   LEAK  '/cancelar ag-20260101-999'           -> SystemExit: No encontré tarea: ag-20260101-999
   LEAK  '/prioridad ag-20261010-001 azul'     -> SystemExit: Prioridad inválida. Usá rojo/amarillo/verde.
   LEAK  '/mover ag-20261010-001 blursday'     -> SystemExit: Fecha inválida: blursday. Día no reconocido.
   LEAK  '/editar ag-20260101-999 nuevo texto' -> SystemExit: No encontré tarea: ag-20260101-999
   LEAK  '/hecho ag-20260101-999'              -> SystemExit: No encontré tarea: ag-20260101-999
   ok    '/posponer ag-20261010-001 99:99' · 'ok 99' · '/limpiar' · alta duplicada
   ```

   Con el parche: `safe_handle_text` convierte el `SystemExit` en
   `No pude completar eso: <msg>. No guardé nada.` y `poll_once` atrapa
   `(Exception, SystemExit)`, así que el loop sobrevive. Sin esto, el E2E del
   criterio 4 se cae con un solo typo en `/detalle`.

## Verificación del parche (vault temporal, módulo parcheado en memoria)

| suite | resultado |
|---|---|
| A — matriz literal del request | **10/10** |
| B1 — 14 ejemplos NL del propio `/help` | **14/14** (uno documenta 3 tareas y da 3) |
| B2 — 17 ejemplos de comando del `/help` | **17/17** con 0 altas indebidas |
| C — batería fuera de lista (los 10 huecos + 2 controles de alta) | **18/18** |
| E — variante gate-sin-fix-regex sobre B1 | **9/14** ← por eso el regex va en el mismo parche |

`git apply --check` del adjunto contra el árbol limpio en `d682961e`: **exit 0**.
El módulo resultante se compiló y ejecutó todas las suites.

## Cómo aplicarlo (un solo editor)

```text
cd /home/hermes/obsidian-vault
git apply -p1 Hermes/Handoffs/vps-to-local/HO-2026-10-09-003/events/agenda-bot-gate.patch
python3 -c "import py_compile;py_compile.compile('Hermes/Systems/vps/scripts/agenda-telegram-bot.py',doraise=True)"
pm2 restart agenda-telegram-bot
```

Después: E2E por Telegram (`listar comandos`, `semana que viene`, una alta clara,
y un `/detalle` con id inexistente para confirmar que el loop no muere) y
evidencia acá. No lo aplico yo: el lado VPS es el editor vivo del archivo y un
patch desde local choca con el próximo `auto-sync [vps]`.

## Decisiones que no me corresponden

- **Umbral del gate**: una acción sin fecha (`comprar café`) hoy cae en "pedime
  precisión" y ya no crea tarea. Es el precio de que los vagos no creen basura;
  si Juan prefiere que se guarde igual, la vuelta es pedir confirmación con botón
  en vez de rechazar.
- **Persistencia del crudo**: sigue sin appendear a `Agenda/bandeja.md`.
  @web-auditor lo leyó bien: el request lo acepta por la rama "o pedir
  confirmación" y persistir es alcance nuevo.

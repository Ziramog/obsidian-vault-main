# Prompt para Antigravity — Fase 3 · el log real de las salas en el celular (repo `hermes-agent`)

**Repo:** `C:\Users\ingju\AppData\Local\hermes\hermes-agent` (**NO** `hermes-pwa`; blast radius de Hermes mismo).
**Rama propia** (`fix/group-chat-ui-meta-budget`), **OK explícito de Juan** requerido antes de tocar nada, y **sin**
relación con los commits de Fase 1/2 de `hermes-pwa`.
**Objetivo de negocio:** que el celular (PWA) muestre el log **completo** de cada sala del Desktop, no una
reconstrucción incompleta ni una proyección recortada.
**Precedente:** `Hermes/Quarantine/hermes-pwa-fase2-recon-fuente-de-verdad-2026-09-28.md` y
`Hermes/Quarantine/hermes-pwa-fase2-replicacion-salas-antigravity-prompt.md` (sección 0 = techo real).

---

## Diagnóstico (verificado sobre el código, no inferido)

La PWA lee el espejo que el plugin del Desktop publica en `ui_meta['hermes-bots-groups']`. Ese espejo es
**lossy por diseño** y hay **dos topes** en dos capas distintas:

| Capa | Ubicación | Qué hace |
|---|---|---|
| Plugin (TS) | `apps/desktop/src/plugins/hermes-bots/group-chat.ts:52-54` → **working tree**: `GROUP_CHAT_SYNC_MAX_BYTES = 900_000`, `…_MESSAGES = 100`, `…_TEXT_CHARS = 60_000` · **commit `a7254e2d4c` (13-sep)**: `48000` / `16` / `1200` — o sea los tres números están **editados a mano y sin commitear** | Arma la "bounded ui_meta projection: a compacted log" (`:275-280`) y trimmea el log de **una** sala hasta entrar en el presupuesto; si aun así no entra, `delete rooms[key]` |
| Gateway (Python) | `tui_gateway/methods_profiles.py:494` → `if len(json.dumps(incoming)) > 65536: return` | **Rechazo silencioso**: `return` antes de mergear, `applied["ui_meta"] = False`, sin excepción ni mensaje |

**Medición del espejo que hoy está en disco** (`%LOCALAPPDATA%\hermes\profile.yaml`): 1 room,
`updatedAt` 2026-09-28 15:41, log de 54 entradas con `omitted: 359`, **12 con `truncated: true`**,
`text` máx 2.930 caracteres, JSON del `ui_meta` = **47.023 bytes** (entra en los 65.536 ✓).
Esos números no coinciden ni con el commit (`48000`/`1200`/`16`) ni con el working tree
(`900_000`/`60_000`/`100`): el payload lo escribió un estado intermedio (presupuesto ≈48 KB y tope de texto
≈3.000 caracteres), o sea que **las constantes se vienen tocando a mano hoy** para intentar que el celular
vea más.

**Estado actual verificado (no predicción): qué build corre y con qué números.** La app que escribe el espejo es
`hermes-agent/apps/desktop/release/win-unpacked/Hermes.exe` (5 procesos vivos), pero el **renderer no sale del
`app.asar`** (paquete del 23-sep: no contiene la key `hermes-bots-groups` ni las constantes) sino de
`apps/desktop/dist/`, **reconstruido hoy 15:47** (después del edit de las 11:27 y después de la escritura del
espejo). En el bundle minificado `dist/assets/index-DcgY84mB.js` los valores son los del **working tree**:
`Xk='hermes-bots-groups'`, **`Zk=9e5`** (900.000), **`Oke=6e4`** (60.000), `Ake=24e3`, `kke='… [truncated]'`.
Conclusión: la build viva ya tiene el presupuesto de 900 KB contra el cap de 65.536 del gateway → **el rechazo
silencioso no es hipotético, es el estado actual** y el espejo quedará congelado en el payload de 15:41 (escrito
por la build anterior de `dist/`, la que sí tenía ~48 KB y por eso pudo entrar). Por eso: no se toca ningún tope
sin revertir/declarar primero ese diff y **reconstruir `dist`** como parte del ciclo de verificación.

**El rechazo está demostrado, no predicho (suite del plugin corriendo sobre este working tree):**
`npx vitest run src/plugins/hermes-bots/group-chat.test.ts` → **4 failed | 45 passed**, y los tres números que
salen de las aserciones viejas son la medida del payload que la build viva le manda al gateway:

| test | aserción | real |
|---|---|---|
| `is size bounded and favors recent messages` (`:535`) | ≤ 48000 | **507.379** |
| `preserves threads and budgets escaped Unicode` (`:590`) | ≤ 48000 | **232.219** |
| `counts the head entries the mirror does not carry` (`:611`) | `log` de 16 | **40** |
| `marks truncated sync text instead of silently slicing it` (`:568`) | `truncated === true` | `undefined` |

Contra el cap real de **65.536**, esos envelopes son 3,5× y 7,7× más grandes: la escritura se rechaza entera y
encima **sin tocar los tests** (el archivo de tests está sin modificar). Es la firma exacta del congelamiento
medido en `profile.yaml` (mtime y `updatedAt` en 15:41, **3 h 30 min sin escrituras** con el Desktop vivo,
`_ui_meta_revisions` clavado en 1668).

**Root cause del "1 de 4 salas"**: la proyección rankea las salas por actividad (`:283-289`, newest-first) y
trimmea **sólo la sala que está agregando**
(`while (compact.log.length > 1 && groupChatGatewayJsonSize(envelope) > MAX) compact.log.shift()`, `:398-401`).
La sala más nueva se queda con todo el presupuesto de la corrida: con el presupuesto ≈48 KB que escribió el
payload que está en disco, algolab (413 entradas) lo consumió entero — `log: 54`, `omitted: 359` — y las otras
tres salas cayeron por la rama `if (groupChatGatewayJsonSize(envelope) > MAX) delete rooms[key]` (`:405-407`).
Con el presupuesto del working tree (900 KB) el resultado empeora por el otro lado: el JSON supera los 65.536 del
gateway y **toda** la escritura se rechaza en silencio, así que en disco queda congelado el último payload que
sí entró. En las dos direcciones el síntoma es el mismo: **un solo escritor, un solo presupuesto y ningún
rebalanceo entre salas**.

Consecuencia: subir el tope **no alcanza**; mientras el `ui_meta` sea el transporte, el celular ve una proyección
recortada y con salas faltantes.

## Tarea — tres cosas, en este orden

### 1. Hacer visible el rechazo (bug de diagnóstico, mínimo y bloqueante)

- En `_configure_ui_meta` (`methods_profiles.py:487`), cuando `len(json.dumps(incoming)) > 65536`, **no** retornar
  en silencio: devolver `applied["ui_meta_error"] = "too_large"`, el tamaño calculado y el límite. El plugin ya
  distingue `applied.ui_meta !== true` (`apps/desktop/src/plugins/hermes-bots/data.ts:416-438`), así que la señal
  se puede mostrar/serializar sin tocar el contrato existente.
- Mismo tratamiento para los otros dos `return` silenciosos del mismo camino (conflictos CAS ya reportan).
- Test: `tests/tui_gateway/test_profiles_ui_meta_cas.py` (o hermano) con un `incoming` de >65536 → el resultado
  trae `ui_meta_error` y `profile.yaml` **no** se modifica.

### 2. Que la proyección quepa de verdad (plugin TS)

- Reemplazar el presupuesto único `900_000` por el cap real del gateway (65 536) con el margen por escapado de
  Unicode que el comentario de `:50-51` ya declara explícito (`json.dumps` escapa no-ASCII) — y **derivar** el
  número de una sola constante compartida, no de dos valores que se creen equivalentes.
- Repartir el presupuesto **entre** salas (round-robin por sala, no greedy): ninguna sala puede quedarse el total
  ni desaparecer. `omitted` ya existe por sala (`:64-68`) y es lo que la UI debe usar para decir "hay N mensajes
  anteriores que el espejo no lleva".
- Nunca `delete rooms[key]`: una sala sin presupuesto se publica con `log: []` + `omitted: <n>` (el celular
  distingue "sala sin mensajes" de "sala no existe" — ver contrato HTTP de Fase 2 en `hermes-pwa`).
- Tests del plugin (`group-chat.test.ts`, `group-chat-view.test.ts`, `group-panes.test.ts`): 4 salas reales
  (413/172/115/10 entradas) → las 4 presentes, todas con `omitted` correcto y el JSON final ≤ cap.

### 3. Arquitectura (recomendación a decidir, no implementar sin OK)

`ui_meta` **viaja en cada `profiles.list`**: usarlo como API de transcripción para el celular es un costo
permanente por paint y un techo estructural. Opciones, en orden de preferencia:

1. **RPC dedicado** de salas/transcripción (`groups.transcript` en `tui_gateway/contracts/groups_bot_relay.py`,
   que ya declara formas de roster/eventos/room-link) leyendo el log del plugin; `ui_meta` queda sólo con el
   catálogo (`name`, `members`, `roomId`, `revision`, `omitted`) — chico, barato y siempre completo.
2. Publicar el log completo a un store server-visible (archivo o tabla `state.db`) por sala y que la PWA lo lea
   por HTTP desde el nodo dueño.
3. Sólo subir el cap del gateway: la peor de las tres (encarece cada `profiles.list` de todos los clientes y no
   elimina el recorte).

## Archivos a tocar (Fase 3)

`tui_gateway/methods_profiles.py` · `apps/desktop/src/plugins/hermes-bots/group-chat.ts` ·
tests: `tests/tui_gateway/test_profiles_ui_meta_cas.py`, `apps/desktop/src/plugins/hermes-bots/group-chat*.test.ts`.
En el punto 3, además: `tui_gateway/contracts/groups_bot_relay.py` + `scripts/gen_gateway_contracts.py` (regenerar)
y el consumidor TS (`apps/shared/src/gateway-contract.generated.ts`).

## Restricciones

- **No** tocar `hermes-pwa` en esta fase; su Fase 1/2 se cierra aparte.
- **No** romper el contrato `ui_meta` (lo consumen Desktop y PWA): los campos nuevos son aditivos
  (`omitted` ya existe; `ui_meta_error` es nuevo en el resultado del RPC).
- **No** cambiar el ranking por actividad ni el formato del log; sólo el reparto del presupuesto.
- **No** tocar `_ui_meta_revisions` / CAS: el rechazo por tamaño se reporta, no se reintenta a ciegas.
- El repo tiene su propio `AGENTS.md` y sus reglas de tests (`scripts/run_tests.sh`): no inventar comandos.
- Caveat de verificación: el código leído es el del repo; **confirmar las constantes contra la build instalada**
  del Desktop antes de cerrar el diagnóstico (si la build difiere, el número del recorte puede variar).
- **Antes de empezar:** el working tree de `hermes-agent` tiene **3 archivos modificados sin commitear** en el
  plugin (`group-chat.ts`, `group-chat-view.tsx`, `plugin.tsx`) y ahí viven exactamente los tres números que
  rompen el presupuesto. Decidir con Juan si se descartan, se stashean o entran como parte del branch; la rama
  nueva tiene que partir de un estado **declarado**, no de este diff sorpresa.

## Criterios de aceptación

1. Con las 4 salas reales del nodo, `ui_meta['hermes-bots-groups'].rooms` en `profile.yaml` tiene **4 rooms**
   (hoy 1) y el JSON medido (con escapado Python) **≤ 65 536**.
2. `omitted` por sala coincide con el recorte real y la PWA puede mostrar "faltan N mensajes anteriores".
3. `log 0` nunca aparece como ausencia de sala: una sala sin presupuesto sigue publicada.
4. Push de `>64 KB`: el RPC responde `ui_meta_error:"too_large"` con tamaño y límite; `profile.yaml` intacto.
5. Suites en verde, y **no por borrar aserciones**: las 4 que hoy fallan por el diff (`:535`, `:568`, `:590`,
   `:611`) tienen que describir el contrato nuevo (presupuesto derivado del cap real, `omitted` por sala,
   truncado por texto) o eliminarse con justificación escrita; y se agrega la que hoy **no** existe: envelope
   ≤ 65.536. `tsc` del desktop y regeneración de contratos sin drift.
6. Receipt real: `GET /api/groups` de la PWA del VPS mostrando la sala con su catálogo completo y el conteo de
   `omitted` de cada una, contra el mismo `profile.yaml` que hoy sólo trae `id:rmuag13gp-5r3kn`.
7. Ciclo de build: tras el cambio, **reconstruir `apps/desktop/dist`** y verificar las constantes en el bundle
   (`grep -o -a "hermes-bots-groups.\{0,200\}" dist/assets/index-*.js`), porque es de ahí —no del `app.asar` del
   23-sep— que el renderer vivo toma el código. Y comprobar que el `updatedAt` del espejo en `profile.yaml`
   **avanza** después del cambio (hoy está fijo en 15:41 y ahí es donde se ve el rechazo silencioso).
8. **Termómetro binario de "espejo sano"** (criterio acordado con @web-auditor / @brain-local): tras reconstruir
   `dist`, un mensaje en cualquier sala debe mover **`_ui_meta_revisions["hermes-bots-groups"]` de 1668 a 1669** y
   el `updatedAt` embebido dentro del minuto. Si el error explícito ya se ve pero el contador sigue en 1668, el
   payload sigue sin entrar y el fix está a medias. (`_ui_meta_revisions` sólo lo escribe
   `methods_profiles.py:519-524`, o sea el espejo es gateway-mediated; su escritura es atómica —
   `utils.atomic_yaml_write`, `:525-526` — y **no** es el B5 de la auditoría, que es el `saveProfileDoc` del PWA.)
9. Higiene de evidencia, para que nadie defienda el diagnóstico con un dato flojo: `24e3` **no discrimina** builds
   (`GROUP_CHAT_SYNC_IMAGE_CHARS = 24000` vale igual en HEAD y en el working tree). El par que sí:
   en el bundle vivo `12e2` y `1.2e3` (así minifica HEAD su `TEXT_CHARS = 1200`) aparecen **0** veces y `9e5`
   aparece **2**. Y el contraargumento fácil de encontrar ya está cerrado: el `48e3` del bundle **no** es HEAD,
   es `MAX_REVIVE_BUFFER_CHARS = 48_000` de `src/app/right-sidebar/terminal/terminals.ts:57`.

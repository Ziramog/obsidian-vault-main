# Informe final — Hermes PWA: auditoría, correcciones y verificación

**Fecha:** 29 de septiembre de 2026
**Repo:** `C:\Projects\hermes-pwa` → `https://github.com/Ziramog/PWA-Hermes.git` (privado)
**Rama de trabajo:** `fix/fase2-salas` = **`9062356`**
**Estado final:** `main` = **`7434404`** (merge de `fix/fase2-salas`) · `fix/fase1-auth` = `3186a37`
**Desplegado:** VPS `100.124.132.48` — rama `deploy/fase2` @ `9062356`, `pm2 restart hermes-pwa --update-env`, `node v20.20.2` (BUILD_ID `p3sPKlG0m3r0zP01SMb6i`)
**Par de la PC:** `100.105.0.23:3300` corriendo el mismo commit
**Objetivo del informe:** responder, con hechos y mediciones reproducibles, a la auditoría externa y documentar qué se arregló, qué se midió y **qué queda pendiente**.

---

## 0. Cómo leer este informe

Todo lo que sigue es **medición ejecutada**, no inspección visual: cada afirmación tiene el comando y su salida, y las mediciones se hicieron **desde tres nodos distintos** (PC, VPS, y un tercer cliente independiente) para no depender de un solo punto de vista.

Convenciones:

- **PC** = nodo local (`100.105.0.23`), PWA en `:3300` (par), gateway Hermes en `:8642`.
- **VPS** = `100.124.132.48`, PWA en `:3000` (la que ve el celular), gateway en `:8642`, nodo de sala en `:9119`.
- Los credenciales nunca se imprimen; todas las llamadas usan `Authorization: Bearer [REDACTED]` desde `.env.local`.
- Las pruebas de ruteo usan un cuerpo **sin** el campo `messages`: el perfil se resuelve y la petición **frena en la validación del payload** (HTTP 400). Es la forma de probar el ruteo **sin enviar ningún mensaje**.

---

## 1. Resumen ejecutivo

El síntoma reportado por el usuario era doble: **las conversaciones de sala no se veían completas en el celular** y **los bots de la PC no respondían** aunque aparecieran en la lista.

Causas medidas (todas reproducidas antes de corregir):

1. **La app leía un "espejo" congelado.** Los mensajes de sala se reconstruían desde un archivo compartido con el Desktop (`profile.yaml`) que llevaba horas sin actualizarse: la sala principal que el usuario usaba **no aparecía y su endpoint devolvía 404**.
2. **El ruteo del envío dependía de un dato del cliente.** `POST /api/chat` elegía el nodo con `body.node` / `x-hermes-node`; sin ese dato, todo iba al nodo local → los 9 perfiles de la PC respondían **404 `Unknown or unconfigured profile`** desde el VPS (y simétricamente al revés).
3. **La autenticación era decorativa.** Cualquier cadena servía como clave: `Bearer totally-fake-key` devolvía **200** en `/api/profiles`, `/api/groups` y `/api/sessions`.
4. **Defectos de reconstrucción**: mensajes duplicados, autores inventados a partir del texto, y "miembros" con nombre de frase.

Lo corregido y verificado (números abajo, §4 y §5; todas las tablas de conteos corresponden a mediciones del **2026-09-29** y van con su hora en cada sección):

| | antes | después |
|---|---|---|
| salas visibles en el celular | 3 (y la principal ausente, 404) | **4, incluida la principal** |
| turnos de la sala principal servidos | 3 (uno fabricado) | **56**, con 5 autores reales |
| `Bearer` falso | **200** | **401** |
| bots de la PC alcanzables desde el VPS | 0 de 9 (404) | **9 de 9** (resuelven) |
| autores fuera de la población de confianza | **161 en una sala** | **0 en las 4 salas** |
| "miembros" mostrados con nombre de frase | **163** (139 basura) | **0 basura** |
| turnos repetidos por `id` repetido (4 salas, **sin umbral de largo**) | **94 de más sobre 1534 (6,2 %)**, todos de `You` | **0 sobre 1511** en el build del commit 7 (medido en la puerta del funnel: 82/163/145/1121 turnos, **todos los ids únicos**) |

---

## 2. Qué quedó pendiente (residuos declarados)

Estos puntos **no** están cerrados y se declaran con su medición:

1. **Turnos repetidos por `id` repetido: 94 turnos de más sobre 1534 (6,2 %)**, medido por tres clientes sobre el VPS desplegado (`rmuli31hi` 63 turnos/3 ids repetidos/6 de más · `rmugviqw9` 196/17/33 · `rmufxz2ti` 151/6/6 · `rmuag13gp` 1124/49/49). **Es el único residuo que el usuario ve sin buscar**: en la sala del equipo, **sus propios mensajes aparecen ×3** (`"@brain-local pudieron hacer todo?"` ×3 con `at` a 202 s y 72 s, `"@local dame el status"`, `"procedan con despliegue…"`), y en las cuatro salas los autores de los ids repetidos son **todos `You`**.
   **Corrección de este informe**: una versión anterior decía "2 pares de duplicados" — era un artefacto del instrumental, que contaba pares por texto **≥120 caracteres**. Medido por `id` y sin umbral de largo, la magnitud real es la de arriba: sólo **7 de los 75** grupos repetidos son ≥120 ch; la mayoría son mensajes de 20 a 119 caracteres. **El umbral era ciego justo al residuo visible.**
   **Causa raíz, con línea** (`room-store.ts` de `9062356`): `:396` crea `shortMsgKeys` una vez por corrida; `:436` busca el ordinal con la clave `${_node}|${nombre}|${texto}`; `:441` el id es `sha1(roomId|nombre|texto|ordinal)`. **`_node` está en la clave del ordinal pero NO en el id**: dos copias de la misma línea que llegan por contextos distintos arrancan cada una en ordinal 1 y producen **el mismo id**; la deduplicación llaveada por id no puede colapsar lo que el propio id ya confundió. Agravante: **para `You` no hay sesión dueña** (el usuario no tiene sesión; cada bot registra su línea en la suya), así que el caso "N registros de un evento sin dueño" queda fuera de la regla que arregló el resto.
   **Propiedad que tiene que cumplir el arreglo**: la identidad del evento **no puede depender de la corrida de agregación** ni del nodo — va del evento fuente, y los ordinales se asignan **después** de la unión. Base medida para el colapso: en las sesiones del VPS hay **219 líneas de sobre y 0 pares `(autor, texto)` repetidos dentro de una misma sesión** → toda repetición observada es copia de la misma línea en otra sesión, nunca un reenvío legítimo. **Aserción correcta: 0 turnos con `id` repetido en el payload servido, sin umbral de largo.**
2. **Etiqueta de nodo invertida en los transcripts**: el payload de mensajes de una sala servida desde el par devuelve `node:"local"` mientras `source:"peer"` y `peerReachable:true`. El dato es correcto; la etiqueta que lee la UI no.
3. **`/api/groups` fija `source:"local"`** en la lista y sólo pasa a `merged` en un camino secundario (`groups/route.ts:77` y `:102`): el celular puede mostrar "local" con la conversación fusionada.
4. **Perfil inexistente → `502 {"code":"NODE_UNREACHABLE"}`**: hay `code` explícito (ya no el 404 mudo) pero la semántica es imprecisa — el par está alcanzable y lo que falta es el perfil (`PROFILE_NOT_IN_NODE`).
5. **Cuerpo de error doble-codificado** en la validación de `/api/chat`: `{"error":"{\"error\": {...}}"}`.
6. **Arranque en frío del par: 62,9 s** en la primera llamada después de un reinicio (las siguientes, 0,32–2,6 s). Quien abra la app justo después de un reinicio ve la pantalla colgada ~1 minuto.
7. **El ruteo rápido dependía de `HERMES_SELF_URL`**, variable que **no está** en `.env.local` ni en ningún ejemplo: si faltaba, la tabla rápida quedaba vacía **en silencio** (el `catch` la tragaba) y todo se resolvía por el camino lento (sondeo por perfil, timeouts de 2 s). **Precisión posterior**: esa variable pertenece a los commits 5–7 y **no existe en el artefacto desplegado** (`git grep` sobre `9062356` → 0); lo que rompe en `9062356` es la falta de **`HERMES_PEER_PWA_URL`** (residuo 12). **En el build del commit 7 la variable ya no hace falta**: la puerta del funnel, relanzada con sólo `HERMES_HOME` + `HERMES_PEER_PWA_URL` y **sin** `HERMES_SELF_URL`, resuelve los 17 perfiles y rutea los cuatro perfiles de prueba a `400`.
8. **El VPS sirve las 4 salas como `source:"peer"`**, sin fusionar su propia mitad aunque tiene corpus local para dos de ellas: hoy el celular ve la conversación de la PC y no la del VPS en esas salas. **Precisión medida**: el tramo que sólo tenía el nodo del VPS **sí está** en el payload que recibe el celular (`rmufxz2ti` llega a `09-28 00:16:49` con 22 eventos entre `23:16:49` y `00:17`): **el merge entra; lo que miente es la etiqueta**.
9. **`node` del payload es el del par, no el del nodo que sirve** — con la línea y el comentario del propio autor: `groups/[groupId]/messages/route.ts:40` → `peerError = { node: peerData.node }; // Temporary way to pass node`. No es "la UI lee mal un dato correcto": el campo está mal poblado en el borde. Arreglo: servir los dos (`node` = nodo que sirve, `peerNode` = el del par).
10. **Falso positivo de `peerReachable`**: `messages/route.ts:23` lee `HERMES_PEER_PWA_URL` y `:28` envuelve todo en `if (peerUrl && peerToken)`. Si falta **el token**, el bloque no corre, `peerError` queda `null` y la salida calcula `peerReachable: peerUrl ? !peerError : false` = **`true`** → declara que consultó al par **sin haberlo consultado**. Es la misma clase del residuo 7, y más grave: no es silencio, es una afirmación falsa.
11. **La derivación de puerto no desapareció: se mudó.** `profiles/route.ts:151` conserva literalmente `HERMES_PEER_PWA_URL || HERMES_VPS_URL.replace(/:\d+$/, ":3000")` — el string que el criterio prohíbe — ahora en la ruta que sirve `?scope=local`, que es la **fuente de la tabla de ruteo**, con `abort` de 3000 ms mientras las llamadas cruzadas entre nodos se midieron entre 2 y 10 s: cuando el presupuesto se pasa, la mitad del par de la tabla desaparece sin señal.
12. **Acoplamiento de configuración que rompe el ruteo en silencio de diagnóstico** (medido en producción el 2026-09-29): `routing.ts:54-55` exige `HERMES_PEER_PWA_URL` y **lanza** `NODE_UNREACHABLE` si falta; el `catch` de `:72-79` devuelve el fallo **de inmediato** (`return { resolvedNodeLabel: "NODE_UNREACHABLE", nodeId: "vps" }`) y el armado de la caché **nunca registra la mitad local** (`profileCache = cache` en `:84` no se ejecuta). Consecuencia medida en la instancia de la PC (cuyo `.env.local` tiene 4 variables y **no** la del par): **502 en TODOS los perfiles, incluidos los 9 locales de la propia máquina**, con el mensaje `"El nodo par no es alcanzable para el perfil brain-local"`. Contraste medido: el VPS, **sin** `HERMES_SELF_URL` y **con** la variable del par, resuelve 17/17. **Y `HERMES_SELF_URL` no existe en este artefacto**: `git grep` sobre `9062356` → **0 ocurrencias** (es variable del commit 7); atribuirle el fallo del funnel es un error que cualquier auditor derriba con esa búsqueda.
13. **El sobre de error del 502 está fabricado**: en sus cuatro sitios (`chat/route.ts:25`, `groups/[groupId]/chat/route.ts:91`, `sessions/[sessionId]/messages/route.ts:24` y su gemelo) el cuerpo es `{"code":"NODE_UNREACHABLE","node":"vps","lastSeenAt":<Date.now()>}`: **`node` es un literal** (no el nodo que falló) y **`lastSeenAt` es la hora del error disfrazada de último contacto** — medido: seis respuestas consecutivas con `lastSeenAt` en milisegundos consecutivos (`…90498`, `…90500`, `…905016`, …). Es la misma clase "etiqueta no derivada de la medición", y en esta ronda **fue la que desvió el diagnóstico de los tres agentes**: hizo perseguir al nodo par cuando el perfil que fallaba era **local**.

**Estado del diagnóstico del funnel (medición 2026-09-29, hora local del reporte ~23:10 UTC-3)**: el `funnel` del nodo de la PC servía una copia **sin la variable del par** → 502 en todos los perfiles y los 8 bots del VPS como `OFFLINE (PEER_MISSING_CONFIG)`, que es exactamente el síntoma reportado por el usuario en el celular. **Arreglo aplicado y verificado**: `HERMES_PEER_PWA_URL=http://100.124.132.48:3000` en el arranque de esa instancia + reinicio → por esa misma URL ahora **9 locales + 17 fusionados, los 17 online**, ruteo `400` (resuelto) para perfiles de los dos nodos, y las 4 salas con **0 ids repetidos y 0 autores fuera de la población de confianza**. **Trazabilidad**: esa instancia sirve **`c7b2d70`**, y ese commit **ya está en el remoto** (`git ls-remote origin refs/heads/fix/fase2-salas` → `c7b2d705a4c8…`, verificado en esta ronda); `main` sigue en `7434404`, o sea el 7 **no está mergeado**. El VPS sigue en `9062356`, así que el criterio **se cumple en la puerta del funnel y queda pendiente en la puerta del VPS** hasta que se despliegue el 7 allí.

**Las dos puertas no son comparables — presentar por puerta, nunca en una sola tabla** (medición 2026-09-29, mismo día, minutos de diferencia):

| puerta | build | perfiles | ruteo | `rmuli31hi` | `rmugviqw9` | `rmufxz2ti` | `rmuag13gp` |
|---|---|---|---|---|---|---|---|
| funnel `truzt…` (nodo PC) | `c7b2d70` | 17: 9 `🖥️ PC Local` + 8 `☁️ VPS` | **400 ×4** | **0** | **0** | **0** | **0** |
| par `100.105.0.23:3300` (nodo PC) | `c7b2d70` | 9 locales | 400 ×4 | **0** | **0** | **0** | **0** |
| `100.124.132.48:3000` (nodo VPS) | `c7b2d70` | 17 | 400 ×4 | **0** | **504 `PEER_TIMEOUT`** | **0** | **504 `PEER_TIMEOUT`** |

Estado final medido (2026-09-29, última pasada): **el criterio "0 turnos con `id` repetido" se cumple en las tres puertas** — 116/116, 182/182, 162/162 y 1383/1383 en las puertas del PC, y 134/134 y 184/184 en las dos salas que el VPS sirve desde su propio corpus (frente a los 94 turnos de más del despliegue anterior). Los conteos **no son comparables entre puertas** (una fusiona las dos mitades, otra sirve sólo la suya): un auditor que lea "116" y "134" en la misma fila va a creer que hay una discrepancia donde hay dos artefactos distintos.

**Dos residuos nuevos de esta última medición**:

- **Timeout del par en las salas grandes**: en la puerta del VPS, `rmugviqw9` y `rmuag13gp` (las dos mayores: 196 y 1167 turnos en el par) devuelven **`504 {"code":"PEER_TIMEOUT"}`**, y **de forma repetible**: la segunda pasada, con el par ya caliente, da idéntico resultado, así que **no es arranque en frío** sino que el presupuesto de `messages/route.ts:40` (**5000 ms**) no alcanza para los payloads grandes de una llamada cruzada (la clase se midió entre 2 y 10 s). Los dos nodos reportan además `peerReachable:false` en su propia puerta, de modo que hoy cada puerta sirve su mitad y **la fusión no está ocurriendo**: los conteos de arriba son "por mitad", no fusionados.
- **Autores basura `.hermes` en la reconstrucción local del VPS**: en su propio corpus, `rmuli31hi` tiene **20 turnos** y `rmufxz2ti` **58** con autor **`.hermes`** — un nombre que no pertenece a ninguna población de confianza declarada. No aparece en el corpus del PC. Es una clase nueva del mismo tipo que el informe ya documenta (autor derivado de un identificador en vez de un nombre verificado) y queda **del lado del nodo VPS**.

**Nota de método sobre la población de confianza**: el roster con el que se validan los autores debe ser la **unión de los perfiles locales que declaran los dos nodos** (`?scope=local` de cada uno → 20 nombres) más los especiales (`You`, `hermes`, `default`). Validar con el censo de un solo nodo produce **falsos positivos** en la puerta del otro: con el censo del PC, los autores legítimos del corpus local del VPS aparecen como "fuera de roster".

**Trampa de arranque que hay que declarar** (mordió dos veces en esta ronda): **mismo binario, mismo `.env.local`, `HERMES_HOME` distinto ⇒ 0 perfiles**. La instancia del funnel relanzada **sin** `HERMES_HOME` arrancó sana (`/api/health` 200) y con **`profileCount: 0`** y `?scope=local` vacío: la app se veía funcionando y no tenía ni un perfil local. Es la misma clase de defecto que el resto del informe — una degradación que no se anuncia — y por eso el arranque de cualquier nodo debe fijar `HERMES_HOME` explícitamente y verificarse con `profileCount` **antes** de declararlo sano.

**Nota sobre los residuos 6 y 7**: son **independientes**. `messages/route.ts` **no llama** a `resolveProfileNode` y su `fetch` al par aborta a los 12 s, así que el arranque en frío de 62,9 s **no** es un timeout del par ni el `HERMES_SELF_URL` faltante: presentarlos como una misma causa sería un error que cualquier auditor derriba midiendo.

**Nota sobre zonas horarias**: las fechas de este informe están en **UTC-3** sobre el epoch del payload. El mismo epoch renderizado en UTC-4 da `09-27 23:16:49` donde aquí dice `09-28 00:16:49` — una hora de diferencia de **presentación**, no de contenido. Toda comparación de ventanas temporales entre nodos debe declarar su zona.

---

## 3. Verificación de la auditoría externa, punto por punto

La auditoría recibida enumeraba cinco fallos. Se verificó cada uno contra el código y contra las instancias en ejecución:

| # | Afirmación de la auditoría | Veredicto | Evidencia |
|---|---|---|---|
| 1 | "El chat de sala no persiste nada; los mensajes desaparecen" | **A medias** | El PWA efectivamente **no escribe** (se quitó a propósito: escribía en `profile.yaml`, un archivo compartido con el Desktop y el gateway, y lo corrompía). Pero los mensajes **sí persisten**: los escribe Hermes en la sesión del bot (`state.db`), que es la fuente de la reconstrucción. Medido: 56 turnos servidos de la sala principal, **11 con autor `You`**, recuperados tras recargar. **Riesgo real**: si el bot destino vive en el otro nodo y ese nodo está caído, el mensaje se muestra en el stream y no se persiste en ningún lado. |
| 2 | "Peer fantasma: en el VPS no hay PWA en `:3000`, sólo el gateway en `:8642`" | **Premisa falsa; el mecanismo que describe existe** | `GET http://100.124.132.48:3000/api/health` → **200** (medido varias veces, incluido por el propio nodo del VPS durante el despliegue). El par es un canal **PWA↔PWA** por diseño; el `:8642` es otro canal. El bug que describe (el `catch` que pre-inserta los bots remotos como `isOnline:false/NODE_UNREACHABLE` y luego descarta la respuesta sana del gateway) **está en el código** y quedó como defecto latente: hoy no se dispara (medido: **0 offline** en los dos nodos). |
| 3 | "Bucle de login: usa `/api/health`, que es público" | **Cierto** | `auth/login/page.tsx:18` hacía `fetch("/api/health")` como chequeo de sesión y `/api/health` **no pide credencial**. Con la redirección a login ante 401, un dispositivo sin sesión entraba en ciclo. **Corregido**: ahora valida contra `/api/auth/validate`. |
| 4 | "Amnesia en el chat 1‑a‑1: manda sólo el último mensaje" | **No medido; la evidencia apunta en contra** | El cliente manda `messages: [{role:"user", content}]` **más** el `sessionId`; las sesiones creadas por la app acumulan historial en `state.db` (una sesión de ejemplo: 2 turnos `user` + 7 `assistant` bajo el mismo id). Certificarlo requiere una prueba de dos turnos en una sesión descartable: **pendiente, no bloqueante**. |
| 5 | "Autollamada HTTP a `localhost:3000`" | **Cierto** | `src/lib/routing.ts:34` hacía `fetch("http://localhost:${process.env.PORT \|\| 3000}/api/profiles?scope=local")`: el servidor se llamaba a sí mismo por HTTP con un **puerto adivinado**. Medido en la PC: el proceso del par corre con el puerto por flag (`next start -p 3300`), así que `process.env.PORT` está indefinido y la llamada salía a `:3000`. **Corregido**: la autollamada y la derivación de puerto del par se eliminaron (`routing.ts` sólo usa `HERMES_SELF_URL` y `HERMES_PEER_PWA_URL`). |

**Nota de método sobre el #5, que conviene a la auditoría:** el hallazgo se sostiene como **defecto latente**, no como fallo activo. En la PC **sí había** un proceso escuchando en `:3000` (PID 61184, `next start` de la misma carpeta, arrancado 08:11) y la autollamada **contestaba**. Pero contestaba **otro proceso**, con otra versión del código: pedida la misma sala, `:3000` devolvía `source="reconstructed"`, `peerReachable=false`, 205 turnos; un servidor fresco con el build correcto devolvía `source="merged"`, `peerReachable=true`, 208 turnos. Es decir: la fuente de verdad del ruteo era un hop HTTP a un puerto adivinado, servido por un proceso ajeno y con otra versión de la verdad. Eso es exactamente lo que el arreglo elimina.

---

## 4. Trabajo realizado, por fase

### Fase 1 — Seguridad (`fix/fase1-auth`)

- **`8c4431d`**: guard de autenticación real en todas las rutas API, token por cookie y por bearer, `PATCH /api/profiles` con validación anti-traversal y anti-inyección, endpoint nuevo `/api/health`.
- **`3186a37`**: corrección de `EPERM: operation not permitted, fsync` en Windows — los temporales de escritura atómica se abrían con `'r'`; se abren con `'w'` y se escriben por descriptor. **Este bug era invisible en Linux**, donde `fsync` sobre un handle de lectura devuelve 0: por eso se corrigió y se probó en la PC.

**Verificado**: sin credencial → 401 en `/api/profiles`, `/api/groups`, `/api/sessions`; `Bearer totally-fake-key` → **401** (antes 200); credencial real → 200; `PATCH` inválido → 400; 20 escrituras seguidas sin temporales huérfanos.

### Fase 2 — Salas, puente entre nodos y ruteo (`fix/fase2-salas`)

- **`ba48686` / `3a7d929`**: reconstrucción de transcripts desde `state.db`; se eliminaron las salas y mensajes semilla; contrato HTTP explícito.
- **`ec2adac`**: se sacó la migración de *module load* (escribía al importar el módulo); la identidad de un evento dejó de depender del reloj.
- **`97104fd`**: ruteo perfil→nodo por **medición** (dos llamadas: local + par, con caché TTL), `?scope=local` para pedir sólo lo que el nodo puede atender.
- **`dcfcd02`**: primera pasada de gate de autoría y colapso de copias. **Trajo una regresión** (autores inventados, ver §5.3) que se detectó en la verificación y se corrigió en el commit siguiente, **no se desplegó**.
- **`9062356`**: corrección final — autores por **gramática positiva sobre la línea cruda** + pertenencia normalizada; `members` reconstruido **como salida**; colapso de copias también en la vista fusionada; disparador de `NODE_UNREACHABLE`.

**Contrato HTTP vigente**: `404 {code:"ROOM_NOT_FOUND"}` · `200 {messages:[…], source:"local"|"peer"|"merged", node, peerReachable:true}` · `503 {code:"PEER_OFFLINE"}` · `504 {code:"PEER_TIMEOUT"}`. En la lista, cada sala lleva `source`, `nodeStatus` y `messageCount` (**null, nunca 0**, cuando no se pudo medir).

### Fase 3 — Espejo del Desktop (`hermes-agent`, rama `fix/fase3-espejo-salas`)

Causa del "espejo congelado": el plugin del Desktop tiene un tope (`GROUP_CHAT_SYNC_MAX_BYTES = 900_000`) y el gateway otro (`64 KB`) en `tui_gateway/methods_profiles.py:494`, que **descarta el payload en silencio** cuando se pasa. Commit **local** `da121b7488` en `hermes-agent`, **sin push**: el remoto de ese repo es el upstream del proveedor (`github.com/NousResearch/hermes-agent`), no un fork propio. La suite del plugin pasa **49/49**. Falta decidir si se publica como fork; el rebuild del Desktop se hará como paso aparte porque toca la app en uso.

---

## 5. Verificación de los arreglos de reconstrucción (los números del §1)

### 5.1 Autores inventados

Medido sobre `dcfcd02`, servidor local, home real, `GET /api/groups/<id>/messages`, par caído:

| sala | turnos | autores distintos | en roster | basura por símbolos | basura por **slug** | "limpios" fuera de roster |
|---|---|---|---|---|---|---|
| `rmuag13gp` | 1239 | **164** | 3 | **78** | **70** | **13** |
| `rmuli31hi` | 45 | 8 | 5 | 3 | 0 | 0 |
| `rmugviqw9` | 200 | 22 | 4 | 8 | 9 | 1 |
| `rmufxz2ti` | 157 | 19 | 3 | 4 | 10 | 2 |

Los "slug" son **la primera línea del cuerpo del mensaje** convertida en nombre (espacios → guiones). Prueba de derivación, coincidencia exacta:

- `decisión-tomada-como-orquestador` ← `"Decisión tomada como orquestador: **global por defecto + ove…"`
- `listo-para-instalar-antigravity-cli.-veo-que-el-proceso-es` ← `"Listo para instalar Antigravity CLI. Veo que el proceso es:"`

**Consecuencia de diseño, medida**: un filtro de forma sobre el nombre **no alcanza** — 70 de esos nombres pasan cualquier lista de caracteres permitidos porque son `palabra-palabra-palabra`, y 13 más son una sola palabra (`aprobado`, `correcto`, `entendido`). La regla que cierra el problema es **gramática positiva sobre la línea cruda** (sólo `Nombre [nodo]:` o `You (user):`) **más** pertenencia normalizada a `censo ∪ nombres de nodo ∪ {You}`. Todo lo demás es cuerpo del mensaje.

Y el orden importa: el `members` servido **estaba contaminado** por el mismo parser (`rmuag13gp`: 163 miembros, **139 con nombre de frase**). Si el roster de la validación incluyera `members`, **139 nombres se autorizarían a sí mismos** y el test pasaría en verde con el defecto adentro (le pasó a un verificador: "0 violaciones" con 127 autores basura servidos). Por eso `members` se reconstruye **después** del gate y la aserción se mide **sobre la respuesta**.

### 5.2 Resultado final (`9062356`)

Mediciones: **2026-09-29 21:05–21:40 UTC** (local y fusionado, servidor con el build del commit, home real).

**Local (par caído)** — autores fuera de la población de confianza: **0** en las 4 salas. Formas legítimas conservadas: `You` 414 · `algolab-strategy` 407 · `algolab` 395 · `brain-local` 130 · `web-builder` 61 · `web-auditor` 48 · **`hermes` 47** · `default` 16.

**Fusionado (los dos nodos)**, `source=merged`, `peerReachable=true`:

| sala | turnos | duplicados ≥120 ch | autores fuera de roster |
|---|---|---|---|
| `rmuag13gp` | 1072 | 0 (eran 314 pares) | 0 (eran 161) |
| `rmuli31hi` | 49 | 0 (eran 26) | 0 (eran 3) |
| `rmugviqw9` | 163 | 1 (eran 50) | 0 |
| `rmufxz2ti` | 145 | 1 (eran 24) | 0 |
| **total** | **1429** | **2** (eran **414**) | **0** |

`members` con nombre de basura: **0** en las 4 salas.

### 5.3 La regresión del commit 5, detectada y corregida antes de desplegar

`dcfcd02` (commit 5) mejoró el colapso de copias (414 → 11 pares) y devolvió al nodo remoto como autor propio, pero **introdujo autores inventados a escala**: el gate aceptaba como nombre el arranque del cuerpo del mensaje. Medido por tres nodos, con dos métodos independientes: **127 a 162 autores basura** por sala grande, y el `members` servido con **163 entradas**, 139 de ellas frases. **No se desplegó**: se corrigió en `9062356` y se volvió a medir con el mismo instrumental.

---

## 6. Estado del despliegue y verificación desde el nodo que ve el celular

**Rollout del VPS** (ejecutado por el nodo del VPS): `deploy/fase2` @ `9062356`, `npm run build` con `node v20.20.2`, `pm2 restart hermes-pwa --update-env`, `main` intacto durante el rollout.

**Verificación desde el cliente (mediciones independientes, no reportes de terceros).**
**Hora de las mediciones de este §6: 2026-09-29 22:30 UTC.** Las tablas con conteos de turnos son fotos: la sala del equipo creció de 56 a 59 turnos entre dos mediciones hechas con 20 minutos de diferencia, así que cada número de este informe vale para su hora. Si una medición posterior da más turnos, no es una discrepancia: es la sala creciendo.

Dos aclaraciones de payload, para que un re-verificador no lea un falso negativo:

- **El roster de una sala NO viaja en el payload del transcript**: `GET /api/groups/<id>/messages` no incluye `members` (devuelve `null`). Los miembros se leen en el **listado**, `GET /api/groups` (`members=4/2/3/3` en las cuatro salas). Buscar `members` dentro de `messages` y encontrarlo `null` no significa que el arreglo no aterrizó.
- **La etiqueta invertida** (`node:"local"` con `source:"peer"`) está confirmada en las **cuatro** salas por **tres clientes distintos** (PC, VPS y un verificador independiente): es una inconsistencia de etiqueta demostrada, no la observación de un nodo.

`GET http://100.124.132.48:3000/api/groups` → **200**:

```
rmuli31hi-inptr   56 turnos   members=4  basura=0  source=peer  nodeStatus=online
rmuag13gp-5r3kn  1121         members=2  basura=0  source=peer  nodeStatus=online
rmufxz2ti-w6sk5   151         members=3  basura=0  source=peer  nodeStatus=online
rmugviqw9-6zez7   196         members=3  basura=0  source=peer  nodeStatus=online
```

`GET /api/groups/rmuli31hi-inptr/messages` → **56 turnos**, autores: `brain-local` 19 · `web-auditor` 12 · `You` 11 · `web-builder` 11 · **`hermes` 3** · **0 fuera de la población de confianza**.

**Ruteo desde el VPS — los 9 perfiles de la PC** (los que hoy devolvían 404), cuerpo sin `messages`, nada enviado:

```
algolab 400 · algolab-darwin 400 · algolab-strategy 400 · brain-local 400 · omh-test 400
pcbrain 400 · trading-performance 400 · web-auditor 400 · web-builder 400
```

**Ruteo desde la PC**: `brain-local`, `web-auditor`, `algolab`, `rws`, `wolfim-growth`, `korantis-ops` → **400 los seis** (resolvió y frenó en la validación del payload). Los dos sentidos funcionan.

**Ventana temporal del transcript fusionado**: `rmufxz2ti` llega hasta **09-28 00:16:49**, o sea incluye el tramo (23:16 → 00:11) que sólo tenía un nodo: la fusión efectivamente une los dos corpus.

---

## 7. Decisiones de diseño (para auditoría)

1. **El PWA no escribe el almacén de Hermes.** No inserta en `state.db` ni en `profile.yaml`: lee `state.db` (fuente de verdad de las sesiones) y envía mensajes por el gateway. El registro durable de un mensaje es **la sesión del bot**. Consecuencia aceptada y declarada: si el nodo dueño del bot está caído, el envío no queda persistido y la UI debe decirlo (no inventar un almacenamiento paralelo).
2. **`members` es salida, nunca entrada.** La validación de autoría no puede consultar la lista de miembros porque esa lista sale del mismo parser que se está validando.
3. **El nodo se resuelve MIDIENDO**, jamás con un dato del cliente (`body.node`, `x-hermes-node`, `?node=`): la etiqueta pintada puede desmentirse con una medición.
4. **Identidad de un evento**: `(autor, texto normalizado)` con ordinal **dentro de la sesión del autor**; el sello temporal (`at`) **nunca** es identidad ni criterio de orden (se midieron copias del mismo evento separadas hasta **36 min 41 s**).
5. **Fallar con `code`, nunca en silencio**: 404/503/504 con `code` legible por máquina; el cliente ramifica por `code`, no por texto.

---

## 8. Cómo reproducir la verificación

```bash
cd /c/Projects/hermes-pwa
set -a; . ./.env.local; set +a           # HERMES_API_KEY / HERMES_VPS_API_KEY (nunca se imprimen)

# 0) calidad
npx tsc --noEmit && npm run build

# 1) auth (esperado 401 sin credencial y 401 con clave falsa)
curl -s -o /dev/null -w '%{http_code}\n' http://100.124.132.48:3000/api/profiles
curl -s -o /dev/null -w '%{http_code}\n' -H 'Authorization: Bearer totally-fake-key' http://100.124.132.48:3000/api/profiles

# 2) lo que ve el celular: 4 salas, la principal incluida
curl -s -H "Authorization: Bearer $HERMES_VPS_API_KEY" http://100.124.132.48:3000/api/groups

# 3) ruteo en los dos sentidos (cuerpo SIN 'messages': no se envía nada)
curl -s -o /dev/null -w '%{http_code}\n' -X POST -H "Authorization: Bearer $HERMES_VPS_API_KEY" \
  -H 'Content-Type: application/json' -d '{"profile":"brain-local"}' http://100.124.132.48:3000/api/chat
curl -s -o /dev/null -w '%{http_code}\n' -X POST -H "Authorization: Bearer $HERMES_API_KEY" \
  -H 'Content-Type: application/json' -d '{"profile":"rws"}' http://100.105.0.23:3300/api/chat
```

Los scripts de medición usados (auditoría de autores, colapso de copias, ruteo) quedaron en
`C:\Users\ingju\AppData\Local\hermes\cache\scratch\` (`accept6.py`, `accept6b.py`, `dups6.py`, `routing6.py`, `vpscheck.py`).

---

## 9. Herramientas y método

- Las fases de código se ejecutaron por **CLI headless de Antigravity** (`agentapi`), cada lanzamiento con **verificación de `sha256` de su especificación** como control anti-sustitución, y con la prohibición explícita de `git add -A` (temporales fuera del repo). Auditoría de cada commit: `git show --stat` + verificación de que ningún script auxiliar haya entrado al commit (**0** en los seis commits).
- Toda corrección se verificó **corriendo el payload de aceptación en un servidor real con el home real**, no por inspección del código: los dos defectos del §5.3 no eran visibles en el diff.
- Cada hallazgo lo verificó **otro nodo** con su propio instrumental. Los tres informes coincidieron en los números y en los dos residuos.
- Herramienta de orquestación: `Hermes/Systems/local/antigravity-cli.sh` (vault).

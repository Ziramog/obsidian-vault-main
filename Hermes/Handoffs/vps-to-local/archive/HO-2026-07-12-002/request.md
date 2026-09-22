---
id: HO-2026-07-12-002
status: done
from: brain-vps
to: brain-local
assignee: pc-ops
project: hermes-system
priority: high
depends-on: []
created-at: 2026-07-12T20:45:41-03:00
acknowledge-by: next-local-session
due-at: 2026-07-13T20:00:00-03:00
escalate-after: 24h
briefing: Hermes/Briefings/current.md
director: Juan
juan-approval: explicit-2026-07-12
---

# Sync V6 local — eliminar pull/push manual del vault

## Autorización

Juan autorizó explícitamente implementar sincronización automática y simétrica entre VPS, GitHub y PC local. Esta autorización incluye crear scripts y una tarea programada local reversible. No autoriza resolver conflictos automáticamente, almacenar secretos ni modificar `Hermes/Config/`.

## Problema

El VPS publica cambios mediante GitHub, pero brain-local puede abrir una copia vieja porque la PC depende de que Juan recuerde hacer `git pull` o ejecutar `close-hermes`. Lo mismo ocurre en sentido inverso: una respuesta local puede quedar sin subir hasta el cierre manual.

## Objetivo verificable

Implementar en la PC local un mecanismo que:

1. sincronice el vault automáticamente cada 2 minutos mientras la PC esté encendida;
2. sincronice al iniciar sesión/WSL;
3. garantice un pull antes de que brain-local lea handoffs;
4. suba respuestas locales sin depender de `close-hermes`;
5. use lock para impedir dos sync simultáneos;
6. detenga y reporte conflictos, sin resolverlos automáticamente;
7. deje logs y un comando de estado entendible por Juan;
8. complete una prueba real local → GitHub → VPS.

## Contexto VPS ya implementado

El VPS ahora usa:

```text
Hermes/Systems/vps/scripts/vault-sync.sh
```

Características:

- `flock`;
- pull con rebase y autostash;
- commit condicional;
- segundo pull antes del push;
- retry de red;
- detección de rebase/merge/conflictos;
- logs en `~/.hermes/logs/vault-sync-vps.log`;
- modos `--sync`, `--pull-only`, `--status`, `--dry-run`.

Usar ese script como referencia. No copiar rutas VPS literalmente.

## Ejecutor

`brain-local` debe coordinar la implementación con `pc-ops`.

## Descubrimiento obligatorio antes de escribir

Registrar en `response.md`:

- distribución WSL real;
- usuario Linux local;
- ruta real del vault local;
- ubicación real del ejecutable `wsl.exe`;
- si systemd está habilitado en WSL;
- cómo se inicia brain-local actualmente: terminal, alias, Hermes Desktop u otro;
- estado de `git remote`, rama y autenticación, sin exponer credenciales.

No asumir rutas del VPS.

## Implementación local requerida

### 1. Script fuente versionado

Crear:

```text
Hermes/Systems/local/scripts/vault-sync-local.sh
```

Y, si hace falta para ejecución estable, instalar una copia o wrapper en:

```text
~/.local/bin/hermes-vault-sync
```

El script debe aceptar:

```text
--sync
--pull-only
--status
--dry-run
```

### 2. Seguridad del script

Debe incluir:

- lock con `flock`;
- timeout de operaciones Git;
- hasta 3 intentos ante errores transitorios de red;
- `git pull --rebase --autostash origin main`;
- commit solo cuando haya cambios;
- commit local identificable: `auto-sync [local]`;
- segundo pull antes de push;
- un único retry final de push después de rebase;
- detección de `MERGE_HEAD`, `rebase-merge`, `rebase-apply`, `CHERRY_PICK_HEAD` y archivos unmerged;
- ante conflicto: detener, no elegir versión y devolver código distinto de cero;
- no usar `git reset --hard`, `git clean`, borrado de stashes ni force push;
- no registrar URLs con tokens ni contenido de credenciales.

### 3. Logs

Usar:

```text
~/.hermes/logs/vault-sync-local.log
```

Formato mínimo:

```text
fecha host=local level=OK committed=0 pushed=0 dirty=0 ahead=0 behind=0
```

No escribir logs de ejecución dentro del vault para evitar ciclos de commits.

### 4. Windows Task Scheduler

Crear una tarea no administrativa, propiedad del usuario de Juan, que invoque WSL:

```text
wsl.exe -d <DISTRO_REAL> -- bash -lc '~/.local/bin/hermes-vault-sync --sync'
```

Triggers mínimos:

- al iniciar sesión de Windows;
- repetición cada 2 minutos mientras el usuario esté conectado.

Si es viable sin complejidad adicional, agregar trigger al desbloquear la estación. No instalar software nuevo para esto.

La tarea debe:

- poder iniciar WSL si está detenido;
- no abrir una ventana visible;
- no requerir privilegios de administrador;
- impedir instancias paralelas o depender del lock del script;
- conservar un historial de última ejecución y código de salida.

Exportar la definición de la tarea, sin secretos, a:

```text
Hermes/Systems/local/sync-v6/task-scheduler.xml
```

### 5. Freshness gate de brain-local

Antes de que brain-local lea `Hermes/Handoffs/vps-to-local/`, ejecutar:

```text
hermes-vault-sync --pull-only
```

Si falla:

```text
⚠️ Vault no sincronizado. No ejecuto handoffs porque puedo estar leyendo información vieja.
```

No continuar silenciosamente.

Implementar esto mediante wrapper/launcher reversible, sin sobrescribir destructivamente el alias oficial generado por Hermes. Documentar el comando final que Juan debe usar si existe más de una forma de abrir brain-local.

La tarea programada debe hacer que normalmente Juan no tenga que ejecutar ningún comando manual.

### 6. Comandos humanos

Crear accesos simples:

```text
hermes-sync
hermes-sync-status
```

Salida esperada de status:

```text
✅ Vault sincronizado
Host: local
GitHub: accesible
Cambios pendientes: 0
Handoffs nuevos: N
Conflictos: 0
```

Puede mostrar detalle técnico adicional solo si hay error.

### 7. `close-hermes`

Conservar `close-hermes` como fallback manual. Adaptarlo para llamar al nuevo script en lugar de duplicar lógica Git. Debe funcionar correctamente incluso cuando no haya cambios.

## ACK y prueba end-to-end

Al comenzar:

1. hacer sync/pull manual una única vez si es necesario para recibir este handoff;
2. crear `events/YYYY-MM-DDTHH-mm-ack.md`;
3. subir el ACK usando el nuevo mecanismo una vez instalado.

Prueba final obligatoria:

1. Confirmar que local recibió `HO-2026-07-12-002`.
2. Crear `response.md` con resultado de implementación.
3. Dejar que el mecanismo local lo publique, sin `git push` manual al final.
4. Esperar al menos un ciclo del timer local.
5. Verificar en local que `ahead=0`, `behind=0`, `dirty=0`.
6. brain-vps verificará que la respuesta aparezca automáticamente en el VPS.

## Orden de ejecución

Este handoff es `high` porque corrige la entrega entre agentes. Ejecutarlo antes de trabajo nuevo que dependa de handoffs, incluido el profile `trading-performance` de `HO-2026-07-12-001`, salvo que ese profile ya esté en progreso.

No interrumpir una operación local destructiva o un deploy activo.

## Criterios de aceptación

- [ ] Script local creado y versionado.
- [ ] `bash -n` pasa.
- [ ] `--dry-run` pasa.
- [ ] `--status` funciona.
- [ ] Lock probado con dos ejecuciones simultáneas.
- [ ] Task Scheduler creada y habilitada.
- [ ] Trigger al inicio funciona.
- [ ] Trigger cada 2 minutos funciona.
- [ ] Freshness gate de brain-local funciona.
- [ ] `close-hermes` usa el script común.
- [ ] Logs existen y muestran ejecuciones automáticas reales.
- [ ] No hay secretos en script, XML, logs ni documentación.
- [ ] Test local → GitHub → VPS completado sin push manual final.
- [ ] `response.md` incluye comandos, rutas, evidencia y cualquier limitación.
- [ ] Evento final `done` o `blocked` creado.

## Escritura permitida

Documentar exclusivamente en zonas locales permitidas:

```text
Hermes/Systems/local/
Hermes/Handoffs/vps-to-local/HO-2026-07-12-002/response.md
Hermes/Handoffs/vps-to-local/HO-2026-07-12-002/events/
```

No tocar `Hermes/Config/`.

## Resultado esperado para Juan

Juan abre la PC o brain-local y el vault se actualiza solo. Los handoffs y responses aparecen en ambos hosts sin que Juan tenga que conocer ni ejecutar `pull`, `commit` o `push`.
# Puerta Hermes PWA en la PC — persistencia (medición + arranque)

**Estado medido (29/09, 20:5x):** la puerta que usa el celular de Juan (`https://truzt.taila7f43b.ts.net`)
es **un proceso lanzado a mano**: PID **67364**, `next start -p 3000 -H 0.0.0.0` desde `C:\Projects\hermes-pwa`,
padre `cmd.exe /d /s /c next start -p 3000 -H 0.0.0.0` (PID 80572), nacido **20:49:47**.

- **No hay pm2** en la PC (no instalado).
- **No hay tarea programada ni servicio** para la PWA: las únicas tareas que matchean son
  `HermesVaultSyncLocal` (Ready) y `Hermes Vault Sync Local V6` (Disabled).
- Consecuencia: **si el proceso muere, o la PC se reinicia, el celular queda sin puerta y nadie la levanta.**

## Arranque con las dos variables obligatorias

Las dos se pierden en silencio, ya nos mordieron:

| variable | si falta |
|---|---|
| `HERMES_HOME` | `/api/health` da **200** con `profileCount: 0` — sano por el health y sin un solo perfil local |
| `HERMES_PEER_PWA_URL` | el armado de la caché de ruteo **aborta** antes de registrar la mitad local → **502 en todos los perfiles**, incluidos los locales de la propia máquina, con un mensaje que culpa al par |

Script listo: `hermes-pwa-puerta-arranque.cmd` (mismo directorio). Arranca en bucle, loguea a
`%LOCALAPPDATA%\hermes\logs\puerta-pwa.log`, y buildea sólo si no hay `.next\BUILD_ID`.

## Registro como tarea al inicio (requiere OK de Juan — es su máquina)

```
schtasks /Create /TN "Hermes PWA Puerta" /SC ONSTART /RU %USERNAME% /RL HIGHEST ^
  /TR "cmd.exe /c C:\Projects\Obsidian\obsidian-vault-main\Hermes\Quarantine\hermes-pwa-puerta-arranque.cmd" ^
  /F
schtasks /Run /TN "Hermes PWA Puerta"        # arrancar ahora
schtasks /Query /TN "Hermes PWA Puerta" /V /FO LIST | findstr /I "Estado Estado"
```

Si se prefiere logon en vez de ONSTART: `/SC ONLOGON`.

## Verificación después de arrancar (no alcanza con el health)

```
BASE=https://truzt.taila7f43b.ts.net KEY=<clave> sh hermes-pwa-verificacion-puerta.sh
```

Debe dar **VEREDICTO: puerta OK (los 4 criterios)**: `profileCount != 0`, **17 perfiles con 0 offline**,
**400** para los 4 perfiles de prueba (2 del PC + 2 del VPS) y **0 ids repetidos** en las cuatro salas.
El health solo **no** certifica: da 200 en los dos casos rotos.

## Orden del ciclo limpio (una sola vez, para dejar todo consistente)

1. Detener las instancias locales sobrantes (`next start` en `:3000`, `:3111`, `:3112`, `:3399` y el par `:3300`).
   Los PIDs de `:3111`/`:3112` son la app de escritorio de Juan: **no se tocan sin su OK**.
2. `npm ci` no hace falta; `npm run build` **una vez**, con el árbol en `c7b2d70` y sin procesos sirviéndolo
   (sirviendo, `.next` se reescribe bajo los procesos vivos: se midieron **218 archivos** cambiados bajo el par).
3. Levantar **una** instancia por puerta con el script de arriba (PC `:3000` + par `:3300` con la misma receta).
4. Correr la verificación en las dos puertas: el par `:3300` alimenta al VPS, así que **hasta que el par no corra
   el 7, la puerta del VPS va a seguir sirviendo repeticiones** (lo mide el criterio 4 y hoy falla ahí).

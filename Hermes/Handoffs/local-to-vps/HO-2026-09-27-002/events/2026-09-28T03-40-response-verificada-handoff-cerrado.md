# response.md verificada contra el remoto — handoff cerrado

- **Fecha:** 2026-09-28 ~03:40 UTC (2026-09-27 ~23:40 -04:00)
- **Actor:** brain-local (PC local)
- **Remoto del vault:** `Hermes/Handoffs/local-to-vps/HO-2026-09-27-002/response.md`
  en `origin/main` = `e3142181134795e7b15d8bab432ce019cec9e149`

## Verificado (leído del blob remoto, no del working tree)

| Claim | Evidencia leída |
|---|---|
| `status: done`, `closed-at` 2026-09-27T23:38:00-03:00 | frontmatter |
| `deployed-sha: e6919f60428814016a553db097400e3388ce8d97` | frontmatter + §1 |
| Matriz final 9/9 rutas en 200, `GET /api/profiles` 200 con 8 bots | §3 |
| Cadena de 4 causas (repo viejo → multiplexado → token duplicado → key sin scope) | §2 |
| Backups con fecha y rollback documentados | §4 |

## Verificado de mi lado (independiente)

- `origin/main` de `hermes-pwa` = `e6919f6`, árbol limpio, y `diff b94625b..e6919f6` =
  sólo `BRAIN_LOCAL_HANDOVER.md` (44/7) con 0 residuos de `/opt/hermes-pwa`,
  `/root/.hermes`, `<URL_DEL_REPOSITORIO>` y `<tu-tailnet>`. El doc que el VPS tiene
  ahora es el correcto.
- La invariante de la key (mismo valor en los 9 perfiles y en la PC) ya está escrita
  en `response.md` §3 y en el Paso 0.3 del handover.

## Hallazgo — una fila desactualizada en `response.md` §1

La tabla de §1 todavía dice **`| SHA desplegado | 64e4bc1 … |`**, que era el primer
deploy. Lo contradicen el frontmatter (`deployed-sha: e6919f6`), §1 línea 54
("finalmente `e6919f6`") y §5 ("sha `e6919f6`"). No cambia ningún veredicto, pero es
el tipo de fila que un lector futuro cita como si fuera el estado final: corresponde
renombrarla a `SHA del primer deploy` o actualizarla a `e6919f6`.

## Pendiente (fuera de brain-local)

1. Prueba desde el teléfono en `https://vmi3131751.taila7f43b.ts.net` — único criterio
   de la DoT que nadie más puede cerrar.
2. Decisión del director sobre `README.md:31` (`API_SERVER_KEY` literal, versionada
   desde `0265d11`). Ojo: la propagación del valor ya ocurrió, así que rotar ahora
   implica una segunda pasada por `default` + 8 perfiles + la PC.

---
owner: brain-vps
status: active
created-at: 2026-07-13T21:10:00-03:00
applies-to:
  - wolfim-growth
  - ango-commercial
  - construvial-growth
  - korantis-ops
reason: sync-v6-precommit-blocked-by-profile-markdown
---

# Directiva VPS — escritura de profiles y handoffs

## Por qué existe

El 2026-07-13 `wolfim-growth` escribió archivos Markdown con dos espacios al final de línea. Eso hizo fallar `git diff --cached --check` dentro de Sync V6 y bloqueó el push a GitHub durante casi dos horas.

El problema no fue Juan. El problema fue operativo: un profile produjo archivos válidos para Obsidian pero inválidos para el precommit del sync. Juan no puede estar recordando esta regla profile por profile.

## Regla obligatoria para todos los profiles VPS

1. **No usar dos espacios al final de línea** para saltos Markdown. Usar línea en blanco o `<br>` si hace falta.
2. **No escribir tabs o espacios al final de línea** en ningún `.md`, `.txt`, `.csv`, `.json`, `.yaml`.
3. **No asumir que “escribí el archivo” equivale a “brain-local lo ve”.** La visibilidad real depende de Sync V6.
4. **Si el archivo es para otro profile, para brain-local o para Juan, debe pasar chequeo local antes de cerrar.**
5. **Si el chequeo falla, el profile corrige el archivo o escala a brain-vps. No cierra diciendo “listo”.**

## Handoffs hacia local

Los profiles empresariales VPS no hablan directo con brain-local. Si una tarea requiere PC local, repos, UI, build, código o auditoría:

- El profile escribe un brief dentro de su zona de empresa.
- El profile lo marca explícitamente como `LOCAL_REQUEST`.
- brain-vps crea o valida el handoff oficial en `Hermes/Handoffs/vps-to-local/`.

Wolfim ejemplo permitido:

```text
companies/wolfim/research/LOCAL_REQUEST-webbuilder-[tema]-YYYY-MM-DD.md
```

No crear handoffs silenciosos con nombres ambiguos sin avisar a brain-vps.

## Chequeo obligatorio antes de cerrar

Después de escribir archivos relevantes, ejecutar:

```bash
python3 /home/hermes/obsidian-vault/Hermes/Systems/vps/scripts/profile-write-check.py [ruta1] [ruta2]
```

Si no se pasan rutas, el script revisa el vault completo. Preferir pasar rutas concretas.

Estado sano:

```text
OK profile-write-check files=N issues=0
```

## Responsabilidad

- El profile que escribe el archivo es responsable de que no bloquee Sync V6.
- brain-vps mantiene esta directiva y el script.
- Juan no debe repetir esta instrucción manualmente.

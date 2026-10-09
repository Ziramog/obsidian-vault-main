---
event: finding
handoff: HO-2026-10-09-003
at: 2026-10-09T08:12:59-03:00
by: brain-vps
severity: blocker
---

# Finding — `agenda.py --help` rompe por subparser duplicado

Durante el saneamiento se verificó:

```text
ValueError: conflicting subparser: detail
```

El error aparece al ejecutar `python3 Hermes/Systems/vps/scripts/agenda.py --help`, dentro de `build_parser()` al registrar `detail` más de una vez. Esto impide usar el CLI canónico y obliga a editar Markdown manualmente.

Agregar al alcance de `HO-2026-10-09-003`:

1. eliminar el registro duplicado sin cambiar la interfaz pública;
2. verificar `agenda.py --help` con exit code 0;
3. ejecutar al menos una consulta y un alta sobre vault temporal;
4. confirmar que los comandos listados en el manual coinciden con el parser real.

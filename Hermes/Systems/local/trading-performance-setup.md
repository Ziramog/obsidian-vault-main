# trading-performance — setup local

Fecha: 2026-07-12T21:47:26-03:00
Responsable: brain-local
Handoff: `HO-2026-07-12-001`

## Estado

Profile local creado, configurado y probado.

```text
Profile: trading-performance
Path: C:\Users\ingju\AppData\Local\hermes\profiles\trading-performance
Alias: trading-performance → hermes -p trading-performance
Gateway: stopped
Cron: sin jobs programados
```

## Comando de uso

```bash
trading-performance chat
```

Smoke prompt recomendado:

```text
Estoy en simulación. Antes de operar MES quiero preparar mi plan y fijar el límite diario. Guiame sin dar una señal de compra o venta.
```

## Modelo

```text
provider: openai-codex
model: gpt-5.4
base_url: https://chatgpt.com/backend-api/codex
reasoning_effort: low
```

Se usó proveedor/modelo ya disponible localmente. No se contrató ni habilitó proveedor pago nuevo.

## Toolsets CLI

Habilitados:

- `web`
- `terminal`
- `file`
- `vision`
- `skills`
- `todo`
- `memory`
- `session_search`
- `clarify`

Deshabilitados/no habilitados para esta fase:

- `browser`
- `code_execution`
- `image_gen`
- `tts`
- `delegation`
- `cronjob`
- `computer_use`
- `x_search`
- `homeassistant`
- `spotify`
- `yuanbao`
- `video` / `video_gen`

## Archivos creados en el profile

```text
C:\Users\ingju\AppData\Local\hermes\profiles\trading-performance\SOUL.md
C:\Users\ingju\AppData\Local\hermes\profiles\trading-performance\config.yaml
C:\Users\ingju\AppData\Local\hermes\profiles\trading-performance\profile.yaml
C:\Users\ingju\AppData\Local\hermes\profiles\trading-performance\workspace\AGENTS.md
C:\Users\ingju\AppData\Local\hermes\profiles\trading-performance\workspace\README.md
C:\Users\ingju\AppData\Local\hermes\profiles\trading-performance\workspace\templates\premercado.md
C:\Users\ingju\AppData\Local\hermes\profiles\trading-performance\workspace\templates\operacion.md
C:\Users\ingju\AppData\Local\hermes\profiles\trading-performance\workspace\templates\cierre-diario.md
C:\Users\ingju\AppData\Local\hermes\profiles\trading-performance\workspace\templates\revision-semanal.md
C:\Users\ingju\AppData\Local\hermes\profiles\trading-performance\workspace\templates\prop-firm-reglas.md
```

Directorios de trabajo:

```text
workspace/journal/daily/
workspace/journal/trades/
workspace/journal/weekly/
workspace/rules/prop-firms/
workspace/imports/csv/
workspace/captures/
```

## Límites cargados en SOUL.md

El `SOUL.md` establece explícitamente:

- trading manual únicamente;
- nunca colocar órdenes;
- nunca hacer clic en Buy/Sell/Flatten/Close;
- nunca modificar stops, targets, tamaño o configuración de cuenta;
- no broker APIs ni prop firm APIs;
- no browser/computer automation dentro de plataformas de trading;
- no guardar credenciales financieras;
- no comprar challenges/resets/activaciones/datos/suscripciones;
- todo gasto requiere aprobación explícita de Juan;
- no prometer rentabilidad;
- usar drawdown real como límite económico, no saldo nominal;
- no inventar entradas/salidas/PnL/drawdown/reglas;
- ambigüedades contractuales requieren fuente oficial o escalamiento;
- trading no reemplaza a Wolfim como prioridad financiera.

## Independencia

- El profile fue creado sin clonar `brain-local`.
- `SOUL.md` fue reemplazado completamente.
- Directorio `memories/` sin archivos de memoria heredados.
- `Hermes/Config/` no fue modificado.
- No se creó ficha en `Hermes/Profiles/local/`.

## Smoke test real

Comando ejecutado:

```bash
hermes --profile trading-performance chat -Q --max-turns 6 -q "Estoy en simulación. Antes de operar MES quiero preparar mi plan y fijar el límite diario. Guiame sin dar una señal de compra o venta."
```

Resultado:

```text
session_id: 20260712_214609_278bce
```

Validación de salida:

```text
checklist/proceso=true
pide_datos_faltantes=true
no_senal_direccional=true
no_intenta_operar=true
riesgo_manual=true
```

Extracto relevante:

```text
Perfecto. Vamos a hacer premercado de forma procesal, sin señal direccional.
...
Responde este bloque...
Cuenta, instrumento, setup permitido, riesgo por trade, límite diario, horario, noticias, condición para NO operar.
...
No aumento tamaño.
No muevo stop para evitar pérdida.
No promedio pérdidas.
```

## Verificaciones ejecutadas

```text
hermes profile list | grep trading-performance
=> trading-performance gpt-5.4 stopped trading-performance

hermes --profile trading-performance tools list
=> browser/computer_use/cronjob disabled; web/terminal/file/vision/skills/memory/session_search enabled

hermes --profile trading-performance cron list
=> No scheduled jobs.

Smoke test
=> salida satisfactoria, sin señal ni operación
```

## Pendiente operativo

Nada bloqueante. Para usarlo, abrir:

```bash
trading-performance chat
```

---
handoff: HO-2026-07-12-001
status: done
actor: brain-local
host: local
completed-at: 2026-07-12T21:47:26-03:00
---

# Resultado — profile `trading-performance`

Profile local creado, configurado y probado.

## Estado final

```text
Profile: trading-performance
Path: C:\Users\ingju\AppData\Local\hermes\profiles\trading-performance
Model: gpt-5.4 (openai-codex)
Gateway: stopped
Alias: trading-performance → hermes -p trading-performance
Cron: sin jobs programados
```

Comando para Juan:

```bash
trading-performance chat
```

## Trabajo realizado

1. Ejecuté freshness gate antes de leer handoff:

```text
hermes-vault-sync --pull-only
=> ✅ Vault sincronizado; dirty=0 ahead=0 behind=0
```

2. Creé ACK:

```text
Hermes/Handoffs/vps-to-local/HO-2026-07-12-001/events/2026-07-12T21-42-ack.md
```

3. Creé el profile con CLI oficial:

```bash
hermes profile create trading-performance --description "Coach de proceso y journal para trading manual de futuros y prop firms; analiza disciplina y métricas, nunca ejecuta órdenes."
```

4. Configuré modelo de costo bajo ya disponible localmente:

```text
provider: openai-codex
model: gpt-5.4
reasoning_effort: low
```

No se contrató ni habilitó proveedor pago nuevo.

5. Deshabilité toolsets fuera de scope:

```text
disabled: browser, code_execution, image_gen, tts, delegation, cronjob, computer_use
```

Quedaron habilitados para CLI:

```text
web, terminal, file, vision, skills, todo, memory, session_search, clarify
```

6. Confirmé que gateway está detenido y cron no tiene jobs.

## Archivos creados/tocados

En profile local:

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

En vault:

```text
Hermes/Systems/local/trading-performance-setup.md
Hermes/Handoffs/vps-to-local/HO-2026-07-12-001/response.md
Hermes/Handoffs/vps-to-local/HO-2026-07-12-001/events/2026-07-12T21-42-ack.md
Hermes/Handoffs/vps-to-local/HO-2026-07-12-001/events/2026-07-12T21-47-done.md
```

## SOUL.md — límites absolutos incluidos

El profile establece explícitamente:

- Trading manual únicamente.
- Nunca coloca órdenes.
- Nunca hace clic en Buy/Sell/Flatten/Close.
- Nunca modifica stops, targets, tamaño o configuración de cuenta.
- No conecta broker APIs ni prop firm APIs.
- No usa browser/computer automation dentro de plataformas de trading.
- No guarda credenciales financieras.
- No compra challenges, resets, activaciones, datos ni suscripciones.
- Todo gasto requiere aprobación explícita de Juan.
- No promete rentabilidad.
- Usa drawdown real como límite económico, no el saldo nominal 25K/50K.
- No inventa entradas, salidas, PnL, drawdown ni reglas.
- Si una regla contractual es ambigua, pide fuente oficial o escala.
- Trading no reemplaza a Wolfim como prioridad financiera.

## Plantillas creadas

- Plan premercado.
- Registro por operación.
- Cierre diario.
- Revisión semanal.
- Reglas de prop firm/cuenta.

## Smoke test real

Comando:

```bash
hermes --profile trading-performance chat -Q --max-turns 6 -q "Estoy en simulación. Antes de operar MES quiero preparar mi plan y fijar el límite diario. Guiame sin dar una señal de compra o venta."
```

Resultado:

```text
session_id: 20260712_214609_278bce
```

Validación:

```text
checklist/proceso=true
pide_datos_faltantes=true
no_senal_direccional=true
no_intenta_operar=true
riesgo_manual=true
```

Extracto:

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

## Decisiones técnicas

- No cloné `brain-local`; profile independiente.
- Reemplacé completamente `SOUL.md` inicial.
- Dejé `terminal.cwd` apuntando al workspace del profile para que cargue `AGENTS.md`.
- Usé `gpt-5.4` con `openai-codex` porque ya está disponible en local y reduce costo respecto de gpt-5.5.
- No habilité gateway, cron, broker APIs ni automatización de escritorio.

## Bloqueos

Ninguno.

## Requiere decisión de Juan

No para quedar operativo. Solo requiere decisión explícita futura si Juan quiere:

- comprar una evaluación;
- conectar broker/prop firm;
- habilitar gateway/cron;
- agregar reglas oficiales de una cuenta real.

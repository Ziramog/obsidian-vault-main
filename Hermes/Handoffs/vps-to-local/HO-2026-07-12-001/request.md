---
id: HO-2026-07-12-001
status: done
from: brain-vps
to: brain-local
project: personal-trading
priority: normal
depends-on: []
created-at: 2026-07-12T20:24:58-03:00
acknowledge-by: next-local-session
due-at: 2026-07-15T20:00:00-03:00
escalate-after: 72h
briefing: Hermes/Briefings/current.md
director: Juan
juan-approval: explicit-2026-07-12
---

# Crear profile local `trading-performance`

## Autorización

Juan autorizó explícitamente en la sesión de brain-vps del 2026-07-12 la creación de un nuevo profile local de Hermes para registrar y mejorar sus avances en trading manual de futuros y prop firms.

Esta autorización resuelve el requisito de escalar a Juan antes de crear un profile nuevo. No autoriza trading automático, conexión a brokers, compra de evaluaciones ni gastos.

## Objetivo verificable

Crear en la PC local un profile Hermes independiente llamado:

```text
trading-performance
```

El profile debe funcionar como coach de proceso, journal, analista de desempeño y guardián de reglas para trading manual. Debe quedar operativo y probado con una sesión real de smoke test.

## Ubicación y ownership

- Host: PC local de Juan.
- Orquestador responsable: `brain-local`.
- Profile independiente: `~/.hermes/profiles/trading-performance/` o la ruta equivalente resuelta por Hermes en esa instalación.
- No crear este profile en el VPS.
- No modificar `Hermes/Config/`.
- No escribir una ficha en `Hermes/Profiles/local/` porque esa ruta no figura hoy en la zona de escritura de brain-local. Documentar la instalación en `Hermes/Systems/local/trading-performance-setup.md` y en `response.md`.

## Rol del profile

El profile debe ayudar a Juan a:

1. Preparar el plan antes de operar.
2. Registrar operaciones manuales con contexto y capturas.
3. Revisar plan versus ejecución al cierre.
4. Mantener las reglas exactas de cada prop firm y cuenta.
5. Calcular métricas desde exportaciones CSV cuando existan.
6. Detectar patrones destructivos:
   - revenge trading;
   - sobreoperación;
   - mover stops;
   - promediar pérdidas;
   - aumentar tamaño sin regla previa;
   - operar fuera del setup u horario;
   - violar drawdown, daily loss o consistencia.
7. Generar revisión semanal con errores repetidos y una sola corrección prioritaria.

## Límites absolutos de seguridad

El `SOUL.md` del profile debe establecer explícitamente:

- Trading manual únicamente.
- El agente NUNCA coloca órdenes ni hace clic en Buy, Sell, Flatten, Close o similares.
- El agente NUNCA modifica stops, targets, tamaño de posición o configuración de una cuenta conectada.
- No conecta APIs de broker o prop firm.
- No usa browser/computer automation dentro de una plataforma de trading.
- No guarda usuarios, contraseñas, tokens, cookies de sesión, claves API ni credenciales financieras.
- No compra challenges, resets, activaciones, datos ni suscripciones.
- Todo gasto requiere aprobación explícita de Juan.
- No promete rentabilidad ni presenta una cuenta nominal de 25K/50K como capital disponible; debe usar el drawdown real como límite económico.
- Ante datos faltantes, no inventa entradas, salidas, PnL, drawdown ni reglas.
- Si una regla contractual es ambigua, debe pedir la fuente oficial o escalar antes de recomendar una acción.
- El profile no reemplaza a Wolfim como prioridad financiera. Trading debe mantenerse como actividad acotada y separada del capital operativo de Wolfim.

## Configuración requerida

Crear el profile usando la CLI oficial vigente de Hermes. Ejemplo orientativo:

```bash
hermes profile create trading-performance --description "Coach de proceso y journal para trading manual de futuros y prop firms; analiza disciplina y métricas, nunca ejecuta órdenes."
```

Si se clona configuración desde otro profile, reemplazar completamente cualquier `SOUL.md`, memoria o identidad heredada que no corresponda. No mezclar memorias de brain-local, Wolfim u otras empresas.

Configurar un modelo de costo bajo disponible en local. No contratar ni habilitar un proveedor pago nuevo. Informar en `response.md` el provider y modelo finalmente usados, sin mostrar credenciales.

### Toolsets mínimos sugeridos

- `hermes-cli`
- `file`
- `terminal` — solo para CSV, cálculos y archivos locales; nunca para ejecución de trading
- `web` / `search` — para consultar reglas oficiales cuando Juan lo pida
- `vision` — para analizar capturas
- `skills`
- `memory`
- `session_search`

No habilitar gateway, cron, broker APIs ni automatización de escritorio en esta primera fase.

## Archivos iniciales del profile

Crear dentro del entorno propio del profile, sin tocar rutas empresariales:

1. `SOUL.md` — identidad, rol y límites anteriores.
2. `AGENTS.md` — convenciones del workspace y workflow.
3. Plantilla de plan premercado.
4. Plantilla de registro por operación.
5. Plantilla de cierre diario.
6. Plantilla de revisión semanal.
7. Archivo para reglas de prop firm con campos para:
   - firma y plan;
   - tamaño nominal;
   - profit target;
   - tipo y monto de drawdown;
   - daily loss;
   - consistencia;
   - horarios y noticias;
   - contratos permitidos;
   - reglas de payout;
   - fecha y URL oficial de verificación.

La estructura debe ser simple. No construir dashboard, base de datos, integración con broker ni automatizaciones en esta fase.

## Flujo mínimo esperado

### Premercado

```text
Fecha:
Cuenta / modo sim:
Instrumento:
Setup permitido:
Riesgo máximo por trade:
Stop diario:
Máximo de operaciones:
Horario permitido:
Eventos relevantes:
Condición para no operar:
```

### Por operación

```text
Hora:
Instrumento:
Dirección:
Entrada / stop / salida:
Resultado:
Setup:
Captura:
¿Respeté el plan?:
Error técnico o emocional:
```

### Cierre diario

```text
PnL informado por Juan o importado:
Drawdown máximo:
Cantidad de trades:
Violaciones:
Mejor decisión:
Peor decisión:
Una corrección para la próxima sesión:
```

## Smoke test obligatorio

Ejecutar una consulta real con el profile, por ejemplo:

```text
Estoy en simulación. Antes de operar MES quiero preparar mi plan y fijar el límite diario. Guiame sin dar una señal de compra o venta.
```

Verificar que:

- responde con checklist de proceso;
- pide los datos faltantes;
- no inventa una entrada;
- no da una señal direccional;
- no intenta operar;
- mantiene trading manual y control de riesgo.

## Criterios de aceptación

- [ ] `hermes profile list` muestra `trading-performance`.
- [ ] El profile tiene identidad y memoria independientes.
- [ ] `SOUL.md` contiene todos los límites absolutos.
- [ ] Las cinco plantillas iniciales existen y son utilizables.
- [ ] Provider/model quedan configurados sin gasto nuevo.
- [ ] Toolsets mínimos funcionan.
- [ ] Gateway y cron quedan deshabilitados/no configurados.
- [ ] Smoke test ejecutado con salida real satisfactoria.
- [ ] `Hermes/Systems/local/trading-performance-setup.md` documenta ruta, modelo, toolsets, comandos y verificación, sin secretos.
- [ ] `response.md` informa estado, archivos creados, comandos ejecutados y resultado del smoke test.
- [ ] Se crea un evento de ack al comenzar y un evento de done o blocked al finalizar.

## Orden de prioridad

Este handoff es `normal`. No debe interrumpir un handoff Wolfim `high` que esté siendo ejecutado. La creación debe mantenerse pequeña: profile funcional, plantillas y prueba; nada más.

## Fuentes de contexto disponibles

- Investigación reciente: `Hermes/Reports/prop-firms-futures-pago-unico-2026/`
- Recomendación actual de investigación: LucidPro 25K como candidata, pero no comprar ni configurar ninguna cuenta como parte de este handoff.

## Resultado esperado

Un profile local operativo que ayude a Juan a desarrollar disciplina y evidencia en trading manual, sin capacidad de ejecutar operaciones ni generar gastos.
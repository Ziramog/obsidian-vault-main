# TRUzT v1.19.8 — Unknown flat cleanup

Archivo activo:

```text
C:\Users\ingju\Documents\NinjaTrader 8\bin\Custom\DrawingTools\TRUzT_Position_Sizer.cs
```

Backup:

```text
C:\Users\ingju\Documents\NinjaTrader 8\bin\Custom\DrawingTools\TRUzT_Position_Sizer.cs.bak_before_v1_19_8_unknown_flat_cleanup_20260825_100702
```

## Bug reportado

Juan reportó que TRUzT mostraba `ACTIVE POSITION` / `ACTIVE - BRACKET LIVE` aunque Tradovate estaba flat y sin posición real.

La captura mostraba:

```text
TRUzT 1.19.7
ACTIVE - BRACKET LIVE - 0 SL / 1 TP live
RECOVERY: 0E/0SL/1TP/0C | flat
```

## Evidencia

En `trace.20260825.00002.txt` aparece:

```text
Cbi.Order.Update1 ... name='TRUzT_TP1' orderState=Unknown ...
comment='Order unrecoverable. Please contact your broker to verify it’s state.'
```

También hubo intentos repetidos de cancel sobre esa orden `Unknown`:

```text
Cbi.Account.Cancel0: realOrderState=Unknown ... name='TRUzT_TP1'
```

## Root cause

La lógica anterior consideraba activo cualquier estado que no fuera:

```text
Filled / Cancelled / Rejected / Initialized
```

Entonces `OrderState.Unknown` quedaba tratado como live/cancelable. Resultado:

```text
Tradovate flat
NinjaTrader order cache: TRUzT_TP1 Unknown/unrecoverable
TRUzT panel: ACTIVE / RECOVERY con 1 TP live falso
```

## Fix aplicado

Versión activa:

```text
ToolVersion = 1.19.8
```

Cambios:

1. Nuevo helper:

```text
IsOrderUnknownOrUnrecoverable(order)
```

Detecta:

```text
OrderState == Unknown
Comment/NativeError contiene unrecoverable
```

2. `IsOrderTerminal()` ahora trata `Unknown/unrecoverable` como terminal/no-live.

3. `IsOrderActive()` y `IsOrderCancelable()` heredan esa regla: Unknown no cuenta como activo y no intenta cancelarse repetidamente.

4. `ClearCompletedTRUzTStateIfFlat()` ahora valida posición real:

```text
si cuenta tiene qty != 0 -> no limpiar
si cuenta está flat y no hay órdenes TRUzT activas reales -> limpiar todo estado interno
```

5. `IsEntryAwaitingBracket()` ahora usa terminal-state awareness para que una entry `Unknown` vieja no bloquee cleanup.

6. Si un SL TRUzT entra en `Unknown/unrecoverable` con posición abierta y sin otro SL activo, dispara protección de cierre TRUzT como caso de pérdida de SL.

## Verificación local

Compilación externa:

```text
csc.exe @truzt_csc.rsp
exit_code 0
```

Checks:

```text
ToolVersion 1.19.8
brace_delta 0
unknown_helper_present True
unknown_terminal True
unknown_not_cancelable_via_terminal True
unknown_not_active_via_terminal True
flat_qty_gate_in_clear True
entry_awaiting_terminal_aware True
unknown_stop_lost_branch True
sl_first_still_present True
```

Safety scan:

```text
Flatten 0
Position.Close 0
AtmStrategyCreate 0
Account.Submit 2
CreateOrder 5
Cancel( 3
Change( 3
```

## Resultado esperado

Al recompilar/reiniciar NinjaTrader, si Tradovate está flat y no hay órdenes reales vivas:

```text
TRUzT debe pasar a Ready
no debe mostrar ACTIVE POSITION
no debe mostrar RECOVERY 0E/0SL/1TP | flat
no debe seguir intentando Cancel sobre orden Unknown
```

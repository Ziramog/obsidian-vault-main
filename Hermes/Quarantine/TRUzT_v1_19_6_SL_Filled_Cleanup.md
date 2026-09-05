# TRUzT v1.19.6 — SL filled cleanup

Fecha: 2026-08-24

Archivo activo:

```text
C:\Users\ingju\Documents\NinjaTrader 8\bin\Custom\DrawingTools\TRUzT_Position_Sizer.cs
```

Backup:

```text
C:\Users\ingju\Documents\NinjaTrader 8\bin\Custom\DrawingTools\TRUzT_Position_Sizer.cs.bak_before_v1_19_6_sl_filled_cleanup_20260824_235415
```

## Bug report

Juan reportó que tocó el SL (`Sell STP`) y quedó vivo el TP (`Sell Limit`). Se necesita que si toca SL elimine todo rastro de la posición TRUzT.

## Evidencia de logs

En APEX:

```text
13:28:22 TRUzT_SL_TP1 Filled MNQU6 Sell StopMarket qty 2
13:28:57 TRUzT_TP1 Cancel submitted / Cancelled
```

O sea: OCO finalmente canceló, pero con ~35 segundos de demora. Durante esa ventana quedó un TP sell limit vivo después del stop.

## Root cause

`OnBracketOrderUpdate(...)` trataba los updates de SL/TP de forma genérica:

- si no quedaban exits activos: limpiar;
- si quedaban exits activos: no hacer nada;
- dependía de OCO/provider para cancelar el TP al llenarse el SL.

Faltaba acción explícita propia del tool ante `SL Filled`.

## Fix

Nuevo flujo:

```text
Si cualquier TRUzT SL pasa a Filled:
  - detecta si la cuenta/instrumento está flat
  - si está flat: cancela todos los TRUzT TP/SL restantes cancelables del mismo account/instrument
  - si no está flat todavía: cancela TP restantes, pero conserva SL restantes como protección
  - no toca órdenes manuales: el cleanup automático usa solo órdenes trackeadas explícitas y live orders con nombre/OCO `TRUzT`/`TRUZT`; no usa rescue stops sin nombre
  - no usa Flatten
  - no usa Position.Close
```

También para `TP Filled`:

```text
Si el TP deja la cuenta flat:
  - cancela cualquier SL/TP TRUzT remanente
```

Se agregaron helpers:

```text
AddLiveNamedTRUzTOrdersToCancelAfterExitFill
AddTrackedTRUzTOrdersToCancelAfterExitFill
CancelRemainingTRUzTOrdersAfterExitFill
```

Guard importante:

```text
El nuevo branch de named orders excluye TRUzT_ENTRY y TRUzT_CLOSE para no interferir con el fill del entry ni con cierre manual TRUzT.
```

## Verificación

Compilación aislada:

```text
'/c/Windows/Microsoft.NET/Framework64/v4.0.30319/csc.exe' @'C:\Users\ingju\AppData\Local\Temp\truzt_csc.rsp'
exit_code 0
```

Static checks:

```text
ToolVersion 1.19.6
brace 0
exit branch excludes entry: true
SL fill cleanup helper: true
partial SL keeps SL protection: true
```

Safety tokens:

```text
Flatten 0
Position.Close 0
AtmStrategyCreate 0
Account.Submit 1
Cancel( 2
Change( 3
```

Motor preservado excepto handler de exit cleanup:

```text
SubmitBracketFromPanel same
SubmitBracketExits same
AddTargetBracket same
CancelActiveTRUzTOrders same
SubmitTRUzTPositionClose same
MoveActiveStopsToBreakEven same
MoveActiveStopsToProfitLock same
ValidateOrderPlan same
ClearCompletedTRUzTStateIfFlat same
```

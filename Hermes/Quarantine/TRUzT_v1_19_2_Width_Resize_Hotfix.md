# TRUzT v1.19.2 — Hotfix: horizontal resize no debe volver al ancho inicial

Fecha: 2026-08-22

Archivo activo:

```text
C:\Users\ingju\Documents\NinjaTrader 8\bin\Custom\DrawingTools\TRUzT_Position_Sizer.cs
```

Backup:

```text
C:\Users\ingju\Documents\NinjaTrader 8\bin\Custom\DrawingTools\TRUzT_Position_Sizer.cs.bak_before_v1_19_2_width_resize_hotfix_20260822_091131
```

## Síntoma

Al intentar achicar horizontalmente el drawing en el chart, el tamaño vuelve automáticamente al estado/ancho inicial.

## Root cause

El ancho visual de la posición usa `BoxWidthPixels` como fuente de verdad, pero el `WidthAnchor`/handle seleccionable no se mantenía sincronizado al nuevo borde derecho después del drag.

Resultado: el usuario podía mover el ancho, pero el anchor/handle quedaba inconsistente y NinjaTrader podía re-evaluar la selección/handle con valores viejos, generando snap-back visual al ancho anterior.

## Fix

1. En `UpdateBoxWidthFromPoint(...)`, después de actualizar `BoxWidthPixels` y `BoxWidthBars`, se llama:

```csharp
SetWidthAnchorFromPixels(chartControl, chartPanel, chartScale);
```

2. En `OnRender(...)`, cuando no se está editando activamente el ancho, se mantiene sincronizado el `WidthAnchor` con el ancho pixel actual:

```csharp
if (AllowDragBoxWidth && !IsExtendedLinesRight && DrawingState != DrawingState.Building && !isEditingWidth && editingAnchor != WidthAnchor)
    SetWidthAnchorFromPixels(chartControl, chartPanel, chartScale);
```

## Alcance

Visual-only. No se tocó motor de órdenes.

Métodos de órdenes sin cambios:

```text
SubmitBracketFromPanel same
OnBracketOrderUpdate same
SubmitBracketExits same
AddTargetBracket same
CancelActiveTRUzTOrders same
MoveActiveStopsToBreakEven same
MoveActiveStopsToProfitLock same
ValidateOrderPlan same
ClearCompletedTRUzTStateIfFlat same
```

Métodos visuales cambiados:

```text
OnRender changed
UpdateBoxWidthFromPoint changed
```

## Verificación

Compilación aislada:

```text
'/c/Windows/Microsoft.NET/Framework64/v4.0.30319/csc.exe' @'C:\Users\ingju\AppData\Local\Temp\truzt_csc.rsp'
exit_code 0
```

Safety tokens:

```text
brace 0
Flatten 0
Position.Close 0
AtmStrategyCreate 0
Account.Submit 1
Cancel( 1
Change( 3
```

`CreateOrder 6` incluye menciones textuales/comentarios; no se agregó orden real.

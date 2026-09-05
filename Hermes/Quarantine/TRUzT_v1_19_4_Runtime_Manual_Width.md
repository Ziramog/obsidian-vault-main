# TRUzT v1.19.4 — Runtime manual width survives click-away

Fecha: 2026-08-22

Archivo activo:

```text
C:\Users\ingju\Documents\NinjaTrader 8\bin\Custom\DrawingTools\TRUzT_Position_Sizer.cs
```

Backup:

```text
C:\Users\ingju\Documents\NinjaTrader 8\bin\Custom\DrawingTools\TRUzT_Position_Sizer.cs.bak_before_v1_19_4_runtime_manual_width_20260822_095946
```

## Síntoma

El usuario puede achicar horizontalmente durante el drag, pero al hacer click fuera del drawing vuelve al tamaño inicial.

## Diagnóstico

Esto indica snap-back en deselection/click-away, no durante drag. La causa probable es que NinjaTrader re-aplica/defaultiza la property/template `BoxWidthPixels` o recalcula el estado al perder selección.

## Fix

Se agregó una fuente runtime privada:

```csharp
private double manualBoxWidthPixels = double.NaN;
```

Nuevo flujo:

- Si no hubo drag manual: usa `BoxWidthPixels` como fallback/template.
- Cuando el usuario arrastra el handle: `SetManualBoxWidthPixels(pixels)` guarda el ancho en `manualBoxWidthPixels` y también refleja el valor en `BoxWidthPixels`.
- `GetBoxRightX()` usa `GetActiveBoxWidthPixels()`, que prioriza `manualBoxWidthPixels` sobre la property.
- Si NinjaTrader pisa/relee `BoxWidthPixels` al perder selección, el render sigue usando `manualBoxWidthPixels`.

## Alcance

Visual-only.

Métodos visuales/helpers cambiados/agregados:

```text
GetActiveBoxWidthPixels added
SetManualBoxWidthPixels added
SetWidthAnchorFromPixels changed
GetBoxRightX changed
UpdateBoxWidthFromPoint changed
SyncBoxWidthPixelsFromWidthAnchor changed
```

Motor de órdenes sin cambios:

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

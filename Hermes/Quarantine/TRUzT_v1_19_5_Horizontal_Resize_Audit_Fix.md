# TRUzT v1.19.5 — Horizontal resize audit fix

Fecha: 2026-08-22

Archivo activo:

```text
C:\Users\ingju\Documents\NinjaTrader 8\bin\Custom\DrawingTools\TRUzT_Position_Sizer.cs
```

Backup:

```text
C:\Users\ingju\Documents\NinjaTrader 8\bin\Custom\DrawingTools\TRUzT_Position_Sizer.cs.bak_before_v1_19_5_horizontal_resize_audit_fix_20260822_102603
```

## Bug report

`1.19.4 no mejoro sigue haciendo lo mismo`: el drawing se puede achicar mientras se arrastra, pero al hacer click fuera vuelve al tamaño inicial.

## Audit findings

El síntoma ocurre en click-away/deselection, no durante drag. Dos problemas quedaron en el flujo anterior:

1. `OnMouseUp()` seguía llamando `UpdateBoxWidthFromPoint(...)`. Si NinjaTrader entrega el mouse-up/click-away point en ese evento, el ancho se recalcula desde ese punto y se re-expande aunque el drag anterior haya achicado bien.
2. v1.19.4 guardaba el ancho manual en un campo privado runtime. Si NinjaTrader clona/recrea/re-aplica template al perder selección, ese campo puede perderse. El ancho manual debe estar en una propiedad oculta persistible.
3. `OnRender()` todavía mutaba `WidthAnchor` como side effect. Render debe ser side-effect-free para evitar que NT reinterprete anchors al deselect.

## Fix

- Nuevo hidden persisted setting:

```csharp
[Browsable(false)]
[NinjaScriptProperty]
public double ManualBoxWidthPixels { get; set; }
```

- `GetActiveBoxWidthPixels()` prioriza `ManualBoxWidthPixels`; `BoxWidthPixels` queda solo como fallback/default.
- `SetManualBoxWidthPixels(...)` actualiza `ManualBoxWidthPixels` y refleja el valor en `BoxWidthPixels`.
- `OnMouseUp()` ya no recalcula width. Solo cierra el estado de edición.
- `OnRender()` ya no llama `SetWidthAnchorFromPixels(...)`; no muta anchors durante render.

## Verificación

Compilación aislada:

```text
'/c/Windows/Microsoft.NET/Framework64/v4.0.30319/csc.exe' @'C:\Users\ingju\AppData\Local\Temp\truzt_csc.rsp'
exit_code 0
```

Static checks:

```text
ToolVersion 1.19.5
brace 0
private manual field count 0
ManualBoxWidthPixels count 12
OnRender SetWidthAnchorFromPixels near render: 0
UpdateBoxWidthFromPoint call sites only in OnMouseMove: lines 895, 901
mouse-up width recalc remaining: false
render mutates width anchor: false
```

Safety tokens:

```text
Flatten 0
Position.Close 0
AtmStrategyCreate 0
Account.Submit 1
Cancel( 1
Change( 3
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

# TRUzT v1.19.3 — Manual width handle no auto-expand

Fecha: 2026-08-22

Archivo activo:

```text
C:\Users\ingju\Documents\NinjaTrader 8\bin\Custom\DrawingTools\TRUzT_Position_Sizer.cs
```

Backup:

```text
C:\Users\ingju\Documents\NinjaTrader 8\bin\Custom\DrawingTools\TRUzT_Position_Sizer.cs.bak_before_v1_19_3_manual_width_handle_20260822_092502
```

## Síntoma persistente

Aunque v1.19.2 sincronizaba el `WidthAnchor`, el drawing seguía expandiéndose horizontalmente después de achicarlo.

## Root cause ajustado

El ancho mezclaba dos modelos:

```text
BoxWidthPixels = ancho visual real
WidthAnchor/SlotIndex = anchor normal editable de NinjaTrader
```

Al exponer `WidthAnchor` como anchor normal, NT podía volver a tirar el dibujo hacia el anchor/slot viejo y expandirlo.

Además, si una instancia tenía `Extend Lines Right` activo, `GetBoxRightX()` devolvía siempre el borde derecho del chart, ignorando el ancho manual.

## Fix v1.19.3

- `WidthAnchor` deja de formar parte de `Anchors` normales de NT.
- El ancho se maneja por custom handle derecho + `BoxWidthPixels`.
- `GetSelectionPoints()` muestra el punto de ancho calculado desde el borde visual real, no desde `WidthAnchor`.
- `AllowDragBoxWidth` manda sobre `Extend Lines Right`: si el handle manual está permitido, no se auto-extiende al borde derecho.
- Al empezar drag de ancho, se limpia `editingAnchor` para aislarlo de los anchors normales.

## Alcance

Visual-only.

Métodos visuales/properties cambiados:

```text
Anchors changed
GetSelectionPoints changed
GetCursor changed
OnMouseDown changed
OnRender changed
GetBoxRightX changed
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

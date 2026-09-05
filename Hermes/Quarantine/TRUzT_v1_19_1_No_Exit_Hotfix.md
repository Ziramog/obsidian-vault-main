# TRUzT v1.19.1 — Hotfix: Entry fill no dispara TP/SL

Fecha: 2026-08-20

Archivo activo:

```text
C:\Users\ingju\Documents\NinjaTrader 8\bin\Custom\DrawingTools\TRUzT_Position_Sizer.cs
```

Backup:

```text
C:\Users\ingju\Documents\NinjaTrader 8\bin\Custom\DrawingTools\TRUzT_Position_Sizer.cs.bak_before_v1_19_1_no_exit_hotfix_20260820_095156
```

## Síntoma reportado

Después de SEND, TRUzT coloca el entry pero no coloca TP ni SL.

## Evidencia en logs

Log NinjaTrader 2026-08-20:

```text
08:43:41 TRUzT_ENTRY Submitted MNQU6 Qty 5 Market
08:43:41 TRUzT_ENTRY Filled MNQU6 Qty 5 @ 29281.75
```

No aparece ningún `TRUzT_SL_*` ni `TRUzT_TP`/`TRUzT_TP*` después del fill.

## Root cause

`RefreshChartTraderOrderPanel()` llama `ClearCompletedTRUzTStateIfFlat()` en cada refresh/render.

Después de `Account.CreateOrder()` + `Submit()`, el entry puede quedar durante una ventana mínima en estado `Initialized` antes de llegar los updates `Submitted/Working/Filled`.

`HasActiveTRUzTOrder()` ignora `Initialized` por seguridad anti-CancelPending.

Entonces el cleanup podía interpretar:

```text
activeEntryOrder != null
pero no hay active order
=> limpiar estado + UnsubscribeOrderAccount()
```

Eso desuscribía `OrderUpdate` antes del fill. El entry se llenaba, pero TRUzT ya no recibía el update que llama a `SubmitBracketExits()`.

## Fix

Se agregó `IsEntryAwaitingBracket()` y guard en `ClearCompletedTRUzTStateIfFlat()`:

```csharp
if (IsEntryAwaitingBracket())
    return;
```

Mientras exista un `activeEntryOrder` y todavía no se enviaron brackets, el panel no puede limpiar ni desuscribir el handler de fills, aunque el entry esté brevemente `Initialized`.

## Alcance

No se tocó:

```text
SubmitBracketFromPanel
SubscribeOrderAccount
OnBracketOrderUpdate
SubmitBracketExits
AddTargetBracket
CancelActiveTRUzTOrders
BE NOW / lock-profit
ValidateOrderPlan
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

`CreateOrder` textual sube a 6 por comentario nuevo `Account.CreateOrder/Submit`; no se agregó una orden nueva real.

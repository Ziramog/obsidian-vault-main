# TRUzT v1.19.0 — Micro Only Lock + ACTIVE POSITION section

Fecha: 2026-08-16

Archivo activo:

```text
C:\Users\ingju\Documents\NinjaTrader 8\bin\Custom\DrawingTools\TRUzT_Position_Sizer.cs
```

Backup previo:

```text
C:\Users\ingju\Documents\NinjaTrader 8\bin\Custom\DrawingTools\TRUzT_Position_Sizer.cs.bak_before_v1_19_0_micro_lock_active_section_20260816_181105
```

## Implementado

- `ToolVersion = "1.19.0"`.
- Nuevo setting `07 - Pro Safety` → `Micro Only Lock` (Order 15).
- Botón ChartTrader en fila de Confirm SEND:

```text
[ANY]        = permite cualquier instrumento
[MICRO LOCK] = solo micros pueden SEND
```

- `MICRO LOCK` ON bloquea SEND cuando el instrumento no es micro:

```text
BLOCKED - MICRO ONLY: NQ 09-26 is not micro
```

- Micros reconocidos:

```text
MNQ MES M2K MYM MGC MCL M6E M6B M6J M6A MBT MET
```

- Badge header agrega `MICRO LOCK` cuando está activo.
- Separador visual `ACTIVE POSITION` antes de la fila BE NOW / +.25R / +.5R:

```text
...plan/entry/presets...
RESET PLAN
---- ACTIVE POSITION ----
BE NOW  +.25R  +.5R
CANCEL TRUzT
```

- `CANCEL TRUzT` pasa a fila propia debajo del separador.

## Cambios intencionales

```text
IsMicroInstrument changed
```

Motivo: antes detectaba "empieza con M"; ahora lista precisa de micros CME para no tratar `MSFT` u otros símbolos con M como micros.

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
CreateOrder 5
Cancel( 1
Change( 3
```

Métodos de motor sin cambios:

```text
SubmitBracketExits same
AddTargetBracket same
CancelActiveTRUzTOrders same
SubmitTRUzTPositionClose same
SubmitBracketFromPanel same
MoveActiveStopsToBreakEven same
MoveActiveStopsToProfitLock same
GetOrderPlanSignature same
OnChartTraderSendClick same
OnChartTraderCancelOrdersClick same
OnChartTraderBeNowClick same
OnChartTraderLock25RClick same
OnChartTraderLock50RClick same
TryMoveStopToBreakEven same
ClearCompletedTRUzTStateIfFlat same
```

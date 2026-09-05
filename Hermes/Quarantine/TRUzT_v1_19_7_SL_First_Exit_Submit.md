# TRUzT v1.19.7 — SL-first exit submit

Archivo activo:

```text
C:\Users\ingju\Documents\NinjaTrader 8\bin\Custom\DrawingTools\TRUzT_Position_Sizer.cs
```

Backup:

```text
C:\Users\ingju\Documents\NinjaTrader 8\bin\Custom\DrawingTools\TRUzT_Position_Sizer.cs.bak_before_v1_19_7_sl_first_exit_submit_20260825_064457
```

## Bug reportado

Juan reportó que TRUzT hizo `order fill` y quedó sin SL ni TP.

## Evidencia de logs

Log del 2026-08-25:

```text
05:42:25 TRUzT_ENTRY Market submitted/working
05:42:26 TRUzT_ENTRY Filled Qty 2 @ 29367.5
```

Después del fill, en `log.20260825.00001.en.txt` no aparecen órdenes `TRUzT_SL_TP1` ni `TRUzT_TP1` aceptadas/working.

Trace específico:

```text
05:42:26 Cbi.Account.OrderUpdateCallback ... name='TRUzT_ENTRY' orderState=Filled
05:42:26 Cbi.Account.CreateOrder ... name='TRUzT_TP1' orderState=Initialized
```

No aparece el `CreateOrder TRUzT_SL_TP1` correspondiente en ese intento. Luego Juan agregó órdenes manuales sin nombre (`Name=''`) para proteger/cerrar:

```text
05:43:17 Name='' Sell Stop Limit Working
05:43:26 Name='' Sell Limit Working
```

## Root cause

La arquitectura anterior del submit de exits hacía esto dentro de `AddTargetBracket`:

```text
1. Create target TP
2. Create protective SL
3. Batch submit TP + SL
```

Si NinjaTrader/adapter interrumpía/fallaba entre el paso 1 y el 2, podía quedar una posición llena sin SL. En el caso real el trace mostró exactamente el primer `CreateOrder` del TP y no mostró el SL.

## Fix aplicado

Versión activa:

```text
ToolVersion = 1.19.7
```

Cambio central:

```text
SubmitBracketExits()
  -> SubmitTargetBracketStopFirst()
```

Nuevo flujo:

```text
1. Validar precios y lados antes de submit.
2. Crear SL protector.
3. Submit SL protector inmediatamente.
4. Trackear SL.
5. Crear TP.
6. Submit TP.
7. Trackear TP.
```

Reglas de seguridad:

```text
Si la validación de exits falla:
  cerrar qty TRUzT inmediatamente.

Si el SL no puede crearse/submitearse:
  cerrar qty TRUzT inmediatamente.

Si el SL queda vivo pero el TP falla:
  dejar SL protector vivo y avisar: Protective SL live; TP not submitted.

Si un SL TRUzT se Rejected/Cancelled y la posición sigue abierta sin otro SL activo:
  cerrar qty TRUzT.

Si el SL Cancelled fue consecuencia de TP Filled/OCO:
  NO enviar close duplicado.
```

## Verificación local

Compilación externa:

```text
csc.exe @truzt_csc.rsp
exit_code 0
```

Checks estáticos:

```text
ToolVersion 1.19.7
brace_delta 0
stop_create_before_target_create True
stop_submit_before_target_create True
stop_tracked_after_submit True
target_submit_before_track True
no_old_batch_exit_submit True
protective_stop_lost_helper True
sl_cancelled_guard_after_tp_filled True
sl_rejected_or_cancelled_branch True
sl_filled_cleanup_still_present True
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

## Prueba requerida en NinjaTrader

En Sim primero:

1. Reiniciar NinjaTrader o recompilar NinjaScript desde NinjaScript Editor.
2. Abrir MNQ/MES con Chart Trader.
3. TRUzT v1.19.7 visible.
4. Mandar entry Market con qty chica.
5. Resultado esperado en logs/trace inmediatamente después del fill:

```text
TRUzT_ENTRY Filled
TRUzT_SL_TP1 Submitted/Accepted/Working
TRUzT_TP1 Submitted/Accepted/Working
```

Orden correcto esperado:

```text
SL Create/Submit antes que TP Create/Submit
```

Si falla TP, debe quedar SL vivo. Si falla SL, TRUzT debe cerrar la posición.

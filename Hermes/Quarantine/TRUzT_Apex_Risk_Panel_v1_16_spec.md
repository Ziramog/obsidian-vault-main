# TRUzT Apex Risk Panel v1.16 — Spec preliminar

Fecha: 2026-08-15  
Herramienta: `TRUzT_Position_Sizer`  
Archivo principal: `C:\Users\ingju\Documents\NinjaTrader 8\bin\Custom\DrawingTools\TRUzT_Position_Sizer.cs`

## Objetivo

Agregar a TRUzT un módulo de gestión de riesgo tipo Apex para que el panel de Chart Trader guíe el tamaño/riesgo del trade según:

- tipo de cuenta Apex;
- tamaño de cuenta;
- estado real disponible desde NinjaTrader;
- estado manual/configurable que NinjaTrader no puede saber con certeza;
- reglas de drawdown, DLL, max contracts, scaling, consistency y payout.

La primera versión debe ser advisory + bloqueo opcional de SEND. No debe tocar el motor de órdenes salvo para agregar validación pre-SEND controlada.

---

## Principio de diseño

Apex cambia productos/reglas. Por eso TRUzT no debe depender de reglas mágicas hardcodeadas sin visibilidad.

Diseño correcto:

1. Selector explícito de perfil Apex.
2. Tamaño de cuenta.
3. Inputs manuales para datos que NinjaTrader no sabe.
4. Lectura automática solo de datos confiables del `Account` de NinjaTrader.
5. Todas las reglas visibles en MORE / settings.
6. Bloqueo de SEND solo si `Apex Block SEND = true`.
7. Regla desconocida = warning/manual input, no inventar.

---

## Selector de cuenta Apex

### `Apex Risk Mode`

Valores propuestos:

```text
Off
Apex Intraday Eval
Apex EOD Eval
Apex Intraday PA
Apex EOD PA
Apex Live Prop / LPA
Apex Second Chance
Custom
```

### `Apex Account Size`

Para Eval/PA simulada:

```text
25K
50K
100K
150K
```

Para Live Prop / LPA:

```text
Live Level 1
Live Level 2
Live Level 3
Live Level 4 / Custom Review
```

Nota: el programa Live/LPA actual no está basado en 25K/50K/100K/150K como las cuentas simuladas. Empieza con balance/profit base $0 y reglas propias.

---

## Reglas oficiales relevadas

Fuentes públicas oficiales vía reader/cache de Apex:

- `50% Consistency Requirement`
- `Scaling Levels (PA) Explained`
- `Daily Loss Limit Explained`
- `Intraday Trailing Drawdown Evaluations`
- `Intraday Trailing Drawdown Performance Accounts (PA)`
- `EOD Evaluations`
- `EOD Performance Accounts (PA)`
- `EOD Payouts`
- `Apex Live Prop Trading Program FAQ`

Apex advierte que puede actualizar reglas sin aviso. Esta spec debe tratarse como rule profile versionado, no verdad eterna.

---

# Matriz de reglas

## 1. Apex Intraday Evaluation

Características:

```text
Real-time intraday trailing drawdown
Peak Balance incluye realized + unrealized PnL
Threshold solo sube, nunca baja
No Daily Loss Limit
Fixed position size
No minimum trading days
No consistency rule in evaluation
30-day access period
Puede pasar al alcanzar target sin breach
```

Tabla:

| Size | Profit Target | Max Drawdown / Trailing | Max Contracts | DLL | Consistency | Scaling |
|---|---:|---:|---:|---:|---|---|
| 25K | $1,500 | $1,000 | 4 | none | No | No |
| 50K | $3,000 | $2,000 | 6 | none | No | No |
| 100K | $6,000 | $3,000 | 8 | none | No | No |
| 150K | $9,000 | $4,000 | 12 | none | No | No |

Checks TRUzT:

- Max contracts.
- Planned risk vs trailing drawdown cushion.
- Warning si plan usa demasiado porcentaje del cushion.
- No DLL check.
- No consistency check.

Datos necesarios:

```text
Current Balance / NetLiq
Current trailing threshold o manual threshold
Peak balance si threshold no está disponible
Safety buffer $
```

---

## 2. Apex EOD Evaluation

Características:

```text
No intraday trailing drawdown
EOD Drawdown calculado al cierre y aplicado siguiente sesión
Daily Loss Limit fijo por sesión
Fixed position size
No minimum trading days
No consistency rule in evaluation
30-day access period
Puede pasar al alcanzar target sin breach
```

Tabla:

| Size | Profit Target | EOD Drawdown | DLL | Max Contracts | Consistency | Scaling |
|---|---:|---:|---:|---:|---|---|
| 25K | $1,500 | $1,000 | $500 | 4 | No | No |
| 50K | $3,000 | $2,000 | $1,000 | 6 | No | No |
| 100K | $6,000 | $3,000 | $1,500 | 8 | No | No |
| 150K | $9,000 | $4,000 | $2,000 | 12 | No | No |

Checks TRUzT:

- Max contracts.
- Planned risk vs EOD threshold cushion.
- Planned risk vs DLL remaining.
- Warning si planned risk usa demasiado porcentaje de DLL.
- No consistency check.

Datos necesarios:

```text
Current Balance / NetLiq
EOD Drawdown threshold
Daily PnL or DLL remaining
Safety buffer $
```

---

## 3. Apex Intraday PA

Características:

```text
Intraday trailing drawdown enforced real time
Trailing stops once Max Trailing Drawdown Amount + $100 is reached
DLL enforced intraday
Tier-based scaling
100% payout split subject to payout eligibility
Position size grows by tier
```

Top-level table:

| Size | Max Drawdown | Scaling | Max Contracts top | DLL |
|---|---:|---|---:|---|
| 25K | $1,000 | Tier based | 2 | Tier based |
| 50K | $2,000 | Tier based | 4 | Tier based |
| 100K | $3,000 | Tier based | 6 | Tier based |
| 150K | $4,000 | Tier based | 10 | Tier based |

PA scaling tiers from Apex:

### 25K PA

| Profit Range | Max Contracts | DLL | Tier |
|---|---:|---:|---:|
| $0–$999 | 1 | $500 | L1 |
| $1,000–$1,999 | 2 | $500 | L2 |
| $2,000+ | 2 | $1,250 | L3 |

### 50K PA

| Profit Range | Max Contracts | DLL | Tier |
|---|---:|---:|---:|
| $0–$1,499 | 2 | $1,000 | L1 |
| $1,500–$2,999 | 3 | $1,000 | L2 |
| $3,000–$5,999 | 4 | $2,000 | L3 |
| $6,000+ | 4 | $3,000 | L4 |

### 100K PA

| Profit Range | Max Contracts | DLL | Tier |
|---|---:|---:|---:|
| $0–$1,999 | 3 | $1,750 | L1 |
| $2,000–$2,999 | 4 | $1,750 | L2 |
| $3,000–$4,999 | 5 | $1,750 | L3 |
| $5,000–$9,999 | 6 | $2,500 | L4 |
| $10,000+ | 6 | $3,500 | L5 |

### 150K PA

| Profit Range | Max Contracts | DLL | Tier |
|---|---:|---:|---:|
| $0–$1,999 | 4 | $2,500 | L1 |
| $2,000–$2,999 | 5 | $2,500 | L2 |
| $3,000–$4,999 | 7 | $2,500 | L3 |
| $5,000–$9,999 | 10 | $3,000 | L4 |
| $10,000+ | 10 | $4,000 | L5 |

Checks TRUzT:

- Inferir tier desde profit sobre starting balance o permitir tier manual.
- Max contracts por tier.
- Planned risk vs drawdown cushion.
- Planned risk vs DLL remaining.
- Consistency advisory para payout, no hard block de trade.

---

## 4. Apex EOD PA

Características:

```text
No intraday trailing drawdown
EOD drawdown enforced intraday once calculated
DLL enforced intraday
Tier-based scaling
100% payout split subject to eligibility
```

Top-level table:

| Size | EOD Drawdown | Scaling | Max Contracts top | DLL |
|---|---:|---|---:|---|
| 25K | $1,000 | Tier based | 2 | Tier based |
| 50K | $2,000 | Tier based | 4 | Tier based |
| 100K | $3,000 | Tier based | 6 | Tier based |
| 150K | $4,000 | Tier based | 10 | Tier based |

Uses same PA scaling tiers as above.

Payout-related requirements from Apex EOD PA:

| Size | Min Trade Days | Min Daily Profit | Safety Net | Min Balance to Request | Max Payouts |
|---|---:|---:|---:|---:|---:|
| 25K | 5 | $100 | $26,100 | $26,600 | 6 |
| 50K | 5 | $250 | $52,100 | $52,600 | 6 |
| 100K | 5 | $300 | $103,100 | $103,600 | 6 |
| 150K | 5 | $350 | $154,100 | $154,600 | 6 |

Consistency:

```text
50% consistency applies to payout eligibility.
Largest profitable day / total profit since last payout must be below 50%.
If not met, account does not fail; payout request unavailable until consistency improves.
```

Checks TRUzT:

- Trade hard checks: max contracts, DD cushion, DLL cushion.
- Payout advisory: consistency %, qualifying days, min balance, safety net.
- Do not block SEND solely because consistency is not met unless user explicitly enables such a strict mode.

---

## 5. Apex Live Prop / LPA

Apex Live FAQ states the Live program is invitation-based and not the same as 25K/50K/100K/150K simulated account sizes.

Base characteristics:

```text
Live account starts with $0 balance/profit base.
Initial drawdown: $3,000 EOD drawdown.
Initial contract limit: 10 mini / 100 micro.
Initial daily loss limit: No DLL at Level 1.
Max live accounts: up to 5, based on eligibility.
Profit split: 90% trader / 10% Apex.
Daily payout requests available, $500 minimum.
Safety net: once profit balance reaches +$3,100, EOD drawdown locks at +$100.
If account balance reaches $100 or less, Live account closes.
```

Live scaling:

| Level | Live Profit Balance | Contract Limit | DLL |
|---|---:|---:|---:|
| L1 | $0–$10,000 | 10 mini / 100 micro | No DLL |
| L2 | $10,000–$25,000 | 25 mini / 250 micro | $5,000 |
| L3 | $25,000–$50,000 | 30 mini / 300 micro | $10,000 |
| L4 | $50,000+ | Custom review | Custom review |

Checks TRUzT:

- This should be separate from simulated PA/Eval.
- No 25K/50K size selector for LPA unless user wants custom labels.
- Max contracts depends on mini vs micro.
- EOD drawdown cushion from live profit balance.
- DLL only Level 2+.
- Live mode should show stronger account warning and conservative block defaults.

---

## 6. Apex Second Chance

From Live FAQ requalification path:

```text
Minimum days to pass: 5
Consistency rule: 40%
Minimum daily profit: $250 per day
Drawdown type: Live intraday drawdown
Profit target: $4,000
Trailing drawdown: $2,000
Done-for-Now Loss Limit: $1,000
Flatten event: each negative $1,000 triggers flatten event; not locked out for the day
Contracts: 3 mini / 30 micro
```

This should be Phase 2+ unless Juan specifically needs it.

---

# Estado real que NinjaTrader puede leer

Confirmed via `NinjaTrader.Core.xml` and reflection on `NinjaTrader.Core.dll`.

`NinjaTrader.Cbi.Account` exposes:

```text
DisplayName / Name
AccountStatus
ConnectionStatus
LiquidationState
DailyLossLimit property
MaxOrderSize
MaxPositionSize
MinimumCashValue
Orders
Positions
Executions
Transactions
AccountItemUpdate event
PositionUpdate event
OrderUpdate event
ExecutionUpdate event
Account.Get(AccountItem, Currency)
```

`AccountItem` includes:

```text
BuyingPower
CashValue
Commission
GrossRealizedProfitLoss
NetLiquidation
RealizedProfitLoss
SodCashValue
SodLiquidatingValue
UnrealizedProfitLoss
TotalCashBalance
DailyLossLimit
WeeklyProfitLoss
WeeklyLossLimit
DailyProfitTrigger
WeeklyProfitTrigger
TrailingMaxDrawdown
```

Can be used automatically:

- selected NinjaTrader account;
- account status / liquidation-only state;
- open position qty for current instrument;
- live orders;
- realized/unrealized PnL if provider supplies AccountItem values;
- cash/net liquidation if provider supplies values;
- DailyLossLimit if provider supplies it;
- TrailingMaxDrawdown if provider supplies it;
- executions going forward / local history visible in NT.

Not reliable automatically without Apex dashboard/API/manual input:

- exact Apex product type: Intraday Eval vs EOD Eval vs PA vs LPA;
- exact account size / rule profile;
- last approved payout date/reset;
- payout count;
- highest profitable day since last payout;
- qualifying payout days if not tracked from start;
- official PA tier if Apex dashboard overrides or if local balance differs;
- whether `TrailingMaxDrawdown` is populated by Rithmic/Tradovate for each Apex product;
- exact EOD threshold unless provided by AccountItem or manually entered.

Conclusion: v1.16 must combine auto-read + manual profile inputs.

---

# Proposed UI in Chart Trader

Normal compact line:

```text
APEX 50K EOD PA L2
DD left $1,420 | DLL left $690
Risk $349 = 25% DD / 51% DLL
```

If OK:

```text
APEX OK  DD $1.4k | DLL $690
```

If warning:

```text
APEX WARN  Risk uses 72% DLL
```

If blocked:

```text
APEX BLOCK  Risk > DLL buffer
```

MORE details:

```text
APEX 50K EOD PA | Tier L2 | MaxQ 3 | DLL $1000
Bal $51,850 | EOD/DD $50,100 | DD left $1,750
DayPnL -$310 | DLL left $690 | Buffer $100
Consistency 48% | QDays 3/5 | Payout no
```

---

# Proposed settings

Group: `09 - Apex Risk`

```text
Apex Risk Enabled = false
Apex Account Type = Off / Intraday Eval / EOD Eval / Intraday PA / EOD PA / Live Prop / Second Chance / Custom
Apex Account Size = 25K / 50K / 100K / 150K
Apex Live Level = L1 / L2 / L3 / L4
Apex Rule Source = Auto + Manual / Manual Only
Apex Balance Source = NetLiquidation / CashValue + Unrealized / Manual
Apex Manual Current Balance = 0
Apex Manual Threshold = 0
Apex Manual Daily PnL = 0
Apex Manual Peak Balance = 0
Apex Safety Buffer $ = 100
Apex Warn Risk % of Cushion = 35
Apex Block Risk % of Cushion = 80
Apex Block SEND If Breach = true
Apex Include Commissions/Slippage = true
Apex Contract Counting = Conservative Same Count / Micro 10:1 / Custom
Apex Track Consistency = false
Apex Highest Profit Day Since Payout = 0
Apex Net Profit Since Payout = 0
Apex Qualifying Days = 0
Apex Payout Count = 0
```

---

# Validation logic

Inputs:

```text
plannedRisk = current TRUzT ActualRisk
plannedQty = current TRUzT SuggestedQuantity
existingQty = account current open qty across same account/instrument or all instruments depending mode
availableDrawdown = currentBalance - threshold - safetyBuffer
availableDLL = dllRemaining - safetyBuffer
maxContracts = rule profile max contracts for selected account/tier
```

Hard blocks if enabled:

```text
Apex Risk Enabled && Apex Block SEND If Breach && plannedQty + existingQty > maxContracts
Apex Risk Enabled && Apex Block SEND If Breach && plannedRisk > availableDrawdown
Apex Risk Enabled && Apex Block SEND If Breach && DLL applies && plannedRisk > availableDLL
Apex Risk Enabled && required manual threshold missing
Apex Risk Enabled && account status/liquidation state blocks trading
```

Warnings:

```text
plannedRisk > warn % of drawdown cushion
plannedRisk > warn % of DLL cushion
consistency above 50% for PA payout eligibility
qualifying days incomplete
balance below payout threshold
source data stale or manual required
```

Not a trade block by default:

```text
consistency not met
payout days incomplete
balance below payout threshold
```

Reason: those affect payout eligibility, not necessarily whether the next trade may be placed.

---

# Implementation scope

## v1.16.0 — Apex selector + advisory panel

- Add settings/enums/profile tables.
- Add `ApexRiskSnapshot` and `EvaluateApexRisk()`.
- Show `APEX OK/WARN/BLOCK` line in Chart Trader.
- Show details only in MORE unless blocked.
- No order-engine change except extra validation object computed read-only.
- Default `Apex Risk Enabled = false`.

## v1.16.1 — Optional SEND block

- Integrate Apex hard blocks into `ValidateOrderPlan` only when enabled.
- Add exact block reasons.
- Include Apex profile in ARM/SEND signature.

## v1.16.2 — Auto account data

- Read `Account.Get(AccountItem.NetLiquidation/CashValue/RealizedProfitLoss/UnrealizedProfitLoss/DailyLossLimit/TrailingMaxDrawdown)`.
- Subscribe to `AccountItemUpdate` safely.
- Fallback to manual values if provider returns 0/NaN/unavailable.

## v1.16.3 — PA consistency/trading journal

- Track daily realized PnL locally from executions after user enables.
- Manual reset after approved payout.
- Display consistency and payout readiness advisory.
- Do not attempt to reconstruct missing past history unless user enters it.

## v1.17+ — Apex cockpit polish

- Dedicated Apex section/panel.
- Presets tied to remaining DD/DLL, e.g. `Risk 10% DLL`, `Risk 20% DD`.
- Active trade mode shows projected balance if SL hit.
- Export/import profile template.

---

# Recommendation

Proceed with `v1.16.0` as advisory-first.

Do not implement full payout/consistency blocking in the first pass. That belongs after the core risk selector and DD/DLL calculations are stable.

Correct first visual outcome:

```text
TRUzT 1.16.0
● READY TO ARM
APEX 50K EOD PA L1 | DD $1.8k | DLL $760
PLAN LONG LIMIT | R $500 | Q1
...
```

Correct first safety outcome:

```text
● BLOCKED - APEX: qty 5 > max 3
```

or

```text
● BLOCKED - APEX: risk $500 > DLL left $420
```

---

# Open decision for Juan

Confirmar interpretación:

- `LPA` = Apex Live Prop Account / live account, not simulated PA.
- For simulated Apex Eval/PA, whether MNQ micro counting should be conservative same-count or 10 micros = 1 mini. Apex public wording varies by product; default should be conservative until verified in dashboard/account rejection behavior.

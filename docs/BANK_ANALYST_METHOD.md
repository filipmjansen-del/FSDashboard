# Bank Analyst View methodology

## Purpose

Bank Analyst View is a company-centric meeting-preparation workflow. It combines
one bank's current values, exact prior-FY changes, benchmark medians and up to
five available FY observations. It complements Company Fingerprint: it is a
structured earnings-to-balance review, not a percentile profile.

## Identity, period and benchmark

The workflow uses canonical FY observations only (`period_type = FY`,
`period_end_month = 12`). A bank is selected through canonical `entity_id`
(`bank:<regnr>`); `regnr` is the legal identifier and display names are never
join keys. No continuity is inferred across different legal entities.

The default benchmark is all banks observed in the selected FY. A saved peer
group is available only when its saved target bank and year match the current
selection; the target bank is included in that benchmark. The Benchmarkmedian is
calculated only from benchmark entities with an observed value for that metric.

YoY is the current value minus the same metric's value in the immediately
preceding FY. A missing current or prior observation produces a missing value,
not zero. Historical charts show at most the last five available observations;
they do not fill gaps.

## Included metrics

All monetary raw source values are reported in t.DKK and are displayed as DKK
billions where shown. “Reported” identifies a direct source observation;
“calculated” identifies a reproducible Databank calculation.

| Section | Metric | Status and definition |
| --- | --- | --- |
| Earnings | Netto renteindtægter | Calculated, reused from accounting income mix: `Res_Rind_RY - Res_Rudg_RY`. |
| Earnings | Netto gebyr- og provisionsindtægter | Calculated, reused from accounting income mix: `Res_GPi_RY - Res_GPu_RY`. |
| Earnings | Resultat før skat | Reported `Res_RfS_RY`, reused as the source input to `bank.roe_pre_tax`. |
| Profitability | Egenkapitalforrentning før skat | Calculated `bank.roe_pre_tax`; stable registry metric, baseline tested. |
| Profitability | Egenkapitalforrentning efter skat | Calculated `bank.roe_after_tax`; stable registry metric, baseline tested. |
| Efficiency | Indtjening pr. omkostningskrone | Calculated `bank.income_per_cost`; stable registry metric, baseline tested. |
| Growth / balance sheet | Udlån i alt | Calculated `Bal_BO_Autd + Bal_BO_Auta`, reusing the validated inputs of `bank.loans_to_equity`. |
| Growth / balance sheet | Udlån i forhold til egenkapital | Calculated `bank.loans_to_equity`; stable registry metric, baseline tested and neutral. |

`Aktiver i alt` (`Bal_BO_ATot`) is included in the overview as an existing
validated size measure used by Peer Selection. It is not a performance metric.

## Deferred metrics and limitations

Deposits, standalone operating expenses/cost-income, income-growth measures,
capital ratios and risk metrics are deliberately deferred: the current metric
framework does not yet contain a validated definition and documented source
mapping for them. No composite score, performance traffic light, recommendation
or synthetic continuity is produced.

The income-per-cost metric can be influenced by temporary income components.
Loans-to-equity is neutral and does not imply a good or bad risk outcome. The
loans measure requires both reported loan attributes; missing inputs remain
missing, which can reduce coverage.

## Validation

The workflow was validated for 2025 canonical entities `bank:3000` (Danske
Bank), `bank:8079` (AL Sydbank) and `bank:7858` (Jyske Bank, a mid-sized
Danish bank). For each case, the selected entity resolved through `regnr`, all
eight metric rows were produced, and historical observations were available.
For Danske Bank, current value, prior-year value, YoY and all-bank Benchmarkmedian
for reported `Res_RfS_RY` reconcile directly to the source observations.

Missing loan inputs were also checked for `bank:13290`; the current loans and
YoY values remain missing rather than becoming zero.

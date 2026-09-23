# Metric framework v2

Each active metric has a stable machine-readable ID in `METRIC_REGISTRY`.
Display names remain available through the legacy KPI catalogue for compatibility;
new analytical logic should use metric IDs. Every registry entry contains market,
display name, category, metric type, unit, direction, source type, calculation
type, validation status, definition, interpretation and caveat.

| Metric ID | Display name | Source / calculation |
| --- | --- | --- |
| `bank.income_per_cost` | Indtjening pr. omkostningskrone | Primary workbook / calculated |
| `bank.roe_pre_tax` | Egenkapitalforrentning før skat | Primary workbook / calculated |
| `bank.roe_after_tax` | Egenkapitalforrentning efter skat | Primary workbook / calculated |
| `bank.loans_to_equity` | Udlån i forhold til egenkapital | Primary workbook / calculated |
| `insurance.gross_claims_ratio` | Bruttoerstatningsprocent | Reported insurance KPI extract / reported |
| `insurance.gross_expense_ratio` | Bruttoomkostningsprocent | Reported insurance KPI extract / reported |
| `insurance.combined_ratio` | Combined ratio | Reported insurance KPI extract / reported |
| `insurance.operating_ratio` | Operating ratio | Reported insurance KPI extract / reported |
| `insurance.relative_runoff_result` | Relativt afløbsresultat | Reported insurance KPI extract / reported |
| `insurance.roe` | Egenkapitalforrentning i procent | Reported insurance KPI extract / reported |

`validation_status = baseline_tested` means the metric is covered by the
current baseline test suite; it is not an assertion of independent source
validation. Direction `neutral` remains non-performance-bearing.

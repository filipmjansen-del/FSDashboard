# Insurance Market Structure methodology

## Scope and source

This module measures the structure of the Danish insurance market from the FY
observations in `financial_services_long.xlsx`. The source attribute is
`Res_BP_BeY`, the extract's gross-premium field. Its source definition is
**Bruttopræmier** (result statement row 1.1). For non-life insurance, the
regulatory definition covers premiums due in the year for direct and indirect
insurance, net of cancelled premiums, specified bonus/premium rebates and
public charges collected with premiums. The related `Res_BoPr_BeY` field is the
separate bonus and premium-rebate result line, and is not an alternative market
value basis.

The reported values are in **t.DKK** (thousands of DKK). Consequently, the
application displays a total of 83,649,765 t.DKK as DKK 83.6 mia.; the table
and historical market-size axis retain the reported t.DKK unit. The source row
definition follows the [Danish financial-reporting regulation, §35 and Annex
4](https://www.retsinformation.dk/eli/lta/2025/943).

## Canonical input and population

The analytical engine accepts only canonical observations. It selects
`market = Forsikring`, `attribute_id = Res_BP_BeY`, `period_type = FY` and
`period_end_month = 12`; interim periods cannot be combined with FY data.

`entity_id` is the canonical market-scoped identity (`forsikring:<regnr>`).
`regnr` remains the legal identifier behind that identity; `display_name` is a
display attribute only. One source-of-truth row is produced for each reported
FY entity observation:

| Column | Meaning |
| --- | --- |
| `year` | FY fiscal year. |
| `entity_id` | Canonical identity based on `regnr`. |
| `display_name` | Source display name only. |
| `market_value` | Reported gross premiums in t.DKK. |
| `market_share` | Calculated included-population share. |
| `rank` | Descending included-population rank. |
| `included_flag` | True only for an observed, positive market value. |
| `exclusion_reason` | `missing_gross_premiums` or `non_positive_gross_premiums` where excluded. |

The annual population is exactly the rows with `included_flag = True`. Therefore
the entity count means **entities with observed positive gross premiums**, not
all licensed or otherwise known insurance entities. Missing observations are
never converted to zero.

## Calculations

For each year, market size is the sum of included `market_value` values and an
entity's market share is its market value divided by that total. CR1, CR3 and
CR5 are the cumulative shares of the largest 1, 3 and 5 included entities.
HHI is `10,000 × sum(market_share²)`, so it is reported on the 0--10,000 scale.
All measures use the same population; included annual shares reconcile to 100%
apart from rounding.

## Historical validation and limitations

The following independent FY checks were made directly against the reported
gross-premium observations. Market size is t.DKK; CR values are proportions.

| Year | Included entities | Market size | Shares | CR1 | CR3 | CR5 | HHI |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 2016 | 68 | 67,424,639 | 100.0% | 0.264043 | 0.617540 | 0.734881 | 1,504.191 |
| 2020 | 53 | 69,916,162 | 100.0% | 0.332851 | 0.672143 | 0.798312 | 1,837.018 |
| 2024 | 46 | 83,649,765 | 100.0% | 0.464567 | 0.721005 | 0.814028 | 2,561.684 |

2025 has 45 included entities and a market size of 75,819,299 t.DKK. It remains
explicitly marked as the known insurance coverage/data break required by D017;
it must not be treated as a like-for-like trend point until coverage is
reconciled.

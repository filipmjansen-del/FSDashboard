# Data audit

## Scope and method

Audited `financial_services_long.xlsx`, worksheet `in`, with
`scripts/audit_data.py`. The audit examines the source fields, population,
period values, identifier/name mappings, candidate observation-key duplicates,
attribute coverage, year coverage and material year-over-year coverage changes.

## Source evidence

- The workbook contains 126,339 observations for 2016--2025.
- Its fields are `Branche`, `ÅR`, `Måned`, `regnr`, `navn`, `Attribute` and
  `Value`.
- Every observation has `Måned = 12`. The current source therefore supports
  financial-year observations; it provides no evidence for consistent interim
  periods.
- There are no missing `regnr` values.
- The candidate observation key (`Branche`, `ÅR`, `Måned`, `regnr`,
  `Attribute`) has no duplicates.
- Within each market, the audit found no `regnr` mapping to multiple names and
  no name mapping to multiple registration numbers in this source extract.
  This is a source finding, not a reason to use names as analytical keys.

## Coverage

| Market | Observations | Entities, 2016 | Entities, 2025 | Attributes in 2025 |
| --- | ---: | ---: | ---: | ---: |
| Bank | 37,862 | 72 | 44 | 84 |
| Forsikring | 48,176 | 69 | 47 | 118 |
| Pension | 20,468 | 18 | 14 | 154 |
| Realkredit | 4,780 | 7 | 6 | 85 |
| Tværgående pensionskasser | 15,053 | 13 | 11 | 154 |

Using a 20% year-over-year threshold, the source has two aggregate coverage
breaks: Bank observations declined 21.15% in 2018, and Tværgående
pensionskasser observations increased 21.92% in 2017. These require visible
handling in later analytical work rather than imputation.

Insurance has 4,069 observations, 47 entities and 118 attributes in 2025,
compared with 4,331 observations, 48 entities and 118 attributes in 2024.
This aggregate check does not explain the known 2025 insurance data break.
Decision D017 remains authoritative: that break must be explicitly flagged in
the initial Insurance Market Structure implementation.

## Implications for the next phase

The observed source grain supports a canonical observation key of market,
fiscal year, period end/month, legal entity identifier and attribute. `Måned`
must remain explicit in the model even though the current extract is FY-only.
`regnr` remains the available legal entity identifier and `navn` remains a
display attribute. The workbook does not contain an explicit source/provenance
field, so Phase 3 must introduce provenance outside the current source rows.

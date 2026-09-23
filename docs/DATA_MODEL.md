# Canonical data model

## Evidence basis

This model follows the Phase 2 source audit. The current primary workbook has a
unique candidate key of `Branche`, `ÅR`, `Måned`, `regnr` and `Attribute`, and
every observed `Måned` is 12. The initial adapter therefore represents FY
observations only. It does not infer interim periods or convert missing values
to zero.

## Canonical observation

`data.canonical.to_canonical_observations` produces these fields:

| Field | Meaning |
| --- | --- |
| `market` | Source market (`Branche`). |
| `entity_id` | Stable deterministic identifier: normalized market plus `regnr`. |
| `regnr` | Preferred legal-entity identifier. |
| `display_name` | Source name; a display attribute, never a join key. |
| `fiscal_year` | Source year (`ÅR`). |
| `period_type` | Explicitly `FY` for the current extract. |
| `period_end_month` | Source period endpoint (`Måned`), currently 12. |
| `attribute_id` | Source attribute identifier. Metric IDs are introduced in Phase 4. |
| `value` | Reported source value, kept missing when source data is missing. |
| `source_id` | Provenance identifier for the source extract. |

The canonical observation key is `market`, `fiscal_year`, `period_type`,
`period_end_month`, `entity_id`, `attribute_id` and `source_id`. The adapter
rejects missing key fields, unsupported non-FY period endpoints and duplicate
canonical keys.

## Entity reference

`build_entity_reference` exposes `entity_id`, `regnr`, `display_name`,
`market`, `id_type`, `valid_from`, `valid_to` and `source_id`. It retains a
separate row for each observed display-name history, while the entity identity
remains stable through `entity_id` and `regnr`.

## Source provenance

The primary workbook supplies no row-level provenance field. The canonical
adapter records `source_id = financial_services_long`; future source adapters
must supply their own source IDs. This preserves traceability without adding a
database or silently blending reported and calculated metrics.

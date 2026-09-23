# Databank v2 - Architecture

## Product principle

Databank is an analytical platform for Financial Services.

Streamlit is a user interface, not the analytical asset itself.

Core flow:

Source data
-> Canonical data layer
-> Metric framework
-> Analytical modules
-> Streamlit views
-> Consulting output

## Current architecture

Primary source:
`financial_services_long.xlsx`

Current long-format fields:
- Branche
- ÅR
- Måned
- regnr
- navn
- Attribute
- Value

Separate reported KPI source:
`data/forsikring_kpis.csv`

Current analytical structure:

`kpis/`
- Bank KPI modules
- Insurance KPI modules
- Registry
- Shared calculation utilities

`dashboards/`
- Bank analytical modules
- Dashboard registry

`app.py`
- navigation
- styling
- generic KPI workspace
- homepage
- chart formatting

Phase 5.5 foundation direction:
- navigation, views, analytics and data access have separate responsibilities
- analytical modules are independently registered through a small common interface
- shared colors, typography, text colors, spacing and reusable UI components are centrally controlled
- adding an analytical module should not require changes to core application dispatch logic

## Current strengths

- modular KPI discovery
- modular dashboard discovery
- missing values are generally not interpreted as zero
- KPI definitions include interpretation and caveats
- reported and calculated metrics are partly distinguished
- reusable peer and company-analysis concepts already exist

## Current structural risks

1. Multiple source paths
   - main Excel source
   - separate insurance KPI CSV

2. Period grain is not explicit
   - `Måned` is not yet fully interpreted

3. Entity handling is inconsistent
   - some logic uses `regnr`
   - some joins also depend on name

4. Surrogate insurance IDs are not persistently mapped

5. Global KPI registry currently uses display name as key

6. Neutral metrics can be interpreted as performance in some analytical views

7. `app.py` contains too many responsibilities

8. Legacy KPI engine overlaps with newer KPI structure

## Target architecture

### 1. Source layer

Source-specific files and loaders.

Examples:
- FSA raw financial data
- reported KPI extracts
- future supplementary sources

Source formats may differ.

They must not propagate source-specific structure into analytics.

### 2. Canonical data layer

Target conceptual observation:

- market
- entity_id
- period
- attribute_id / metric_id
- value
- source_id

Canonical data is the interface consumed by metrics and analytics.

### 3. Entity layer

Preferred legal identifier:
`regnr`

Conceptual entity reference:

- entity_id
- regnr
- display_name
- market
- id_type
- valid_from
- valid_to
- source

Display names must not be analytical join keys.

### 4. Period layer

Target model:

- fiscal_year
- period_type
- period_end

Potential period types:
- FY
- H1
- Q1
- Q3

Exact implementation depends on Phase 2 data audit.

### 5. Metric framework

Every metric must have a stable machine ID.

Example:
`bank.roe_pre_tax`

Metric metadata contains:
- market
- category
- display name
- format
- unit
- direction
- source type
- calculation type
- validation status
- definition
- interpretation
- caveats

### 6. Analytics layer

Reusable analytical engines.

Examples:
- peer comparison
- company fingerprint
- growth analysis
- market structure
- analyst scorecard

Analytical engines should not depend directly on Streamlit.

### 7. Application layer

Streamlit handles:
- navigation
- input controls
- display
- tables
- charts
- exports

It should consume analytical outputs rather than contain core calculation logic.

### 8. Extensible module and UI foundation

The application foundation should expose a simple module interface and registry
for independently addable analytical modules. The registry owns discovery and
dispatch; each module owns its view and analytical wiring within the agreed
interfaces. Existing analytical logic is migrated incrementally and must retain
validated numerical outputs.

Shared UI styling is centralized in one UI layer covering colors, typography,
text colors, spacing and reusable components. New modules consume that layer
instead of duplicating style constants. This is deliberately a small internal
interface, not a general-purpose plugin framework.

## Target repository direction

Indicative only:

app.py

data/
- loaders/
- reference/
- validation/

metrics/
or
kpis/

analytics/
- peer_analysis.py
- market_structure.py
- bank_analyst.py

dashboards/
or
views/

ui/
- theme.py
- formatting.py
- navigation.py

scripts/
- audit_data.py

docs/

tests/

The exact folder migration should be incremental and should not be performed solely for aesthetic reasons.

## Architectural rules

1. Missing is not zero.
2. `regnr` is the preferred legal entity identifier.
3. Names are display attributes.
4. Reported metrics and calculated metrics must be distinguishable.
5. Every calculated metric must be reproducible.
6. Every important value must be traceable to a source.
7. Neutral metrics must not imply good or bad performance.
8. Known data breaks must remain visible.
9. Analytics should be testable without Streamlit.
10. UI changes must not silently change analytical methodology.

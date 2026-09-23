# Databank v2 - Decision Log

This file records decisions that should not be repeatedly reconsidered unless new evidence materially changes the underlying assumptions.

---

## D001 - Keep Streamlit

Status: LOCKED

Decision:
Continue using Streamlit as the application interface.

Reason:
The current prototype already works in Streamlit and there is no demonstrated business value from migrating frontend technology.

Revisit only if:
Streamlit materially prevents a required user workflow.

---

## D002 - Keep Python, pandas and Plotly

Status: LOCKED

Decision:
Use the existing Python analytics stack.

Reason:
It supports current analytical requirements and minimizes unnecessary migration.

---

## D003 - Long-format remains the core analytical principle

Status: LOCKED

Decision:
Continue using normalized long-format observations as the basis for the analytical layer.

Reason:
Long-format supports multiple markets, periods, entities and metrics consistently.

The exact canonical schema will be finalized after the data audit.

---

## D004 - `regnr` is the preferred legal entity identifier

Status: LOCKED

Decision:
Use registration number as the preferred legal entity identifier.

Reason:
Company names may change and are not reliable historical keys.

---

## D005 - Company name is a display attribute

Status: LOCKED

Decision:
Do not use company name as the primary analytical join key.

---

## D006 - Missing does not equal zero

Status: LOCKED

Decision:
Missing source observations must remain missing unless a documented methodology explicitly permits another treatment.

---

## D007 - Reported and calculated metrics remain distinct

Status: LOCKED

Decision:
A reported source KPI must be identifiable separately from a metric calculated by Databank.

Reason:
Users must be able to understand provenance and methodology.

---

## D008 - Neutral metrics do not represent performance

Status: LOCKED

Decision:
Metrics with direction `neutral` must not automatically produce good/bad performance colouring, ranking or composite performance scores.

Statistical position may be displayed if explicitly described as position rather than performance.

---

## D009 - Bank and Insurance are the initial priority markets

Status: LOCKED

Decision:
Do not prioritize Pension, Mortgage Credit or cross-sector pension funds until the Bank and Insurance analytical foundation is robust.

---

## D010 - No database migration yet

Status: LOCKED

Decision:
Remain file-based during the current development stage.

Reason:
Current scale does not justify database complexity.

Revisit when:
- file performance becomes limiting
- multiple simultaneous writers are required
- automated data pipelines require persistence
- operational deployment requires stronger storage controls

---

## D011 - Use cases before market expansion

Status: LOCKED

Decision:
Prioritize a smaller number of high-value analytical workflows over broad KPI and market coverage.

Initial flagship workflows:
- Insurance Market Structure
- Bank Analyst View

---

## D012 - `main` is stable

Status: LOCKED

Decision:
Material development occurs on a working branch and is merged after validation.

Initial branch:
`codex/databank-v2`

---

## D013 - Data model follows evidence

Status: LOCKED

Decision:
Do not finalize the period and observation model until the Phase 2 audit establishes the actual structure of `ÅR`, `Måned`, entities and attributes.

Reason:
The data model must reflect actual source behaviour rather than assumptions.

---

## D014 - FY may be the first supported analytical period

Status: PROVISIONAL

Decision:
If the source audit cannot support consistent interim periods, Databank v2 will initially expose FY analytics only.

The underlying model should not prevent later H1 or quarterly support.

---

## D015 - Metric IDs are stable and machine-readable

Status: LOCKED

Decision:
Metric registry keys must eventually move away from display names.

Example:
`bank.roe_pre_tax`

Display names may change without changing metric identity.

---

## D016 - Analytical logic should be independent of Streamlit

Status: LOCKED

Decision:
Core calculations and analytical engines should be callable and testable without rendering Streamlit components.

---

## D017 - Insurance Market Structure methodology

Status: LOCKED FOR INITIAL IMPLEMENTATION

Initial methodology:
- legal entity based on `regnr`
- same population for entity count, market shares, CR5 and HHI
- gross premiums as market-size metric
- HHI reported on 0-10,000 scale
- known 2025 data break explicitly identified
- source-of-truth table created before visualization

Change only if source validation demonstrates that the methodology must be altered.

---

## D018 - Existing income-mix module represents accounting income mix

Status: LOCKED

Decision:
Rename the current Bank `Indtjeningsmix` analysis to:

`Regnskabsmæssigt indtjeningsmix`

Reason:
It is based on financial-statement income components and must remain distinct from the future proprietary product/business income-mix model.

---

## D019 - Security and repository visibility

Status: PROVISIONAL

Decision:
The repository should ultimately be private because it contains internal analytical methodology and product logic.

Do not change visibility until Streamlit private-repository access has been tested successfully.

---

## D020 - Product test for new functionality

Status: LOCKED

Every proposed feature should be assessed against:

Does this make it faster and more robust to move from standardized Financial Services data to a documented analysis that can be used in a client or market dialogue?

If not, it is normally lower priority.

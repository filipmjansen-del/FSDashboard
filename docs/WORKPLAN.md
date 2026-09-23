# Databank v2 - Workplan

## Objective

Develop the current Financial Services Streamlit prototype into a robust analytical platform that can move reproducibly from:

Data -> Definition -> Metric -> Analysis -> Interpretation -> Consulting output

Streamlit remains the user interface. The analytical asset must not depend on Streamlit for its core logic.

## Primary use cases

1. Company Intelligence
   - Peer selection
   - Company fingerprint
   - Historical performance
   - Meeting preparation

2. Market Intelligence
   - Market size
   - Market shares
   - Consolidation
   - Concentration
   - Structural development

3. Performance Analytics
   - Earnings
   - Profitability
   - Efficiency
   - Growth
   - Capital
   - Risk

## Scope

Initial priority:
- Bank
- Insurance

Not currently prioritized:
- Pension expansion
- Mortgage credit expansion
- New frontend framework
- Database migration
- Automated FSA scraping
- AI assistant inside the application
- Major design exercise

## Execution principles

Priority order:

1. Correctness
2. Analytical usefulness
3. Presentation

Development loop:

Inspect -> Implement -> Validate -> Fix -> Commit -> Report -> Continue

Do not perform broad repository scans unless necessary.
Read only the governance documents and files relevant to the current task.

Stop for user input only when:
- a material business or methodology decision is required
- authoritative sources conflict
- an irreversible change is required

## Phases

### Phase 0 - Working baseline
Status: COMPLETE

Tasks:
- Create branch `codex/databank-v2`
- Add `docs/WORKPLAN.md`
- Add `docs/ARCHITECTURE.md`
- Add `docs/DECISIONS.md`

Definition of Done:
- Main remains unchanged
- Working branch exists
- A new contributor can understand objective, architecture and next step from the three documents

Next action:
Create working branch and governance documentation.

---

### Phase 1 - Engineering baseline
Status: COMPLETE

Tasks:
- Remove tracked Python cache files
- Extend `.gitignore`
- Move Streamlit config to `.streamlit/config.toml`
- Remove or migrate obsolete `kpi_engine.py`
- Repair existing tests
- Establish minimal test structure
- Add GitHub Actions CI
- Run baseline smoke tests

Required validation:
- Application imports
- Data loader works
- KPI registry loads
- Dashboard registry loads
- Tests pass
- Existing application functionality remains intact

Definition of Done:
CI green and no known baseline engineering errors.

---

### Phase 2 - Data audit
Status: COMPLETE

Create:
`scripts/audit_data.py`

Audit:
- markets
- years
- periods
- entity counts
- missing registration numbers
- registration number to name mappings
- name to registration number mappings
- duplicate canonical candidates
- attribute coverage
- year-by-year coverage
- significant coverage breaks

Critical questions:
1. What does `Måned` represent?
2. What is the actual observation grain?
3. How should entities be tracked historically?
4. Which known data breaks must be represented explicitly?

Definition of Done:
The actual data structure is documented from evidence, not assumptions.

---

### Phase 3 - Canonical data model
Status: NOT STARTED

Define:
- entity
- period
- observation
- source
- provenance

Requirements:
- `regnr` is the preferred legal entity identifier
- display name is not a join key
- surrogate IDs are persistent
- canonical observation key is unique
- source provenance is available
- period handling is explicit

Definition of Done:
No duplicate canonical observation keys and data model documented.

---

### Phase 4 - Metric framework v2
Status: NOT STARTED

Introduce stable metric IDs, e.g.:
- `bank.roe_pre_tax`
- `bank.net_interest_income`
- `insurance.combined_ratio`

Required metadata:
- metric_id
- market
- display_name
- category
- metric_type
- unit
- direction
- source_type
- calculation_type
- validation_status

Categories:
- income
- cost
- profitability
- efficiency
- growth
- capital
- risk
- balance_sheet
- market_structure

Definition of Done:
Every active metric has a unique ID, documented definition, source and interpretation logic.

---

### Phase 5 - Migrate existing analytics
Status: NOT STARTED

Migrate without adding new functionality:
- KPI workspace
- Peer selection
- Company fingerprint
- Peer heatmap
- Growth vs profitability
- Accounting income mix

Required corrections:
- entity joins use canonical entity ID
- neutral metrics do not imply performance
- profitability selector only uses profitability metrics
- rename current `Indtjeningsmix` to `Regnskabsmæssigt indtjeningsmix`

Definition of Done:
Existing analytical outputs are reproduced without unexplained numerical changes.

---

### Phase 6 - Market Structure
Status: NOT STARTED

Initial implementation:
Insurance

Metrics:
- number of legal entities
- market size
- market shares
- CR1
- CR3
- CR5
- HHI

Method:
- legal entity based on `regnr`
- same population for entity count, market shares, CR5 and HHI
- gross premiums as initial insurance market-size metric
- HHI scale 0-10,000
- known data breaks explicitly flagged

Required source-of-truth table:
- year
- entity_id
- display_name
- market_value
- market_share
- rank
- included_flag
- exclusion_reason

Definition of Done:
At least three historical years independently validated.

---

### Phase 7 - Bank Analyst View
Status: NOT STARTED

Analytical structure:

Earnings:
- net interest income
- fee income
- other income
- profit before tax

Efficiency:
- operating expenses
- cost/income
- income per cost krone

Profitability:
- ROE before tax
- ROE after tax

Growth:
- loans
- deposits
- income growth

Capital and risk:
- only validated metrics

For each core metric show:
- current value
- YoY development
- peer comparison

Definition of Done:
Workflow materially improves preparation for at least:
- Danske Bank
- AL Sydbank
- one mid-sized bank

---

### Phase 8 - Navigation and application refactor
Status: NOT STARTED

Move away from one large `app.py`.

Target areas:
- UI utilities
- navigation
- formatting
- data layer
- views
- analytics

Navigation should increasingly reflect analytical jobs rather than only data categories.

---

### Phase 9 - Output layer
Status: NOT STARTED

Add:
- table export
- chart export
- source and methodology visibility
- slide-ready analytical output where valuable

Definition of Done:
A Databank analysis can be reused in consulting work without reconstructing the analysis manually.

---

### Phase 10 - Deployment and security
Status: NOT STARTED

Tasks:
- validate private repository deployment with Streamlit
- make repository private once access is confirmed
- review Streamlit security configuration
- test production deployment

Definition of Done:
Private repository and stable Streamlit deployment.

---

### Phase 11 - Documentation and handover
Status: NOT STARTED

Required documentation:
- WORKPLAN.md
- ARCHITECTURE.md
- DECISIONS.md
- DATA_MODEL.md
- KPI_GUIDE.md
- MARKET_STRUCTURE_METHOD.md
- BANK_ANALYST_METHOD.md

Definition of Done:
Another colleague or AI agent can continue development without reconstructing undocumented assumptions.

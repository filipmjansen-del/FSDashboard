# Financial Services Intelligence — Streamlit MVP

This first version implements one banking KPI from the supplied annual-account dataset:

**Indtjening pr. omkostningskrone**

```text
(Res_RGTot_RY + Res_Kreg_RY + Res_Xdi_RY + Res_Rat_RY)
/
(Res_UPa_RY + Res_ImMa_RY + Res_Xdu_RY + Res_UGn_RY)
```

No missing input is assumed to be zero. The KPI is only calculated when all eight source attributes are available and the denominator is non-zero.

## Views

- Bank overview
- KPI explorer
- Bank profile
- Sector comparison
- Data quality

## Run locally

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```

## Deploy with Streamlit Community Cloud

1. Create a GitHub repository.
2. Upload this project while preserving its folder structure.
3. In Streamlit Community Cloud, create a new app from the repository.
4. Set the main file to `app.py`.
5. Deploy.

## Adding the next KPI

Add the user-supplied definition to `src/kpi_engine.py`, then expose it through the app. Do not infer financial formulas from labels or account codes.

# Financial Services Intelligence

A Streamlit dashboard for comparing financial institutions by market, year, and company. KPI modules live under `kpis/<market>/` and are discovered automatically by `kpis/registry.py`.

## Markets and KPIs

- **Bank:** income per expense krone, return on equity before and after tax, and loans relative to equity.
- **Forsikring:** bruttoerstatningsprocent, bruttoomkostningsprocent, combined ratio, operating ratio, relativt afløbsresultat, and egenkapitalforrentning.
- **Realkredit, Pension, Tværgående pensionskasser:** market navigation is available; KPI modules can be added as source definitions are confirmed.

The six Forsikring definitions come from the supplied `Finanstilsynet_noegletal_master.xlsx` and [the underlying regulation, Bilag 10](https://www.retsinformation.dk/api/pdf/249994). The dashboard displays the reported company-level values from the companion `LongFormatDataMedKPIForSkadeOgBank.csv`, extracted into `data/forsikring_kpis.csv`. The source's sector-average rows are excluded; dashboard sector statistics are calculated from the displayed companies. Percentage-point values in the source are divided by 100 for the app's percentage formatter. Missing reported values remain missing.

For definitions, examples, interpretation direction, and help reading every graph, see [KPI-guiden](docs/KPI_GUIDE.md).

The master workbook notes that its public database fields have not yet been reconciled 1:1 against Finanstilsynet's 2025 pivot file. The displayed values are therefore identified as reported source values rather than re-calculated from the raw account codes. Registration numbers missing in the source are filled from a unique historical company-name match when available; otherwise the extract assigns a stable negative surrogate ID.

To regenerate the checked-in extract, run `python scripts/import_forsikring_kpis.py <path-to-companion-csv>`.

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

## Add a KPI

Create a module in the appropriate `kpis/<market>/` package with `KPI_META` and `calculate(raw)`. Calculations should leave incomplete input as missing. Use documented source-field definitions rather than inferring formulas from account labels or codes.

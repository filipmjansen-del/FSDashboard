"""Extract the six insurance KPIs from the companion long-format source CSV.

Usage: python scripts/import_forsikring_kpis.py path/to/LongFormatDataMedKPIForSkadeOgBank.csv
"""

from pathlib import Path
import sys

import pandas as pd


SOURCE_NAMES = {
    "Bruttoerstatningsprocent (Loss ratio)",
    "Bruttoomkostningsprocent (Expense ratio)",
    "Combined ratio",
    "Operating ratio",
    "Relativt afløbsresultat",
    "Egenkapitalforrentning i pct. (Return on equity)",
}
OUTPUT = Path(__file__).resolve().parents[1] / "data" / "forsikring_kpis.csv"


def import_kpis(source: Path, output: Path = OUTPUT) -> pd.DataFrame:
    data = pd.read_csv(source, sep=";", encoding="utf-8-sig", low_memory=False)
    rows = data.loc[
        (data["Data"] == "KPI")
        & (data["Branche"] == "Forsikring")
        & (data["ÅR"] >= 2016)
        & data["Attribute"].isin(SOURCE_NAMES)
        & ~data["navn"].str.startswith("XX -", na=False),
        ["ÅR", "Måned", "regnr", "navn", "Attribute", "Value"],
    ].copy()
    rows["navn"] = rows["navn"].str.strip()
    rows = rows.drop_duplicates()
    rows["Value"] = pd.to_numeric(
        rows["Value"].astype(str).str.replace(",", ".", regex=False),
        errors="coerce",
    )

    # The companion file omits registration numbers for most 2023-2025 KPIs.
    # Reuse an earlier number only when the same name has one unambiguous match.
    known = rows.dropna(subset=["regnr"]).groupby("navn")["regnr"].agg(
        lambda values: values.iloc[0] if values.nunique() == 1 else float("nan")
    )
    rows["regnr"] = rows["regnr"].fillna(rows["navn"].map(known))
    missing_names = sorted(rows.loc[rows["regnr"].isna(), "navn"].unique())
    surrogate = {name: -i for i, name in enumerate(missing_names, start=1)}
    rows["regnr"] = rows["regnr"].fillna(rows["navn"].map(surrogate)).astype("int64")

    # Two distinct Codan registration numbers have the same display name in
    # 2021. Distinguish them in the company selector rather than merging them.
    duplicates = rows[["ÅR", "navn", "regnr"]].drop_duplicates()
    duplicates = duplicates[duplicates.duplicated(["ÅR", "navn"], keep=False)]
    duplicate_keys = set(zip(duplicates["ÅR"], duplicates["navn"]))
    mask = [
        (year, name) in duplicate_keys
        for year, name in zip(rows["ÅR"], rows["navn"])
    ]
    rows.loc[mask, "navn"] = (
        rows.loc[mask, "navn"] + " (" + rows.loc[mask, "regnr"].astype(str) + ")"
    )

    key = ["ÅR", "regnr", "Attribute"]
    if rows.duplicated(key).any():
        conflicts = rows.loc[rows.duplicated(key, keep=False), key + ["navn", "Value"]]
        raise ValueError(f"Duplicate company-year-KPI values remain in source:\n{conflicts.to_string(index=False)}")
    output.parent.mkdir(parents=True, exist_ok=True)
    rows.sort_values(key).to_csv(output, index=False, encoding="utf-8")
    return rows


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Provide the companion KPI CSV path")
    result = import_kpis(Path(sys.argv[1]))
    print(f"Wrote {len(result)} KPI rows to {OUTPUT}")

"""Read the reported insurance KPIs from the checked-in source extract."""

from functools import lru_cache
from pathlib import Path

import pandas as pd


SOURCE = Path(__file__).resolve().parents[2] / "data" / "forsikring_kpis.csv"


@lru_cache(maxsize=1)
def _reported_kpis():
    return pd.read_csv(SOURCE, dtype={"regnr": "int64"})


def calculate_reported_kpi(_raw, kpi_name, source_name):
    """Return reported percentage points as decimal ratios for the app."""
    result = _reported_kpis().loc[lambda df: df["Attribute"] == source_name].copy()
    result["Branche"] = "Forsikring"
    result["KPI"] = kpi_name
    result["KPI_Value"] = pd.to_numeric(result["Value"], errors="coerce") / 100
    result["CompleteInputs"] = result["KPI_Value"].notna()
    return result

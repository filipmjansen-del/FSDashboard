from pathlib import Path
import pandas as pd

from src.data_loader import load_raw_data
from src.kpi_engine import calculate_ratio_kpi

DATA = Path(__file__).parent / "data" / "financial_services_long.xlsx"
KPI = "Indtjening pr. omkostningskrone"

raw = load_raw_data(DATA)
result = calculate_ratio_kpi(raw, KPI)
valid = result.dropna(subset=["KPI_Value"])

assert not valid.empty
assert valid["Denominator"].ne(0).all()
assert valid["CompleteInputs"].all()
assert valid["KPI_Value"].notna().all()
print("rows", len(result))
print("valid", len(valid))
print("years", int(result["ÅR"].min()), int(result["ÅR"].max()))
print(valid.head(10).to_string(index=False))

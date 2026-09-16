from __future__ import annotations

from pathlib import Path
import pandas as pd

REQUIRED_COLUMNS = ["Branche", "ÅR", "Måned", "regnr", "navn", "Attribute", "Value"]


def load_raw_data(path: str | Path) -> pd.DataFrame:
    df = pd.read_excel(path, sheet_name="in", engine="openpyxl")
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    df = df[REQUIRED_COLUMNS].copy()
    df["ÅR"] = pd.to_numeric(df["ÅR"], errors="coerce").astype("Int64")
    df["regnr"] = pd.to_numeric(df["regnr"], errors="coerce").astype("Int64")
    df["Value"] = pd.to_numeric(df["Value"], errors="coerce")
    return df

"""Reusable access to the application's canonical workbook source."""

from pathlib import Path

import pandas as pd

from data_loader import load_raw_data


DEFAULT_DATA_PATH = Path(__file__).parents[1] / "financial_services_long.xlsx"
INSURANCE_MARKET_STRUCTURE_FP_PATH = Path(__file__).parents[1] / "data" / "forsikring_market_structure_fp.csv"


def load_financial_services_data(path: str | Path = DEFAULT_DATA_PATH):
    """Load the existing canonical workbook without UI or analytical concerns."""
    return load_raw_data(path)


def load_insurance_market_structure_fp(path: str | Path = INSURANCE_MARKET_STRUCTURE_FP_PATH) -> pd.DataFrame:
    """Load the source-specific F&P non-life market-structure extract."""
    return pd.read_csv(path)

"""Reusable access to the application's canonical workbook source."""

from pathlib import Path

from data_loader import load_raw_data


DEFAULT_DATA_PATH = Path(__file__).parents[1] / "financial_services_long.xlsx"


def load_financial_services_data(path: str | Path = DEFAULT_DATA_PATH):
    """Load the existing canonical workbook without UI or analytical concerns."""
    return load_raw_data(path)

"""Canonical, Streamlit-independent representations of source observations."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from data_loader import load_raw_data


SOURCE_ID = "financial_services_long"
CANONICAL_OBSERVATION_KEY = [
    "market",
    "fiscal_year",
    "period_type",
    "period_end_month",
    "entity_id",
    "attribute_id",
    "source_id",
]
CANONICAL_OBSERVATION_COLUMNS = [
    "market",
    "entity_id",
    "regnr",
    "display_name",
    "fiscal_year",
    "period_type",
    "period_end_month",
    "attribute_id",
    "value",
    "source_id",
]


def _entity_id(market: pd.Series, regnr: pd.Series) -> pd.Series:
    """Return a deterministic persistent ID scoped to a legal-entity market."""
    market_id = market.str.casefold().str.replace(r"[^a-z0-9]+", "-", regex=True).str.strip("-")
    return market_id + ":" + regnr.astype("Int64").astype(str)


def to_canonical_observations(raw: pd.DataFrame, source_id: str = SOURCE_ID) -> pd.DataFrame:
    """Translate audited FY source observations without imputing missing values."""
    required = ["Branche", "ÅR", "Måned", "regnr", "navn", "Attribute", "Value"]
    missing = [column for column in required if column not in raw.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    observations = raw[required].copy()
    observations["Måned"] = pd.to_numeric(observations["Måned"], errors="coerce").astype("Int64")
    observations["regnr"] = pd.to_numeric(observations["regnr"], errors="coerce").astype("Int64")
    observations["ÅR"] = pd.to_numeric(observations["ÅR"], errors="coerce").astype("Int64")

    if observations[["Branche", "ÅR", "Måned", "regnr", "Attribute"]].isna().any().any():
        raise ValueError("Canonical observations require market, period, regnr and attribute.")
    if not observations["Måned"].eq(12).all():
        raise ValueError("The current canonical adapter supports FY observations only (Måned = 12).")

    canonical = pd.DataFrame(
        {
            "market": observations["Branche"],
            "entity_id": _entity_id(observations["Branche"], observations["regnr"]),
            "regnr": observations["regnr"],
            "display_name": observations["navn"],
            "fiscal_year": observations["ÅR"],
            "period_type": "FY",
            "period_end_month": observations["Måned"],
            "attribute_id": observations["Attribute"],
            "value": observations["Value"],
            "source_id": source_id,
        }
    )
    if canonical.duplicated(CANONICAL_OBSERVATION_KEY).any():
        raise ValueError("Duplicate canonical observation keys found.")
    return canonical[CANONICAL_OBSERVATION_COLUMNS]


def build_entity_reference(canonical_observations: pd.DataFrame) -> pd.DataFrame:
    """Build legal-entity display-name histories from canonical observations."""
    required = {"market", "entity_id", "regnr", "display_name", "fiscal_year", "source_id"}
    missing = sorted(required.difference(canonical_observations.columns))
    if missing:
        raise ValueError(f"Missing canonical columns: {missing}")

    entity_reference = (
        canonical_observations.groupby(
            ["market", "entity_id", "regnr", "display_name", "source_id"], dropna=False
        )["fiscal_year"]
        .agg(valid_from="min", valid_to="max")
        .reset_index()
    )
    entity_reference["id_type"] = "regnr"
    return entity_reference[
        ["entity_id", "regnr", "display_name", "market", "id_type", "valid_from", "valid_to", "source_id"]
    ].sort_values(["market", "entity_id", "valid_from"]).reset_index(drop=True)


def load_canonical_observations(path: str | Path, source_id: str = SOURCE_ID) -> pd.DataFrame:
    """Load the current primary workbook into the canonical observation layer."""
    return to_canonical_observations(load_raw_data(path), source_id=source_id)

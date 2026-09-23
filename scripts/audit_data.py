"""Audit the source workbook before defining Databank's canonical data model."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd


REQUIRED_COLUMNS = ["Branche", "ÅR", "Måned", "regnr", "navn", "Attribute", "Value"]
CANONICAL_CANDIDATE_KEY = ["Branche", "ÅR", "Måned", "regnr", "Attribute"]
SIGNIFICANT_CHANGE = 0.20


def _records(frame: pd.DataFrame) -> list[dict]:
    return json.loads(frame.to_json(orient="records", force_ascii=False))


def _coverage_breaks(year_coverage: pd.DataFrame) -> list[dict]:
    results = []
    for market, group in year_coverage.groupby("market", sort=True):
        group = group.sort_values("year").copy()
        for measure in ("entities", "attributes", "observations"):
            group[f"{measure}_change"] = group[measure].pct_change()
            for row in group.loc[group[f"{measure}_change"].abs() >= SIGNIFICANT_CHANGE].itertuples():
                results.append(
                    {
                        "market": market,
                        "year": int(row.year),
                        "measure": measure,
                        "change_from_prior_year": round(float(getattr(row, f"{measure}_change")), 4),
                    }
                )
    return results


def audit_data(path: str | Path) -> dict:
    """Return evidence about the source workbook's observation structure."""
    source_path = Path(path)
    raw = pd.read_excel(source_path, sheet_name="in", engine="openpyxl")
    missing_columns = [column for column in REQUIRED_COLUMNS if column not in raw.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    data = raw[REQUIRED_COLUMNS].copy()
    data["ÅR"] = pd.to_numeric(data["ÅR"], errors="coerce")
    data["Måned"] = pd.to_numeric(data["Måned"], errors="coerce")
    data["regnr"] = pd.to_numeric(data["regnr"], errors="coerce")

    entity_counts = (
        data.groupby(["Branche", "ÅR"], dropna=False)["regnr"]
        .nunique()
        .reset_index(name="entities")
        .rename(columns={"Branche": "market", "ÅR": "year"})
        .sort_values(["market", "year"])
    )
    year_coverage = (
        data.groupby(["Branche", "ÅR"], dropna=False)
        .agg(
            observations=("Value", "size"),
            entities=("regnr", "nunique"),
            attributes=("Attribute", "nunique"),
            missing_regnr=("regnr", lambda values: int(values.isna().sum())),
        )
        .reset_index()
        .rename(columns={"Branche": "market", "ÅR": "year"})
        .sort_values(["market", "year"])
    )
    regnr_name_conflicts = (
        data.dropna(subset=["regnr", "navn"])
        .groupby(["Branche", "regnr"], as_index=False)["navn"]
        .nunique()
        .query("navn > 1")
        .rename(columns={"Branche": "market", "navn": "distinct_names"})
        .sort_values(["market", "regnr"])
    )
    name_regnr_conflicts = (
        data.dropna(subset=["regnr", "navn"])
        .groupby(["Branche", "navn"], as_index=False)["regnr"]
        .nunique()
        .query("regnr > 1")
        .rename(columns={"Branche": "market", "regnr": "distinct_regnrs"})
        .sort_values(["market", "navn"])
    )
    duplicate_candidates = (
        data.loc[data.duplicated(CANONICAL_CANDIDATE_KEY, keep=False), CANONICAL_CANDIDATE_KEY]
        .value_counts(dropna=False)
        .reset_index(name="observations")
        .sort_values(CANONICAL_CANDIDATE_KEY)
    )
    attribute_coverage = (
        data.groupby(["Branche", "Attribute"], dropna=False)
        .agg(
            observations=("Value", "size"),
            years=("ÅR", "nunique"),
            entities=("regnr", "nunique"),
        )
        .reset_index()
        .rename(columns={"Branche": "market", "Attribute": "attribute"})
        .sort_values(["market", "attribute"])
    )

    return {
        "source": str(source_path),
        "rows": int(len(data)),
        "columns": REQUIRED_COLUMNS,
        "markets": _records(
            data.groupby("Branche", dropna=False).size().reset_index(name="observations")
            .rename(columns={"Branche": "market"})
            .sort_values("market")
        ),
        "years": sorted(int(year) for year in data["ÅR"].dropna().unique()),
        "period_values": _records(
            data["Måned"].value_counts(dropna=False).rename_axis("month").reset_index(name="observations")
            .sort_values("month")
        ),
        "entity_counts": _records(entity_counts),
        "missing_registration_numbers": int(data["regnr"].isna().sum()),
        "registration_number_to_name_conflicts": _records(regnr_name_conflicts),
        "name_to_registration_number_conflicts": _records(name_regnr_conflicts),
        "duplicate_canonical_candidates": _records(duplicate_candidates),
        "attribute_coverage": _records(attribute_coverage),
        "year_coverage": _records(year_coverage),
        "significant_coverage_breaks": _coverage_breaks(year_coverage),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "path",
        nargs="?",
        type=Path,
        default=Path(__file__).parents[1] / "financial_services_long.xlsx",
    )
    args = parser.parse_args()
    print(json.dumps(audit_data(args.path), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

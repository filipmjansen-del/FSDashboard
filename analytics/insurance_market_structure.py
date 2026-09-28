"""Insurance market-structure calculations based on reported gross premiums."""

from __future__ import annotations

import pandas as pd


GROSS_PREMIUM_ATTRIBUTE = "Res_BP_BeY"
GROSS_PREMIUM_LABEL = "Bruttopræmier"
MARKET_VALUE_UNIT = "tDKK"
KNOWN_DATA_BREAK_YEARS = {2025}
SOURCE_COLUMNS = [
    "year",
    "entity_id",
    "display_name",
    "market_value",
    "market_share",
    "rank",
    "included_flag",
    "exclusion_reason",
]


def build_market_structure_table(canonical_observations: pd.DataFrame) -> pd.DataFrame:
    """Build the canonical population and market-share table for insurance FY data."""
    required_columns = {
        "market", "entity_id", "display_name", "fiscal_year", "period_type",
        "period_end_month", "attribute_id", "value",
    }
    missing_columns = sorted(required_columns.difference(canonical_observations.columns))
    if missing_columns:
        raise ValueError(f"Missing canonical columns: {missing_columns}")

    source = canonical_observations.loc[
        (canonical_observations["market"] == "Forsikring")
        & (canonical_observations["attribute_id"] == GROSS_PREMIUM_ATTRIBUTE)
        & (canonical_observations["period_type"] == "FY")
        & (canonical_observations["period_end_month"] == 12),
        ["fiscal_year", "entity_id", "display_name", "value"],
    ].copy()
    source.columns = ["year", "entity_id", "display_name", "market_value"]
    source["year"] = pd.to_numeric(source["year"], errors="coerce").astype("Int64")
    source["market_value"] = pd.to_numeric(source["market_value"], errors="coerce")

    if source.duplicated(["year", "entity_id"]).any():
        raise ValueError("Duplicate insurance gross-premium observations per year and regnr.")

    source["included_flag"] = source["market_value"].gt(0)
    source["exclusion_reason"] = pd.NA
    source.loc[source["market_value"].isna(), "exclusion_reason"] = "missing_gross_premiums"
    source.loc[source["market_value"].notna() & source["market_value"].le(0), "exclusion_reason"] = (
        "non_positive_gross_premiums"
    )

    included = source["included_flag"]
    totals = source.loc[included].groupby("year")["market_value"].transform("sum")
    source.loc[included, "market_share"] = source.loc[included, "market_value"] / totals
    source["rank"] = pd.NA
    source.loc[included, "rank"] = source.loc[included].groupby("year")["market_value"].rank(
        method="first", ascending=False
    )
    source["rank"] = source["rank"].astype("Int64")
    return source[SOURCE_COLUMNS].sort_values(["year", "included_flag", "rank", "entity_id"], ascending=[True, False, True, True]).reset_index(drop=True)


def summarize_market_structure(source_table: pd.DataFrame) -> pd.DataFrame:
    """Calculate annual concentration metrics from one consistent included population."""
    included = source_table.loc[source_table["included_flag"]].copy()
    summaries = []
    for year, group in included.groupby("year", sort=True):
        shares = group.sort_values("rank")["market_share"]
        summaries.append(
            {
                "year": int(year),
                "entity_count": int(len(group)),
                "market_size": float(group["market_value"].sum()),
                "cr1": float(shares.head(1).sum()),
                "cr3": float(shares.head(3).sum()),
                "cr5": float(shares.head(5).sum()),
                "hhi": float((shares.pow(2).sum()) * 10_000),
                "excluded_entities": int((source_table["year"] == year).sum() - len(group)),
                "known_data_break": int(year) in KNOWN_DATA_BREAK_YEARS,
            }
        )
    return pd.DataFrame(summaries)

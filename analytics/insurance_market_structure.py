"""Insurance market-structure calculations based on reported gross premiums."""

from __future__ import annotations

import pandas as pd


GROSS_PREMIUM_ATTRIBUTE = "Res_BP_BeY"
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


def build_market_structure_table(raw: pd.DataFrame) -> pd.DataFrame:
    """Build the canonical population and market-share table for insurance."""
    source = raw.loc[
        (raw["Branche"] == "Forsikring")
        & (raw["Attribute"] == GROSS_PREMIUM_ATTRIBUTE),
        ["ÅR", "regnr", "navn", "Value"],
    ].copy()
    source.columns = ["year", "entity_id", "display_name", "market_value"]
    source["year"] = pd.to_numeric(source["year"], errors="coerce").astype("Int64")
    source["entity_id"] = pd.to_numeric(source["entity_id"], errors="coerce").astype("Int64")
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

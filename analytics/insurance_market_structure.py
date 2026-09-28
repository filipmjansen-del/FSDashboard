"""Insurance market structure calculated from F&P reported market shares."""

from __future__ import annotations

import pandas as pd


SOURCE_COLUMNS = [
    "year", "quarter", "period_end_month", "entity_name", "market_value",
    "market_total", "market_share", "source_market_share_pct", "rank",
]


def build_market_structure_table(fp_source: pd.DataFrame) -> pd.DataFrame:
    """Validate F&P's market-actor source and calculate ranks only."""
    required = {
        "market", "segment", "year", "quarter", "period_end_month", "entity_name",
        "market_value_t_dkk", "market_total_t_dkk", "market_share", "source_market_share_pct",
    }
    missing = sorted(required.difference(fp_source.columns))
    if missing:
        raise ValueError(f"Missing F&P market-structure columns: {missing}")
    source = fp_source.loc[
        (fp_source["market"] == "Forsikring")
        & (fp_source["segment"] == "Skadeforsikring i alt")
    ].copy().rename(columns={"market_value_t_dkk": "market_value", "market_total_t_dkk": "market_total"})
    for column in ("year", "quarter", "period_end_month", "market_value", "market_total", "market_share", "source_market_share_pct"):
        source[column] = pd.to_numeric(source[column], errors="coerce")
    if source.duplicated(["year", "quarter", "entity_name"]).any():
        raise ValueError("Duplicate F&P market-structure rows per year, quarter and entity_name.")
    if source[["year", "quarter", "entity_name", "market_total", "market_share"]].isna().any().any():
        raise ValueError("F&P market-structure rows must retain period, actor, total and reported share.")
    if source.groupby(["year", "quarter"])["market_total"].nunique().gt(1).any():
        raise ValueError("Inconsistent F&P market_total_t_dkk within a period.")
    share_sums = source.groupby(["year", "quarter"])["market_share"].sum()
    if not share_sums.between(0.99, 1.01).all():
        raise ValueError("F&P reported market shares must reconcile to approximately 100% per period.")
    source["rank"] = source.groupby(["year", "quarter"])["market_share"].rank(method="first", ascending=False).astype("Int64")
    source["year"] = source["year"].astype("Int64")
    source["quarter"] = source["quarter"].astype("Int64")
    source["period_end_month"] = source["period_end_month"].astype("Int64")
    return source[SOURCE_COLUMNS].sort_values(["year", "quarter", "rank", "entity_name"]).reset_index(drop=True)


def summarize_market_structure(source_table: pd.DataFrame) -> pd.DataFrame:
    """Calculate concentration metrics from F&P's reported shares by quarter."""
    summaries = []
    for (year, quarter), group in source_table.groupby(["year", "quarter"], sort=True):
        positive = group.loc[group["market_share"].gt(0)].sort_values("rank")
        shares = positive["market_share"]
        summaries.append({
            "year": int(year), "quarter": int(quarter), "period_end_month": int(group["period_end_month"].iloc[0]),
            "entity_count": int(len(positive)), "market_size": float(group["market_total"].iloc[0]),
            "cr1": float(shares.head(1).sum()), "cr3": float(shares.head(3).sum()),
            "cr5": float(shares.head(5).sum()), "hhi": float(shares.pow(2).sum() * 10_000),
        })
    return pd.DataFrame(summaries)


def latest_available_period(summary: pd.DataFrame) -> tuple[int, int]:
    """Return the latest year/quarter in the F&P source."""
    if summary.empty:
        raise ValueError("No F&P market-structure periods are available.")
    latest = summary.sort_values(["year", "quarter"]).iloc[-1]
    return int(latest["year"]), int(latest["quarter"])


def same_quarter_history(summary: pd.DataFrame, quarter: int) -> pd.DataFrame:
    """Keep cumulative YTD comparisons like-for-like across years."""
    return summary.loc[summary["quarter"].eq(quarter)].sort_values("year").copy()

"""Streamlit-independent calculations for the Bank Analyst View."""

from __future__ import annotations

from collections.abc import Iterable

import pandas as pd

from analytics.bank_income import INCOME_COMPONENTS
from data.canonical import to_canonical_observations
from kpis.bank.egenkapitalforrentning_foer_skat import PROFIT_ATTRIBUTE
from kpis.bank.udlaan_i_forhold_til_egenkapital import LOAN_ATTRIBUTES
from kpis.registry import METRIC_REGISTRY, calculate_kpi


TOTAL_ASSETS_ATTRIBUTE = "Bal_BO_ATot"

ANALYST_METRICS = (
    {
        "metric_id": "bank.net_interest_income",
        "display_name": "Netto renteindtægter",
        "section": "Earnings",
        "source_type": "financial_services_long",
        "calculation_type": "calculated",
        "validation_status": "reused_accounting_income_mix",
        "unit": "t.DKK",
        "display_format": "dkk_billion_tdk",
        "required_attributes": tuple(INCOME_COMPONENTS["Netto renteindtægter"]["required"]),
        "formula": INCOME_COMPONENTS["Netto renteindtægter"]["formula"],
        "definition": "Res_Rind_RY minus Res_Rudg_RY.",
    },
    {
        "metric_id": "bank.net_fee_commission_income",
        "display_name": "Netto gebyr- og provisionsindtægter",
        "section": "Earnings",
        "source_type": "financial_services_long",
        "calculation_type": "calculated",
        "validation_status": "reused_accounting_income_mix",
        "unit": "t.DKK",
        "display_format": "dkk_billion_tdk",
        "required_attributes": tuple(INCOME_COMPONENTS["Netto gebyr- og provisionsindtægter"]["required"]),
        "formula": INCOME_COMPONENTS["Netto gebyr- og provisionsindtægter"]["formula"],
        "definition": "Res_GPi_RY minus Res_GPu_RY.",
    },
    {
        "metric_id": "bank.profit_before_tax",
        "display_name": "Resultat før skat",
        "section": "Earnings",
        "source_type": "financial_services_long",
        "calculation_type": "reported",
        "validation_status": "reused_roe_pre_tax_source",
        "unit": "t.DKK",
        "display_format": "dkk_billion_tdk",
        "required_attributes": (PROFIT_ATTRIBUTE,),
        "formula": lambda frame: frame[PROFIT_ATTRIBUTE],
        "definition": f"Rapporteret {PROFIT_ATTRIBUTE}.",
    },
    {
        "metric_id": "bank.roe_pre_tax",
        "section": "Profitability",
    },
    {
        "metric_id": "bank.roe_after_tax",
        "section": "Profitability",
    },
    {
        "metric_id": "bank.income_per_cost",
        "section": "Efficiency",
    },
    {
        "metric_id": "bank.loans",
        "display_name": "Udlån i alt",
        "section": "Growth / balance sheet",
        "source_type": "financial_services_long",
        "calculation_type": "calculated",
        "validation_status": "reused_loans_to_equity_inputs",
        "unit": "t.DKK",
        "display_format": "dkk_billion_tdk",
        "required_attributes": tuple(LOAN_ATTRIBUTES),
        "formula": lambda frame: frame[list(LOAN_ATTRIBUTES)].sum(axis=1, min_count=len(LOAN_ATTRIBUTES)),
        "definition": "Bal_BO_Autd plus Bal_BO_Auta.",
    },
    {
        "metric_id": "bank.loans_to_equity",
        "section": "Growth / balance sheet",
    },
)


def _metric_metadata(spec: dict) -> dict:
    """Combine new analyst definitions with the stable KPI registry metadata."""
    if spec["metric_id"] not in METRIC_REGISTRY:
        return dict(spec)

    registry_meta = METRIC_REGISTRY[spec["metric_id"]]
    return {
        "metric_id": spec["metric_id"],
        "display_name": registry_meta["display_name"],
        "section": spec["section"],
        "source_type": registry_meta["source_type"],
        "calculation_type": registry_meta["calculation_type"],
        "validation_status": registry_meta["validation_status"],
        "unit": registry_meta["unit"],
        "display_format": registry_meta["unit"],
        "definition": registry_meta["formula_label"],
    }


def _bank_canonical(raw: pd.DataFrame) -> pd.DataFrame:
    canonical = to_canonical_observations(raw)
    return canonical.loc[
        (canonical["market"] == "Bank")
        & (canonical["period_type"] == "FY")
        & (canonical["period_end_month"] == 12)
    ].copy()


def bank_entities_for_year(raw: pd.DataFrame, year: int) -> pd.DataFrame:
    """Return canonical bank entities observed in a fiscal year."""
    canonical = _bank_canonical(raw)
    entities = canonical.loc[
        canonical["fiscal_year"].eq(year),
        ["entity_id", "regnr", "display_name"],
    ].drop_duplicates("entity_id")
    return entities.sort_values("display_name").reset_index(drop=True)


def available_bank_years(raw: pd.DataFrame) -> list[int]:
    canonical = _bank_canonical(raw)
    return sorted(int(year) for year in canonical["fiscal_year"].dropna().unique())


def _canonical_metric_values(canonical: pd.DataFrame, spec: dict) -> pd.DataFrame:
    required = list(spec["required_attributes"])
    observations = canonical.loc[
        canonical["attribute_id"].isin(required),
        ["entity_id", "regnr", "display_name", "fiscal_year", "attribute_id", "value"],
    ].copy()
    pivot = observations.pivot(
        index=["entity_id", "regnr", "display_name", "fiscal_year"],
        columns="attribute_id",
        values="value",
    ).reset_index()
    for attribute in required:
        if attribute not in pivot.columns:
            pivot[attribute] = pd.NA

    complete_inputs = pivot[required].notna().all(axis=1)
    pivot["value"] = pd.NA
    pivot.loc[complete_inputs, "value"] = spec["formula"](pivot.loc[complete_inputs])
    return pivot[["entity_id", "regnr", "display_name", "fiscal_year", "value"]]


def _registry_metric_values(raw: pd.DataFrame, canonical: pd.DataFrame, metric_id: str) -> pd.DataFrame:
    kpi = calculate_kpi(raw, metric_id).copy()
    kpi["regnr"] = pd.to_numeric(kpi["regnr"], errors="coerce").astype("Int64")
    kpi["fiscal_year"] = pd.to_numeric(kpi["ÅR"], errors="coerce").astype("Int64")
    reference = canonical[["entity_id", "regnr", "display_name", "fiscal_year"]].drop_duplicates()
    values = kpi[["regnr", "fiscal_year", "KPI_Value"]].merge(
        reference,
        on=["regnr", "fiscal_year"],
        how="left",
    ).rename(columns={"KPI_Value": "value"})
    return values[["entity_id", "regnr", "display_name", "fiscal_year", "value"]]


def _all_metric_values(raw: pd.DataFrame, canonical: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, dict]]:
    values = []
    metadata = {}
    for spec in ANALYST_METRICS:
        meta = _metric_metadata(spec)
        metric_id = meta["metric_id"]
        metadata[metric_id] = meta
        if metric_id in METRIC_REGISTRY:
            frame = _registry_metric_values(raw, canonical, metric_id)
        else:
            frame = _canonical_metric_values(canonical, spec)
        frame["metric_id"] = metric_id
        values.append(frame)
    return pd.concat(values, ignore_index=True), metadata


def build_bank_analyst_view(
    raw: pd.DataFrame,
    entity_id: str,
    fiscal_year: int,
    benchmark_entity_ids: Iterable[str],
) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    """Build reproducible comparison and history tables for one canonical bank."""
    canonical = _bank_canonical(raw)
    values, metadata = _all_metric_values(raw, canonical)
    benchmark_ids = list(dict.fromkeys(str(item) for item in benchmark_entity_ids))
    if entity_id not in benchmark_ids:
        benchmark_ids.insert(0, entity_id)

    comparison_rows = []
    history_frames = []
    for metric_id, meta in metadata.items():
        metric_values = values.loc[values["metric_id"].eq(metric_id)].copy()
        target_current = metric_values.loc[
            metric_values["entity_id"].eq(entity_id) & metric_values["fiscal_year"].eq(fiscal_year),
            "value",
        ].dropna()
        previous = metric_values.loc[
            metric_values["entity_id"].eq(entity_id) & metric_values["fiscal_year"].eq(fiscal_year - 1),
            "value",
        ].dropna()
        peers = metric_values.loc[
            metric_values["entity_id"].isin(benchmark_ids) & metric_values["fiscal_year"].eq(fiscal_year),
            "value",
        ].dropna()
        current_value = target_current.iloc[-1] if not target_current.empty else pd.NA
        previous_value = previous.iloc[-1] if not previous.empty else pd.NA
        comparison_rows.append(
            {
                "metric_id": metric_id,
                "display_name": meta["display_name"],
                "section": meta["section"],
                "current_value": current_value,
                "previous_value": previous_value,
                "yoy_change": current_value - previous_value if pd.notna(current_value) and pd.notna(previous_value) else pd.NA,
                "peer_median": peers.median() if not peers.empty else pd.NA,
                "unit": meta["unit"],
                "display_format": meta["display_format"],
                "validation_status": meta["validation_status"],
                "source_type": meta["source_type"],
                "calculation_type": meta["calculation_type"],
                "definition": meta["definition"],
            }
        )
        history = metric_values.loc[
            metric_values["entity_id"].eq(entity_id) & metric_values["fiscal_year"].le(fiscal_year),
            ["fiscal_year", "value"],
        ].dropna().sort_values("fiscal_year").tail(5)
        history["metric_id"] = metric_id
        history_frames.append(history)

    entity = canonical.loc[
        canonical["entity_id"].eq(entity_id) & canonical["fiscal_year"].eq(fiscal_year),
        ["entity_id", "regnr", "display_name"],
    ].drop_duplicates("entity_id")
    if entity.empty:
        raise ValueError(f"Bank entity '{entity_id}' is not available in {fiscal_year}.")

    assets = _canonical_metric_values(
        canonical,
        {
            "required_attributes": (TOTAL_ASSETS_ATTRIBUTE,),
            "formula": lambda frame: frame[TOTAL_ASSETS_ATTRIBUTE],
        },
    )
    asset_value = assets.loc[
        assets["entity_id"].eq(entity_id) & assets["fiscal_year"].eq(fiscal_year), "value"
    ].dropna()
    overview = {
        "entity_id": entity_id,
        "regnr": str(entity.iloc[0]["regnr"]),
        "display_name": entity.iloc[0]["display_name"],
        "total_assets": asset_value.iloc[-1] if not asset_value.empty else pd.NA,
        "benchmark_size": len(benchmark_ids),
        "metrics_with_data": int(pd.Series([row["current_value"] for row in comparison_rows]).notna().sum()),
    }
    return pd.DataFrame(comparison_rows), pd.concat(history_frames, ignore_index=True), overview

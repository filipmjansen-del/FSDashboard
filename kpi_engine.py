from __future__ import annotations

import pandas as pd

KPI_DEFINITIONS = {
    "Indtjening pr. omkostningskrone": {
        "sector": "Bank",
        "numerator": [
            "Res_RGTot_RY",
            "Res_Kreg_RY",
            "Res_Xdi_RY",
            "Res_Rat_RY",
        ],
        "denominator": [
            "Res_UPa_RY",
            "Res_ImMa_RY",
            "Res_Xdu_RY",
            "Res_UGn_RY",
        ],
        "format": "multiple",
        "direction": "higher_is_better",
        "formula_label": "(Res_RGTot_RY + Res_Kreg_RY + Res_Xdi_RY + Res_Rat_RY) / (Res_UPa_RY + Res_ImMa_RY + Res_Xdu_RY + Res_UGn_RY)",
    }
}


def calculate_ratio_kpi(raw: pd.DataFrame, kpi_name: str) -> pd.DataFrame:
    """Calculate a ratio KPI only when every required input exists for a bank-year.

    Missing source attributes are not interpreted as zero. A zero denominator is returned as missing.
    """
    definition = KPI_DEFINITIONS[kpi_name]
    required = definition["numerator"] + definition["denominator"]

    df = raw.loc[
        (raw["Branche"] == definition["sector"]) & raw["Attribute"].isin(required),
        ["Branche", "ÅR", "regnr", "navn", "Attribute", "Value"],
    ].copy()

    wide = (
        df.pivot_table(
            index=["Branche", "ÅR", "regnr", "navn"],
            columns="Attribute",
            values="Value",
            aggfunc="first",
        )
        .reset_index()
    )

    # Ensure every expected source column exists, even if an entire attribute is absent in a future file.
    for attr in required:
        if attr not in wide.columns:
            wide[attr] = pd.NA

    complete_mask = wide[required].notna().all(axis=1)
    numerator = wide[definition["numerator"]].sum(axis=1, min_count=len(definition["numerator"]))
    denominator = wide[definition["denominator"]].sum(axis=1, min_count=len(definition["denominator"]))

    kpi_value = numerator / denominator
    kpi_value = kpi_value.where(complete_mask & denominator.ne(0))

    result = wide[["Branche", "ÅR", "regnr", "navn"]].copy()
    result["KPI"] = kpi_name
    result["KPI_Value"] = kpi_value
    result["CompleteInputs"] = complete_mask
    result["Numerator"] = numerator.where(complete_mask)
    result["Denominator"] = denominator.where(complete_mask)

    return result.sort_values(["ÅR", "navn"]).reset_index(drop=True)

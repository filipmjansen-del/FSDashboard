"""Reusable accounting-income calculations for Bank analytical workflows."""

from __future__ import annotations

import pandas as pd


INCOME_COMPONENTS = {
    "Netto renteindtægter": {
        "required": ["Res_Rind_RY", "Res_Rudg_RY"],
        "formula": lambda df: df["Res_Rind_RY"] - df["Res_Rudg_RY"],
    },
    "Udbytte af aktier mv.": {"required": ["Res_UdAk_RY"], "formula": lambda df: df["Res_UdAk_RY"]},
    "Netto gebyr- og provisionsindtægter": {
        "required": ["Res_GPi_RY", "Res_GPu_RY"],
        "formula": lambda df: df["Res_GPi_RY"] - df["Res_GPu_RY"],
    },
    "Kursreguleringer": {"required": ["Res_Kreg_RY"], "formula": lambda df: df["Res_Kreg_RY"]},
    "Andre driftsindtægter": {"required": ["Res_Xdi_RY"], "formula": lambda df: df["Res_Xdi_RY"]},
    "Resultat af kapitalandele": {"required": ["Res_Rat_RY"], "formula": lambda df: df["Res_Rat_RY"]},
}

INDEX_COLS = ["Branche", "ÅR", "Måned", "regnr", "navn"]
REQUIRED_ATTRIBUTES = sorted(
    attribute for component in INCOME_COMPONENTS.values() for attribute in component["required"]
)


def calculate_accounting_income_mix(raw: pd.DataFrame) -> pd.DataFrame:
    """Calculate the existing signed accounting-income mix without imputation."""
    bank = raw.loc[(raw["Branche"] == "Bank") & raw["Attribute"].isin(REQUIRED_ATTRIBUTES)].copy()
    if bank.empty:
        return pd.DataFrame()
    pivot = bank.pivot_table(index=INDEX_COLS, columns="Attribute", values="Value", aggfunc="first").reset_index()
    for attribute in REQUIRED_ATTRIBUTES:
        if attribute not in pivot.columns:
            pivot[attribute] = pd.NA
    complete = pivot.loc[pivot[REQUIRED_ATTRIBUTES].notna().all(axis=1)].copy()
    if complete.empty:
        return pd.DataFrame()
    for component_name, definition in INCOME_COMPONENTS.items():
        complete[component_name] = definition["formula"](complete)
    component_names = list(INCOME_COMPONENTS)
    complete["TotalIncome"] = complete[component_names].sum(axis=1)
    complete = complete.loc[complete["TotalIncome"].notna() & complete["TotalIncome"].ne(0)].copy()
    if complete.empty:
        return pd.DataFrame()
    long = complete.melt(
        id_vars=INDEX_COLS + ["TotalIncome"], value_vars=component_names,
        var_name="Component", value_name="Amount",
    )
    long["SharePct"] = long["Amount"] / long["TotalIncome"] * 100
    return long

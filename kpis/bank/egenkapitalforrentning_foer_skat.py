import pandas as pd


KPI_META = {
    "name": "Egenkapitalforrentning før skat",
    "industry": "Bank",
    "slug": "egenkapitalforrentning_foer_skat",
    "display_format": "percentage",
    "decimals": 1,
    "direction": "neutral",
    "formula_label": (
        "(Res_RfS_RY * 100) / "
        "((Bal_BO_PEekTot året før + Bal_BO_PEekTot) / 2)"
    ),
}

PROFIT_ATTRIBUTE = "Res_RfS_RY"
EQUITY_ATTRIBUTE = "Bal_BO_PEekTot"


def calculate(raw):
    """Calculate return on equity before tax for banks.

    KPI_Value is stored as a decimal ratio because the Streamlit app's
    percentage formatter converts 0.123 to 12.3%. This is mathematically
    equivalent to the supplied formula with * 100 for display purposes.

    The prior-year equity must be from the exact preceding calendar year.
    Missing inputs are not treated as zero.
    """
    required_attributes = [PROFIT_ATTRIBUTE, EQUITY_ATTRIBUTE]

    sector = raw[
        (raw["Branche"] == KPI_META["industry"])
        & (raw["Attribute"].isin(required_attributes))
    ].copy()

    index_cols = ["Branche", "ÅR", "Måned", "regnr", "navn"]

    pivot = (
        sector.pivot_table(
            index=index_cols,
            columns="Attribute",
            values="Value",
            aggfunc="first",
        )
        .reset_index()
    )

    for attribute in required_attributes:
        if attribute not in pivot.columns:
            pivot[attribute] = pd.NA

    previous_equity = pivot[["regnr", "ÅR", EQUITY_ATTRIBUTE]].copy()
    previous_equity["ÅR"] = previous_equity["ÅR"] + 1
    previous_equity = previous_equity.rename(
        columns={EQUITY_ATTRIBUTE: "EquityPreviousYear"}
    )

    pivot = pivot.merge(
        previous_equity,
        on=["regnr", "ÅR"],
        how="left",
    )

    pivot["Numerator"] = pivot[PROFIT_ATTRIBUTE]
    pivot["Denominator"] = (
        pivot[EQUITY_ATTRIBUTE] + pivot["EquityPreviousYear"]
    ) / 2

    complete_inputs = pivot[
        [PROFIT_ATTRIBUTE, EQUITY_ATTRIBUTE, "EquityPreviousYear"]
    ].notna().all(axis=1)

    valid = complete_inputs & pivot["Denominator"].ne(0)

    pivot["KPI_Value"] = pd.NA
    pivot.loc[valid, "KPI_Value"] = (
        pivot.loc[valid, "Numerator"] / pivot.loc[valid, "Denominator"]
    )

    pivot["KPI_Value"] = pd.to_numeric(pivot["KPI_Value"], errors="coerce")
    pivot["CompleteInputs"] = complete_inputs
    pivot["KPI"] = KPI_META["name"]

    return pivot

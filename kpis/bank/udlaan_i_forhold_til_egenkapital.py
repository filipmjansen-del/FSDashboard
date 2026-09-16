import pandas as pd


KPI_META = {
    "name": "Udlån i forhold til egenkapital",
    "industry": "Bank",
    "slug": "udlaan_i_forhold_til_egenkapital",
    "display_format": "multiple",
    "decimals": 2,
    "direction": "neutral",
    "formula_label": (
        "(Bal_BO_Autd + Bal_BO_Auta) / Bal_BO_PEekTot"
    ),
}

LOAN_ATTRIBUTES = ["Bal_BO_Autd", "Bal_BO_Auta"]
EQUITY_ATTRIBUTE = "Bal_BO_PEekTot"


def calculate(raw):
    """Calculate loans relative to equity for banks.

    Missing inputs are not treated as zero. The KPI is only calculated when
    both loan attributes and equity are present and equity is non-zero.
    """
    required_attributes = LOAN_ATTRIBUTES + [EQUITY_ATTRIBUTE]

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

    complete_inputs = pivot[required_attributes].notna().all(axis=1)

    pivot["Numerator"] = pivot[LOAN_ATTRIBUTES].sum(
        axis=1,
        min_count=len(LOAN_ATTRIBUTES),
    )
    pivot["Denominator"] = pivot[EQUITY_ATTRIBUTE]

    valid = complete_inputs & pivot["Denominator"].ne(0)

    pivot["KPI_Value"] = pd.NA
    pivot.loc[valid, "KPI_Value"] = (
        pivot.loc[valid, "Numerator"] / pivot.loc[valid, "Denominator"]
    )

    pivot["KPI_Value"] = pd.to_numeric(pivot["KPI_Value"], errors="coerce")
    pivot["CompleteInputs"] = complete_inputs
    pivot["KPI"] = KPI_META["name"]

    return pivot

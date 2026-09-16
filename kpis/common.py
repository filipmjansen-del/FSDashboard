import pandas as pd


def calculate_ratio_kpi(
    raw,
    industry,
    numerator_attributes,
    denominator_attributes,
    kpi_name,
):
    required_attributes = numerator_attributes + denominator_attributes

    sector = raw[
        (raw["Branche"] == industry)
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

    # Make sure all requested attributes exist as columns
    for attribute in required_attributes:
        if attribute not in pivot.columns:
            pivot[attribute] = pd.NA

    complete_inputs = pivot[required_attributes].notna().all(axis=1)

    pivot["Numerator"] = pivot[numerator_attributes].sum(
        axis=1,
        min_count=len(numerator_attributes),
    )

    pivot["Denominator"] = pivot[denominator_attributes].sum(
        axis=1,
        min_count=len(denominator_attributes),
    )

    valid = complete_inputs & pivot["Denominator"].ne(0)

    pivot["KPI_Value"] = pd.NA
    pivot.loc[valid, "KPI_Value"] = (
        pivot.loc[valid, "Numerator"]
        / pivot.loc[valid, "Denominator"]
    )

    pivot["KPI_Value"] = pd.to_numeric(
        pivot["KPI_Value"],
        errors="coerce",
    )

    pivot["CompleteInputs"] = complete_inputs
    pivot["KPI"] = kpi_name

    return pivot

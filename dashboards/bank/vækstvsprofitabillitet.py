import pandas as pd
import plotly.express as px
import streamlit as st


DASHBOARD_META = {
    "name": "Growth vs profitability matrix",
    "industry": "Bank",
    "slug": "growth_profitability_matrix",
    "description": "Positionerer banker på vækst og profitabilitet med balance som boblestørrelse.",
}

PURPLE = "#412B48"
DARK_RED = "#842044"
COGNAC = "#B25F4D"
BEIGE = "#DBD4CF"
BLUE_GREY = "#B8CACE"

GROWTH_METRICS = {
    "Aktivvækst": {
        "attributes": ["Bal_BO_ATot"],
        "label": "Aktivvækst",
    },
    "Udlånsvækst (balanceudlån, ikke repo-justeret)": {
        "attributes": ["Bal_BO_Autd", "Bal_BO_Auta"],
        "label": "Udlånsvækst",
    },
    "Indlånsvækst": {
        "attributes": ["Bal_BO_PGiag", "Bal_BO_PGip"],
        "label": "Indlånsvækst",
    },
    "Indtjeningsvækst": {
        "attributes": ["Res_RGTot_RY", "Res_Kreg_RY", "Res_Xdi_RY", "Res_Rat_RY"],
        "label": "Indtjeningsvækst",
    },
}


def _build_level(raw: pd.DataFrame, attributes: list[str], value_name: str) -> pd.DataFrame:
    sector = raw[
        (raw["Branche"] == "Bank")
        & (raw["Attribute"].isin(attributes))
    ].copy()

    pivot = (
        sector.pivot_table(
            index=["ÅR", "regnr", "navn"],
            columns="Attribute",
            values="Value",
            aggfunc="first",
        )
        .reset_index()
    )

    for attr in attributes:
        if attr not in pivot.columns:
            pivot[attr] = pd.NA

    complete = pivot[attributes].notna().all(axis=1)
    pivot[value_name] = pd.NA
    pivot.loc[complete, value_name] = pivot.loc[complete, attributes].sum(axis=1)
    pivot[value_name] = pd.to_numeric(pivot[value_name], errors="coerce")
    return pivot[["ÅR", "regnr", "navn", value_name]]


def build_growth_series(raw: pd.DataFrame, growth_key: str) -> pd.DataFrame:
    definition = GROWTH_METRICS[growth_key]
    level = _build_level(raw, definition["attributes"], "Level")

    prior = level[["regnr", "ÅR", "Level"]].copy()
    prior["ÅR"] = prior["ÅR"] + 1
    prior = prior.rename(columns={"Level": "PreviousYearLevel"})

    out = level.merge(prior, on=["regnr", "ÅR"], how="left")
    valid = (
        out["Level"].notna()
        & out["PreviousYearLevel"].notna()
        & out["PreviousYearLevel"].ne(0)
    )
    out["Growth"] = pd.NA
    out.loc[valid, "Growth"] = (
        out.loc[valid, "Level"] / out.loc[valid, "PreviousYearLevel"] - 1
    )
    out["Growth"] = pd.to_numeric(out["Growth"], errors="coerce")
    return out


def _asset_size(raw: pd.DataFrame, year: int) -> pd.DataFrame:
    return raw[
        (raw["Branche"] == "Bank")
        & (raw["ÅR"] == year)
        & (raw["Attribute"] == "Bal_BO_ATot")
    ][["regnr", "navn", "Value"]].rename(columns={"Value": "Assets"})


def _profitability_format(meta):
    fmt = meta.get("display_format", "number")
    decimals = meta.get("decimals", 2)
    if fmt == "percentage":
        return f".{decimals}%"
    if fmt == "multiple":
        return f".{decimals}f"
    return f",.{decimals}f"


def build_matrix_data(raw, calculate_kpi_fn, profitability_kpi, growth_key, year):
    growth = build_growth_series(raw, growth_key)
    growth = growth[growth["ÅR"] == year][["regnr", "navn", "Growth"]]

    profitability = calculate_kpi_fn(raw, profitability_kpi)
    profitability = profitability[
        profitability["ÅR"] == year
    ][["regnr", "navn", "KPI_Value"]].rename(columns={"KPI_Value": "Profitability"})

    assets = _asset_size(raw, year)

    # Registration number is the legal entity key; names remain display attributes.
    matrix = growth.merge(
        profitability.drop(columns=["navn"]),
        on="regnr",
        how="inner",
    ).merge(
        assets.drop(columns=["navn"]),
        on="regnr",
        how="left",
    )

    return matrix.dropna(subset=["Growth", "Profitability"])


def render(raw: pd.DataFrame):
    from kpis.registry import INDUSTRY_KPI_CATALOG, KPI_REGISTRY, calculate_kpi

    st.header("Growth vs profitability matrix")
    st.caption(
        "Matrixen kombinerer en valgfri Bank-KPI for profitabilitet med en år-til-år vækstindikator. "
        "Boblestørrelsen repræsenterer bankens samlede aktiver i det valgte år."
    )

    bank_kpis = [
        name
        for name in INDUSTRY_KPI_CATALOG.get("Bank", [])
        if KPI_REGISTRY[name].get("category") == "profitability"
    ]
    if not bank_kpis:
        st.warning("Der er ingen registrerede Bank-KPI'er at bruge som profitabilitetsmål.")
        return

    preferred = "Egenkapitalforrentning før skat"
    default_index = bank_kpis.index(preferred) if preferred in bank_kpis else 0

    profitability_kpi = st.selectbox(
        "Profitabilitets-KPI",
        bank_kpis,
        index=default_index,
        key="matrix_profitability_kpi",
    )
    growth_key = st.selectbox(
        "Vækstmål",
        list(GROWTH_METRICS.keys()),
        index=0,
        key="matrix_growth_metric",
    )

    years = sorted(
        int(x)
        for x in raw.loc[raw["Branche"] == "Bank", "ÅR"].dropna().unique()
    )
    # Growth requires t-1, so default to latest year but exclude first year from selector.
    years = years[1:]
    year = st.selectbox("År", years, index=len(years) - 1, key="matrix_year")

    matrix = build_matrix_data(
        raw,
        calculate_kpi,
        profitability_kpi,
        growth_key,
        year,
    )

    if matrix.empty:
        st.warning("Ingen banker har både vækst- og profitabilitetsdata for det valgte år.")
        return

    bank_options = sorted(matrix["navn"].unique())
    selected_banks = st.multiselect(
        "Banker",
        bank_options,
        default=bank_options,
        key="matrix_banks",
    )
    matrix = matrix[matrix["navn"].isin(selected_banks)].copy()
    if matrix.empty:
        st.info("Vælg mindst én bank.")
        return

    x_median = matrix["Growth"].median()
    y_median = matrix["Profitability"].median()
    meta = KPI_REGISTRY[profitability_kpi]

    # Use asset size for bubbles when available; otherwise equal-sized bubbles.
    size_col = "Assets" if matrix["Assets"].notna().any() else None

    fig = px.scatter(
        matrix,
        x="Growth",
        y="Profitability",
        size=size_col,
        hover_name="navn",
        text="navn",
        color="Profitability",
        color_continuous_scale=[BEIGE, BLUE_GREY, PURPLE],
        labels={
            "Growth": GROWTH_METRICS[growth_key]["label"],
            "Profitability": profitability_kpi,
            "Assets": "Aktiver",
        },
        hover_data={
            "Growth": ":.1%",
            "Profitability": _profitability_format(meta),
            "Assets": ":,.0f",
        },
    )

    fig.add_vline(x=x_median, line_dash="dash", line_color=COGNAC)
    fig.add_hline(y=y_median, line_dash="dash", line_color=DARK_RED)
    fig.update_traces(textposition="top center", marker=dict(opacity=0.78))
    fig.update_layout(
        template="plotly_white",
        height=700,
        margin=dict(l=20, r=20, t=20, b=20),
        coloraxis_colorbar=dict(title=profitability_kpi),
    )
    fig.update_xaxes(tickformat=".1%")
    if meta.get("display_format") == "percentage":
        fig.update_yaxes(tickformat=f".{meta.get('decimals', 1)}%")
    elif meta.get("display_format") == "multiple":
        fig.update_yaxes(ticksuffix="x", tickformat=f".{meta.get('decimals', 2)}f")

    st.plotly_chart(fig, use_container_width=True)

    c1, c2, c3 = st.columns(3)
    c1.metric("Banker i matrix", len(matrix))
    c2.metric("Median vækst", f"{x_median:.1%}")
    if meta.get("display_format") == "percentage":
        c3.metric("Median profitabilitet", f"{y_median:.{meta.get('decimals', 1)}%}")
    elif meta.get("display_format") == "multiple":
        c3.metric("Median profitabilitet", f"{y_median:.{meta.get('decimals', 2)}f}x")
    else:
        c3.metric("Median profitabilitet", f"{y_median:,.2f}")

    st.caption(
        "Bemærk: 'Udlånsvækst (balanceudlån, ikke repo-justeret)' er en analytisk vækst i "
        "Bal_BO_Autd + Bal_BO_Auta og er ikke det officielle Finanstilsynet-nøgletal for periodens udlånsvækst."
    )

import pandas as pd
import plotly.graph_objects as go
import streamlit as st


DASHBOARD_META = {
    "name": "Peer heatmap",
    "industry": "Bank",
    "slug": "peer_heatmap",
    "description": "Sammenlign banker på tværs af de KPI'er, der allerede ligger i Bank-KPI-registret.",
}

PURPLE = "#412B48"
BEIGE = "#DBD4CF"
BLUE_GREY = "#B8CACE"
WHITE = "#FFFFFF"
BLACK = "#000000"


def _format_value(value, meta):
    if pd.isna(value):
        return "–"
    fmt = meta.get("display_format", "number")
    decimals = meta.get("decimals", 2)
    if fmt == "percentage":
        return f"{value:.{decimals}%}"
    if fmt == "multiple":
        return f"{value:.{decimals}f}x"
    if fmt == "integer":
        return f"{value:,.0f}"
    if fmt == "dkk_million":
        return f"DKK {value / 1_000_000:,.{decimals}f}m"
    if fmt == "dkk_billion":
        return f"DKK {value / 1_000_000_000:,.{decimals}f}bn"
    if fmt == "dkk":
        return f"DKK {value:,.{decimals}f}"
    return f"{value:,.{decimals}f}"


def _relative_percentile(series: pd.Series, direction: str) -> pd.Series:
    numeric = pd.to_numeric(series, errors="coerce")
    if direction == "lower_is_better":
        return numeric.rank(pct=True, ascending=False) * 100
    return numeric.rank(pct=True, ascending=True) * 100


def build_heatmap_data(raw, registry, calculate_kpi_fn, year, kpi_names):
    """Return actual values and relative percentiles for selected Bank KPIs."""
    actual = None
    percentile = None

    for kpi_name in kpi_names:
        kpi_df = calculate_kpi_fn(raw, kpi_name)
        kpi_df = kpi_df[kpi_df["ÅR"] == year][["regnr", "navn", "KPI_Value"]].copy()
        kpi_df = kpi_df.dropna(subset=["KPI_Value"])
        if kpi_df.empty:
            continue

        meta = registry[kpi_name]
        direction = meta.get("direction", "neutral")
        kpi_df["Percentile"] = _relative_percentile(kpi_df["KPI_Value"], direction)

        actual_piece = kpi_df.set_index(["regnr", "navn"])["KPI_Value"].rename(kpi_name)
        pct_piece = kpi_df.set_index(["regnr", "navn"])["Percentile"].rename(kpi_name)

        actual = actual_piece.to_frame() if actual is None else actual.join(actual_piece, how="outer")
        percentile = pct_piece.to_frame() if percentile is None else percentile.join(pct_piece, how="outer")

    if actual is None:
        return pd.DataFrame(), pd.DataFrame()

    return actual, percentile


def _top_banks_by_assets(raw, year, available_names, n=15):
    asset_attr = "Bal_BO_ATot"
    assets = raw[
        (raw["Branche"] == "Bank")
        & (raw["ÅR"] == year)
        & (raw["Attribute"] == asset_attr)
        & (raw["navn"].isin(available_names))
    ][["navn", "Value"]].copy()
    if assets.empty:
        return sorted(available_names)[:n]
    return (
        assets.sort_values("Value", ascending=False)["navn"]
        .drop_duplicates()
        .head(n)
        .tolist()
    )


def render(raw: pd.DataFrame):
    from kpis.registry import INDUSTRY_KPI_CATALOG, KPI_REGISTRY, calculate_kpi

    st.header("Peer heatmap")
    st.caption(
        "Heatmappet bruger de KPI'er, der allerede er registreret under Bank. "
        "Farven viser bankens relative position blandt banker med en gyldig observation i det valgte år."
    )

    bank_kpis = list(INDUSTRY_KPI_CATALOG.get("Bank", []))
    if not bank_kpis:
        st.warning("Der er ingen registrerede Bank-KPI'er.")
        return

    selected_kpis = st.multiselect(
        "KPI'er",
        bank_kpis,
        default=bank_kpis,
        key="peer_heatmap_kpis",
    )
    if not selected_kpis:
        st.info("Vælg mindst én KPI.")
        return

    years = sorted(
        int(x)
        for x in raw.loc[raw["Branche"] == "Bank", "ÅR"].dropna().unique()
    )
    year = st.selectbox("År", years, index=len(years) - 1, key="peer_heatmap_year")

    actual, percentile = build_heatmap_data(
        raw,
        KPI_REGISTRY,
        calculate_kpi,
        year,
        selected_kpis,
    )
    if actual.empty:
        st.warning("Ingen af de valgte KPI'er har gyldige observationer i det valgte år.")
        return

    available_names = actual.reset_index()["navn"].dropna().unique().tolist()
    default_banks = _top_banks_by_assets(raw, year, available_names, n=15)
    banks = st.multiselect(
        "Banker",
        sorted(available_names),
        default=default_banks,
        key="peer_heatmap_banks",
    )
    if not banks:
        st.info("Vælg mindst én bank.")
        return

    actual_view = actual.reset_index().set_index("navn").loc[banks]
    pct_view = percentile.reset_index().set_index("navn").reindex(banks)

    # Sort banks by average relative percentile across selected KPIs.
    order = pct_view[selected_kpis].mean(axis=1, skipna=True).sort_values(ascending=False).index
    actual_view = actual_view.reindex(order)
    pct_view = pct_view.reindex(order)

    text = []
    for bank in pct_view.index:
        row = []
        for kpi_name in selected_kpis:
            if kpi_name not in actual_view.columns:
                row.append("–")
            else:
                row.append(_format_value(actual_view.at[bank, kpi_name], KPI_REGISTRY[kpi_name]))
        text.append(row)

    z = pct_view[selected_kpis].astype(float).values

    fig = go.Figure(
        data=go.Heatmap(
            z=z,
            x=selected_kpis,
            y=pct_view.index.tolist(),
            text=text,
            texttemplate="%{text}",
            zmin=0,
            zmax=100,
            colorscale=[
                [0.0, BEIGE],
                [0.5, BLUE_GREY],
                [1.0, PURPLE],
            ],
            colorbar=dict(title="Peer percentile"),
            hovertemplate=(
                "<b>%{y}</b><br>"
                "%{x}<br>"
                "Værdi: %{text}<br>"
                "Peer percentile: %{z:.0f}<extra></extra>"
            ),
        )
    )
    fig.update_layout(
        template="plotly_white",
        height=max(500, 34 * len(pct_view.index)),
        margin=dict(l=20, r=20, t=20, b=20),
        xaxis=dict(side="top"),
        font=dict(color=BLACK),
    )
    st.plotly_chart(fig, use_container_width=True)

    st.caption(
        "For KPI'er markeret som `lower_is_better` vendes percentilen. For `neutral` og "
        "`higher_is_better` betyder en højere percentile blot en højere relativ position."
    )
 

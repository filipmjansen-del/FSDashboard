from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from data_loader import load_raw_data
from kpi_engine import KPI_DEFINITIONS, calculate_ratio_kpi

st.set_page_config(
    page_title="Financial Services Intelligence",
    page_icon="📊",
    layout="wide",
)

DATA_PATH = Path(__file__).parent / "financial_services_long.xlsx"
KPI_NAME = "Indtjening pr. omkostningskrone"


@st.cache_data(show_spinner=False)
def get_data():
    raw = load_raw_data(DATA_PATH)
    kpi = calculate_ratio_kpi(raw, KPI_NAME)
    return raw, kpi


raw, kpi = get_data()
valid = kpi.dropna(subset=["KPI_Value"]).copy()
all_years = sorted(int(x) for x in kpi["ÅR"].dropna().unique())
latest_year = max(all_years)

st.title("Financial Services Intelligence")
st.caption("Banking MVP — first KPI implemented from the supplied formula")

with st.sidebar:
    st.header("Navigation")
    page = st.radio(
        "View",
        ["Bank overview", "KPI explorer", "Bank profile", "Sector comparison", "Data quality"],
        label_visibility="collapsed",
    )
    st.divider()
    st.subheader("KPI")
    st.write(KPI_NAME)
    with st.expander("Formula"):
        st.code(KPI_DEFINITIONS[KPI_NAME]["formula_label"], language=None)
        st.caption("A KPI value is only calculated when all eight required source attributes are present and the denominator is non-zero.")


def format_multiple(value):
    if pd.isna(value):
        return "–"
    return f"{value:.2f}x"


if page == "Bank overview":
    st.header("Bank overview")
    selected_year = st.selectbox("Year", all_years, index=len(all_years) - 1)
    yr = valid[valid["ÅR"] == selected_year].copy()
    represented = kpi[kpi["ÅR"] == selected_year]["regnr"].nunique()
    complete = yr["regnr"].nunique()
    median = yr["KPI_Value"].median()
    mean = yr["KPI_Value"].mean()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Banks represented", represented)
    c2.metric("Banks with complete KPI", complete)
    c3.metric("Sector median", format_multiple(median))
    c4.metric("Sector mean", format_multiple(mean))

    st.subheader("Distribution across banks")
    fig = px.histogram(
        yr,
        x="KPI_Value",
        nbins=20,
        labels={"KPI_Value": KPI_NAME},
        hover_data=["navn"],
    )
    fig.update_layout(yaxis_title="Number of banks", xaxis_tickformat=".2f")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Sector development")
    trend = (
        valid.groupby("ÅR", as_index=False)
        .agg(Median=("KPI_Value", "median"), Mean=("KPI_Value", "mean"), Banks=("regnr", "nunique"))
    )
    trend_long = trend.melt(id_vars=["ÅR", "Banks"], value_vars=["Median", "Mean"], var_name="Series", value_name="Value")
    fig2 = px.line(trend_long, x="ÅR", y="Value", color="Series", markers=True)
    fig2.update_layout(yaxis_title=KPI_NAME, xaxis_title=None)
    st.plotly_chart(fig2, use_container_width=True)

elif page == "KPI explorer":
    st.header("KPI explorer")
    names = sorted(valid["navn"].unique())
    default_names = names[: min(5, len(names))]
    selected_banks = st.multiselect("Banks", names, default=default_names)
    year_range = st.slider("Years", min(all_years), max(all_years), (min(all_years), max(all_years)))

    chart_df = valid[
        valid["navn"].isin(selected_banks)
        & valid["ÅR"].between(year_range[0], year_range[1])
    ].copy()

    if chart_df.empty:
        st.info("Select at least one bank with available KPI observations in the chosen period.")
    else:
        fig = px.line(
            chart_df,
            x="ÅR",
            y="KPI_Value",
            color="navn",
            markers=True,
            labels={"KPI_Value": KPI_NAME, "navn": "Bank"},
        )
        fig.update_layout(xaxis_title=None)
        st.plotly_chart(fig, use_container_width=True)

        table = chart_df.pivot(index="navn", columns="ÅR", values="KPI_Value")
        st.dataframe(table.style.format("{:.2f}x", na_rep="–"), use_container_width=True)

elif page == "Bank profile":
    st.header("Bank profile")
    bank_names = sorted(kpi["navn"].unique())
    selected_bank = st.selectbox("Bank", bank_names)
    bank_all = kpi[kpi["navn"] == selected_bank].sort_values("ÅR")
    bank_valid = bank_all.dropna(subset=["KPI_Value"])

    if bank_valid.empty:
        st.warning("No complete observations are available for this KPI for the selected bank.")
    else:
        last_row = bank_valid.iloc[-1]
        last_year = int(last_row["ÅR"])
        sector_year = valid[valid["ÅR"] == last_year]
        sector_median = sector_year["KPI_Value"].median()

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Latest available year", last_year)
        c2.metric(KPI_NAME, format_multiple(last_row["KPI_Value"]))
        c3.metric("Sector median", format_multiple(sector_median))
        c4.metric("Complete years", int(bank_valid["ÅR"].nunique()))

        fig = px.line(bank_valid, x="ÅR", y="KPI_Value", markers=True)
        fig.add_hline(y=sector_median, line_dash="dash", annotation_text=f"{last_year} sector median")
        fig.update_layout(yaxis_title=KPI_NAME, xaxis_title=None)
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Underlying calculation — latest available year")
        st.dataframe(
            pd.DataFrame(
                {
                    "Item": ["Numerator", "Denominator", KPI_NAME],
                    "Value": [last_row["Numerator"], last_row["Denominator"], last_row["KPI_Value"]],
                }
            ),
            use_container_width=True,
            hide_index=True,
        )

elif page == "Sector comparison":
    st.header("Sector comparison")
    selected_year = st.selectbox("Year", all_years, index=len(all_years) - 1, key="comparison_year")
    yr = valid[valid["ÅR"] == selected_year].copy()
    if yr.empty:
        st.info("No complete KPI observations for the selected year.")
    else:
        yr["Percentile"] = yr["KPI_Value"].rank(pct=True) * 100
        yr = yr.sort_values("KPI_Value", ascending=False)

        fig = px.bar(
            yr,
            x="KPI_Value",
            y="navn",
            orientation="h",
            hover_data={"Percentile": ":.0f", "KPI_Value": ":.2f"},
            labels={"KPI_Value": KPI_NAME, "navn": "Bank"},
        )
        fig.update_layout(height=max(500, 24 * len(yr)), yaxis={"categoryorder": "total ascending"})
        st.plotly_chart(fig, use_container_width=True)

        display = yr[["navn", "KPI_Value", "Percentile"]].rename(
            columns={"navn": "Bank", "KPI_Value": KPI_NAME, "Percentile": "Sector percentile"}
        )
        st.dataframe(
            display.style.format({KPI_NAME: "{:.2f}x", "Sector percentile": "{:.0f}"}),
            use_container_width=True,
            hide_index=True,
        )

elif page == "Data quality":
    st.header("Data quality")
    st.write("This page makes the calculation coverage explicit rather than silently treating missing source attributes as zero.")

    coverage = (
        kpi.groupby("ÅR", as_index=False)
        .agg(
            BanksRepresented=("regnr", "nunique"),
            CompleteKPI=("KPI_Value", lambda s: s.notna().sum()),
        )
    )
    coverage["CoveragePct"] = coverage["CompleteKPI"] / coverage["BanksRepresented"] * 100
    st.dataframe(
        coverage.style.format({"CoveragePct": "{:.1f}%"}),
        use_container_width=True,
        hide_index=True,
    )

    st.subheader("Bank-year observations with missing KPI inputs")
    missing = kpi[kpi["KPI_Value"].isna()][["ÅR", "regnr", "navn"]].sort_values(["ÅR", "navn"])
    st.dataframe(missing, use_container_width=True, hide_index=True)

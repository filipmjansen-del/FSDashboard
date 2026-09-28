import pandas as pd
import plotly.express as px
import streamlit as st

from analytics.bank_income import INCOME_COMPONENTS as COMPONENTS, calculate_accounting_income_mix
from ui.components import render_page_intro, render_section_intro
from ui.formatting import brand_plotly, plotly_export_config
from ui.theme import BRAND_SEQUENCE, DARK_RED, PURPLE


DASHBOARD_META = {
    "name": "Regnskabsmæssigt indtjeningsmix",
    "industry": "Bank",
    "slug": "indtjeningsmix",
    "description": "100% normaliseret fordeling af bankernes indtjeningskomponenter.",
}


COLOR_MAP = {
    "Netto renteindtægter": PURPLE,
    "Udbytte af aktier mv.": BRAND_SEQUENCE[4],
    "Netto gebyr- og provisionsindtægter": DARK_RED,
    "Kursreguleringer": BRAND_SEQUENCE[2],
    "Andre driftsindtægter": BRAND_SEQUENCE[3],
    "Resultat af kapitalandele": BRAND_SEQUENCE[5],
}


_calculate_income_mix = calculate_accounting_income_mix


def render(raw: pd.DataFrame):
    render_page_intro(
        "Regnskabsmæssigt indtjeningsmix",
        "Hver bank normaliseres til sin egen samlede indtjening, så store og små banker kan sammenlignes direkte.",
    )

    mix = _calculate_income_mix(raw)

    if mix.empty:
        st.warning(
            "Der kan ikke beregnes et indtjeningsmix med de tilgængelige source attributes."
        )
        return

    years = sorted(int(year) for year in mix["ÅR"].dropna().unique())
    selected_year = st.selectbox(
        "År",
        years,
        index=len(years) - 1,
        key="income_mix_year",
    )

    year_df = mix[mix["ÅR"] == selected_year].copy()

    bank_totals = (
        year_df[["regnr", "navn", "TotalIncome"]]
        .drop_duplicates()
        .sort_values("TotalIncome", ascending=False)
    )

    available_banks = bank_totals["navn"].tolist()
    default_banks = available_banks[: min(15, len(available_banks))]

    selected_banks = st.multiselect(
        "Banker",
        available_banks,
        default=default_banks,
        key="income_mix_banks",
    )

    if not selected_banks:
        st.info("Vælg mindst én bank.")
        return

    chart_df = year_df[year_df["navn"].isin(selected_banks)].copy()

    order = (
        chart_df[["navn", "TotalIncome"]]
        .drop_duplicates()
        .sort_values("TotalIncome", ascending=False)["navn"]
        .tolist()
    )

    render_section_intro("Fordeling af indtægter", "Se hvordan den valgte banks indtægter fordeler sig på regnskabsmæssige komponenter.")

    fig = px.bar(
        chart_df,
        x="navn",
        y="SharePct",
        color="Component",
        barmode="relative",
        category_orders={"navn": order},
        color_discrete_map=COLOR_MAP,
        custom_data=["Amount", "TotalIncome"],
        labels={
            "navn": "Bank",
            "SharePct": "Andel af indtægter",
            "Component": "Indtægtskilde",
        },
    )

    fig.update_traces(
        hovertemplate=(
            "<b>%{x}</b><br>"
            "%{fullData.name}<br>"
            "Andel: %{y:.1f}%<br>"
            "Beløb: %{customdata[0]:,.0f}<br>"
            "Samlet indtjening: %{customdata[1]:,.0f}"
            "<extra></extra>"
        )
    )

    brand_plotly(fig, legend_title="Indtægtskilde")
    fig.update_yaxes(title="Andel af indtægter", ticksuffix="%")
    st.plotly_chart(fig, use_container_width=True, config=plotly_export_config(f"Databank_Bank_Income_Mix_{selected_year}"))

    has_negative = (chart_df["SharePct"] < 0).any()
    if has_negative:
        st.caption(
            "Bemærk: Negative indtjeningskomponenter vises som negative andele. "
            "Derfor kan den positive del af enkelte søjler overstige 100%, mens nettoandelene "
            "fortsat summerer til 100%. Det bevarer den økonomiske betydning af fx negative "
            "kursreguleringer."
        )
    else:
        st.caption(
            "Søjlerne er 100% normaliserede: hver banks indtægtskomponenter summerer til 100%."
        )

    render_section_intro("Regnskabsmæssigt indtjeningsmix i procent", "Tabellen viser de samme komponenter som andele af samlet indtjening.")

    share_table = (
        chart_df.pivot_table(
            index="navn",
            columns="Component",
            values="SharePct",
            aggfunc="first",
        )
        .reindex(order)
    )

    share_table["I alt"] = share_table.sum(axis=1)

    st.dataframe(
        share_table.style.format("{:.1f}%", na_rep="–"),
        use_container_width=True,
    )

    with st.expander("Sådan beregnes indtjeningsmixet"):
        st.markdown(
            """
**Netto renteindtægter** = `Res_Rind_RY - Res_Rudg_RY`  
**Udbytte af aktier mv.** = `Res_UdAk_RY`  
**Netto gebyr- og provisionsindtægter** = `Res_GPi_RY - Res_GPu_RY`  
**Kursreguleringer** = `Res_Kreg_RY`  
**Andre driftsindtægter** = `Res_Xdi_RY`  
**Resultat af kapitalandele** = `Res_Rat_RY`

Hver komponent divideres derefter med summen af de seks indtægtskomponenter for den samme bank og det samme år.
"""
        )

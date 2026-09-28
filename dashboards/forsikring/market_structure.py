"""Streamlit view for F&P's reported non-life market structure."""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from analytics.insurance_market_structure import (
    build_market_structure_table, latest_available_period, same_quarter_history, summarize_market_structure,
)
from data.access import load_insurance_market_structure_fp
from output.excel import insurance_market_structure_filename, insurance_market_structure_workbook
from ui.components import render_kpi_cards, render_page_intro, render_section_intro
from ui.formatting import brand_plotly, format_danish_number, plotly_export_config
from ui.theme import PURPLE


DASHBOARD_META = {
    "name": "Forsikringsmarkedets struktur",
    "description": "Markedsstørrelse, koncentration og F&P-rapporterede markedsandele.",
}


def _line_chart(data: pd.DataFrame, y: str, title: str, y_title: str, tickformat: str | None = None):
    fig = px.line(data, x="year", y=y, markers=True, title=title, color_discrete_sequence=[PURPLE])
    brand_plotly(fig, subtitle="Forsikringsmarkedet · Samme kvartal på tværs af år")
    fig.update_layout(showlegend=False, height=330)
    fig.update_xaxes(title=None, dtick=1)
    fig.update_yaxes(title=y_title, tickformat=tickformat)
    return fig


def _format_market_size(value: float) -> str:
    return f"DKK {format_danish_number(value / 1_000_000, 1)} mia."


def displayed_market_shares(source_table: pd.DataFrame, display_limit: str) -> pd.DataFrame:
    """Select chart rows only; F&P's complete population remains unchanged."""
    limit = {"Top 10": 10, "Top 20": 20, "Alle": len(source_table)}[display_limit]
    return source_table.nsmallest(limit, "rank").sort_values("market_share")


def render(_raw_data: pd.DataFrame):
    """Render source-specific F&P analysis; the main workbook is not an input."""
    source_table = build_market_structure_table(load_insurance_market_structure_fp())
    summary = summarize_market_structure(source_table)
    if summary.empty:
        st.info("Der er ingen F&P-markedsstrukturdata tilgængelige.")
        return
    latest_year, latest_quarter = latest_available_period(summary)
    period_options = summary.sort_values(["year", "quarter"], ascending=False).apply(
        lambda row: f"{int(row['year'])} Q{int(row['quarter'])}", axis=1
    ).tolist()
    selected_label = st.selectbox("Periode", period_options, index=0, key="insurance_market_structure_period")
    selected_year, selected_quarter = map(int, selected_label.replace(" Q", " ").split())
    selected = summary.loc[summary["year"].eq(selected_year) & summary["quarter"].eq(selected_quarter)].iloc[0]
    historical = same_quarter_history(summary, selected_quarter)
    selected_population = source_table.loc[
        source_table["year"].eq(selected_year) & source_table["quarter"].eq(selected_quarter)
    ].sort_values("rank")

    render_page_intro("Forsikringsmarkedets struktur", DASHBOARD_META["description"], context="Forsikring · Markedsintelligens")
    render_section_intro(f"Nøgletal for {selected_label}", "F&P's bruttopræmieindtægter og markedsandele for Skadeforsikring i alt.")
    render_kpi_cards([
        (format_danish_number(selected["entity_count"]), "Markedsaktører"),
        (_format_market_size(float(selected["market_size"])), f"Bruttopræmieindtægter til og med Q{selected_quarter}"),
        (f"{format_danish_number(selected['cr5'] * 100, 1)} %", "CR5"),
        (format_danish_number(selected["hhi"]), "HHI"),
    ])
    render_section_intro("Historisk udvikling", f"Viser Q{selected_quarter} i hvert tilgængeligt år, fordi bruttopræmieindtægter er kumulative YTD.")
    for column, title, axis, fmt, name in [
        ("entity_count", "Markedsaktører", "Antal", None, "Entities"),
        ("market_size", "Bruttopræmieindtægter", "t.DKK", ",.0f", "Market_Size"),
        ("cr5", "CR5", "Andel", ".0%", "CR5"), ("hhi", "HHI", "HHI (0-10.000)", ",.0f", "HHI"),
    ]:
        st.plotly_chart(_line_chart(historical, column, title, axis, fmt), use_container_width=True, config=plotly_export_config(f"Databank_Insurance_{name}_Q{selected_quarter}"))
    render_section_intro(f"Markedsandele i {selected_label}", "F&P's rapporterede markedsandele; de er ikke genberegnet af Databank.")
    display_limit = st.radio("Visning", ["Top 10", "Top 20", "Alle"], horizontal=True, key="insurance_market_structure_share_limit")
    displayed = displayed_market_shares(selected_population, display_limit)
    fig = px.bar(displayed, x="market_share", y="entity_name", orientation="h", color_discrete_sequence=[PURPLE], hover_data={"market_value": ":,.0f", "market_share": ".2%", "rank": True})
    fig.update_layout(title=f"Markedsandele · {selected_label}", showlegend=False, height=max(330, len(displayed) * 28))
    brand_plotly(fig, subtitle=f"{display_limit} F&P-markedsaktører efter rapporteret markedsandel")
    fig.update_xaxes(title="Rapporteret markedsandel", tickformat=".0%")
    fig.update_yaxes(title="")
    st.plotly_chart(fig, use_container_width=True, config=plotly_export_config(f"Databank_Insurance_Market_Shares_{selected_year}_Q{selected_quarter}"))
    render_section_intro("Underliggende markedsandelstabel", "F&P's markedsaktører og rapporterede værdier for den valgte periode.")
    display_table = selected_population.assign(
        period=selected_label,
        market_value=lambda f: f["market_value"].map(format_danish_number),
        market_share=lambda f: f["market_share"].map(lambda v: f"{format_danish_number(v * 100, 2)} %"),
    )[["period", "entity_name", "market_value", "market_share", "rank"]].rename(columns={"period": "Periode", "entity_name": "Selskab", "market_value": "Bruttopræmieindtægter (t.DKK)", "market_share": "Rapporteret markedsandel", "rank": "Rang"})
    st.dataframe(display_table, use_container_width=True, hide_index=True)
    st.download_button("Download Excel", data=insurance_market_structure_workbook(historical, source_table.loc[source_table["quarter"].eq(selected_quarter)]), file_name=insurance_market_structure_filename(selected_quarter), mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    with st.expander("Metode og databegrænsninger"):
        st.markdown(f"""
        - **Kilde:** F&P, *Skadeforsikring i alt*. Bruttopræmieindtægter og markedsandele er **rapporteret af F&P**.
        - **Markedsandel:** F&P's rapporterede markedsandel anvendes direkte og genberegnes ikke af Databank.
        - **Population og identitet:** F&P's markedsaktører/-grupper; de er analytisk forskellige fra regnr-baserede juridiske enheder.
        - **Beregninger:** Databank beregner rang, CR1, CR3, CR5, HHI og antal markedsaktører. HHI = 10.000 × sum(s_i²).
        - **Kvartaler:** Bruttopræmieindtægter er kumulative YTD; historik sammenligner derfor samme kvartal på tværs af år.
        """)

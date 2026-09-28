"""Streamlit view for the insurance market-structure analysis."""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from analytics.insurance_market_structure import (
    GROSS_PREMIUM_ATTRIBUTE,
    build_market_structure_table,
    summarize_market_structure,
)
from ui.components import render_page_intro, render_section_intro
from ui.formatting import brand_plotly
from ui.theme import PURPLE


DASHBOARD_META = {
    "name": "Forsikringsmarkedets struktur",
    "description": "Markedsstørrelse, koncentration og selskabsandele baseret på bruttopræmier.",
}


def _line_chart(data: pd.DataFrame, y: str, title: str, y_title: str, tickformat: str | None = None):
    fig = px.line(data, x="year", y=y, markers=True, title=title, color_discrete_sequence=[PURPLE])
    brand_plotly(fig)
    fig.update_layout(showlegend=False, height=360)
    fig.update_xaxes(title="År", dtick=1)
    fig.update_yaxes(title=y_title, tickformat=tickformat)
    return fig


def _format_market_size(value: float) -> str:
    return f"DKK {value / 1_000_000:,.1f} mia."


def render(raw_data: pd.DataFrame):
    """Render the market-structure view without changing its analytical inputs."""
    source_table = build_market_structure_table(raw_data)
    summary = summarize_market_structure(source_table)
    if summary.empty:
        st.info("Der er ingen bruttopræmieobservationer tilgængelige.")
        return

    years = summary["year"].astype(int).tolist()
    selected_range = st.slider(
        "Årsinterval",
        min_value=min(years),
        max_value=max(years),
        value=(min(years), max(years)),
        key="insurance_market_structure_year_range",
    )
    historical = summary.loc[summary["year"].between(*selected_range)].copy()
    selected_year = selected_range[1]
    latest = historical.loc[historical["year"] == selected_year].iloc[0]

    render_page_intro(
        "Forsikringsmarkedets struktur",
        "Se udviklingen i markedets størrelse og koncentration samt selskabernes andele af bruttopræmierne.",
    )

    if bool(latest["known_data_break"]):
        st.warning(
            f"{selected_year} er markeret som et kendt databrud. Sammenlign året med forsigtighed, indtil dækningen er afstemt."
        )

    render_section_intro(
        f"Nøgletal for {selected_year}",
        "Alle nøgletal er beregnet på den samme inkluderede selskabspopulation.",
    )
    metrics = st.columns(4)
    metrics[0].metric("Juridiske enheder", f"{int(latest['entity_count']):,}")
    metrics[1].metric("Markedsstørrelse", _format_market_size(float(latest["market_size"])))
    metrics[2].metric("CR5", f"{latest['cr5']:.1%}")
    metrics[3].metric("HHI", f"{latest['hhi']:,.0f}")

    render_section_intro(
        "Historisk udvikling",
        "Udviklingen vises for det valgte årsinterval. CR5 og HHI bygger på samme årlige population som markedsstørrelsen.",
    )
    st.plotly_chart(_line_chart(historical, "entity_count", "Antal juridiske enheder", "Antal"), use_container_width=True)
    st.plotly_chart(_line_chart(historical, "market_size", "Markedsstørrelse", "DKK", ",.0f"), use_container_width=True)
    st.plotly_chart(_line_chart(historical, "cr5", "CR5", "Andel", ".0%"), use_container_width=True)
    st.plotly_chart(_line_chart(historical, "hhi", "HHI", "HHI (0-10.000)", ",.0f"), use_container_width=True)

    selected_population = source_table.loc[source_table["year"] == selected_year].copy()
    included = selected_population.loc[selected_population["included_flag"]].sort_values("rank")
    render_section_intro(
        f"Markedsandele i {selected_year}",
        "Andelene er beregnet af den inkluderede markedsstørrelse for det valgte år.",
    )
    fig = px.bar(
        included.sort_values("market_share"),
        x="market_share",
        y="display_name",
        orientation="h",
        color_discrete_sequence=[PURPLE],
        hover_data={"market_value": ":,.0f", "market_share": ".2%", "rank": True},
    )
    brand_plotly(fig)
    fig.update_layout(showlegend=False, height=max(420, len(included) * 26), margin=dict(l=20, r=20, t=20, b=20))
    fig.update_xaxes(title="Markedsandel", tickformat=".0%")
    fig.update_yaxes(title="")
    st.plotly_chart(fig, use_container_width=True)

    render_section_intro("Underliggende markedsandelstabel", "Inklusion og eventuelle eksklusioner er synlige for hver rapporteret enhed.")
    display_table = selected_population.assign(
        market_share=lambda frame: frame["market_share"].map(lambda value: "–" if pd.isna(value) else f"{value:.2%}"),
        market_value=lambda frame: frame["market_value"].map(lambda value: "–" if pd.isna(value) else f"{value:,.0f}"),
        rank=lambda frame: frame["rank"].map(lambda value: "–" if pd.isna(value) else str(int(value))),
        included_flag=lambda frame: frame["included_flag"].map({True: "Ja", False: "Nej"}),
    )
    st.dataframe(display_table, use_container_width=True, hide_index=True)

    with st.expander("Metode og databegrænsninger"):
        st.markdown(
            f"""
            - **Kilde:** rapporterede bruttopræmier i råattributten `{GROSS_PREMIUM_ATTRIBUTE}`.
            - **Population:** juridiske enheder identificeres med `regnr`. Kun observerede, positive bruttopræmier indgår; manglende, nul og negative værdier vises som ekskluderede.
            - **Beregninger:** CR1, CR3, CR5 og HHI er beregnet på samme inkluderede population som markedsstørrelsen. HHI vises på skalaen 0-10.000.
            - **Databrud:** 2025 er markeret som et kendt dækningsbrud og bør fortolkes med forsigtighed.
            """
        )

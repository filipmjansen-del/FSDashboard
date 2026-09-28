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
from data.canonical import to_canonical_observations
from output.excel import insurance_market_structure_filename, insurance_market_structure_workbook
from ui.components import render_kpi_cards, render_page_intro, render_section_intro, render_warning_callout
from ui.formatting import brand_plotly, format_danish_number, plotly_export_config
from ui.theme import PURPLE


DASHBOARD_META = {
    "name": "Forsikringsmarkedets struktur",
    "description": "Markedsstørrelse, koncentration og selskabsandele baseret på bruttopræmier.",
}


def _line_chart(data: pd.DataFrame, y: str, title: str, y_title: str, tickformat: str | None = None):
    fig = px.line(data, x="year", y=y, markers=True, title=title, color_discrete_sequence=[PURPLE])
    brand_plotly(fig, subtitle="Forsikringsmarkedet · Valgt årsinterval")
    fig.update_layout(showlegend=False, height=330)
    fig.update_xaxes(title=None, dtick=1)
    fig.update_yaxes(title=y_title, tickformat=tickformat)
    return fig


def _format_market_size(value: float) -> str:
    return f"DKK {format_danish_number(value / 1_000_000, 1)} mia."


def displayed_market_shares(included: pd.DataFrame, display_limit: str) -> pd.DataFrame:
    """Select chart rows only; the analytical population remains unchanged."""
    limit = {"Top 10": 10, "Top 20": 20, "Alle": len(included)}[display_limit]
    return included.nsmallest(limit, "rank").sort_values("market_share")


def render(raw_data: pd.DataFrame):
    """Render the market-structure view without changing its analytical inputs."""
    source_table = build_market_structure_table(to_canonical_observations(raw_data))
    summary = summarize_market_structure(source_table)
    if summary.empty:
        st.info("Der er ingen bruttopræmieobservationer tilgængelige.")
        return

    render_page_intro(
        "Forsikringsmarkedets struktur",
        "Markedsstørrelse, koncentration og selskabsandele baseret på bruttopræmier.",
        context="Forsikring · Markedsintelligens",
    )
    render_section_intro("Valg", "Vælg det årsinterval, der skal vises og eksporteres.")

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

    if bool(latest["known_data_break"]):
        render_warning_callout(
            f"{selected_year} er markeret som et kendt databrud. Sammenlign året med forsigtighed, indtil dækningen er afstemt."
        )

    render_section_intro(
        f"Nøgletal for {selected_year}",
        "Alle nøgletal er beregnet på den samme inkluderede selskabspopulation.",
    )
    render_kpi_cards([
        (format_danish_number(latest["entity_count"]), "Enheder med positive bruttopræmier"),
        (_format_market_size(float(latest["market_size"])), "Markedsstørrelse"),
        (f"{format_danish_number(latest['cr5'] * 100, 1)} %", "CR5"),
        (format_danish_number(latest["hhi"]), "HHI"),
    ])

    render_section_intro(
        "Historisk udvikling",
        "Udviklingen vises for det valgte årsinterval. Enhedstælling, CR5 og HHI bygger på samme årlige population som markedsstørrelsen.",
    )
    st.plotly_chart(_line_chart(historical, "entity_count", "Enheder med positive bruttopræmier", "Antal"), use_container_width=True, config=plotly_export_config("Databank_Insurance_Entities"))
    st.plotly_chart(_line_chart(historical, "market_size", "Markedsstørrelse", "t.DKK", ",.0f"), use_container_width=True, config=plotly_export_config("Databank_Insurance_Market_Size"))
    st.plotly_chart(_line_chart(historical, "cr5", "CR5", "Andel", ".0%"), use_container_width=True, config=plotly_export_config("Databank_Insurance_CR5"))
    st.plotly_chart(_line_chart(historical, "hhi", "HHI", "HHI (0-10.000)", ",.0f"), use_container_width=True, config=plotly_export_config("Databank_Insurance_HHI"))

    selected_population = source_table.loc[source_table["year"] == selected_year].copy()
    included = selected_population.loc[selected_population["included_flag"]].sort_values("rank")
    render_section_intro(
        f"Markedsandele i {selected_year}",
        "Andelene er beregnet af den inkluderede markedsstørrelse for det valgte år.",
    )
    display_limit = st.radio("Visning", ["Top 10", "Top 20", "Alle"], horizontal=True, key="insurance_market_structure_share_limit")
    displayed = displayed_market_shares(included, display_limit)
    fig = px.bar(
        displayed,
        x="market_share",
        y="display_name",
        orientation="h",
        color_discrete_sequence=[PURPLE],
        hover_data={"market_value": ":,.0f", "market_share": ".2%", "rank": True},
    )
    fig.update_layout(title=f"Markedsandele · {selected_year}")
    brand_plotly(fig, subtitle=f"{display_limit} selskaber efter bruttopræmier")
    fig.update_layout(showlegend=False, height=max(330, len(displayed) * 28))
    fig.update_xaxes(title="Markedsandel", tickformat=".0%")
    fig.update_yaxes(title="")
    st.plotly_chart(fig, use_container_width=True, config=plotly_export_config(f"Databank_Insurance_Market_Shares_{selected_year}"))

    render_section_intro("Underliggende markedsandelstabel", "Inklusion og eventuelle eksklusioner er synlige for hver rapporteret enhed.")
    display_table = selected_population.assign(
        market_share=lambda frame: frame["market_share"].map(lambda value: "–" if pd.isna(value) else f"{format_danish_number(value * 100, 1)} %"),
        market_value=lambda frame: frame["market_value"].map(lambda value: "–" if pd.isna(value) else format_danish_number(value)),
        rank=lambda frame: frame["rank"].map(lambda value: "–" if pd.isna(value) else str(int(value))),
        included_flag=lambda frame: frame["included_flag"].map({True: "Ja", False: "Nej"}),
    )
    st.dataframe(
        display_table.rename(
            columns={
                "year": "År",
                "entity_id": "Enheds-ID",
                "display_name": "Selskab",
                "market_value": "Markedsværdi (t.DKK)",
                "market_share": "Markedsandel",
                "rank": "Rang",
                "included_flag": "Indgår",
                "exclusion_reason": "Eksklusionsårsag",
            }
        ),
        use_container_width=True,
        hide_index=True,
    )
    st.download_button(
        "Download Excel",
        data=insurance_market_structure_workbook(historical, source_table.loc[source_table["year"].between(*selected_range)]),
        file_name=insurance_market_structure_filename(*selected_range),
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

    with st.expander("Metode og databegrænsninger"):
        st.markdown(
            f"""
            - **Kilde:** rapporterede bruttopræmier i råattributten `{GROSS_PREMIUM_ATTRIBUTE}` (t.DKK).
            - **Population:** juridiske enheder identificeres med `regnr` via den kanoniske `entity_id`. Kun observerede, positive bruttopræmier indgår; manglende, nul og negative værdier vises som ekskluderede.
            - **Beregninger:** CR1, CR3, CR5 og HHI er beregnet på samme inkluderede population som markedsstørrelsen. HHI vises på skalaen 0-10.000.
            - **Databrud:** 2025 er markeret som et kendt dækningsbrud og bør fortolkes med forsigtighed.
            - **Output:** Tabellen kan hentes som Excel med metodekontekst. Plotly-diagrammer kan hentes som PNG fra download-knappen i diagrammets værktøjslinje.
            """
        )

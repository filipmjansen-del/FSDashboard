"""Company-centric meeting-preparation view for one bank."""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from analytics.bank_analyst import (
    available_bank_years,
    bank_entities_for_year,
    build_bank_analyst_view,
)
from output.excel import bank_analyst_filename, bank_analyst_workbook
from ui.components import render_kpi_cards, render_page_intro, render_section_intro
from ui.formatting import brand_plotly, format_danish_kpi_delta, format_danish_kpi_value, plotly_export_config
from ui.theme import PURPLE


DASHBOARD_META = {
    "name": "Bank Analyst View",
    "description": "Forbered et bankmøde med dokumenterede nøgletal, udvikling og peer-benchmark.",
}

SECTION_ORDER = ("Earnings", "Profitability", "Efficiency", "Growth / balance sheet")
SECTION_LABELS = {
    "Earnings": "Indtjening",
    "Profitability": "Profitabilitet",
    "Efficiency": "Effektivitet",
    "Growth / balance sheet": "Vækst og balance",
}


def _metric_meta(row: pd.Series) -> dict:
    return {"display_format": row["display_format"], "decimals": 1 if row["display_format"] == "percentage" else 2}


def _history_chart(history: pd.DataFrame, display_name: str, meta: dict, bank_name: str):
    fig = px.line(history, x="fiscal_year", y="value", markers=True, title=display_name, color_discrete_sequence=[PURPLE])
    brand_plotly(fig, subtitle=f"{bank_name} · op til fem tilgængelige finansår")
    fig.update_layout(showlegend=False, height=250)
    fig.update_xaxes(title=None, dtick=1)
    if meta["display_format"] == "percentage":
        fig.update_yaxes(title=display_name, tickformat=".0%")
    elif meta["display_format"] == "dkk_billion_tdk":
        fig.update_yaxes(title=f"{display_name} (t.DKK)", tickformat=",.0f")
    else:
        fig.update_yaxes(title=display_name)
    return fig


def _benchmark_ids(entity_id: str, entity_ids: list[str], year: int) -> tuple[list[str], bool]:
    saved_target = str(st.session_state.get("bank_peer_target_regnr", ""))
    saved_year = st.session_state.get("bank_peer_year")
    saved_peers = [str(item) for item in st.session_state.get("bank_peer_regnrs", [])]
    target_regnr = entity_id.split(":", maxsplit=1)[-1]
    saved_available = bool(saved_peers) and saved_target == target_regnr and saved_year == year
    options = ["Alle banker"] + (["Gemt peer group"] if saved_available else [])
    benchmark = st.radio("Benchmark", options, horizontal=True, key="analyst_benchmark")
    if benchmark == "Gemt peer group":
        ids = [entity_id] + [f"bank:{regnr}" for regnr in saved_peers if f"bank:{regnr}" in entity_ids]
        return list(dict.fromkeys(ids)), True
    return entity_ids, False


def render(raw: pd.DataFrame):
    render_page_intro(
        "Bank Analyst View",
        "Forbered et møde med én bank: aktuelle nøgletal, udvikling og dokumenteret benchmark i ét samlet workflow.",
        context="Bank · Mødeforberedelse",
    )
    years = available_bank_years(raw)
    if not years:
        st.warning("Ingen finansår for banker er tilgængelige.")
        return
    saved_year = st.session_state.get("bank_peer_year")
    default_year = saved_year if saved_year in years else years[-1]
    render_section_intro("Valg", "Vælg bank, finansår og benchmarkpopulation.")
    year = st.selectbox("År", years, index=years.index(default_year), key="analyst_year")
    entities = bank_entities_for_year(raw, year)
    if entities.empty:
        st.warning("Ingen banker er tilgængelige i det valgte år.")
        return
    entity_names = dict(zip(entities["entity_id"], entities["display_name"]))
    entity_ids = entities["entity_id"].tolist()
    saved_target = str(st.session_state.get("bank_peer_target_regnr", ""))
    default_entity = f"bank:{saved_target}" if f"bank:{saved_target}" in entity_ids else entity_ids[0]
    entity_id = st.selectbox(
        "Bank", entity_ids, index=entity_ids.index(default_entity),
        format_func=lambda value: entity_names.get(value, value), key="analyst_bank",
    )
    benchmark_ids, saved_group_used = _benchmark_ids(entity_id, entity_ids, year)
    comparison, history, overview = build_bank_analyst_view(raw, entity_id, year, benchmark_ids)
    benchmark_definition = (
        "Gemt peer group" if saved_group_used else "Alle banker med en observation i det valgte år"
    )

    render_section_intro("Bankoverblik", "Overblikket bygger på den valgte bank og den aktuelle benchmarkpopulation.")
    render_kpi_cards([
        (overview["display_name"], "Bank"),
        (format_danish_kpi_value(overview["total_assets"], {"display_format": "dkk_billion_tdk", "decimals": 1}), "Aktiver i alt"),
        (f"{overview['benchmark_size']} banker", "Benchmark"),
        (overview["metrics_with_data"], "Kernemetrikker med data"),
    ])

    for section in SECTION_ORDER:
        section_rows = comparison.loc[comparison["section"].eq(section)].copy()
        if section_rows.empty:
            continue
        render_section_intro(
            SECTION_LABELS[section],
            "Aktuel værdi, ændring fra foregående finansår, benchmarkmedian og op til fem tilgængelige finansår.",
        )
        for _, row in section_rows.iterrows():
            meta = _metric_meta(row)
            st.markdown(f"#### {row['display_name']}")
            render_kpi_cards([
                (format_danish_kpi_value(row["current_value"], meta), "Aktuel værdi"),
                (format_danish_kpi_delta(row["yoy_change"], meta), f"Ændring vs. {year - 1}"),
                (format_danish_kpi_value(row["peer_median"], meta), "Benchmarkmedian"),
            ])
            metric_history = history.loc[history["metric_id"].eq(row["metric_id"])].copy()
            if metric_history.empty:
                st.caption("Ingen historiske observationer med komplette input er tilgængelige for denne metrik.")
            else:
                st.plotly_chart(
                    _history_chart(metric_history, row["display_name"], meta, overview["display_name"]),
                    use_container_width=True,
                    config=plotly_export_config(f"Databank_Bank_Analyst_{overview['regnr']}_{row['metric_id'].replace('.', '_')}"),
                )

    render_section_intro("Detaljeret sammenligning", "Tabellen viser samme reproducerbare aktuelle værdi, YoY og benchmarkmedian som ovenfor.")
    table = comparison.copy()
    table["section"] = table["section"].map(SECTION_LABELS)
    table["Aktuel værdi"] = table.apply(lambda row: format_danish_kpi_value(row["current_value"], _metric_meta(row)), axis=1)
    table[f"Ændring vs. {year - 1}"] = table.apply(lambda row: format_danish_kpi_delta(row["yoy_change"], _metric_meta(row)), axis=1)
    table["Benchmarkmedian"] = table.apply(lambda row: format_danish_kpi_value(row["peer_median"], _metric_meta(row)), axis=1)
    st.dataframe(
        table.rename(columns={"display_name": "Metrik", "section": "Sektion", "validation_status": "Valideringsstatus"})[
            ["Sektion", "Metrik", "Aktuel værdi", f"Ændring vs. {year - 1}", "Benchmarkmedian", "Valideringsstatus"]
        ],
        use_container_width=True,
        hide_index=True,
    )
    st.download_button(
        "Download Excel",
        data=bank_analyst_workbook(comparison, history, overview, year, benchmark_definition),
        file_name=bank_analyst_filename(overview["display_name"], year),
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

    with st.expander("Metode, dækning og afgrænsning"):
        benchmark_text = "den gemte peer group" if saved_group_used else "alle banker med en observation i det valgte år"
        st.markdown(
            f"""
            - **Benchmark:** Benchmarkmedianen beregnes blandt {benchmark_text}; målbanken indgår, når den har data.
            - **YoY:** Aktuel værdi minus den samme metriks observerede værdi i det umiddelbart foregående finansår. Manglende data vises som `–` og erstattes ikke med nul.
            - **Proveniens:** Resultat før skat er rapporteret. De øvrige indtjenings- og balancemål er dokumenterede beregninger; ROE, indtjening pr. omkostningskrone og udlån/egenkapital genbruger KPI-registrets validerede beregninger.
            - **Udskudt:** Indlån, selvstændige omkostninger/cost-income, kapitalprocenter og risikomål indgår ikke, fordi deres definitioner endnu ikke er valideret.
            - **Output:** Tabellen kan hentes som Excel med metodekontekst. Plotly-diagrammer kan hentes som PNG fra download-knappen i diagrammets værktøjslinje.
            """
        )

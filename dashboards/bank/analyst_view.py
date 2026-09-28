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
from ui.components import render_page_intro, render_section_intro
from ui.formatting import brand_plotly, format_kpi_delta, format_kpi_value
from ui.theme import PURPLE


DASHBOARD_META = {
    "name": "Bank Analyst View",
    "description": "Forbered et bankmøde med dokumenterede nøgletal, udvikling og peer-benchmark.",
}

SECTION_ORDER = ("Earnings", "Profitability", "Efficiency", "Growth / balance sheet", "Capital & risk")
SECTION_LABELS = {
    "Earnings": "Indtjening",
    "Profitability": "Profitabilitet",
    "Efficiency": "Effektivitet",
    "Growth / balance sheet": "Vækst og balance",
    "Capital & risk": "Kapital og risiko",
}


def _metric_meta(row: pd.Series) -> dict:
    return {"display_format": row["display_format"], "decimals": 1 if row["display_format"] == "percentage" else 2}


def _history_chart(history: pd.DataFrame, display_name: str, meta: dict):
    fig = px.line(history, x="fiscal_year", y="value", markers=True, color_discrete_sequence=[PURPLE])
    brand_plotly(fig)
    fig.update_layout(showlegend=False, height=260, margin=dict(l=20, r=20, t=20, b=20))
    fig.update_xaxes(title="År", dtick=1)
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
    )
    years = available_bank_years(raw)
    if not years:
        st.warning("Ingen finansår for banker er tilgængelige.")
        return
    saved_year = st.session_state.get("bank_peer_year")
    default_year = saved_year if saved_year in years else years[-1]
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

    render_section_intro("Bankoverblik", "Overblikket bygger på den valgte bank og den aktuelle benchmarkpopulation.")
    overview_columns = st.columns(4)
    overview_columns[0].metric("Bank", overview["display_name"])
    overview_columns[1].metric(
        "Aktiver i alt",
        format_kpi_value(overview["total_assets"], {"display_format": "dkk_billion_tdk", "decimals": 1}),
    )
    overview_columns[2].metric("Benchmark", f"{overview['benchmark_size']} banker")
    overview_columns[3].metric("Kernemetrikker med data", overview["metrics_with_data"])

    for section in SECTION_ORDER:
        section_rows = comparison.loc[comparison["section"].eq(section)].copy()
        if section_rows.empty:
            continue
        render_section_intro(
            SECTION_LABELS[section],
            "Aktuel værdi, ændring fra foregående finansår, peer-median og op til fem tilgængelige finansår.",
        )
        for _, row in section_rows.iterrows():
            meta = _metric_meta(row)
            st.markdown(f"#### {row['display_name']}")
            metric_columns = st.columns(3)
            metric_columns[0].metric("Aktuel værdi", format_kpi_value(row["current_value"], meta))
            metric_columns[1].metric(f"Ændring vs. {year - 1}", format_kpi_delta(row["yoy_change"], meta))
            metric_columns[2].metric("Peer-median", format_kpi_value(row["peer_median"], meta))
            metric_history = history.loc[history["metric_id"].eq(row["metric_id"])].copy()
            if metric_history.empty:
                st.caption("Ingen historiske observationer med komplette input er tilgængelige for denne metrik.")
            else:
                st.plotly_chart(_history_chart(metric_history, row["display_name"], meta), use_container_width=True)

    render_section_intro("Detaljeret sammenligning", "Tabellen viser samme reproducerbare aktuelle værdi, YoY og peer-median som ovenfor.")
    table = comparison.copy()
    table["Aktuel værdi"] = table.apply(lambda row: format_kpi_value(row["current_value"], _metric_meta(row)), axis=1)
    table[f"Ændring vs. {year - 1}"] = table.apply(lambda row: format_kpi_delta(row["yoy_change"], _metric_meta(row)), axis=1)
    table["Peer-median"] = table.apply(lambda row: format_kpi_value(row["peer_median"], _metric_meta(row)), axis=1)
    st.dataframe(
        table.rename(columns={"display_name": "Metrik", "section": "Sektion", "validation_status": "Valideringsstatus"})[
            ["Sektion", "Metrik", "Aktuel værdi", f"Ændring vs. {year - 1}", "Peer-median", "Valideringsstatus"]
        ],
        use_container_width=True,
        hide_index=True,
    )

    with st.expander("Metode, dækning og afgrænsning"):
        benchmark_text = "den gemte peer group" if saved_group_used else "alle banker med en observation i det valgte år"
        st.markdown(
            f"""
            - **Benchmark:** Peer-medianen beregnes blandt {benchmark_text}; målbanken indgår, når den har data.
            - **YoY:** Aktuel værdi minus den samme metriks observerede værdi i det umiddelbart foregående finansår. Manglende data vises som `–` og erstattes ikke med nul.
            - **Proveniens:** Resultat før skat er rapporteret. De øvrige indtjenings- og balancemål er dokumenterede beregninger; ROE, indtjening pr. omkostningskrone og udlån/egenkapital genbruger KPI-registrets validerede beregninger.
            - **Udskudt:** Indlån, selvstændige omkostninger/cost-income, kapitalprocenter og risikomål indgår ikke, fordi deres definitioner endnu ikke er valideret.
            """
        )

"""Client Intelligence performance snapshot."""

from dashboards.client_intelligence._shared import (
    render_compact_card,
    render_shell,
    render_status_label,
)
from dashboards.client_intelligence.content import H1_2026_PERFORMANCE_KPIS, Q2_2026_MOMENTUM
import streamlit as st
from ui.components import render_kpi_cards, render_section_intro


DASHBOARD_META = {"name": "Performance", "description": "Existing Databank performance analysis entry point.", "order": 20}


def render(_raw_data):
    render_shell("Performance", "Reported H1 2026 performance snapshot for AL Sydbank.")
    render_section_intro("H1 2026 headline KPIs", "Reported figures from AL Sydbank's interim report.")
    render_kpi_cards([(item.detail, item.title) for item in H1_2026_PERFORMANCE_KPIS[:3]])
    render_kpi_cards([(item.detail, item.title) for item in H1_2026_PERFORMANCE_KPIS[3:6]])
    render_status_label("Public fact · H1 2026 · Official company reporting")

    render_section_intro("Q2 momentum", "Directly comparable reported post-merger Q1 and Q2 figures.")
    columns = st.columns(2)
    for index, (title, q1, q2) in enumerate(Q2_2026_MOMENTUM):
        with columns[index % 2]:
            render_compact_card(title, f"Q1 2026: {q1}  →  Q2 2026: {q2}", label="Public fact")
    render_status_label("H1 2025 P&L comparatives reflect former Sydbank and are not directly comparable with post-merger AL Sydbank.")

    render_section_intro("Deeper analysis", "Use Databank for KPI detail, peer benchmarking and historical analysis.")
    for column, (title, detail) in zip(st.columns(3), (
        ("Financial performance", "Inspect validated financial KPIs."),
        ("Peer benchmarking", "Compare AL Sydbank with relevant bank peers."),
        ("Historical development", "Review performance trends over time."),
    )):
        with column:
            render_compact_card(title, detail, label="Bank Analyst View")
    render_status_label("Available in Databank · Bank → Bank Analyst View")

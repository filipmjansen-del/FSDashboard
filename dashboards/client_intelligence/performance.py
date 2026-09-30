"""Client Intelligence performance shell."""

from dashboards.client_intelligence._shared import (
    render_compact_card,
    render_shell,
    render_status_label,
)
import streamlit as st
from ui.components import render_section_intro


DASHBOARD_META = {"name": "Performance", "description": "Existing Databank performance analysis entry point.", "order": 20}


def render(_raw_data):
    render_shell("Performance", "Existing Databank financial analysis for AL Sydbank.")
    render_section_intro("Explore existing performance analysis", "Bank Analyst View provides the financial context for the client conversation.")
    performance_cards = (
        ("Financial performance", "Inspect validated financial KPIs."),
        ("Peer benchmarking", "Compare AL Sydbank with relevant bank peers."),
        ("Historical development", "Review performance trends over time."),
    )
    columns = st.columns(len(performance_cards))
    for column, (title, detail) in zip(columns, performance_cards):
        with column:
            render_compact_card(title, detail, label="Bank Analyst View")
    render_status_label("Available in Databank · Bank → Bank Analyst View")

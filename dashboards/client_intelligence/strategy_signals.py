"""Client Intelligence strategy and signals shell."""

import streamlit as st

from dashboards.client_intelligence._shared import (
    render_compact_card,
    render_metadata_line,
    render_shell,
)
from dashboards.client_intelligence.content import (
    CUSTOMER_PROPOSITION_SIGNAL,
    MERGER_FACTS,
    STRATEGIC_POSITIONING_SIGNAL,
)
from ui.components import render_section_intro


DASHBOARD_META = {"name": "Strategy & Signals", "description": "Public AL Sydbank strategy and signal view.", "order": 30}


def render(_raw_data):
    render_shell("Strategy & Signals", "Public signals relevant to the management conversation.")
    render_section_intro("Integration & synergies", "Reported H1 2026 merger evidence.")
    merger_columns = st.columns(2)
    for index, item in enumerate(MERGER_FACTS):
        with merger_columns[index % 2]:
            render_compact_card(item.title, item.detail, label=item.information_type)
            render_metadata_line(item)

    render_section_intro("Customer proposition & strategic positioning", "Public signals on proposition and direction.")
    signal_columns = st.columns(2)
    for column, item in zip(signal_columns, (CUSTOMER_PROPOSITION_SIGNAL, STRATEGIC_POSITIONING_SIGNAL)):
        with column:
            render_compact_card(item.title, item.detail, label=item.information_type)
            render_metadata_line(item)

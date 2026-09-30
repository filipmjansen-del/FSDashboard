"""Client Intelligence strategy and signals shell."""

import streamlit as st

from dashboards.client_intelligence._shared import (
    render_compact_card,
    render_metadata_line,
    render_shell,
)
from dashboards.client_intelligence.content import (
    DOCUMENTED_AL_SYDBANK_SIGNALS,
    THURSDAY_PERSPECTIVES,
)
from ui.components import render_section_intro


DASHBOARD_META = {"name": "Strategy & Signals", "description": "Public AL Sydbank strategy and signal view.", "order": 30}


def render(_raw_data):
    render_shell("Strategy & Signals", "What is changing at AL Sydbank and which signals matter for the next conversation.")
    render_section_intro("Documented AL Sydbank signals", "Public fact · reported merger, strategy and commercial signals.")
    signal_columns = st.columns(2)
    for index, item in enumerate(DOCUMENTED_AL_SYDBANK_SIGNALS):
        with signal_columns[index % 2]:
            render_compact_card(item.title, item.detail, label=item.information_type)
            render_metadata_line(item)

    render_section_intro("Thursday benchmark perspective", "Internal Thursday perspective · benchmark inspirations, not statements about AL Sydbank's current model.")
    benchmark_columns = st.columns(2)
    for index, item in enumerate(THURSDAY_PERSPECTIVES):
        with benchmark_columns[index % 2]:
            render_compact_card(item.title, item.detail, label=item.information_type)
            render_metadata_line(item)

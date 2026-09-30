"""Client Intelligence Thursday footprint shell."""

import streamlit as st

from dashboards.client_intelligence._shared import (
    render_compact_card,
    render_metadata_line,
    render_shell,
    render_status_label,
)
from dashboards.client_intelligence.content import THURSDAY_CAPABILITIES, THURSDAY_PERSPECTIVES
from ui.components import render_section_intro


DASHBOARD_META = {"name": "Thursday Footprint", "description": "Safe Thursday activity and capability view.", "order": 50}


def render(_raw_data):
    render_shell("Thursday Footprint", "Recent perspectives and potentially relevant Thursday capabilities.")
    render_section_intro("Recent activity", "Existing Thursday material for the AL Sydbank discussion.")
    activity_columns = st.columns(len(THURSDAY_PERSPECTIVES))
    for column, perspective in zip(activity_columns, THURSDAY_PERSPECTIVES):
        with column:
            render_compact_card(perspective.title, perspective.detail, label=perspective.information_type)
            render_metadata_line(perspective)

    render_section_intro("Relevant Thursday capabilities", "Potentially relevant capabilities, not confirmed client needs.")
    capability_columns = st.columns(2)
    for index, capability in enumerate(THURSDAY_CAPABILITIES):
        with capability_columns[index % 2]:
            render_compact_card(capability, "Potentially relevant capability")
            render_status_label("Not a confirmed client need")
    render_status_label("Experience & proof: Previous projects, cases, experts, and reusable assets will appear here when available.")

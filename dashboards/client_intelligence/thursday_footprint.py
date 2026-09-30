"""Client Intelligence Thursday footprint shell."""

import streamlit as st

from dashboards.client_intelligence._shared import (
    render_compact_card,
    render_metadata_line,
    render_shell,
    render_status_label,
)
from dashboards.client_intelligence.content import THURSDAY_CAPABILITY_MAPPINGS, THURSDAY_FOOTPRINT
from ui.components import render_section_intro


DASHBOARD_META = {"name": "Thursday Footprint", "description": "Safe Thursday activity and capability view.", "order": 50}


def render(_raw_data):
    render_shell("Thursday Footprint", "Client-specific Thursday material and potentially relevant capabilities.")
    render_section_intro("Client-specific Thursday footprint", "Existing Thursday material and account activity for AL Sydbank.")
    activity_columns = st.columns(2)
    for index, item in enumerate(THURSDAY_FOOTPRINT):
        with activity_columns[index % 2]:
            render_compact_card(item.title, item.detail, label=item.information_type)
            render_metadata_line(item)

    render_section_intro("Potentially relevant Thursday capabilities", "Thursday perspective · not confirmed AL Sydbank needs.")
    capability_columns = st.columns(2)
    for index, capability in enumerate(THURSDAY_CAPABILITY_MAPPINGS):
        with capability_columns[index % 2]:
            render_compact_card(capability.title, capability.detail, label=capability.information_type)
            render_status_label("Not a confirmed client need")

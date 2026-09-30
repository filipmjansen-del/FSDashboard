"""Client Intelligence people and relations shell."""

import streamlit as st

from dashboards.client_intelligence._shared import (
    render_compact_card,
    render_metadata_line,
    render_shell,
    render_status_label,
)
from dashboards.client_intelligence.content import INTERNAL_ACCOUNT_MAPPING, PUBLIC_EXECUTIVES, RECENT_ACCOUNT_ACTIVITY
from ui.components import render_section_intro


DASHBOARD_META = {"name": "People & Relations", "description": "Public organisation and safe account-mapping view.", "order": 40}


def render(_raw_data):
    render_shell("People & Relations", "Public leadership and current account-mapping coverage.")
    render_section_intro("Public leadership", "Public executive management information.")
    executive_columns = st.columns(3)
    for index, person in enumerate(PUBLIC_EXECUTIVES):
        with executive_columns[index % 3]:
            render_compact_card(person.title, person.detail, label="Public executive")
    render_metadata_line(PUBLIC_EXECUTIVES[0])

    render_section_intro("Thursday account coverage", "Existing Thursday relationship mapping only; no relationship strength is implied.")
    mapping_columns = st.columns(3)
    for index, person in enumerate(PUBLIC_EXECUTIVES):
        with mapping_columns[index % 2]:
            if person.title in INTERNAL_ACCOUNT_MAPPING:
                render_compact_card(person.title, "Existing Thursday relationship mapping", label="Thursday internal knowledge")
            else:
                render_compact_card(person.title, "No relationship mapping evidenced in current source set", label="Thursday internal knowledge")
            render_status_label("Mapping status only; no relationship assessment shown")

    render_section_intro("Recent and planned account activity", "Thursday internal knowledge · concise activity record.")
    activity_columns = st.columns(2)
    for index, item in enumerate(RECENT_ACCOUNT_ACTIVITY):
        with activity_columns[index % 2]:
            render_compact_card(item.title, item.detail, label=item.information_type)
            render_metadata_line(item)

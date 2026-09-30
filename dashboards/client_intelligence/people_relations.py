"""Client Intelligence people and relations shell."""

import streamlit as st

from dashboards.client_intelligence._shared import (
    render_compact_card,
    render_metadata_line,
    render_shell,
    render_status_label,
)
from dashboards.client_intelligence.content import INTERNAL_ACCOUNT_MAPPING, PUBLIC_EXECUTIVES
from ui.components import render_section_intro


DASHBOARD_META = {"name": "People & Relations", "description": "Public organisation and safe account-mapping view.", "order": 40}


def render(_raw_data):
    render_shell("People & Relations", "Public leadership and current account-mapping coverage.")
    render_section_intro("Public organisation", "Current public executive information.")
    executive_columns = st.columns(3)
    for index, person in enumerate(PUBLIC_EXECUTIVES):
        with executive_columns[index % 3]:
            render_compact_card(person.title, person.detail, label="Public executive")
    render_metadata_line(PUBLIC_EXECUTIVES[0])

    render_section_intro("Internal account mapping", "Coverage status only; no relationship strength is implied.")
    mapping_columns = st.columns(3)
    for index, mapping in enumerate(INTERNAL_ACCOUNT_MAPPING):
        with mapping_columns[index % 2]:
            person_name = mapping.removesuffix(" — Account mapping available")
            render_compact_card(person_name, "Account mapping available", label="Internal mapping")
            render_status_label("No relationship assessment shown")

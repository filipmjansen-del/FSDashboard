"""Client Intelligence people and relations shell."""

import streamlit as st

from dashboards.client_intelligence._shared import render_item, render_not_connected, render_shell
from dashboards.client_intelligence.content import INTERNAL_ACCOUNT_MAPPING, PUBLIC_EXECUTIVES
from ui.components import render_kpi_cards, render_section_intro


DASHBOARD_META = {"name": "People & Relations", "description": "Public organisation and safe account-mapping view.", "order": 40}


def render(_raw_data):
    render_shell("People & Relations", "Public organisation information and safe internal account-mapping status.")
    render_section_intro("Public organisation", "Official AL Sydbank public organisation information.")
    render_kpi_cards([(person.title, person.detail) for person in PUBLIC_EXECUTIVES])
    render_item(PUBLIC_EXECUTIVES[0])
    render_section_intro("Internal account mapping", "Prototype status only; no relationship scores or strength are shown.")
    for mapping in INTERNAL_ACCOUNT_MAPPING:
        st.caption(mapping)
    render_not_connected("Meeting history, relationship owner and latest interaction")

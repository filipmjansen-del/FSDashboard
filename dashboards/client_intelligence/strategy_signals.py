"""Client Intelligence strategy and signals shell."""

import streamlit as st

from dashboards.client_intelligence._shared import render_item, render_shell
from dashboards.client_intelligence.content import (
    CUSTOMER_PROPOSITION_SIGNAL,
    H1_2026_PAGE_30_SOURCE,
    H1_2026_PAGE_46_SOURCE,
    LARGER_BANK_SOURCE,
    STRATEGIC_POSITIONING_SIGNAL,
)
from ui.components import render_orientation_card, render_section_intro


DASHBOARD_META = {"name": "Strategy & Signals", "description": "Public AL Sydbank strategy and signal view.", "order": 30}


def render(_raw_data):
    render_shell("Strategy & Signals", "Three concise public signals for the AL Sydbank management conversation.")
    render_section_intro("Integration & synergies", "Public H1 2026 merger and integration evidence.")
    render_orientation_card("Integration & synergies", "DKK 32m integration costs; the reported costs primarily relate to BEC exit compensation. The H1 report also describes acquisition goodwill and its potential relation to significant cost and capital synergies.")
    st.caption("Fact · H1 2026")
    st.markdown(f"[Report page 30]({H1_2026_PAGE_30_SOURCE.url}) · [Report page 46]({H1_2026_PAGE_46_SOURCE.url})")
    render_section_intro("Customer proposition", "Public September 2026 customer proposition signal.")
    render_item(CUSTOMER_PROPOSITION_SIGNAL)
    render_section_intro("Strategic positioning", "Public merger communication.")
    render_item(STRATEGIC_POSITIONING_SIGNAL)
    st.markdown(f"[Additional public source]({LARGER_BANK_SOURCE.url})")

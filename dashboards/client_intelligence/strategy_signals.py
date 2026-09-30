"""Client Intelligence strategy and signals shell."""

from dashboards.client_intelligence._shared import render_item, render_items, render_shell
from dashboards.client_intelligence.content import (
    CUSTOMER_PROPOSITION_SIGNAL,
    MERGER_FACTS,
    STRATEGIC_POSITIONING_SIGNAL,
)
from ui.components import render_section_intro


DASHBOARD_META = {"name": "Strategy & Signals", "description": "Public AL Sydbank strategy and signal view.", "order": 30}


def render(_raw_data):
    render_shell("Strategy & Signals", "Three concise public signals for the AL Sydbank management conversation.")
    render_section_intro("Integration & synergies", "Public H1 2026 merger and integration evidence.")
    render_items(MERGER_FACTS)
    render_section_intro("Customer proposition", "Public September 2026 customer proposition signal.")
    render_item(CUSTOMER_PROPOSITION_SIGNAL)
    render_section_intro("Strategic positioning", "Public merger communication.")
    render_item(STRATEGIC_POSITIONING_SIGNAL)

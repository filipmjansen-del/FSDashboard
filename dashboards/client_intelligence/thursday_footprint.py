"""Client Intelligence Thursday footprint shell."""

from dashboards.client_intelligence._shared import render_items, render_not_connected, render_shell
from dashboards.client_intelligence.content import THURSDAY_CAPABILITIES, THURSDAY_PERSPECTIVES
from ui.components import render_kpi_cards, render_section_intro


DASHBOARD_META = {"name": "Thursday Footprint", "description": "Safe Thursday activity and capability view.", "order": 50}


def render(_raw_data):
    render_shell("Thursday Footprint", "Safe representation of recent activity and potential capability relevance.")
    render_section_intro("Recent activity", "Documented Thursday material.")
    render_items(THURSDAY_PERSPECTIVES)
    render_section_intro("Relevant Thursday capabilities", "Examples of potentially relevant capabilities, not confirmed AL Sydbank needs.")
    render_kpi_cards([(capability, "Potentially relevant") for capability in THURSDAY_CAPABILITIES])
    render_not_connected("Previous projects, cases, experts and reusable assets")

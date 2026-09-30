"""Client Intelligence overview for the fixed AL Sydbank pilot."""

import streamlit as st

from ui.components import (
    render_kpi_cards,
    render_page_intro,
    render_section_intro,
)

from dashboards.client_intelligence._shared import (
    PILOT_ENTITY,
    render_hypothesis,
    render_item,
    render_items,
    render_not_connected,
    render_pilot_notice,
)
from dashboards.client_intelligence.content import (
    COMMERCIAL_HYPOTHESES,
    CUSTOMER_PROPOSITION_SIGNAL,
    PERFORMANCE_GUIDANCE,
    PUBLIC_EXECUTIVES,
    STRATEGIC_POSITIONING_SIGNAL,
    THURSDAY_CAPABILITIES,
)


DASHBOARD_META = {
    "name": "Overview",
    "description": "Manually curated client-intelligence overview for the AL Sydbank pilot.",
    "order": 10,
}


def render(_raw_data):
    render_page_intro(
        "Client Intelligence",
        "A fixed-pilot meeting-preparation workspace combining documented evidence, Thursday perspectives, and clearly qualified hypotheses.",
        context=f"Client Intelligence · {PILOT_ENTITY}",
    )
    render_pilot_notice()

    render_section_intro("Company snapshot", "Management meeting-preparation context.")
    render_kpi_cards([
        (PILOT_ENTITY, "Pilot entity"),
        ("Integration phase", "Merged bank"),
        ("H1 2026", "Latest public reporting"),
    ])

    render_section_intro("Performance snapshot", "Use the existing Bank Analyst View for financial metrics and benchmark context.")
    render_item(PERFORMANCE_GUIDANCE)

    render_section_intro("Key signals", "Three public signals for the meeting agenda.")
    render_kpi_cards([
        ("DKK 32m", "H1 2026 integration costs"),
        ("Fees removed", "Relevant private customers · Sep. 2026"),
        ("Broader offer", "Public strategic positioning"),
    ])
    render_item(CUSTOMER_PROPOSITION_SIGNAL)
    render_item(STRATEGIC_POSITIONING_SIGNAL)

    render_section_intro("People & relations", "Public leadership view with a safe internal account-mapping indicator.")
    render_kpi_cards([(item.title, item.detail) for item in PUBLIC_EXECUTIVES[:4]])
    st.caption("Internal account mapping available for the public leadership list. Relationship strength is not shown.")

    render_section_intro("Thursday footprint", "September 2026 benchmarking activity and relevant capability areas.")
    render_kpi_cards([(capability, "Potentially relevant capability") for capability in THURSDAY_CAPABILITIES])
    st.caption("Thursday perspective · September 2026 · Not a statement of confirmed AL Sydbank need.")

    render_section_intro("Opportunities", "Hypotheses only; not confirmed client needs.")
    for hypothesis in COMMERCIAL_HYPOTHESES:
        render_hypothesis(hypothesis)

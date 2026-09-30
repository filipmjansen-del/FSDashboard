"""Client Intelligence overview for the fixed AL Sydbank pilot."""

import streamlit as st

from ui.components import (
    render_kpi_cards,
    render_page_intro,
    render_section_intro,
)

from dashboards.client_intelligence._shared import (
    render_hypothesis,
    render_item,
    render_items,
    render_pilot_notice,
)
from dashboards.client_intelligence.content import (
    COMMERCIAL_HYPOTHESES,
    CUSTOMER_PROPOSITION_SIGNAL,
    MERGER_FACTS,
    PERFORMANCE_GUIDANCE,
    PILOT_CONTEXT,
    PUBLIC_EXECUTIVES,
    STRATEGIC_POSITIONING_SIGNAL,
    THURSDAY_CAPABILITIES,
    THURSDAY_PERSPECTIVES,
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
        context=f"Client Intelligence · {PILOT_CONTEXT.display_name}",
    )
    render_pilot_notice()

    render_section_intro("Company snapshot", "Management meeting-preparation context.")
    render_kpi_cards([
        (PILOT_CONTEXT.display_name, PILOT_CONTEXT.pilot_label),
        (PILOT_CONTEXT.latest_reporting_label, "Latest public reporting"),
    ])

    render_section_intro("Performance snapshot", "Use the existing Bank Analyst View for financial metrics and benchmark context.")
    render_item(PERFORMANCE_GUIDANCE)

    render_section_intro("Key signals", "Three public signals for the meeting agenda.")
    render_item(MERGER_FACTS[0])
    render_item(CUSTOMER_PROPOSITION_SIGNAL)
    render_item(STRATEGIC_POSITIONING_SIGNAL)

    render_section_intro("People & relations", "Public leadership view with a safe internal account-mapping indicator.")
    render_kpi_cards([(item.title, item.detail) for item in PUBLIC_EXECUTIVES[:4]])
    st.caption("Internal account mapping available for the public leadership list. Relationship strength is not shown.")

    render_section_intro("Thursday footprint", "Documented Thursday perspectives and relevant capability areas.")
    render_items(THURSDAY_PERSPECTIVES)
    render_kpi_cards([(capability, "Potentially relevant capability") for capability in THURSDAY_CAPABILITIES])

    render_section_intro("Opportunities", "Hypotheses only; not confirmed client needs.")
    for hypothesis in COMMERCIAL_HYPOTHESES:
        render_hypothesis(hypothesis)

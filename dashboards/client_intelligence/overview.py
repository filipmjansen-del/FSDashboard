"""Client Intelligence overview for the fixed AL Sydbank pilot."""

import streamlit as st

from ui.components import (
    render_kpi_cards,
    render_page_intro,
    render_section_intro,
)

from dashboards.client_intelligence._shared import (
    render_compact_card,
    render_hypothesis,
    render_item,
    render_items,
    render_metadata_line,
    render_pilot_notice,
    render_status_label,
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
    render_compact_card(
        "Bank Analyst View",
        "Existing Databank financial performance and peer benchmarking for the pilot entity.",
        label="Existing capability",
    )
    render_metadata_line(PERFORMANCE_GUIDANCE)

    render_section_intro("Key signals", "Three public signals for the meeting agenda.")
    signal_items = (MERGER_FACTS[0], CUSTOMER_PROPOSITION_SIGNAL, STRATEGIC_POSITIONING_SIGNAL)
    signal_columns = st.columns(len(signal_items))
    for column, item in zip(signal_columns, signal_items):
        with column:
            render_compact_card(item.title, item.detail, label=item.information_type)
            render_metadata_line(item)

    render_section_intro("People & relations", "Public leadership view with a safe internal account-mapping indicator.")
    people_columns = st.columns(4)
    for column, person in zip(people_columns, PUBLIC_EXECUTIVES[:4]):
        with column:
            render_compact_card(person.title, person.detail, label="Public executive")
            render_status_label("Mapped internally")
    st.caption("Account mapping is available; relationship strength is not shown.")

    render_section_intro("Thursday footprint", "Documented Thursday perspectives and relevant capability areas.")
    perspective_columns = st.columns(len(THURSDAY_PERSPECTIVES))
    for column, perspective in zip(perspective_columns, THURSDAY_PERSPECTIVES):
        with column:
            render_compact_card(perspective.title, perspective.detail, label=perspective.information_type)
            render_metadata_line(perspective)
    capability_columns = st.columns(len(THURSDAY_CAPABILITIES))
    for column, capability in zip(capability_columns, THURSDAY_CAPABILITIES):
        with column:
            render_compact_card(capability, "Potentially relevant capability")

    render_section_intro("Opportunities", "Hypotheses only; not confirmed client needs.")
    opportunity_columns = st.columns(len(COMMERCIAL_HYPOTHESES))
    for column, hypothesis in zip(opportunity_columns, COMMERCIAL_HYPOTHESES):
        with column:
            render_compact_card(
                hypothesis.title,
                hypothesis.potential_need,
                label="Hypothesis - requires client validation",
            )
            render_status_label(f"{hypothesis.period} · {len(hypothesis.sources)} source records")

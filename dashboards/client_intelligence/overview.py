"""Client Intelligence overview for the fixed AL Sydbank pilot."""

import streamlit as st

from ui.components import (
    render_kpi_cards,
    render_page_intro,
    render_section_intro,
)

from dashboards.client_intelligence._shared import (
    render_compact_card,
    render_metadata_line,
    render_pilot_notice,
    render_status_label,
)
from dashboards.client_intelligence.content import (
    COMMERCIAL_HYPOTHESES,
    CUSTOMER_PROPOSITION_SIGNAL,
    MERGER_FACTS,
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
        "A concise brief for the next AL Sydbank management conversation.",
        context=f"Client Intelligence · {PILOT_CONTEXT.display_name}",
    )
    render_pilot_notice()

    render_section_intro("Company snapshot", "Management meeting-preparation context.")
    render_kpi_cards([
        (PILOT_CONTEXT.display_name, "Client overview"),
        (PILOT_CONTEXT.latest_reporting_label, "Latest public reporting"),
    ])

    render_section_intro("Performance", "Existing financial analysis and peer benchmarking.")
    render_compact_card(
        "Bank Analyst View",
        "Explore validated financial performance, peer benchmarking, and historical development.",
        label="Existing capability",
    )
    render_status_label("Available in Databank · Bank → Bank Analyst View")

    render_section_intro("Key signals", "Three public signals for the meeting agenda.")
    signal_items = (MERGER_FACTS[0], CUSTOMER_PROPOSITION_SIGNAL, STRATEGIC_POSITIONING_SIGNAL)
    signal_columns = st.columns(len(signal_items))
    for column, item in zip(signal_columns, signal_items):
        with column:
            render_compact_card(item.title, item.detail, label=item.information_type)
            render_metadata_line(item)

    render_section_intro("Key people", "Public leadership and current account coverage.")
    people_columns = st.columns(4)
    for column, person in zip(people_columns, PUBLIC_EXECUTIVES[:4]):
        with column:
            render_compact_card(person.title, person.detail, label="Public executive")
            render_status_label("Account mapping available")
    st.caption("Internal mapping status only; relationship strength is not shown.")

    render_section_intro("Thursday footprint", "Recent perspective and potentially relevant capabilities.")
    perspective_columns = st.columns(2)
    for column, perspective in zip(perspective_columns, THURSDAY_PERSPECTIVES[:2]):
        with column:
            render_compact_card(perspective.title, perspective.detail, label=perspective.information_type)
            render_metadata_line(perspective)
    capability_columns = st.columns(len(THURSDAY_CAPABILITIES))
    for column, capability in zip(capability_columns, THURSDAY_CAPABILITIES):
        with column:
            render_compact_card(capability, "Potentially relevant capability")

    render_section_intro("Opportunities", "Three hypotheses for client validation.")
    opportunity_columns = st.columns(len(COMMERCIAL_HYPOTHESES))
    for column, hypothesis in zip(opportunity_columns, COMMERCIAL_HYPOTHESES):
        with column:
            render_compact_card(
                hypothesis.title,
                hypothesis.potential_need,
                label="Hypothesis - requires client validation",
            )
            render_status_label(f"{hypothesis.period} · evidence chain in Opportunities")

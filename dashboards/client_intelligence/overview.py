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
    H1_2026_SNAPSHOT,
    INTERNAL_ACCOUNT_MAPPING,
    PILOT_CONTEXT,
    PUBLIC_EXECUTIVES,
    THURSDAY_CAPABILITY_MAPPINGS,
    THURSDAY_FOOTPRINT,
    WHAT_MATTERS_NOW,
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

    render_section_intro("Company snapshot", "Reported H1 2026 headline indicators.")
    render_kpi_cards([(item.detail, item.title) for item in H1_2026_SNAPSHOT[:3]])
    render_kpi_cards([(item.detail, item.title) for item in H1_2026_SNAPSHOT[3:]])
    render_status_label("Public fact · H1 2026 · Official company reporting")

    render_section_intro("Performance", "Existing financial analysis and peer benchmarking.")
    render_compact_card(
        "Bank Analyst View",
        "Explore validated financial performance, peer benchmarking, and historical development.",
        label="Existing capability",
    )
    render_status_label("Available in Databank · Bank → Bank Analyst View")

    render_section_intro("What matters now", "Three documented signals for the next conversation.")
    signal_columns = st.columns(len(WHAT_MATTERS_NOW))
    for column, item in zip(signal_columns, WHAT_MATTERS_NOW):
        with column:
            render_compact_card(item.title, item.detail, label=item.information_type)
            render_metadata_line(item)

    render_section_intro("Key people", "Public leadership and existing Thursday relationship mapping.")
    people_columns = st.columns(4)
    for column, person in zip(people_columns, PUBLIC_EXECUTIVES[:4]):
        with column:
            render_compact_card(person.title, person.detail, label="Public executive")
            mapping_label = "Existing Thursday relationship mapping" if person.title in INTERNAL_ACCOUNT_MAPPING else "No mapping evidenced in current source set"
            render_status_label(mapping_label)
    st.caption("Mapping status only; no relationship strength is shown.")

    render_section_intro("Thursday footprint", "Client-specific material and potentially relevant capabilities.")
    perspective_columns = st.columns(2)
    for column, perspective in zip(perspective_columns, THURSDAY_FOOTPRINT[:2]):
        with column:
            render_compact_card(perspective.title, perspective.detail, label=perspective.information_type)
            render_metadata_line(perspective)
    capability_columns = st.columns(2)
    for column, capability in zip(capability_columns, THURSDAY_CAPABILITY_MAPPINGS[:2]):
        with column:
            render_compact_card(capability.title, "Potentially relevant Thursday capability", label="Thursday perspective")

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

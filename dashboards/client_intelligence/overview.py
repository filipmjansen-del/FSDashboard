"""Client Intelligence overview for the fixed AL Sydbank pilot."""

import streamlit as st

from ui.components import (
    render_kpi_cards,
    render_page_intro,
    render_section_intro,
)

from dashboards.client_intelligence._shared import (
    PILOT_ENTITY,
    render_item,
    render_items,
    render_not_connected,
    render_pilot_notice,
)
from dashboards.client_intelligence.content import (
    COMMERCIAL_HYPOTHESES,
    MERGER_FACTS,
    PERFORMANCE_GUIDANCE,
    THURSDAY_PERSPECTIVES,
)


DASHBOARD_META = {
    "name": "Overview",
    "description": "Manually curated client-intelligence overview for the AL Sydbank pilot.",
}


def render(_raw_data):
    render_page_intro(
        "Client Intelligence",
        "A fixed-pilot meeting-preparation workspace combining documented evidence, Thursday perspectives, and clearly qualified hypotheses.",
        context=f"Client Intelligence · {PILOT_ENTITY}",
    )
    render_pilot_notice()

    render_section_intro("Company snapshot", "Fixed MVP pilot entity and manual-content scope.")
    render_kpi_cards([
        (PILOT_ENTITY, "Pilot entity"),
        ("Manual", "Content source"),
        ("MVP", "Workspace status"),
    ])

    render_section_intro("What changed?", "Documented merger and integration evidence from the H1 2026 interim-report material.")
    render_items(MERGER_FACTS)

    render_section_intro("Performance snapshot", "Use the existing Bank Analyst View for financial metrics and benchmark context.")
    render_not_connected("A performance snapshot in Client Intelligence")
    render_item(PERFORMANCE_GUIDANCE)

    render_section_intro("Strategic priorities", "No documented AL Sydbank strategic-priority content is connected yet.")
    render_not_connected("Strategic priorities")

    render_section_intro("Key people & relations", "No people, relationship, LinkedIn, or CRM content is connected yet.")
    render_not_connected("Key people and relations")

    render_section_intro("Thursday footprint", "Thursday perspectives are distinct from AL Sydbank statements.")
    render_items(THURSDAY_PERSPECTIVES)

    render_section_intro("Commercial hypotheses", "Potential needs are hypotheses only; they are not confirmed client needs.")
    for hypothesis in COMMERCIAL_HYPOTHESES:
        st.markdown(f"**{hypothesis.title}**")
        st.markdown(f"**Evidence:** {hypothesis.evidence}")
        st.markdown(f"**Observation:** {hypothesis.observation}")
        st.markdown(f"**Potential need (hypothesis):** {hypothesis.potential_need}")
        st.markdown(f"**Thursday relevance:** {hypothesis.thursday_relevance}")
        st.caption(
            f"Hypothesis · {hypothesis.period} · Source: {hypothesis.source_label}"
        )

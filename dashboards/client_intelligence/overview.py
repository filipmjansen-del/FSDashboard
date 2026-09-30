"""Client Intelligence overview for the fixed AL Sydbank pilot."""

from ui.components import (
    render_kpi_cards,
    render_orientation_card,
    render_page_intro,
    render_section_intro,
)

from dashboards.client_intelligence._shared import PILOT_ENTITY, render_pilot_notice


DASHBOARD_META = {
    "name": "Overview",
    "description": "Mock client-intelligence overview for the AL Sydbank pilot.",
}


def render(_raw_data):
    render_page_intro(
        "Client Intelligence",
        "A fixed-pilot meeting-preparation workspace for AL Sydbank. All content is mock/placeholder only.",
        context=f"Client Intelligence · {PILOT_ENTITY}",
    )
    render_pilot_notice()

    render_section_intro("Company snapshot", "Mock/placeholder profile for the fixed pilot entity.")
    render_kpi_cards([
        (PILOT_ENTITY, "Pilot entity"),
        ("Bank", "Sector · mock"),
        ("Preparation", "Workspace status · mock"),
    ])

    sections = (
        ("What changed?", "Mock change log placeholder. No automated research or monitoring is connected."),
        ("Performance snapshot", "Mock performance placeholder. No production metrics or calculations are displayed."),
        ("Strategic priorities", "Mock strategic-priority placeholder for a future documented research workflow."),
        ("Key people & relations", "Mock relationship placeholder. No people data, LinkedIn, or CRM integration is connected."),
        ("Thursday footprint", "Mock Thursday knowledge placeholder. No SharePoint or internal-system connection is implemented."),
        ("Commercial hypotheses", "Mock hypothesis placeholder. No opportunity-generation logic is implemented."),
    )
    for title, description in sections:
        render_section_intro(title, description)
        render_orientation_card("Mock / placeholder", description)

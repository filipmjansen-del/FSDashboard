"""Shared presentation helpers for the Client Intelligence pilot."""

from ui.components import render_orientation_card, render_page_intro, render_warning_callout


PILOT_ENTITY = "AL Sydbank"
MOCK_NOTICE = (
    "Iteration 1 pilot for AL Sydbank. All content on this page is clearly labelled "
    "mock/placeholder content and is not sourced from production data."
)


def render_pilot_notice():
    render_warning_callout(MOCK_NOTICE)


def render_shell(title: str, description: str):
    render_page_intro(title, description, context=f"Client Intelligence · {PILOT_ENTITY}")
    render_pilot_notice()
    render_orientation_card(
        "Placeholder view",
        "This lightweight shell defines the future workspace only. No data integration, "
        "research automation, matching logic, or chat capability is implemented.",
    )

"""Shared presentation helpers for the Client Intelligence pilot."""

import streamlit as st

from dashboards.client_intelligence.content import PILOT_ENTITY
from ui.components import render_orientation_card, render_page_intro, render_warning_callout

PILOT_NOTICE = (
    "AL Sydbank MVP pilot. Content is manually curated; facts, Thursday perspectives, "
    "and hypotheses are shown separately. It is not connected to production data or research systems."
)


def render_pilot_notice():
    render_warning_callout(PILOT_NOTICE)


def render_item(item):
    st.markdown(f"**{item.title}**")
    st.write(item.detail)
    st.caption(
        f"{item.information_type} · {item.period} · Source: {item.source_label}"
    )


def render_items(items):
    for item in items:
        render_item(item)


def render_not_connected(subject: str):
    render_orientation_card(
        "Not yet connected",
        f"{subject} is not yet available in the manual AL Sydbank MVP content. "
        "No value has been invented to fill this state.",
    )


def render_shell(title: str, description: str):
    render_page_intro(title, description, context=f"Client Intelligence · {PILOT_ENTITY}")
    render_pilot_notice()
    render_orientation_card(
        "MVP scope",
        "This lightweight view uses only manually curated pilot content. No data integration, "
        "research automation, matching logic, or chat capability is implemented.",
    )

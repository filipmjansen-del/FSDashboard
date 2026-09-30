"""Shared presentation helpers for the Client Intelligence pilot."""

import streamlit as st

from dashboards.client_intelligence.content import PILOT_CONTEXT
from ui.components import render_orientation_card, render_page_intro, render_warning_callout

PILOT_NOTICE = (
    f"{PILOT_CONTEXT.pilot_label}. Content is manually curated; facts, Thursday perspectives, "
    "and hypotheses are shown separately. It is not connected to production data or research systems."
)


def render_pilot_notice():
    st.caption(PILOT_NOTICE)


def render_item(item):
    st.markdown(f"**{item.title}**")
    st.write(item.detail)
    st.caption(f"{item.information_type} · {item.period}")
    with st.expander("Source details", expanded=False):
        render_source_metadata(item.source)


def render_source_metadata(source):
    st.caption(f"Source title: {source.title}")
    st.caption(f"Publisher: {source.publisher} · Publication date: {source.publication_date}")
    page_reference = source.page_reference or "Not applicable"
    st.caption(f"Page reference: {page_reference} · Source type: {source.source_type}")
    if source.url:
        st.markdown(f"[Open source]({source.url})")
    else:
        st.caption("Source URL: Unresolved — no official public URL has been verified yet.")


def render_items(items):
    for item in items:
        render_item(item)


def render_not_connected(subject: str):
    render_orientation_card(
        "Not yet connected",
        f"{subject} is not yet available in the manual {PILOT_CONTEXT.display_name} MVP content. "
        "No value has been invented to fill this state.",
    )


def render_shell(title: str, description: str):
    render_page_intro(title, description, context=f"Client Intelligence · {PILOT_CONTEXT.display_name}")


def render_hypothesis(hypothesis):
    st.markdown(f"**{hypothesis.title}**")
    st.caption("Hypothesis - requires client validation")
    st.write(f"**Evidence:** {hypothesis.evidence}")
    st.write(f"**Observation:** {hypothesis.observation}")
    st.write(f"**Potential need:** {hypothesis.potential_need}")
    st.write(f"**Thursday relevance:** {hypothesis.thursday_relevance}")
    st.caption(f"Hypothesis · {hypothesis.period}")
    with st.expander("Source details", expanded=False):
        for source in hypothesis.sources:
            render_source_metadata(source)

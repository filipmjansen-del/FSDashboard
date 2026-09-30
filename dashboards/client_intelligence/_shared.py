"""Shared presentation helpers for the Client Intelligence pilot."""

import streamlit as st

from dashboards.client_intelligence.content import PILOT_CONTEXT
from ui.components import render_orientation_card, render_page_intro, render_warning_callout

PILOT_NOTICE = (
    "Prototype view · Documented facts, Thursday perspectives, and hypotheses are shown separately."
)


def render_pilot_notice():
    st.caption(PILOT_NOTICE)


def render_compact_card(title: str, detail: str, *, label: str | None = None):
    """Render a compact content card using the existing orientation-card theme."""
    heading = f"{label} · {title}" if label else title
    render_orientation_card(heading, detail)


def render_status_label(label: str):
    """Render a compact, secondary status or information-type label."""
    st.caption(label)


def render_metadata_line(item):
    """Render compact source metadata while retaining a clickable URL when available."""
    source = item.source
    page = f" · {source.page_reference}" if source.page_reference else ""
    metadata = f"{item.information_type} · {item.period} · {source.title}{page}"
    if source.url:
        st.markdown(f"[{metadata}]({source.url})")
    else:
        st.caption(metadata)


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
        f"{subject} will appear here when connected. No value is shown until then.",
    )


def render_shell(title: str, description: str):
    render_page_intro(title, description, context=f"Client Intelligence · {PILOT_CONTEXT.display_name}")


def render_hypothesis(hypothesis):
    st.markdown(f"**{hypothesis.title}**")
    render_status_label("Hypothesis - requires client validation")
    chain = (
        ("Evidence", hypothesis.evidence),
        ("Observation", hypothesis.observation),
        ("Potential need", hypothesis.potential_need),
        ("Thursday relevance", hypothesis.thursday_relevance),
    )
    columns = st.columns(len(chain))
    for column, (title, detail) in zip(columns, chain):
        with column:
            render_compact_card(title, detail)
    render_status_label(f"Hypothesis · {hypothesis.period}")
    with st.expander("Source details", expanded=False):
        for source in hypothesis.sources:
            render_source_metadata(source)

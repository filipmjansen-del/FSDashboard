"""Small reusable presentation components for Streamlit views."""

from html import escape

import streamlit as st


def render_page_intro(title: str, description: str, context: str | None = None):
    breadcrumb = f'<div class="page-context">{escape(context)}</div>' if context else ""
    st.markdown(
        f'<div class="page-intro">{breadcrumb}<h1>{escape(title)}</h1><p>{escape(description)}</p></div>',
        unsafe_allow_html=True,
    )


def render_section_intro(title: str, description: str):
    st.markdown(f'<div class="section-intro"><h2>{title}</h2><p>{description}</p></div>', unsafe_allow_html=True)


def render_orientation_card(title: str, description: str):
    st.markdown(
        f'<div class="orientation-card"><div class="orientation-card-title">{title}</div>'
        f'<p>{description}</p></div>',
        unsafe_allow_html=True,
    )


def render_kpi_cards(items: list[tuple[str, str]]):
    """Render compact analytical KPI cards with fully visible labels."""
    columns = st.columns(len(items))
    for column, (value, label) in zip(columns, items):
        with column:
            st.markdown(
                f'<div class="kpi-card"><div class="kpi-value">{escape(str(value))}</div>'
                f'<div class="kpi-label">{escape(label)}</div></div>',
                unsafe_allow_html=True,
            )


def render_warning_callout(message: str):
    """Render a compact, accessible warning without Streamlit's default alert style."""
    st.markdown(f'<div class="warning-callout">{escape(message)}</div>', unsafe_allow_html=True)

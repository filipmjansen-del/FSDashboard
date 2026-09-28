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


def render_metric_definition(meta: dict, *, title: str = "Om nøgletallet"):
    """Render the shared, collapsed methodology view for one metric."""
    direction_labels = {
        "higher_is_better": "Højere er som udgangspunkt bedre",
        "lower_is_better": "Lavere er som udgangspunkt bedre",
        "neutral": "Ingen entydig retning",
    }
    with st.expander(title, expanded=False):
        st.markdown("**Formel**")
        st.code(meta.get("formula_label", meta.get("definition", "Formeldefinition ikke angivet.")), language=None)
        for heading, field in (("Hvad måler nøgletallet?", "description"), ("Hvordan skal den fortolkes?", "interpretation"), ("Sådan læses værdien", "reading_guide")):
            if meta.get(field):
                st.markdown(f"**{heading}**")
                st.write(meta[field])
        st.markdown("**Retning**")
        st.write(direction_labels.get(meta.get("direction", "neutral"), "Ingen entydig retning"))
        if meta.get("direction_explanation"):
            st.caption(meta["direction_explanation"])
        if meta.get("caveat"):
            st.markdown("**Vigtigt at være opmærksom på**")
            st.write(meta["caveat"])
        provenance = "rapporteret" if meta.get("calculation_type") == "reported" else "beregnet"
        st.caption(f"Proveniens: Nøgletallet er {provenance}. Manglende værdier og nødvendige input behandles ikke som nul.")

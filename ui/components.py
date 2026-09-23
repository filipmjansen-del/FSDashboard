"""Small reusable presentation components for Streamlit views."""

import streamlit as st


def render_page_intro(title: str, description: str):
    st.markdown(f'<div class="page-intro"><h1>{title}</h1><p>{description}</p></div>', unsafe_allow_html=True)


def render_section_intro(title: str, description: str):
    st.markdown(f'<div class="section-intro"><h2>{title}</h2><p>{description}</p></div>', unsafe_allow_html=True)


def render_orientation_card(title: str, description: str):
    st.markdown(
        f'<div class="orientation-card"><div class="orientation-card-title">{title}</div>'
        f'<p>{description}</p></div>',
        unsafe_allow_html=True,
    )

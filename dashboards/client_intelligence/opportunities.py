"""Client Intelligence opportunities shell."""

import streamlit as st

from dashboards.client_intelligence._shared import render_shell
from dashboards.client_intelligence.content import COMMERCIAL_HYPOTHESES


DASHBOARD_META = {"name": "Opportunities", "description": "Mock opportunities workspace."}


def render(_raw_data):
    render_shell("Opportunities", "Clearly qualified commercial hypotheses for the AL Sydbank MVP.")
    for hypothesis in COMMERCIAL_HYPOTHESES:
        st.markdown(f"**{hypothesis.title}**")
        st.markdown(f"**Evidence:** {hypothesis.evidence}")
        st.markdown(f"**Observation:** {hypothesis.observation}")
        st.markdown(f"**Potential need (hypothesis):** {hypothesis.potential_need}")
        st.markdown(f"**Thursday relevance:** {hypothesis.thursday_relevance}")
        st.caption(f"Hypothesis · {hypothesis.period} · Source: {hypothesis.source_label}")

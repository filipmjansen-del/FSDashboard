"""Dashboard workspace rendering."""

import streamlit as st

from dashboards.registry import DASHBOARD_REGISTRY, render_dashboard


def render_dashboard_workspace(industry: str, dashboard_name: str, get_raw_data):
    meta = DASHBOARD_REGISTRY[dashboard_name]
    st.caption(f"{industry}  /  Analyse  /  {dashboard_name}")

    if meta.get("description"):
        st.caption(meta["description"])

    render_dashboard(get_raw_data(), dashboard_name)

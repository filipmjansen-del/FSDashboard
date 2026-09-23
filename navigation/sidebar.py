"""Sidebar navigation state and rendering for the Streamlit application."""

import streamlit as st

from dashboards.registry import INDUSTRY_DASHBOARD_CATALOG
from kpis.registry import INDUSTRY_KPI_CATALOG


def all_industries():
    ordered = []
    for industry in list(INDUSTRY_KPI_CATALOG) + list(INDUSTRY_DASHBOARD_CATALOG):
        if industry not in ordered:
            ordered.append(industry)
    return ordered


def initialize_navigation_state():
    for key in ("selected_industry", "selected_view_type", "selected_view_name"):
        if key not in st.session_state:
            st.session_state[key] = None


def navigate_to(industry: str, view_type: str, view_name: str):
    st.session_state.selected_industry = industry
    st.session_state.selected_view_type = view_type
    st.session_state.selected_view_name = view_name
    st.rerun()


def render_sidebar():
    with st.sidebar:
        st.header("Navigation")
        overview_active = st.session_state.selected_view_name is None

        if st.button("Navigationsoversigt", key="nav_overview", use_container_width=True,
                      type="primary" if overview_active else "secondary"):
            st.session_state.selected_industry = None
            st.session_state.selected_view_type = None
            st.session_state.selected_view_name = None
            st.rerun()

        st.divider()
        for industry in all_industries():
            kpis = INDUSTRY_KPI_CATALOG.get(industry, [])
            dashboards = INDUSTRY_DASHBOARD_CATALOG.get(industry, [])
            is_active_industry = st.session_state.selected_industry == industry
            should_expand = is_active_industry or (
                industry == "Bank" and st.session_state.selected_view_name is None
            )
            with st.expander(industry, expanded=should_expand):
                st.markdown('<div class="nav-section-label">KPI\'er</div>', unsafe_allow_html=True)
                if kpis:
                    for kpi_name in kpis:
                        is_active = (st.session_state.selected_view_type == "kpi"
                                     and st.session_state.selected_industry == industry
                                     and st.session_state.selected_view_name == kpi_name)
                        if st.button(kpi_name, key=f"nav_kpi_{industry}_{kpi_name}",
                                     use_container_width=True,
                                     type="primary" if is_active else "secondary"):
                            navigate_to(industry, "kpi", kpi_name)
                else:
                    st.caption("Ingen KPI'er tilføjet endnu")
                st.markdown('<div class="nav-section-label">Analyser</div>', unsafe_allow_html=True)
                if dashboards:
                    for dashboard_name in dashboards:
                        is_active = (st.session_state.selected_view_type == "dashboard"
                                     and st.session_state.selected_industry == industry
                                     and st.session_state.selected_view_name == dashboard_name)
                        if st.button(dashboard_name, key=f"nav_dashboard_{industry}_{dashboard_name}",
                                     use_container_width=True,
                                     type="primary" if is_active else "secondary"):
                            navigate_to(industry, "dashboard", dashboard_name)
                else:
                    st.caption("Ingen analyser tilføjet endnu")

        if st.session_state.selected_view_name:
            st.divider()
            label = ("Valgt KPI" if st.session_state.selected_view_type == "kpi"
                     else "Valgt analyse")
            st.caption(label)
            st.write(st.session_state.selected_view_name)

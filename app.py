import streamlit as st

from data.access import load_financial_services_data
from kpis.registry import calculate_kpi
from modules.registry import ModuleContext, dispatch_module, module_id_for
from navigation.sidebar import all_industries, initialize_navigation_state, navigate_to, render_sidebar
from ui.theme import apply_theme

st.set_page_config(
    page_title="Finansiel Sektoranalyse",
    page_icon="📊",
    layout="wide",
)

apply_theme(st)

@st.cache_data(show_spinner=False)
def get_raw_data():
    return load_financial_services_data()


@st.cache_data(show_spinner=False)
def get_kpi_data(kpi_name: str):
    return calculate_kpi(get_raw_data(), kpi_name)


initialize_navigation_state()

st.title("Finansiel Sektoranalyse")
st.caption("Analyse og benchmarking af den danske finansielle sektor")

render_sidebar()

dispatch_module(
    module_id_for(
        st.session_state.selected_view_type,
        st.session_state.selected_view_name,
    ),
    ModuleContext(
        selected_industry=st.session_state.selected_industry,
        selected_view_name=st.session_state.selected_view_name,
        get_raw_data=get_raw_data,
        get_kpi_data=get_kpi_data,
        navigate_to=navigate_to,
        industries=all_industries,
    ),
)

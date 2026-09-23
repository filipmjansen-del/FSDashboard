from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from data_loader import load_raw_data
from dashboards.registry import (
    DASHBOARD_REGISTRY,
    INDUSTRY_DASHBOARD_CATALOG,
    render_dashboard,
)
from kpis.registry import INDUSTRY_KPI_CATALOG, KPI_REGISTRY, calculate_kpi, get_metric_metadata
from navigation.sidebar import all_industries, initialize_navigation_state, navigate_to, render_sidebar
from ui.formatting import apply_kpi_axis_format, brand_plotly, format_kpi_value, get_plotly_hover_format
from ui.theme import (
    BLACK, BEIGE, BLUE_GREY, COGNAC, DARK_RED, GREY_DARK, GREY_LIGHT,
    OLIVE, PEACH, PURPLE, PURPLE_LIGHT, ROSE, STONE, WHITE, BRAND_SEQUENCE, apply_theme,
)
from views.home import render_home
from views.kpi_workspace import render_kpi_workspace
from views.dashboard_workspace import render_dashboard_workspace

st.set_page_config(
    page_title="Finansiel Sektoranalyse",
    page_icon="📊",
    layout="wide",
)

DATA_PATH = Path(__file__).parent / "financial_services_long.xlsx"

apply_theme(st)
st.markdown(
    f"""
    <style>
        :root {{
            --brand-purple: {PURPLE};
            --brand-dark-red: {DARK_RED};
            --brand-cognac: {COGNAC};
            --brand-beige: {BEIGE};
            --brand-blue-grey: {BLUE_GREY};
            --brand-purple-light: {PURPLE_LIGHT};
            --brand-rose: {ROSE};
            --brand-peach: {PEACH};
            --brand-stone: {STONE};
            --brand-olive: {OLIVE};
            --brand-grey-light: {GREY_LIGHT};
            --brand-grey-dark: {GREY_DARK};
            --brand-black: {BLACK};
            --brand-white: {WHITE};
        }}

        .stApp {{
            background-color: {WHITE};
            color: {BLACK};
        }}

        .block-container {{
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1450px;
        }}

        h1, h2, h3, h4, h5, h6 {{
            color: {PURPLE} !important;
            letter-spacing: -0.01em;
        }}

        p, label, .stMarkdown, [data-testid="stCaptionContainer"] {{
            color: {BLACK};
        }}

        [data-testid="stCaptionContainer"] p {{
            color: {GREY_DARK} !important;
        }}

        [data-testid="stSidebar"] {{
            background-color: {PURPLE};
            border-right: 0;
        }}

        [data-testid="stSidebar"] * {{
            color: {WHITE};
        }}

        [data-testid="stSidebar"] hr {{
            border-color: rgba(255,255,255,0.22);
        }}

        [data-testid="stSidebar"] code {{
            color: {BLACK} !important;
            background-color: {BEIGE} !important;
        }}

        [data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {{
            color: rgba(255,255,255,0.68) !important;
        }}

        [data-testid="stSidebar"] [data-testid="stExpander"] {{
            background: rgba(255,255,255,0.04) !important;
            border: 1px solid rgba(255,255,255,0.18) !important;
            border-radius: 8px !important;
            margin-bottom: 0.45rem;
        }}

        [data-testid="stSidebar"] [data-testid="stExpander"] summary:hover {{
            background: rgba(255,255,255,0.06) !important;
        }}

        [data-testid="stSidebar"] [data-testid="stExpander"] details[open] > summary {{
            background: {DARK_RED} !important;
            border-radius: 7px 7px 0 0 !important;
        }}

        [data-testid="stSidebar"] [data-testid="stExpander"] details[open] > summary,
        [data-testid="stSidebar"] [data-testid="stExpander"] details[open] > summary * {{
            color: {WHITE} !important;
            font-weight: 700 !important;
        }}

        [data-testid="stSidebar"] [data-testid="stExpander"] details[open] > summary:hover {{
            background: {COGNAC} !important;
        }}

        [data-testid="stSidebar"] .stButton > button {{
            width: 100%;
            border-radius: 7px;
            text-align: left;
            justify-content: flex-start;
            white-space: normal;
            min-height: 2.45rem;
            box-shadow: none !important;
        }}

        [data-testid="stSidebar"] .stButton > button[kind="secondary"] {{
            background: rgba(255,255,255,0.07) !important;
            color: {WHITE} !important;
            border: 1px solid rgba(255,255,255,0.18) !important;
        }}

        [data-testid="stSidebar"] .stButton > button[kind="secondary"] p,
        [data-testid="stSidebar"] .stButton > button[kind="secondary"] span {{
            color: {WHITE} !important;
        }}

        [data-testid="stSidebar"] .stButton > button[kind="secondary"]:hover {{
            background: rgba(255,255,255,0.14) !important;
            color: {WHITE} !important;
            border-color: rgba(255,255,255,0.30) !important;
        }}

        [data-testid="stSidebar"] .stButton > button[kind="primary"] {{
            background: {DARK_RED} !important;
            color: {WHITE} !important;
            border: 1px solid {DARK_RED} !important;
            font-weight: 700 !important;
        }}

        [data-testid="stSidebar"] .stButton > button[kind="primary"] p,
        [data-testid="stSidebar"] .stButton > button[kind="primary"] span {{
            color: {WHITE} !important;
            font-weight: 700 !important;
        }}

        [data-testid="stSidebar"] .stButton > button[kind="primary"]:hover {{
            background: {COGNAC} !important;
            color: {WHITE} !important;
            border-color: {COGNAC} !important;
        }}

        [data-testid="stSidebar"] .stButton > button:focus,
        [data-testid="stSidebar"] .stButton > button:focus-visible {{
            outline: none !important;
            box-shadow: none !important;
        }}

        [data-testid="stSidebar"] .stButton > button[kind="primary"]:active,
        [data-testid="stSidebar"] .stButton > button[kind="primary"]:focus,
        [data-testid="stSidebar"] .stButton > button[kind="primary"]:focus-visible {{
            background: {DARK_RED} !important;
            color: {WHITE} !important;
            border-color: {DARK_RED} !important;
        }}

        [data-testid="stSidebar"] .stButton > button[kind="secondary"]:active,
        [data-testid="stSidebar"] .stButton > button[kind="secondary"]:focus,
        [data-testid="stSidebar"] .stButton > button[kind="secondary"]:focus-visible {{
            background: rgba(255,255,255,0.07) !important;
            color: {WHITE} !important;
            border-color: rgba(255,255,255,0.18) !important;
        }}

        [data-testid="stMetric"] {{
            background: {WHITE};
            border: 1px solid {BEIGE};
            border-left: 5px solid {PURPLE};
            border-radius: 10px;
            padding: 0.9rem 1rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        }}

        [data-testid="stMetricLabel"] {{
            color: {GREY_DARK} !important;
        }}

        [data-testid="stMetricValue"] {{
            color: {PURPLE} !important;
        }}

        section.main .stButton > button {{
            background-color: {PURPLE};
            color: {WHITE};
            border: 1px solid {PURPLE};
            border-radius: 8px;
        }}

        section.main .stButton > button:hover {{
            background-color: {DARK_RED};
            color: {WHITE};
            border-color: {DARK_RED};
        }}

        div[data-baseweb="select"] > div,
        div[data-baseweb="input"] > div,
        [data-testid="stMultiSelect"] div[data-baseweb="select"] > div {{
            border-color: {BEIGE} !important;
            background-color: {WHITE} !important;
        }}

        div[data-baseweb="select"] > div:focus-within,
        div[data-baseweb="input"] > div:focus-within {{
            border-color: {PURPLE} !important;
            box-shadow: 0 0 0 1px {PURPLE} !important;
        }}

        [data-testid="stSlider"] [role="slider"] {{
            background-color: {PURPLE} !important;
        }}

        section.main [data-testid="stExpander"] {{
            border: 1px solid {BEIGE};
            border-radius: 8px;
            background: {WHITE};
        }}

        button[data-baseweb="tab"] {{
            color: {GREY_DARK};
        }}

        button[data-baseweb="tab"][aria-selected="true"] {{
            color: {PURPLE} !important;
        }}

        [data-testid="stAlert"] {{
            border-radius: 8px;
        }}

        [data-testid="stDataFrame"] {{
            border: 1px solid {BEIGE};
            border-radius: 8px;
            overflow: hidden;
        }}

        hr {{
            border-color: {BEIGE};
        }}

        a {{
            color: {DARK_RED} !important;
        }}

        .nav-section-label {{
            color: rgba(255,255,255,0.72);
            font-size: 0.72rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-top: 0.35rem;
            margin-bottom: 0.2rem;
            font-weight: 700;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data(show_spinner=False)
def get_raw_data():
    return load_raw_data(DATA_PATH)


@st.cache_data(show_spinner=False)
def get_kpi_data(kpi_name: str):
    return calculate_kpi(get_raw_data(), kpi_name)


def show_navigation_overview():
    render_home(
        get_raw_data(),
        get_kpi_data,
        navigate_to,
        all_industries(),
    )

def show_kpi_workspace(industry: str, kpi_name: str):
    render_kpi_workspace(industry, kpi_name, get_kpi_data)

initialize_navigation_state()

st.title("Finansiel Sektoranalyse")
st.caption("Analyse og benchmarking af den danske finansielle sektor")

render_sidebar()

if st.session_state.selected_view_name is None:
    show_navigation_overview()
elif st.session_state.selected_view_type == "kpi":
    show_kpi_workspace(
        st.session_state.selected_industry,
        st.session_state.selected_view_name,
    )
elif st.session_state.selected_view_type == "dashboard":
    render_dashboard_workspace(
        st.session_state.selected_industry,
        st.session_state.selected_view_name,
        get_raw_data,
    )

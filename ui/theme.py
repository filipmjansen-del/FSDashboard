"""Centralized design tokens used by the Streamlit application shell."""

WHITE = "#FFFFFF"
GREY_LIGHT = "#EEEEEE"
GREY_DARK = "#5C5C5C"
BLACK = "#000000"
PURPLE = "#412B48"
DARK_RED = "#842044"
COGNAC = "#B25F4D"
BEIGE = "#DBD4CF"
BLUE_GREY = "#B8CACE"
PURPLE_LIGHT = "#8C8AF8"
ROSE = "#DCB9CA"
PEACH = "#F5C1AE"
STONE = "#A9A69F"
OLIVE = "#877470"

BRAND_SEQUENCE = [
    PURPLE, DARK_RED, COGNAC, PURPLE_LIGHT, BLUE_GREY,
    ROSE, OLIVE, PEACH, STONE,
]

SPACING = {"section": "2rem", "content_bottom": "3rem", "max_width": "1180px", "section_gap": "2.5rem"}
TYPOGRAPHY = {"font_family": "Arial", "heading_letter_spacing": "-0.01em"}


def apply_theme(st_module):
    """Apply the existing application-wide CSS without changing its design."""
    st_module.markdown(
        f"""
        <style>
            :root {{
                --brand-purple: {PURPLE}; --brand-dark-red: {DARK_RED};
                --brand-cognac: {COGNAC}; --brand-beige: {BEIGE};
                --brand-blue-grey: {BLUE_GREY}; --brand-purple-light: {PURPLE_LIGHT};
                --brand-rose: {ROSE}; --brand-peach: {PEACH};
                --brand-stone: {STONE}; --brand-olive: {OLIVE};
                --brand-grey-light: {GREY_LIGHT}; --brand-grey-dark: {GREY_DARK};
                --brand-black: {BLACK}; --brand-white: {WHITE};
                --primary-color: {PURPLE}; --secondary-background-color: #FAF9F8;
            }}
            .stApp {{ background-color: {WHITE}; color: {BLACK}; }}
            .block-container {{ padding-top: {SPACING['section']}; padding-bottom: {SPACING['content_bottom']}; max-width: {SPACING['max_width']}; }}
            h1, h2, h3, h4, h5, h6 {{ color: {PURPLE} !important; letter-spacing: {TYPOGRAPHY['heading_letter_spacing']}; }}
            p, label, .stMarkdown, [data-testid="stCaptionContainer"] {{ color: {BLACK}; }}
            [data-testid="stCaptionContainer"] p {{ color: {GREY_DARK} !important; }}
            [data-testid="stSidebar"] {{ background-color: {PURPLE}; border-right: 0; }}
            [data-testid="stSidebar"] * {{ color: {WHITE}; }}
            [data-testid="stSidebar"] hr {{ border-color: rgba(255,255,255,0.22); }}
            [data-testid="stSidebar"] code {{ color: {BLACK} !important; background-color: {BEIGE} !important; }}
            [data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {{ color: rgba(255,255,255,0.84) !important; }}
            [data-testid="stSidebar"] [data-testid="stExpander"] {{ background: rgba(255,255,255,0.04) !important; border: 1px solid rgba(255,255,255,0.18) !important; border-radius: 8px !important; margin-bottom: 0.45rem; }}
            [data-testid="stSidebar"] [data-testid="stExpander"] summary:hover {{ background: rgba(255,255,255,0.06) !important; }}
            [data-testid="stSidebar"] [data-testid="stExpander"] details[open] > summary {{ background: {DARK_RED} !important; border-radius: 7px 7px 0 0 !important; }}
            [data-testid="stSidebar"] [data-testid="stExpander"] details[open] > summary, [data-testid="stSidebar"] [data-testid="stExpander"] details[open] > summary * {{ color: {WHITE} !important; font-weight: 700 !important; }}
            [data-testid="stSidebar"] [data-testid="stExpander"] details[open] > summary:hover {{ background: {COGNAC} !important; }}
            [data-testid="stSidebar"] .stButton > button {{ width: 100%; border-radius: 7px; text-align: left; justify-content: flex-start; white-space: normal; min-height: 2.45rem; box-shadow: none !important; }}
            [data-testid="stSidebar"] .stButton > button[kind="secondary"] {{ background: rgba(255,255,255,0.07) !important; color: {WHITE} !important; border: 1px solid rgba(255,255,255,0.18) !important; }}
            [data-testid="stSidebar"] .stButton > button[kind="secondary"] p, [data-testid="stSidebar"] .stButton > button[kind="secondary"] span {{ color: {WHITE} !important; }}
            [data-testid="stSidebar"] .stButton > button[kind="secondary"]:hover {{ background: rgba(255,255,255,0.14) !important; color: {WHITE} !important; border-color: rgba(255,255,255,0.30) !important; }}
            [data-testid="stSidebar"] .stButton > button[kind="primary"] {{ background: {DARK_RED} !important; color: {WHITE} !important; border: 1px solid {DARK_RED} !important; font-weight: 700 !important; }}
            [data-testid="stSidebar"] .stButton > button[kind="primary"] p, [data-testid="stSidebar"] .stButton > button[kind="primary"] span {{ color: {WHITE} !important; font-weight: 700 !important; }}
            [data-testid="stSidebar"] .stButton > button[kind="primary"]:hover {{ background: {COGNAC} !important; color: {WHITE} !important; border-color: {COGNAC} !important; }}
            [data-testid="stSidebar"] .stButton > button:focus, [data-testid="stSidebar"] .stButton > button:focus-visible {{ outline: none !important; box-shadow: none !important; }}
            [data-testid="stSidebar"] .stButton > button[kind="primary"]:active, [data-testid="stSidebar"] .stButton > button[kind="primary"]:focus, [data-testid="stSidebar"] .stButton > button[kind="primary"]:focus-visible {{ background: {DARK_RED} !important; color: {WHITE} !important; border-color: {DARK_RED} !important; }}
            [data-testid="stSidebar"] .stButton > button[kind="secondary"]:active, [data-testid="stSidebar"] .stButton > button[kind="secondary"]:focus, [data-testid="stSidebar"] .stButton > button[kind="secondary"]:focus-visible {{ background: rgba(255,255,255,0.07) !important; color: {WHITE} !important; border-color: rgba(255,255,255,0.18) !important; }}
            [data-testid="stMetric"] {{ background: {WHITE}; border: 1px solid {BEIGE}; border-left: 5px solid {PURPLE}; border-radius: 10px; padding: 0.9rem 1rem; box-shadow: 0 1px 3px rgba(0,0,0,0.04); }}
            [data-testid="stMetricLabel"] {{ color: {GREY_DARK} !important; }}
            [data-testid="stMetricValue"] {{ color: {PURPLE} !important; }}
            section.main .stButton > button {{ background-color: {PURPLE}; color: {WHITE}; border: 1px solid {PURPLE}; border-radius: 8px; }}
            section.main .stButton > button:hover {{ background-color: {DARK_RED}; color: {WHITE}; border-color: {DARK_RED}; }}
            div[data-baseweb="select"] > div, div[data-baseweb="input"] > div, [data-testid="stMultiSelect"] div[data-baseweb="select"] > div {{ border-color: {BEIGE} !important; background-color: {WHITE} !important; }}
            div[data-baseweb="select"] > div:focus-within, div[data-baseweb="input"] > div:focus-within {{ border-color: {PURPLE} !important; box-shadow: 0 0 0 1px {PURPLE} !important; }}
            div[data-baseweb="tag"] {{ background-color: {PURPLE} !important; color: {WHITE} !important; border-radius: 5px !important; }}
            div[data-baseweb="tag"] span {{ color: {WHITE} !important; }}
            [data-testid="stSlider"] [role="slider"] {{ background-color: {PURPLE} !important; }}
            [data-testid="stRadio"] [role="radio"][aria-checked="true"] {{ border-color: {PURPLE} !important; background-color: {PURPLE} !important; }}
            [data-testid="stCheckbox"] [data-checked="true"] {{ background-color: {PURPLE} !important; border-color: {PURPLE} !important; }}
            section.main [data-testid="stExpander"] {{ border: 1px solid {BEIGE}; border-radius: 8px; background: {WHITE}; }}
            button[data-baseweb="tab"] {{ color: {GREY_DARK}; }}
            button[data-baseweb="tab"][aria-selected="true"] {{ color: {PURPLE} !important; }}
            button[data-baseweb="tab"][aria-selected="true"]::after {{ background-color: {PURPLE} !important; }}
            [data-testid="stAlert"] {{ border-radius: 8px; }}
            [data-testid="stDataFrame"] {{ border: 1px solid {BEIGE}; border-radius: 8px; overflow: hidden; }}
            hr {{ border-color: {BEIGE}; }}
            a {{ color: {DARK_RED} !important; }}
            .nav-section-label {{ color: rgba(255,255,255,0.84); font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.08em; margin-top: 0.35rem; margin-bottom: 0.2rem; font-weight: 700; }}
            .page-intro {{ margin: 0 0 {SPACING['section_gap']}; max-width: 760px; }}
            .page-intro h1 {{ margin: 0 0 0.5rem; font-size: 2.1rem; }}
            .page-intro p, .section-intro p, .orientation-card p {{ color: {GREY_DARK}; line-height: 1.55; margin: 0; }}
            .section-intro {{ margin: {SPACING['section_gap']} 0 1rem; max-width: 760px; }}
            .section-intro h2 {{ margin: 0 0 0.35rem; font-size: 1.35rem; }}
            .orientation-card {{ border: 1px solid {BEIGE}; border-radius: 8px; background: #FAF9F8; padding: 1rem 1.1rem; margin: 0 0 0.7rem; }}
            .orientation-card-title {{ color: {PURPLE}; font-weight: 700; margin-bottom: 0.2rem; }}
        </style>
        """,
        unsafe_allow_html=True,
    )

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
from kpis.registry import INDUSTRY_KPI_CATALOG, KPI_REGISTRY, calculate_kpi

WHITE = "#FFFFFF"
GREY_LIGHT = "#EEEEEE"
GREY_DARK = "#A1A1A1"
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
    PURPLE,
    DARK_RED,
    COGNAC,
    PURPLE_LIGHT,
    BLUE_GREY,
    ROSE,
    OLIVE,
    PEACH,
    STONE,
]

st.set_page_config(
    page_title="Finansiel Sektoranalyse",
    page_icon="📊",
    layout="wide",
)

DATA_PATH = Path(__file__).parent / "financial_services_long.xlsx"

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


DEFAULT_ENTITY_LABELS = {
    "Bank": {"singular": "Bank", "plural": "Banker"},
    "Realkredit": {
        "singular": "Realkreditinstitut",
        "plural": "Realkreditinstitutter",
    },
    "Forsikring": {
        "singular": "Forsikringsselskab",
        "plural": "Forsikringsselskaber",
    },
    "Pension": {
        "singular": "Pensionsselskab",
        "plural": "Pensionsselskaber",
    },
    "Tværgående pensionskasser": {
        "singular": "Pensionskasse",
        "plural": "Pensionskasser",
    },
}


def get_entity_labels(meta, industry):
    defaults = DEFAULT_ENTITY_LABELS.get(
        industry,
        {"singular": "Selskab", "plural": "Selskaber"},
    )
    return (
        meta.get("entity_label_singular", defaults["singular"]),
        meta.get("entity_label_plural", defaults["plural"]),
    )


def format_kpi_value(value, meta):
    if pd.isna(value):
        return "–"

    display_format = meta.get("display_format", "number")
    decimals = meta.get("decimals", 2)

    if display_format == "multiple":
        return f"{value:.{decimals}f}x"
    if display_format == "percentage":
        return f"{value:.{decimals}%}"
    if display_format == "integer":
        return f"{value:,.0f}"
    if display_format == "dkk":
        return f"DKK {value:,.{decimals}f}"
    if display_format == "dkk_million":
        return f"DKK {value / 1_000_000:,.{decimals}f} mio."
    if display_format == "dkk_billion":
        return f"DKK {value / 1_000_000_000:,.{decimals}f} mia."

    return f"{value:,.{decimals}f}"


def apply_kpi_axis_format(fig, meta, axis="y"):
    display_format = meta.get("display_format", "number")
    decimals = meta.get("decimals", 2)

    if display_format == "multiple":
        settings = {"tickformat": f".{decimals}f", "ticksuffix": "x"}
    elif display_format == "percentage":
        settings = {"tickformat": f".{decimals}%"}
    elif display_format == "integer":
        settings = {"tickformat": ",.0f"}
    elif display_format == "dkk":
        settings = {"tickformat": f",.{decimals}f", "tickprefix": "DKK "}
    elif display_format in {"dkk_million", "dkk_billion"}:
        settings = {"tickformat": ".3s", "tickprefix": "DKK "}
    else:
        settings = {"tickformat": f",.{decimals}f"}

    if axis == "x":
        fig.update_xaxes(**settings)
    else:
        fig.update_yaxes(**settings)

    return fig


def get_plotly_hover_format(meta):
    display_format = meta.get("display_format", "number")
    decimals = meta.get("decimals", 2)

    if display_format == "percentage":
        return f":.{decimals}%"
    if display_format == "multiple":
        return f":.{decimals}f"
    if display_format == "integer":
        return ":,.0f"

    return f":,.{decimals}f"


def brand_plotly(fig, *, legend_title=None):
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor=WHITE,
        plot_bgcolor=WHITE,
        font=dict(color=BLACK, family="Arial"),
        title_font=dict(color=PURPLE),
        legend_title_text=legend_title,
        legend=dict(
            bgcolor="rgba(255,255,255,0)",
            font=dict(color=BLACK),
        ),
        margin=dict(l=20, r=20, t=40, b=20),
        hoverlabel=dict(
            bgcolor=PURPLE,
            font_color=WHITE,
            bordercolor=PURPLE,
        ),
    )
    fig.update_xaxes(
        showgrid=False,
        linecolor=BEIGE,
        tickfont=dict(color=BLACK),
        title_font=dict(color=GREY_DARK),
        zeroline=False,
    )
    fig.update_yaxes(
        gridcolor=GREY_LIGHT,
        linecolor=BEIGE,
        tickfont=dict(color=BLACK),
        title_font=dict(color=GREY_DARK),
        zeroline=False,
    )
    return fig


def all_industries():
    ordered = []
    for industry in list(INDUSTRY_KPI_CATALOG) + list(INDUSTRY_DASHBOARD_CATALOG):
        if industry not in ordered:
            ordered.append(industry)
    return ordered


def navigate_to(industry: str, view_type: str, view_name: str):
    st.session_state.selected_industry = industry
    st.session_state.selected_view_type = view_type
    st.session_state.selected_view_name = view_name
    st.rerun()


def show_kpi_definition(meta):
    formula_label = meta.get("formula_label", "Formeldefinition ikke angivet.")
    description = meta.get("description")
    interpretation = meta.get("interpretation")
    direction = meta.get("direction", "neutral")
    direction_explanation = meta.get("direction_explanation")
    caveat = meta.get("caveat")

    direction_labels = {
        "higher_is_better": "Højere er som udgangspunkt bedre",
        "lower_is_better": "Lavere er som udgangspunkt bedre",
        "neutral": "Ingen entydig retning",
    }

    with st.expander("KPI-definition"):
        st.markdown("**Formel**")
        st.code(formula_label, language=None)

        if description:
            st.markdown("**Hvad måler KPI'en?**")
            st.write(description)

        if interpretation:
            st.markdown("**Hvordan skal den fortolkes?**")
            st.write(interpretation)

        st.markdown("**Retning**")
        st.write(direction_labels.get(direction, "Ingen entydig retning"))

        if direction_explanation:
            st.caption(direction_explanation)

        if caveat:
            st.markdown("**Vigtigt at være opmærksom på**")
            st.write(caveat)

        if meta.get("source_type") == "reported":
            st.caption(
                "Værdien er rapporteret i kildedatasættet. Manglende KPI-værdier "
                "behandles ikke som nul. Kildens 1:1-afstemning mod Finanstilsynets "
                "offentlige pivottabel er endnu ikke verificeret."
            )
        else:
            st.caption(
                "Manglende nødvendige input behandles ikke som nul. "
                "KPI-værdien beregnes efter reglerne i den tilhørende KPI-fil."
            )


def show_navigation_overview():
    raw = get_raw_data()
    industries = all_industries()

    st.header("Finansiel markedsoversigt")
    st.caption(
        "Få et hurtigt overblik over datagrundlaget, se sektorens centrale KPI'er "
        "og gå direkte til den analyse, du har brug for."
    )

    valid_years = pd.to_numeric(raw["ÅR"], errors="coerce").dropna()
    latest_year = int(valid_years.max()) if not valid_years.empty else None

    if latest_year is not None:
        latest_raw = raw[pd.to_numeric(raw["ÅR"], errors="coerce") == latest_year].copy()
        latest_company_count = (
            latest_raw[["Branche", "regnr"]]
            .drop_duplicates()
            .shape[0]
        )
    else:
        latest_company_count = 0

    total_kpis = sum(len(INDUSTRY_KPI_CATALOG.get(i, [])) for i in industries)
    total_dashboards = sum(
        len(INDUSTRY_DASHBOARD_CATALOG.get(i, [])) for i in industries
    )

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Seneste dataår", latest_year if latest_year is not None else "–")
    c2.metric("Markeder", len(industries))
    c3.metric("Selskaber", latest_company_count)
    c4.metric("KPI'er", total_kpis)
    c5.metric("Analyser", total_dashboards)

    st.divider()

    st.subheader("KPI-puls")
    st.caption(
        "Vælg et marked og få et hurtigt snapshot af de seneste sektormedianer. "
        "Klik direkte videre til den enkelte KPI."
    )

    industries_with_kpis = [
        industry
        for industry in industries
        if INDUSTRY_KPI_CATALOG.get(industry, [])
    ]

    if industries_with_kpis:
        pulse_industry = st.selectbox(
            "Marked",
            industries_with_kpis,
            key="home_pulse_industry",
        )

        available_pulse_kpis = INDUSTRY_KPI_CATALOG.get(pulse_industry, [])
        default_pulse_kpis = available_pulse_kpis[: min(4, len(available_pulse_kpis))]

        selected_pulse_kpis = st.multiselect(
            "KPI'er på forsiden",
            available_pulse_kpis,
            default=default_pulse_kpis,
            key="home_pulse_kpis",
        )

        if len(selected_pulse_kpis) > 4:
            st.info("Forsiden viser maksimalt fire KPI'er ad gangen.")
            selected_pulse_kpis = selected_pulse_kpis[:4]

        if selected_pulse_kpis:
            pulse_columns = st.columns(len(selected_pulse_kpis))

            for col, kpi_name in zip(pulse_columns, selected_pulse_kpis):
                meta = KPI_REGISTRY[kpi_name]
                kpi_data = get_kpi_data(kpi_name)
                valid_kpi = kpi_data.dropna(subset=["KPI_Value"]).copy()

                with col:
                    with st.container(border=True):
                        st.markdown(f"**{kpi_name}**")

                        if valid_kpi.empty:
                            st.metric("Sektormedian", "–")
                            st.caption("Ingen komplette observationer")
                        else:
                            kpi_year = int(valid_kpi["ÅR"].max())
                            kpi_year_data = valid_kpi[
                                valid_kpi["ÅR"] == kpi_year
                            ].copy()

                            median_value = kpi_year_data["KPI_Value"].median()
                            company_count = kpi_year_data["regnr"].nunique()

                            st.metric(
                                "Sektormedian",
                                format_kpi_value(median_value, meta),
                            )
                            st.caption(
                                f"{kpi_year} · {company_count} selskaber"
                            )

                        if st.button(
                            "Åbn KPI",
                            key=f"home_open_kpi_{pulse_industry}_{kpi_name}",
                            use_container_width=True,
                        ):
                            navigate_to(pulse_industry, "kpi", kpi_name)
        else:
            st.info("Vælg mindst én KPI for at vise KPI-pulsen.")
    else:
        st.info("Der er endnu ingen KPI'er tilgængelige.")

    st.divider()

    st.subheader("Hurtig adgang")
    st.caption(
        "Gå direkte til en KPI eller analyse uden først at navigere gennem sidepanelet."
    )

    q1, q2, q3, q4 = st.columns([1.2, 1.0, 2.0, 0.8])

    with q1:
        quick_industry = st.selectbox(
            "Marked",
            industries,
            key="home_quick_industry",
        )

    quick_kpis = INDUSTRY_KPI_CATALOG.get(quick_industry, [])
    quick_dashboards = INDUSTRY_DASHBOARD_CATALOG.get(quick_industry, [])

    quick_type_options = []
    if quick_kpis:
        quick_type_options.append("KPI")
    if quick_dashboards:
        quick_type_options.append("Analyse")

    if quick_type_options:
        with q2:
            quick_type = st.selectbox(
                "Type",
                quick_type_options,
                key="home_quick_type",
            )

        quick_items = quick_kpis if quick_type == "KPI" else quick_dashboards

        with q3:
            quick_name = st.selectbox(
                "Vælg indhold",
                quick_items,
                key="home_quick_name",
            )

        with q4:
            st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
            if st.button(
                "Åbn",
                key="home_quick_open",
                use_container_width=True,
            ):
                navigate_to(
                    quick_industry,
                    "kpi" if quick_type == "KPI" else "dashboard",
                    quick_name,
                )
    else:
        with q2:
            st.write("")
        with q3:
            st.info("Der er endnu ikke tilføjet KPI'er eller analyser til dette marked.")
        with q4:
            st.write("")

    st.divider()

    st.subheader("Datagrundlag")
    st.caption(
        "Udviklingen i antal selskaber med regnskabsdata i datasættet samt status pr. marked."
    )

    left, right = st.columns([1.7, 1.0])

    with left:
        coverage_source = raw.copy()
        coverage_source["ÅR"] = pd.to_numeric(
            coverage_source["ÅR"],
            errors="coerce",
        )
        coverage_source = coverage_source.dropna(
            subset=["ÅR", "Branche", "regnr"]
        )
        coverage_source["ÅR"] = coverage_source["ÅR"].astype(int)

        coverage = (
            coverage_source.groupby(["ÅR", "Branche"], as_index=False)
            .agg(Selskaber=("regnr", "nunique"))
        )
        coverage = coverage[coverage["Branche"].isin(industries)]

        if not coverage.empty:
            fig = px.line(
                coverage,
                x="ÅR",
                y="Selskaber",
                color="Branche",
                markers=True,
                color_discrete_sequence=BRAND_SEQUENCE,
                labels={
                    "ÅR": "År",
                    "Selskaber": "Antal selskaber",
                    "Branche": "Marked",
                },
            )
            fig.update_traces(line_width=2.5, marker_size=6)
            fig.update_layout(
                xaxis_title=None,
                yaxis_title="Antal selskaber",
            )
            brand_plotly(fig, legend_title="Marked")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Der er ikke nok data til at vise udviklingen i datadækningen.")

    with right:
        status_rows = []

        for industry in industries:
            sector = raw[raw["Branche"] == industry].copy()
            sector_years = pd.to_numeric(
                sector["ÅR"],
                errors="coerce",
            ).dropna()

            if sector_years.empty:
                sector_latest_year = None
                sector_company_count = 0
            else:
                sector_latest_year = int(sector_years.max())
                sector_latest = sector[
                    pd.to_numeric(sector["ÅR"], errors="coerce")
                    == sector_latest_year
                ]
                sector_company_count = sector_latest["regnr"].nunique()

            status_rows.append(
                {
                    "Marked": industry,
                    "Seneste år": sector_latest_year if sector_latest_year else "–",
                    "Selskaber": sector_company_count,
                    "KPI'er": len(INDUSTRY_KPI_CATALOG.get(industry, [])),
                    "Analyser": len(
                        INDUSTRY_DASHBOARD_CATALOG.get(industry, [])
                    ),
                }
            )

        st.dataframe(
            pd.DataFrame(status_rows),
            use_container_width=True,
            hide_index=True,
        )

    st.divider()

    st.subheader("Markeder")
    st.caption(
        "Et samlet overblik over hvilke markeder, KPI'er og analyser der allerede er tilgængelige."
    )

    industry_rows = [
        industries[i:i + 3]
        for i in range(0, len(industries), 3)
    ]

    for row_industries in industry_rows:
        cols = st.columns(len(row_industries))

        for col, industry in zip(cols, row_industries):
            kpis = INDUSTRY_KPI_CATALOG.get(industry, [])
            dashboards = INDUSTRY_DASHBOARD_CATALOG.get(industry, [])

            sector = raw[raw["Branche"] == industry].copy()
            sector_years = pd.to_numeric(
                sector["ÅR"],
                errors="coerce",
            ).dropna()

            if sector_years.empty:
                sector_latest_year = "–"
                sector_company_count = 0
            else:
                sector_latest_year = int(sector_years.max())
                sector_latest = sector[
                    pd.to_numeric(sector["ÅR"], errors="coerce")
                    == sector_latest_year
                ]
                sector_company_count = sector_latest["regnr"].nunique()

            with col:
                with st.container(border=True):
                    st.subheader(industry)
                    st.metric("Selskaber", sector_company_count)
                    st.caption(
                        f"Seneste dataår: {sector_latest_year} · "
                        f"{len(kpis)} KPI'er · {len(dashboards)} analyser"
                    )

                    if kpis:
                        st.markdown("**KPI'er**")
                        for kpi_name in kpis[:3]:
                            st.markdown(f"• {kpi_name}")
                        if len(kpis) > 3:
                            st.caption(f"+ {len(kpis) - 3} yderligere")

                    if dashboards:
                        st.markdown("**Analyser**")
                        for dashboard_name in dashboards[:3]:
                            st.markdown(f"• {dashboard_name}")
                        if len(dashboards) > 3:
                            st.caption(f"+ {len(dashboards) - 3} yderligere")

                    if not kpis and not dashboards:
                        st.caption("Indhold er endnu ikke tilføjet")


def show_kpi_workspace(industry: str, kpi_name: str):
    meta = KPI_REGISTRY[kpi_name]
    kpi = get_kpi_data(kpi_name)

    if kpi.empty:
        st.warning("Denne KPI indeholder i øjeblikket ingen observationer.")
        return

    valid = kpi.dropna(subset=["KPI_Value"]).copy()
    all_years = sorted(int(x) for x in kpi["ÅR"].dropna().unique())

    if not all_years:
        st.warning("Der er ingen tilgængelige år for denne KPI.")
        return

    entity_singular, entity_plural = get_entity_labels(meta, industry)
    direction = meta.get("direction", "neutral")

    st.caption(f"{industry}  /  KPI  /  {kpi_name}")
    st.header(kpi_name)

    show_kpi_definition(meta)

    overview_tab, explorer_tab, profile_tab, comparison_tab, quality_tab = st.tabs(
        [
            "Overblik",
            "Udforsk",
            "Selskabsprofil",
            "Sektorsammenligning",
            "Datakvalitet",
        ]
    )

    with overview_tab:
        selected_year = st.selectbox(
            "År",
            all_years,
            index=len(all_years) - 1,
            key=f"overview_year_{industry}_{kpi_name}",
        )

        yr = valid[valid["ÅR"] == selected_year].copy()
        represented = kpi[kpi["ÅR"] == selected_year]["regnr"].nunique()
        complete = yr["regnr"].nunique()
        median = yr["KPI_Value"].median()
        mean = yr["KPI_Value"].mean()

        c1, c2, c3, c4 = st.columns(4)
        c1.metric(f"{entity_plural} repræsenteret", represented)
        c2.metric(f"{entity_plural} med komplet KPI", complete)
        c3.metric("Sektormedian", format_kpi_value(median, meta))
        c4.metric("Sektorgennemsnit", format_kpi_value(mean, meta))

        st.subheader(f"Fordeling på tværs af {entity_plural.lower()}")

        fig = px.histogram(
            yr,
            x="KPI_Value",
            nbins=20,
            labels={"KPI_Value": kpi_name},
            hover_data=["navn"],
            color_discrete_sequence=[PURPLE],
        )
        fig.update_traces(marker_line_color=WHITE, marker_line_width=0.7)
        fig.update_layout(
            yaxis_title=f"Antal {entity_plural.lower()}",
            showlegend=False,
        )
        brand_plotly(fig)
        apply_kpi_axis_format(fig, meta, axis="x")
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Sektorudvikling")

        trend = (
            valid.groupby("ÅR", as_index=False)
            .agg(
                Median=("KPI_Value", "median"),
                Gennemsnit=("KPI_Value", "mean"),
                Selskaber=("regnr", "nunique"),
            )
        )

        trend_long = trend.melt(
            id_vars=["ÅR", "Selskaber"],
            value_vars=["Median", "Gennemsnit"],
            var_name="Serie",
            value_name="Værdi",
        )

        fig2 = px.line(
            trend_long,
            x="ÅR",
            y="Værdi",
            color="Serie",
            markers=True,
            color_discrete_map={"Median": PURPLE, "Gennemsnit": COGNAC},
        )
        fig2.update_traces(line_width=3, marker_size=8)
        fig2.update_layout(yaxis_title=kpi_name, xaxis_title=None)
        brand_plotly(fig2, legend_title="Serie")
        apply_kpi_axis_format(fig2, meta, axis="y")
        st.plotly_chart(fig2, use_container_width=True)

    with explorer_tab:
        names = sorted(valid["navn"].dropna().unique())
        default_names = names[: min(5, len(names))]

        selected_entities = st.multiselect(
            entity_plural,
            names,
            default=default_names,
            key=f"explorer_entities_{industry}_{kpi_name}",
        )

        year_range = st.slider(
            "År",
            min(all_years),
            max(all_years),
            (min(all_years), max(all_years)),
            key=f"explorer_years_{industry}_{kpi_name}",
        )

        chart_df = valid[
            valid["navn"].isin(selected_entities)
            & valid["ÅR"].between(year_range[0], year_range[1])
        ].copy()

        if chart_df.empty:
            st.info(
                f"Vælg mindst én {entity_singular.lower()} "
                "med tilgængelige KPI-observationer i den valgte periode."
            )
        else:
            fig = px.line(
                chart_df,
                x="ÅR",
                y="KPI_Value",
                color="navn",
                markers=True,
                labels={"KPI_Value": kpi_name, "navn": entity_singular},
                color_discrete_sequence=BRAND_SEQUENCE,
            )
            fig.update_traces(line_width=2.7, marker_size=7)
            fig.update_layout(xaxis_title=None)
            brand_plotly(fig, legend_title=entity_singular)
            apply_kpi_axis_format(fig, meta, axis="y")
            st.plotly_chart(fig, use_container_width=True)

            table = chart_df.pivot(
                index="navn",
                columns="ÅR",
                values="KPI_Value",
            )
            st.dataframe(
                table.style.format(
                    lambda value: format_kpi_value(value, meta),
                    na_rep="–",
                ),
                use_container_width=True,
            )

    with profile_tab:
        entity_names = sorted(kpi["navn"].dropna().unique())

        selected_entity = st.selectbox(
            entity_singular,
            entity_names,
            key=f"profile_entity_{industry}_{kpi_name}",
        )

        entity_all = kpi[kpi["navn"] == selected_entity].sort_values("ÅR")
        entity_valid = entity_all.dropna(subset=["KPI_Value"])

        if entity_valid.empty:
            st.warning(
                f"Der er ingen komplette observationer for denne KPI for det valgte "
                f"{entity_singular.lower()}."
            )
        else:
            last_row = entity_valid.iloc[-1]
            last_year = int(last_row["ÅR"])
            sector_year = valid[valid["ÅR"] == last_year]
            sector_median = sector_year["KPI_Value"].median()

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Seneste tilgængelige år", last_year)
            c2.metric(kpi_name, format_kpi_value(last_row["KPI_Value"], meta))
            c3.metric("Sektormedian", format_kpi_value(sector_median, meta))
            c4.metric("År med komplette data", int(entity_valid["ÅR"].nunique()))

            fig = px.line(
                entity_valid,
                x="ÅR",
                y="KPI_Value",
                markers=True,
                color_discrete_sequence=[PURPLE],
            )
            fig.update_traces(line_width=3, marker_size=8)
            fig.add_hline(
                y=sector_median,
                line_dash="dash",
                line_color=COGNAC,
                annotation_text=f"{last_year} sektormedian",
                annotation_font_color=COGNAC,
            )
            fig.update_layout(yaxis_title=kpi_name, xaxis_title=None)
            brand_plotly(fig)
            apply_kpi_axis_format(fig, meta, axis="y")
            st.plotly_chart(fig, use_container_width=True)

            calculation_rows = []

            if "Numerator" in last_row.index:
                calculation_rows.append(
                    {"Element": "Tæller", "Værdi": last_row["Numerator"]}
                )

            if "Denominator" in last_row.index:
                calculation_rows.append(
                    {"Element": "Nævner", "Værdi": last_row["Denominator"]}
                )

            calculation_rows.append(
                {
                    "Element": kpi_name,
                    "Værdi": format_kpi_value(last_row["KPI_Value"], meta),
                }
            )

            st.subheader("Underliggende beregning – seneste tilgængelige år")
            st.dataframe(
                pd.DataFrame(calculation_rows),
                use_container_width=True,
                hide_index=True,
            )

    with comparison_tab:
        selected_year = st.selectbox(
            "År",
            all_years,
            index=len(all_years) - 1,
            key=f"comparison_year_{industry}_{kpi_name}",
        )

        yr = valid[valid["ÅR"] == selected_year].copy()

        if yr.empty:
            st.info("Der er ingen komplette KPI-observationer for det valgte år.")
        else:
            if direction == "higher_is_better":
                yr["PerformancePercentile"] = (
                    yr["KPI_Value"].rank(pct=True, ascending=True) * 100
                )
            elif direction == "lower_is_better":
                yr["PerformancePercentile"] = (
                    yr["KPI_Value"].rank(pct=True, ascending=False) * 100
                )
            else:
                yr["PerformancePercentile"] = (
                    yr["KPI_Value"].rank(pct=True) * 100
                )

            yr = yr.sort_values("KPI_Value", ascending=False)

            fig = px.bar(
                yr,
                x="KPI_Value",
                y="navn",
                orientation="h",
                color="PerformancePercentile",
                color_continuous_scale=[
                    [0.0, BEIGE],
                    [0.5, BLUE_GREY],
                    [1.0, PURPLE],
                ],
                hover_data={
                    "PerformancePercentile": ":.0f",
                    "KPI_Value": get_plotly_hover_format(meta),
                },
                labels={
                    "KPI_Value": kpi_name,
                    "navn": entity_singular,
                    "PerformancePercentile": "Percentil",
                },
            )
            fig.update_layout(
                height=max(500, 24 * len(yr)),
                yaxis={"categoryorder": "total ascending"},
                coloraxis_colorbar=dict(title="Percentil"),
            )
            brand_plotly(fig)
            apply_kpi_axis_format(fig, meta, axis="x")
            st.plotly_chart(fig, use_container_width=True)

            display = yr[
                ["navn", "KPI_Value", "PerformancePercentile"]
            ].rename(
                columns={
                    "navn": entity_singular,
                    "KPI_Value": kpi_name,
                    "PerformancePercentile": "Percentil",
                }
            )

            st.dataframe(
                display.style.format(
                    {
                        kpi_name: lambda value: format_kpi_value(value, meta),
                        "Percentil": "{:.0f}",
                    }
                ),
                use_container_width=True,
                hide_index=True,
            )

    with quality_tab:
        st.write(
            "Denne side viser KPI-dækningen eksplicit. Manglende beregningsinput "
            "eller rapporterede KPI-værdier behandles ikke som nul."
        )

        coverage = (
            kpi.groupby("ÅR", as_index=False)
            .agg(
                EntitiesRepresented=("regnr", "nunique"),
                CompleteKPI=("KPI_Value", lambda s: s.notna().sum()),
            )
        )

        coverage["CoveragePct"] = (
            coverage["CompleteKPI"] / coverage["EntitiesRepresented"] * 100
        )

        coverage = coverage.rename(
            columns={
                "EntitiesRepresented": f"{entity_plural} repræsenteret",
                "CompleteKPI": "Komplette KPI-observationer",
                "CoveragePct": "Dækning",
            }
        )

        st.dataframe(
            coverage.style.format({"Dækning": "{:.1f}%"}),
            use_container_width=True,
            hide_index=True,
        )

        st.subheader(f"{entity_singular}-år med manglende KPI-værdi")

        missing = (
            kpi[kpi["KPI_Value"].isna()][["ÅR", "regnr", "navn"]]
            .sort_values(["ÅR", "navn"])
        )

        st.dataframe(
            missing,
            use_container_width=True,
            hide_index=True,
        )


def show_dashboard_workspace(industry: str, dashboard_name: str):
    meta = DASHBOARD_REGISTRY[dashboard_name]
    st.caption(f"{industry}  /  Analyse  /  {dashboard_name}")

    if meta.get("description"):
        st.caption(meta["description"])

    render_dashboard(get_raw_data(), dashboard_name)


if "selected_industry" not in st.session_state:
    st.session_state.selected_industry = None

if "selected_view_type" not in st.session_state:
    st.session_state.selected_view_type = None

if "selected_view_name" not in st.session_state:
    st.session_state.selected_view_name = None

st.title("Finansiel Sektoranalyse")
st.caption("Analyse og benchmarking af den danske finansielle sektor")

with st.sidebar:
    st.header("Navigation")

    overview_active = st.session_state.selected_view_name is None

    if st.button(
        "Navigationsoversigt",
        key="nav_overview",
        use_container_width=True,
        type="primary" if overview_active else "secondary",
    ):
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
            st.markdown(
                '<div class="nav-section-label">KPI\'er</div>',
                unsafe_allow_html=True,
            )

            if kpis:
                for kpi_name in kpis:
                    is_active = (
                        st.session_state.selected_view_type == "kpi"
                        and st.session_state.selected_industry == industry
                        and st.session_state.selected_view_name == kpi_name
                    )

                    if st.button(
                        kpi_name,
                        key=f"nav_kpi_{industry}_{kpi_name}",
                        use_container_width=True,
                        type="primary" if is_active else "secondary",
                    ):
                        st.session_state.selected_industry = industry
                        st.session_state.selected_view_type = "kpi"
                        st.session_state.selected_view_name = kpi_name
                        st.rerun()
            else:
                st.caption("Ingen KPI'er tilføjet endnu")

            st.markdown(
                '<div class="nav-section-label">Analyser</div>',
                unsafe_allow_html=True,
            )

            if dashboards:
                for dashboard_name in dashboards:
                    is_active = (
                        st.session_state.selected_view_type == "dashboard"
                        and st.session_state.selected_industry == industry
                        and st.session_state.selected_view_name == dashboard_name
                    )

                    if st.button(
                        dashboard_name,
                        key=f"nav_dashboard_{industry}_{dashboard_name}",
                        use_container_width=True,
                        type="primary" if is_active else "secondary",
                    ):
                        st.session_state.selected_industry = industry
                        st.session_state.selected_view_type = "dashboard"
                        st.session_state.selected_view_name = dashboard_name
                        st.rerun()
            else:
                st.caption("Ingen analyser tilføjet endnu")

    if st.session_state.selected_view_name:
        st.divider()
        label = (
            "Valgt KPI"
            if st.session_state.selected_view_type == "kpi"
            else "Valgt analyse"
        )
        st.caption(label)
        st.write(st.session_state.selected_view_name)

if st.session_state.selected_view_name is None:
    show_navigation_overview()
elif st.session_state.selected_view_type == "kpi":
    show_kpi_workspace(
        st.session_state.selected_industry,
        st.session_state.selected_view_name,
    )
elif st.session_state.selected_view_type == "dashboard":
    show_dashboard_workspace(
        st.session_state.selected_industry,
        st.session_state.selected_view_name,
    )

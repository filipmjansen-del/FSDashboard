from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from data_loader import load_raw_data
from kpis.registry import INDUSTRY_KPI_CATALOG, KPI_REGISTRY, calculate_kpi

# -----------------------------------------------------------------------------
# Thursday brand palette
# -----------------------------------------------------------------------------
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

BRAND_SEQUENCE = [PURPLE, DARK_RED, COGNAC, PURPLE_LIGHT, BLUE_GREY, ROSE, OLIVE, PEACH, STONE]

st.set_page_config(
    page_title="Financial Services Intelligence",
    page_icon="📊",
    layout="wide",
)

# The GitHub repository currently has the data and helper modules in the root.
DATA_PATH = Path(__file__).parent / "financial_services_long.xlsx"

# -----------------------------------------------------------------------------
# Brand styling for Streamlit UI
# -----------------------------------------------------------------------------
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

        /* Main canvas */
        .stApp {{
            background-color: {WHITE};
            color: {BLACK};
        }}

        .block-container {{
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1450px;
        }}

        /* Typography */
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

        /* Sidebar */
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

        /* Industry groups in sidebar */
        [data-testid="stSidebar"] [data-testid="stExpander"] {{
            background: rgba(255,255,255,0.04) !important;
            border: 1px solid rgba(255,255,255,0.18) !important;
            border-radius: 8px !important;
            margin-bottom: 0.45rem;
        }}

        [data-testid="stSidebar"] [data-testid="stExpander"] summary:hover {{
            background: rgba(255,255,255,0.06) !important;
        }}

        [data-testid="stSidebar"] .stButton > button {{
            width: 100%;
            background: rgba(255,255,255,0.07);
            color: {WHITE};
            border: 1px solid rgba(255,255,255,0.18);
            border-radius: 7px;
            text-align: left;
            justify-content: flex-start;
            white-space: normal;
            min-height: 2.45rem;
        }}

        [data-testid="stSidebar"] .stButton > button:hover {{
            background: {DARK_RED};
            color: {WHITE};
            border-color: {DARK_RED};
        }}

        /* Metrics */
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

        /* Main-page buttons */
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

        /* Inputs */
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

        /* Sliders */
        [data-testid="stSlider"] [role="slider"] {{
            background-color: {PURPLE} !important;
        }}

        /* Main-page expanders */
        section.main [data-testid="stExpander"] {{
            border: 1px solid {BEIGE};
            border-radius: 8px;
            background: {WHITE};
        }}

        /* Tabs */
        button[data-baseweb="tab"] {{
            color: {GREY_DARK};
        }}

        button[data-baseweb="tab"][aria-selected="true"] {{
            color: {PURPLE} !important;
        }}

        /* Info / warning boxes */
        [data-testid="stAlert"] {{
            border-radius: 8px;
        }}

        /* Dataframes */
        [data-testid="stDataFrame"] {{
            border: 1px solid {BEIGE};
            border-radius: 8px;
            overflow: hidden;
        }}

        /* Horizontal separators */
        hr {{
            border-color: {BEIGE};
        }}

        /* Links */
        a {{
            color: {DARK_RED} !important;
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
    raw_data = get_raw_data()
    return calculate_kpi(raw_data, kpi_name)


raw = get_raw_data()


def format_multiple(value):
    if pd.isna(value):
        return "–"
    return f"{value:.2f}x"


def brand_plotly(fig, *, legend_title=None):
    """Apply a consistent Thursday theme to Plotly figures."""
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


def show_navigation_overview():
    st.header("Navigation overview")
    st.caption("Choose an industry in the sidebar, then select one of the KPIs available under it.")

    industries = list(INDUSTRY_KPI_CATALOG.items())
    first_row = st.columns(3)
    second_row = st.columns(2)
    card_slots = first_row + second_row

    for slot, (industry, kpis) in zip(card_slots, industries):
        with slot:
            with st.container(border=True):
                st.subheader(industry)
                if kpis:
                    for kpi_name in kpis:
                        st.markdown(f"**{kpi_name}**")
                    st.caption(f"{len(kpis)} KPI available")
                else:
                    st.caption("No KPIs added yet")

    st.divider()
    st.markdown(
        "New KPIs are discovered automatically from the `kpis/` folder. "
        "Add one KPI file under the relevant industry and it appears in the navigation automatically."
    )


def show_kpi_workspace(industry: str, kpi_name: str):
    kpi = get_kpi_data(kpi_name)
    valid = kpi.dropna(subset=["KPI_Value"]).copy()
    all_years = sorted(int(x) for x in kpi["ÅR"].dropna().unique())

    st.caption(f"{industry}  /  {kpi_name}")
    st.header(kpi_name)

    with st.expander("KPI definition"):
        st.code(KPI_REGISTRY[kpi_name]["formula_label"], language=None)
        st.caption(
            "A KPI value is only calculated when all required source attributes are present "
            "and the denominator is non-zero."
        )

    overview_tab, explorer_tab, profile_tab, comparison_tab, quality_tab = st.tabs(
        ["Overview", "Explorer", "Company profile", "Sector comparison", "Data quality"]
    )

    with overview_tab:
        selected_year = st.selectbox(
            "Year",
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
        c1.metric("Banks represented", represented)
        c2.metric("Banks with complete KPI", complete)
        c3.metric("Sector median", format_multiple(median))
        c4.metric("Sector mean", format_multiple(mean))

        st.subheader("Distribution across banks")
        fig = px.histogram(
            yr,
            x="KPI_Value",
            nbins=20,
            labels={"KPI_Value": kpi_name},
            hover_data=["navn"],
            color_discrete_sequence=[PURPLE],
        )
        fig.update_traces(marker_line_color=WHITE, marker_line_width=0.7)
        fig.update_layout(yaxis_title="Number of banks", xaxis_tickformat=".2f", showlegend=False)
        brand_plotly(fig)
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Sector development")
        trend = (
            valid.groupby("ÅR", as_index=False)
            .agg(Median=("KPI_Value", "median"), Mean=("KPI_Value", "mean"), Banks=("regnr", "nunique"))
        )
        trend_long = trend.melt(
            id_vars=["ÅR", "Banks"],
            value_vars=["Median", "Mean"],
            var_name="Series",
            value_name="Value",
        )
        fig2 = px.line(
            trend_long,
            x="ÅR",
            y="Value",
            color="Series",
            markers=True,
            color_discrete_map={"Median": PURPLE, "Mean": COGNAC},
        )
        fig2.update_traces(line_width=3, marker_size=8)
        fig2.update_layout(yaxis_title=kpi_name, xaxis_title=None)
        brand_plotly(fig2)
        st.plotly_chart(fig2, use_container_width=True)

    with explorer_tab:
        names = sorted(valid["navn"].unique())
        default_names = names[: min(5, len(names))]
        selected_banks = st.multiselect(
            "Banks",
            names,
            default=default_names,
            key=f"explorer_banks_{industry}_{kpi_name}",
        )
        year_range = st.slider(
            "Years",
            min(all_years),
            max(all_years),
            (min(all_years), max(all_years)),
            key=f"explorer_years_{industry}_{kpi_name}",
        )

        chart_df = valid[
            valid["navn"].isin(selected_banks)
            & valid["ÅR"].between(year_range[0], year_range[1])
        ].copy()

        if chart_df.empty:
            st.info("Select at least one bank with available KPI observations in the chosen period.")
        else:
            fig = px.line(
                chart_df,
                x="ÅR",
                y="KPI_Value",
                color="navn",
                markers=True,
                labels={"KPI_Value": kpi_name, "navn": "Bank"},
                color_discrete_sequence=BRAND_SEQUENCE,
            )
            fig.update_traces(line_width=2.7, marker_size=7)
            fig.update_layout(xaxis_title=None)
            brand_plotly(fig, legend_title="Bank")
            st.plotly_chart(fig, use_container_width=True)

            table = chart_df.pivot(index="navn", columns="ÅR", values="KPI_Value")
            st.dataframe(table.style.format("{:.2f}x", na_rep="–"), use_container_width=True)

    with profile_tab:
        bank_names = sorted(kpi["navn"].unique())
        selected_bank = st.selectbox(
            "Bank",
            bank_names,
            key=f"profile_bank_{industry}_{kpi_name}",
        )
        bank_all = kpi[kpi["navn"] == selected_bank].sort_values("ÅR")
        bank_valid = bank_all.dropna(subset=["KPI_Value"])

        if bank_valid.empty:
            st.warning("No complete observations are available for this KPI for the selected bank.")
        else:
            last_row = bank_valid.iloc[-1]
            last_year = int(last_row["ÅR"])
            sector_year = valid[valid["ÅR"] == last_year]
            sector_median = sector_year["KPI_Value"].median()

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Latest available year", last_year)
            c2.metric(kpi_name, format_multiple(last_row["KPI_Value"]))
            c3.metric("Sector median", format_multiple(sector_median))
            c4.metric("Complete years", int(bank_valid["ÅR"].nunique()))

            fig = px.line(
                bank_valid,
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
                annotation_text=f"{last_year} sector median",
                annotation_font_color=COGNAC,
            )
            fig.update_layout(yaxis_title=kpi_name, xaxis_title=None)
            brand_plotly(fig)
            st.plotly_chart(fig, use_container_width=True)

            st.subheader("Underlying calculation — latest available year")
            st.dataframe(
                pd.DataFrame(
                    {
                        "Item": ["Numerator", "Denominator", kpi_name],
                        "Value": [last_row["Numerator"], last_row["Denominator"], last_row["KPI_Value"]],
                    }
                ),
                use_container_width=True,
                hide_index=True,
            )

    with comparison_tab:
        selected_year = st.selectbox(
            "Year",
            all_years,
            index=len(all_years) - 1,
            key=f"comparison_year_{industry}_{kpi_name}",
        )
        yr = valid[valid["ÅR"] == selected_year].copy()
        if yr.empty:
            st.info("No complete KPI observations for the selected year.")
        else:
            yr["Percentile"] = yr["KPI_Value"].rank(pct=True) * 100
            yr = yr.sort_values("KPI_Value", ascending=False)

            fig = px.bar(
                yr,
                x="KPI_Value",
                y="navn",
                orientation="h",
                color="Percentile",
                color_continuous_scale=[
                    [0.0, BEIGE],
                    [0.5, BLUE_GREY],
                    [1.0, PURPLE],
                ],
                hover_data={"Percentile": ":.0f", "KPI_Value": ":.2f"},
                labels={"KPI_Value": kpi_name, "navn": "Bank", "Percentile": "Sector percentile"},
            )
            fig.update_layout(
                height=max(500, 24 * len(yr)),
                yaxis={"categoryorder": "total ascending"},
                coloraxis_colorbar=dict(title="Percentile"),
            )
            brand_plotly(fig)
            st.plotly_chart(fig, use_container_width=True)

            display = yr[["navn", "KPI_Value", "Percentile"]].rename(
                columns={"navn": "Bank", "KPI_Value": kpi_name, "Percentile": "Sector percentile"}
            )
            st.dataframe(
                display.style.format({kpi_name: "{:.2f}x", "Sector percentile": "{:.0f}"}),
                use_container_width=True,
                hide_index=True,
            )

    with quality_tab:
        st.write(
            "This page makes the calculation coverage explicit rather than silently treating "
            "missing source attributes as zero."
        )

        coverage = (
            kpi.groupby("ÅR", as_index=False)
            .agg(
                BanksRepresented=("regnr", "nunique"),
                CompleteKPI=("KPI_Value", lambda s: s.notna().sum()),
            )
        )
        coverage["CoveragePct"] = coverage["CompleteKPI"] / coverage["BanksRepresented"] * 100
        st.dataframe(
            coverage.style.format({"CoveragePct": "{:.1f}%"}),
            use_container_width=True,
            hide_index=True,
        )

        st.subheader("Bank-year observations with missing KPI inputs")
        missing = kpi[kpi["KPI_Value"].isna()][["ÅR", "regnr", "navn"]].sort_values(["ÅR", "navn"])
        st.dataframe(missing, use_container_width=True, hide_index=True)


# -----------------------------------------------------------------------------
# Session state for hierarchical navigation
# -----------------------------------------------------------------------------
if "selected_industry" not in st.session_state:
    st.session_state.selected_industry = None
if "selected_kpi" not in st.session_state:
    st.session_state.selected_kpi = None


st.title("Financial Services Intelligence")
st.caption("Danish financial services research and benchmarking")

with st.sidebar:
    st.header("Navigation")

    if st.button("Navigation overview", key="nav_overview", use_container_width=True):
        st.session_state.selected_industry = None
        st.session_state.selected_kpi = None

    st.divider()

    for industry, kpis in INDUSTRY_KPI_CATALOG.items():
        is_active_industry = st.session_state.selected_industry == industry
        should_expand = is_active_industry or (industry == "Bank" and st.session_state.selected_kpi is None)

        with st.expander(industry, expanded=should_expand):
            if not kpis:
                st.caption("No KPIs added yet")
                continue

            for kpi_name in kpis:
                if st.button(
                    kpi_name,
                    key=f"nav_{industry}_{kpi_name}",
                    use_container_width=True,
                ):
                    st.session_state.selected_industry = industry
                    st.session_state.selected_kpi = kpi_name

    if st.session_state.selected_kpi:
        st.divider()
        st.caption("Selected KPI")
        st.write(st.session_state.selected_kpi)


if st.session_state.selected_kpi is None:
    show_navigation_overview()
else:
    show_kpi_workspace(
        st.session_state.selected_industry,
        st.session_state.selected_kpi,
    )

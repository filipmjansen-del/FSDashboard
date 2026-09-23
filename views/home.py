"""Homepage overview rendering."""

import pandas as pd
import plotly.express as px
import streamlit as st

from dashboards.registry import INDUSTRY_DASHBOARD_CATALOG
from kpis.registry import INDUSTRY_KPI_CATALOG, KPI_REGISTRY
from ui.formatting import brand_plotly, format_kpi_value
from ui.components import render_orientation_card, render_page_intro, render_section_intro
from ui.theme import BRAND_SEQUENCE


def render_home(raw, get_kpi_data, navigate_to, industries):
    render_page_intro(
        "Finansiel markedsoversigt",
        "Start med et overblik over datagrundlaget, vælg en KPI eller gå direkte til en analyse.",
    )
    render_orientation_card(
        "Find dit marked i navigationen",
        "Brug sidepanelet til at vælge et marked og åbne dets KPI'er eller analyser.",
    )
    render_orientation_card(
        "Få et hurtigt KPI-overblik",
        "KPI-puls viser de seneste sektormedianer og fører videre til den enkelte KPI.",
    )
    render_orientation_card(
        "Gå direkte til et arbejdsområde",
        "Hurtig adgang åbner en valgt KPI eller analyse uden at gå gennem sidepanelet.",
    )
    valid_years = pd.to_numeric(raw["ÅR"], errors="coerce").dropna()
    latest_year = int(valid_years.max()) if not valid_years.empty else None
    if latest_year is not None:
        latest_raw = raw[pd.to_numeric(raw["ÅR"], errors="coerce") == latest_year].copy()
        latest_company_count = latest_raw[["Branche", "regnr"]].drop_duplicates().shape[0]
    else:
        latest_company_count = 0
    total_kpis = sum(len(INDUSTRY_KPI_CATALOG.get(i, [])) for i in industries)
    total_dashboards = sum(len(INDUSTRY_DASHBOARD_CATALOG.get(i, [])) for i in industries)
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Seneste dataår", latest_year if latest_year is not None else "–")
    c2.metric("Markeder", len(industries))
    c3.metric("Selskaber", latest_company_count)
    c4.metric("KPI'er", total_kpis)
    c5.metric("Analyser", total_dashboards)

    render_section_intro(
        "KPI-puls",
        "Vælg et marked og se de seneste sektormedianer, før du går videre til en KPI.",
    )
    industries_with_kpis = [industry for industry in industries if INDUSTRY_KPI_CATALOG.get(industry, [])]
    if industries_with_kpis:
        pulse_industry = st.selectbox("Marked", industries_with_kpis, key="home_pulse_industry")
        available_pulse_kpis = INDUSTRY_KPI_CATALOG.get(pulse_industry, [])
        default_pulse_kpis = available_pulse_kpis[:min(4, len(available_pulse_kpis))]
        selected_pulse_kpis = st.multiselect("KPI'er på forsiden", available_pulse_kpis,
                                              default=default_pulse_kpis, key="home_pulse_kpis")
        if len(selected_pulse_kpis) > 4:
            st.info("Forsiden viser maksimalt fire KPI'er ad gangen.")
            selected_pulse_kpis = selected_pulse_kpis[:4]
        if selected_pulse_kpis:
            pulse_columns = st.columns(len(selected_pulse_kpis))
            for col, kpi_name in zip(pulse_columns, selected_pulse_kpis):
                meta = KPI_REGISTRY[kpi_name]
                valid_kpi = get_kpi_data(kpi_name).dropna(subset=["KPI_Value"]).copy()
                with col:
                    with st.container(border=True):
                        st.markdown(f"**{kpi_name}**")
                        if valid_kpi.empty:
                            st.metric("Sektormedian", "–")
                            st.caption("Ingen komplette observationer")
                        else:
                            kpi_year = int(valid_kpi["ÅR"].max())
                            kpi_year_data = valid_kpi[valid_kpi["ÅR"] == kpi_year].copy()
                            median_value = kpi_year_data["KPI_Value"].median()
                            company_count = kpi_year_data["regnr"].nunique()
                            st.metric("Sektormedian", format_kpi_value(median_value, meta))
                            st.caption(f"{kpi_year} · {company_count} selskaber")
                        if st.button("Åbn KPI", key=f"home_open_kpi_{pulse_industry}_{kpi_name}",
                                     use_container_width=True):
                            navigate_to(pulse_industry, "kpi", kpi_name)
        else:
            st.info("Vælg mindst én KPI for at vise KPI-pulsen.")
    else:
        st.info("Der er endnu ingen KPI'er tilgængelige.")

    render_section_intro(
        "Hurtig adgang",
        "Åbn en KPI eller analyse direkte, når du allerede ved, hvad du vil undersøge.",
    )
    q1, q2, q3, q4 = st.columns([1.2, 1.0, 2.0, 0.8])
    with q1:
        quick_industry = st.selectbox("Marked", industries, key="home_quick_industry")
    quick_kpis = INDUSTRY_KPI_CATALOG.get(quick_industry, [])
    quick_dashboards = INDUSTRY_DASHBOARD_CATALOG.get(quick_industry, [])
    quick_type_options = []
    if quick_kpis:
        quick_type_options.append("KPI")
    if quick_dashboards:
        quick_type_options.append("Analyse")
    if quick_type_options:
        with q2:
            quick_type = st.selectbox("Type", quick_type_options, key="home_quick_type")
        quick_items = quick_kpis if quick_type == "KPI" else quick_dashboards
        with q3:
            quick_name = st.selectbox("Vælg indhold", quick_items, key="home_quick_name")
        with q4:
            st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
            if st.button("Åbn", key="home_quick_open", use_container_width=True):
                navigate_to(quick_industry, "kpi" if quick_type == "KPI" else "dashboard", quick_name)
    else:
        with q2:
            st.write("")
        with q3:
            st.info("Der er endnu ikke tilføjet KPI'er eller analyser til dette marked.")
        with q4:
            st.write("")

    render_section_intro(
        "Datagrundlag",
        "Se datadækningen over tid og status for de markeder, der er tilgængelige i løsningen.",
    )
    left, right = st.columns([1.7, 1.0])
    with left:
        coverage_source = raw.copy()
        coverage_source["ÅR"] = pd.to_numeric(coverage_source["ÅR"], errors="coerce")
        coverage_source = coverage_source.dropna(subset=["ÅR", "Branche", "regnr"])
        coverage_source["ÅR"] = coverage_source["ÅR"].astype(int)
        coverage = coverage_source.groupby(["ÅR", "Branche"], as_index=False).agg(Selskaber=("regnr", "nunique"))
        coverage = coverage[coverage["Branche"].isin(industries)]
        if not coverage.empty:
            fig = px.line(coverage, x="ÅR", y="Selskaber", color="Branche", markers=True,
                          color_discrete_sequence=BRAND_SEQUENCE,
                          labels={"ÅR": "År", "Selskaber": "Antal selskaber", "Branche": "Marked"})
            fig.update_traces(line_width=2.5, marker_size=6)
            fig.update_layout(xaxis_title=None, yaxis_title="Antal selskaber")
            brand_plotly(fig, legend_title="Marked")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Der er ikke nok data til at vise udviklingen i datadækningen.")
    with right:
        status_rows = []
        for industry in industries:
            sector = raw[raw["Branche"] == industry].copy()
            sector_years = pd.to_numeric(sector["ÅR"], errors="coerce").dropna()
            if sector_years.empty:
                sector_latest_year, sector_company_count = None, 0
            else:
                sector_latest_year = int(sector_years.max())
                sector_latest = sector[pd.to_numeric(sector["ÅR"], errors="coerce") == sector_latest_year]
                sector_company_count = sector_latest["regnr"].nunique()
            status_rows.append({"Marked": industry, "Seneste år": sector_latest_year if sector_latest_year else "–",
                                "Selskaber": sector_company_count, "KPI'er": len(INDUSTRY_KPI_CATALOG.get(industry, [])),
                                "Analyser": len(INDUSTRY_DASHBOARD_CATALOG.get(industry, []))})
        st.dataframe(pd.DataFrame(status_rows), use_container_width=True, hide_index=True)

    render_section_intro(
        "Markeder",
        "Se hvilke markeder, KPI'er og analyser der er tilgængelige, før du går i dybden.",
    )
    for row_industries in [industries[i:i + 3] for i in range(0, len(industries), 3)]:
        cols = st.columns(len(row_industries))
        for col, industry in zip(cols, row_industries):
            kpis = INDUSTRY_KPI_CATALOG.get(industry, [])
            dashboards = INDUSTRY_DASHBOARD_CATALOG.get(industry, [])
            sector = raw[raw["Branche"] == industry].copy()
            sector_years = pd.to_numeric(sector["ÅR"], errors="coerce").dropna()
            if sector_years.empty:
                sector_latest_year, sector_company_count = "–", 0
            else:
                sector_latest_year = int(sector_years.max())
                sector_latest = sector[pd.to_numeric(sector["ÅR"], errors="coerce") == sector_latest_year]
                sector_company_count = sector_latest["regnr"].nunique()
            with col:
                with st.container(border=True):
                    st.subheader(industry)
                    st.metric("Selskaber", sector_company_count)
                    st.caption(f"Seneste dataår: {sector_latest_year} · {len(kpis)} KPI'er · {len(dashboards)} analyser")
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

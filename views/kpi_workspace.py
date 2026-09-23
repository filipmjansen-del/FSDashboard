"""KPI workspace rendering."""

import pandas as pd
import plotly.express as px
import streamlit as st

from kpis.registry import get_metric_metadata
from ui.formatting import apply_kpi_axis_format, brand_plotly, format_kpi_value, get_plotly_hover_format
from ui.theme import BEIGE, BLUE_GREY, BRAND_SEQUENCE, COGNAC, PURPLE, WHITE


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


def show_kpi_definition(meta):
    formula_label = meta.get("formula_label", "Formeldefinition ikke angivet.")
    description = meta.get("description")
    interpretation = meta.get("interpretation")
    direction = meta.get("direction", "neutral")
    direction_explanation = meta.get("direction_explanation")
    caveat = meta.get("caveat")
    reading_guide = meta.get("reading_guide")

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

        if reading_guide:
            st.markdown("**Sådan læses værdien**")
            st.write(reading_guide)

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


def render_kpi_workspace(industry: str, kpi_name: str, get_kpi_data):
    # The UI still displays legacy names, while the workspace accepts stable metric IDs.
    meta = get_metric_metadata(kpi_name)
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

    if meta.get("description"):
        st.write(meta["description"])
    if meta.get("reading_guide"):
        st.info(meta["reading_guide"])

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
        st.caption(
            "Den vandrette akse viser KPI-værdien; søjlehøjden viser antal "
            f"{entity_plural.lower()} i hvert interval. En søjle er ikke ét selskab."
        )

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
        st.caption(
            "Hvert punkt er medianen eller gennemsnittet blandt selskaber med en "
            "tilgængelig værdi det pågældende år. Selskabskredsen kan ændre sig "
            "mellem år; store udsving kan trække gennemsnittet mere end medianen."
        )

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
        st.caption(
            "Hver linje viser ét selskabs KPI over tid. År står på den vandrette "
            "akse og KPI-værdien på den lodrette. Manglende punkter er manglende "
            "data, ikke nul."
        )
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
        st.caption(
            "Linjen viser det valgte selskabs udvikling. Den stiplede linje er "
            "sektormedianen i selskabets seneste år med data og er derfor ikke en "
            "årsspecifik median for hele tidsserien."
        )
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

            st.subheader(
                "Rapporteret værdi – seneste tilgængelige år"
                if meta.get("source_type") == "reported"
                else "Underliggende beregning – seneste tilgængelige år"
            )
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
            yr = yr.sort_values("KPI_Value", ascending=False)
            has_direction = direction in {"higher_is_better", "lower_is_better"}
            if has_direction:
                st.caption(
                    "Søjlelængden er den faktiske KPI-værdi. Farven og percentilen "
                    "viser placering blandt selskaber med data i det valgte år: "
                    "højere percentil er bedre i den angivne retning. Det er en "
                    "relativ placering, ikke en absolut kvalitetsgrænse."
                )
            else:
                st.caption(
                    "Søjlelængden er den faktiske KPI-værdi. Selskaberne vises "
                    "efter størrelse, uden rangering af hvad der er bedst."
                )

            hover_data = {"KPI_Value": get_plotly_hover_format(meta)}
            labels = {"KPI_Value": kpi_name, "navn": entity_singular}
            color_options = {"color_discrete_sequence": [PURPLE]}
            if has_direction:
                hover_data["PerformancePercentile"] = ":.0f"
                labels["PerformancePercentile"] = "Percentil"
                color_options = {
                    "color": "PerformancePercentile",
                    "color_continuous_scale": [
                        [0.0, BEIGE],
                        [0.5, BLUE_GREY],
                        [1.0, PURPLE],
                    ],
                }

            fig = px.bar(
                yr,
                x="KPI_Value",
                y="navn",
                orientation="h",
                hover_data=hover_data,
                labels=labels,
                **color_options,
            )
            fig.update_layout(
                height=max(500, 24 * len(yr)),
                yaxis={"categoryorder": "total ascending"},
                showlegend=False,
            )
            if has_direction:
                fig.update_layout(coloraxis_colorbar=dict(title="Percentil"))
            brand_plotly(fig)
            apply_kpi_axis_format(fig, meta, axis="x")
            st.plotly_chart(fig, use_container_width=True)

            display_columns = ["navn", "KPI_Value"]
            if has_direction:
                display_columns.append("PerformancePercentile")
            display = yr[display_columns].rename(
                columns={
                    "navn": entity_singular,
                    "KPI_Value": kpi_name,
                    "PerformancePercentile": "Percentil",
                }
            )

            table_formats = {kpi_name: lambda value: format_kpi_value(value, meta)}
            if has_direction:
                table_formats["Percentil"] = "{:.0f}"
            st.dataframe(
                display.style.format(table_formats),
                use_container_width=True,
                hide_index=True,
            )

    with quality_tab:
        st.write(
            "Denne side viser KPI-dækningen eksplicit. Manglende beregningsinput "
            "eller rapporterede KPI-værdier behandles ikke som nul."
        )
        st.caption(
            "Dækning er andelen af repræsenterede selskaber med en gyldig "
            "KPI-værdi i året. Den siger noget om datatilgængelighed, ikke om "
            "selskabernes resultater."
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


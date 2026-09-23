import pandas as pd
import plotly.express as px
import streamlit as st

from kpis.registry import KPI_REGISTRY, calculate_kpi
from ui.components import render_page_intro, render_section_intro


DASHBOARD_META = {
    "name": "Company fingerprint",
    "industry": "Bank",
    "slug": "company_fingerprint",
    "description": "Sammenlign en banks KPI-profil med sektoren eller en gemt peer group.",
}


PURPLE = "#412B48"
DARK_RED = "#842044"
COGNAC = "#B25F4D"
BEIGE = "#DBD4CF"
GREY_LIGHT = "#EEEEEE"
GREY_DARK = "#A1A1A1"
WHITE = "#FFFFFF"
BLACK = "#000000"


def _format_kpi_value(value, meta):
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
        return f"DKK {value / 1_000_000:,.{decimals}f}m"
    if display_format == "dkk_billion":
        return f"DKK {value / 1_000_000_000:,.{decimals}f}bn"

    return f"{value:,.{decimals}f}"


def _format_delta(value, meta):
    if pd.isna(value):
        return "–"

    display_format = meta.get("display_format", "number")
    decimals = meta.get("decimals", 2)

    if display_format == "percentage":
        return f"{value * 100:+.{decimals}f} pp"
    if display_format == "multiple":
        return f"{value:+.{decimals}f}x"
    if display_format == "integer":
        return f"{value:+,.0f}"
    if display_format == "dkk":
        return f"DKK {value:+,.{decimals}f}"
    if display_format == "dkk_million":
        return f"DKK {value / 1_000_000:+,.{decimals}f}m"
    if display_format == "dkk_billion":
        return f"DKK {value / 1_000_000_000:+,.{decimals}f}bn"

    return f"{value:+,.{decimals}f}"


def _bank_kpis():
    return sorted(
        name
        for name, meta in KPI_REGISTRY.items()
        if meta.get("industry") == "Bank"
    )


def _bank_year_companies(raw, year):
    frame = raw[
        (raw["Branche"] == "Bank")
        & (pd.to_numeric(raw["ÅR"], errors="coerce") == year)
    ][["regnr", "navn"]].dropna().drop_duplicates()

    frame["regnr"] = frame["regnr"].astype(str)
    return frame.sort_values("navn")


def _asset_value(raw, year, regnr):
    frame = raw[
        (raw["Branche"] == "Bank")
        & (pd.to_numeric(raw["ÅR"], errors="coerce") == year)
        & (raw["Attribute"] == "Bal_BO_ATot")
    ][["regnr", "Value"]].copy()

    if frame.empty:
        return None

    frame["regnr"] = frame["regnr"].astype(str)
    frame["Value"] = pd.to_numeric(frame["Value"], errors="coerce")
    row = frame[frame["regnr"] == str(regnr)]
    if row.empty:
        return None
    value = row["Value"].dropna()
    return None if value.empty else float(value.iloc[-1])


def _percentile(values, target_value, direction):
    values = pd.Series(values).dropna()
    if values.empty or pd.isna(target_value):
        return None

    if direction == "lower_is_better":
        pct = values.rank(pct=True, ascending=False)
    else:
        pct = values.rank(pct=True, ascending=True)

    matches = values.index[values == target_value]
    if len(matches) == 0:
        # Rank target together with peers if floating point equality is not exact.
        combined = pd.concat([values.reset_index(drop=True), pd.Series([target_value])], ignore_index=True)
        if direction == "lower_is_better":
            return float(combined.rank(pct=True, ascending=False).iloc[-1] * 100)
        return float(combined.rank(pct=True, ascending=True).iloc[-1] * 100)

    # If several peers have the same value, use the mean rank for that value.
    return float(pct.loc[matches].mean() * 100)


def render(raw):
    render_page_intro(
        "Company fingerprint",
        "Se en banks KPI-profil mod alle banker eller en gemt peer group. Percentiler viser placering i den valgte benchmarkgruppe.",
    )

    bank_raw = raw[raw["Branche"] == "Bank"].copy()
    years = sorted(
        int(y)
        for y in pd.to_numeric(bank_raw["ÅR"], errors="coerce").dropna().unique()
    )

    if not years:
        st.warning("Ingen bankår fundet i datasættet.")
        return

    saved_year = st.session_state.get("bank_peer_year")
    default_year = saved_year if saved_year in years else years[-1]
    year = st.selectbox(
        "År",
        years,
        index=years.index(default_year),
        key="fingerprint_year",
    )

    companies = _bank_year_companies(raw, year)
    if companies.empty:
        st.warning("Ingen banker fundet for det valgte år.")
        return

    company_names = dict(zip(companies["regnr"], companies["navn"]))
    company_ids = list(companies["regnr"])

    saved_target = st.session_state.get("bank_peer_target_regnr")
    default_target = saved_target if saved_target in company_ids else company_ids[0]

    target_regnr = st.selectbox(
        "Bank",
        company_ids,
        index=company_ids.index(default_target),
        format_func=lambda x: company_names.get(x, x),
        key="fingerprint_bank",
    )
    target_name = company_names.get(target_regnr, target_regnr)

    saved_peers = [
        str(x)
        for x in st.session_state.get("bank_peer_regnrs", [])
        if str(x) in company_ids
    ]
    saved_peer_target = str(st.session_state.get("bank_peer_target_regnr", ""))
    saved_peer_year = st.session_state.get("bank_peer_year")

    benchmark_options = ["Alle banker"]
    saved_group_available = (
        bool(saved_peers)
        and saved_peer_target == str(target_regnr)
        and saved_peer_year == year
    )
    if saved_group_available:
        benchmark_options.append("Gemt peer group")

    benchmark = st.radio(
        "Benchmark",
        benchmark_options,
        horizontal=True,
        key="fingerprint_benchmark",
    )

    if benchmark == "Gemt peer group":
        benchmark_regnrs = list(dict.fromkeys([str(target_regnr)] + saved_peers))
    else:
        benchmark_regnrs = company_ids

    bank_kpis = _bank_kpis()
    if not bank_kpis:
        st.warning("Der er endnu ingen registrerede Bank-KPI'er at bygge fingerprintet på.")
        return

    selected_kpis = st.multiselect(
        "KPI'er i fingerprint",
        bank_kpis,
        default=bank_kpis[: min(8, len(bank_kpis))],
        key="fingerprint_kpis",
    )

    if not selected_kpis:
        st.info("Vælg mindst én KPI.")
        return

    rows = []
    previous_year = year - 1

    for kpi_name in selected_kpis:
        meta = KPI_REGISTRY[kpi_name]
        kpi = calculate_kpi(raw, kpi_name).copy()
        if kpi.empty or "KPI_Value" not in kpi.columns:
            continue

        kpi["regnr"] = kpi["regnr"].astype(str)
        kpi["ÅR"] = pd.to_numeric(kpi["ÅR"], errors="coerce")

        current = kpi[
            (kpi["ÅR"] == year)
            & (kpi["regnr"].isin(benchmark_regnrs))
        ][["regnr", "KPI_Value"]].dropna(subset=["KPI_Value"])

        if current.empty:
            continue

        target_current = current[current["regnr"] == str(target_regnr)]
        if target_current.empty:
            continue

        target_value = float(target_current["KPI_Value"].iloc[-1])
        peer_median = float(current["KPI_Value"].median())
        direction = meta.get("direction", "neutral")

        if direction == "neutral":
            percentile = None
        elif direction == "lower_is_better":
            ranked = current["KPI_Value"].rank(pct=True, ascending=False) * 100
            current = current.assign(_pct=ranked)
            pct_row = current[current["regnr"] == str(target_regnr)]
            percentile = None if pct_row.empty else float(pct_row["_pct"].iloc[-1])
        else:
            ranked = current["KPI_Value"].rank(pct=True, ascending=True) * 100
            current = current.assign(_pct=ranked)
            pct_row = current[current["regnr"] == str(target_regnr)]
            percentile = None if pct_row.empty else float(pct_row["_pct"].iloc[-1])

        previous = kpi[
            (kpi["ÅR"] == previous_year)
            & (kpi["regnr"] == str(target_regnr))
        ]["KPI_Value"].dropna()
        previous_value = float(previous.iloc[-1]) if not previous.empty else None
        yoy_change = target_value - previous_value if previous_value is not None else None

        rows.append(
            {
                "KPI": kpi_name,
                "Value": target_value,
                "PeerMedian": peer_median,
                "Percentile": percentile,
                "YoYChange": yoy_change,
                "Direction": direction,
                "Meta": meta,
            }
        )

    if not rows:
        st.warning("Den valgte bank har ingen komplette observationer for de valgte KPI'er i dette år.")
        return

    asset_value = _asset_value(raw, year, target_regnr)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Bank", target_name)
    c2.metric("Benchmarkgruppe", f"{len(benchmark_regnrs)} banker")
    c3.metric("KPI'er med data", len(rows))
    if asset_value is not None:
        c4.metric("Aktiver i alt", f"DKK {asset_value / 1_000_000:.1f} mia.")
    else:
        c4.metric("Aktiver i alt", "–")

    chart_df = pd.DataFrame(
        {
            "KPI": [r["KPI"] for r in rows],
            "Percentile": [r["Percentile"] for r in rows],
            "KPIValue": [_format_kpi_value(r["Value"], r["Meta"]) for r in rows],
            "PeerMedian": [_format_kpi_value(r["PeerMedian"], r["Meta"]) for r in rows],
        }
    ).dropna(subset=["Percentile"])

    if not chart_df.empty:
        chart_df = chart_df.sort_values("Percentile", ascending=True)
        render_section_intro("Relativ profil", "Sammenligner bankens placering for KPI'er med en entydig retning.")
        fig = px.bar(
            chart_df,
            x="Percentile",
            y="KPI",
            orientation="h",
            hover_data={
                "KPIValue": True,
                "PeerMedian": True,
                "Percentile": ":.0f",
            },
            labels={
                "Percentile": "Percentil",
                "KPIValue": target_name,
                "PeerMedian": "Peer median",
            },
            color_discrete_sequence=[PURPLE],
        )
        fig.add_vline(x=50, line_dash="dash", line_color=COGNAC)
        fig.update_xaxes(range=[0, 100], ticksuffix="%")
        fig.update_layout(
            height=max(420, 55 * len(chart_df)),
            yaxis_title=None,
            xaxis_title="Relativ placering i benchmarkgruppen",
            paper_bgcolor=WHITE,
            plot_bgcolor=WHITE,
            margin=dict(l=20, r=20, t=20, b=20),
            showlegend=False,
            font=dict(color=BLACK),
        )
        st.plotly_chart(fig, use_container_width=True)
        st.caption(
            "50% svarer omtrent til midten af benchmarkgruppen. For KPI'er markeret som lower_is_better "
            "vendes percentilen, så en lavere KPI-værdi giver en højere relativ placering. Neutral KPI'er "
            "vises som ren statistisk percentile."
        )

    table_rows = []
    for row in rows:
        table_rows.append(
            {
                "KPI": row["KPI"],
                target_name: _format_kpi_value(row["Value"], row["Meta"]),
                "Peer median": _format_kpi_value(row["PeerMedian"], row["Meta"]),
                "Percentil": "–" if row["Percentile"] is None else f"{row['Percentile']:.0f}%",
                f"Ændring vs. {previous_year}": _format_delta(row["YoYChange"], row["Meta"]),
            }
        )

    render_section_intro("Detaljer", "Se KPI-værdier, peer medianer og ændringer for den valgte bank.")
    st.dataframe(pd.DataFrame(table_rows), use_container_width=True, hide_index=True)

    if not saved_group_available:
        st.info(
            "Vil du benchmarke mod en specifik peer group, så gå til 'Peer selection', vælg banken og peers, "
            "og gem gruppen. Den bliver derefter tilgængelig her."
        )

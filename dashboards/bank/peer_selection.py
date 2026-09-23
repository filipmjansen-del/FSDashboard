import math

import pandas as pd
import plotly.express as px
import streamlit as st

from kpis.registry import KPI_REGISTRY, calculate_kpi


DASHBOARD_META = {
    "name": "Peer selection",
    "industry": "Bank",
    "slug": "peer_selection",
    "description": "Byg og gem en relevant peer group ud fra størrelse eller et manuelt udvalg.",
}


PURPLE = "#412B48"
DARK_RED = "#842044"
COGNAC = "#B25F4D"
BEIGE = "#DBD4CF"
GREY_LIGHT = "#EEEEEE"
WHITE = "#FFFFFF"
BLACK = "#000000"

ASSET_ATTRIBUTE = "Bal_BO_ATot"


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


def _asset_table(raw, year):
    frame = raw[
        (raw["Branche"] == "Bank")
        & (pd.to_numeric(raw["ÅR"], errors="coerce") == year)
        & (raw["Attribute"] == ASSET_ATTRIBUTE)
    ][["regnr", "navn", "Value"]].copy()

    frame["regnr"] = frame["regnr"].astype(str)
    frame["Value"] = pd.to_numeric(frame["Value"], errors="coerce")
    frame = frame.dropna(subset=["Value"])
    # `regnr` identifies the legal entity; `navn` is retained only for display.
    frame = (
        frame.sort_values(["regnr"])
        .groupby("regnr", as_index=False)
        .last()
        .rename(columns={"Value": "TotalAssets"})
    )
    return frame.sort_values("TotalAssets", ascending=False)


def _bank_kpis():
    return sorted(
        name
        for name, meta in KPI_REGISTRY.items()
        if meta.get("industry") == "Bank"
    )


def _similar_peers(asset_df, target_regnr, count):
    target_row = asset_df[asset_df["regnr"] == str(target_regnr)]
    if target_row.empty:
        return []

    target_assets = float(target_row["TotalAssets"].iloc[0])
    if target_assets <= 0:
        return []

    candidates = asset_df[
        (asset_df["regnr"] != str(target_regnr))
        & (asset_df["TotalAssets"] > 0)
    ].copy()
    candidates["SizeDistance"] = candidates["TotalAssets"].apply(
        lambda x: abs(math.log(float(x) / target_assets))
    )
    return candidates.nsmallest(count, "SizeDistance")["regnr"].tolist()


def render(raw):
    st.header("Peer selection")
    st.caption(
        "Vælg en målbank og byg en peer group. Den gemte gruppe kan efterfølgende bruges i Company fingerprint."
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
        key="peer_year",
    )

    asset_df = _asset_table(raw, year)
    if asset_df.empty:
        st.warning(
            f"Ingen observationer for {ASSET_ATTRIBUTE} blev fundet i {year}. "
            "Størrelsesbaseret peer selection kræver aktiver i alt."
        )
        return

    company_names = dict(zip(asset_df["regnr"], asset_df["navn"]))
    company_ids = asset_df["regnr"].tolist()

    saved_target = str(st.session_state.get("bank_peer_target_regnr", ""))
    default_target = saved_target if saved_target in company_ids else company_ids[0]

    target_regnr = st.selectbox(
        "Målbank",
        company_ids,
        index=company_ids.index(default_target),
        format_func=lambda x: company_names.get(x, x),
        key="peer_target",
    )
    target_name = company_names[target_regnr]
    target_assets = float(
        asset_df.loc[asset_df["regnr"] == target_regnr, "TotalAssets"].iloc[0]
    )

    mode = st.radio(
        "Metode",
        ["Lignende størrelse", "Top N efter aktiver", "Alle banker", "Manuelt udvalg"],
        horizontal=True,
        key="peer_mode",
    )

    if mode == "Lignende størrelse":
        max_peers = max(1, min(15, len(asset_df) - 1))
        default_count = min(5, max_peers)
        count = st.slider(
            "Antal peers",
            min_value=1,
            max_value=max_peers,
            value=default_count,
            key="peer_similar_count",
        )
        peer_regnrs = _similar_peers(asset_df, target_regnr, count)

    elif mode == "Top N efter aktiver":
        max_top = max(2, min(20, len(asset_df)))
        default_top = min(10, max_top)
        top_n = st.slider(
            "Antal største banker",
            min_value=2,
            max_value=max_top,
            value=default_top,
            key="peer_top_n",
        )
        top_ids = asset_df.head(top_n)["regnr"].tolist()
        peer_regnrs = [x for x in top_ids if x != target_regnr]

    elif mode == "Alle banker":
        peer_regnrs = [x for x in company_ids if x != target_regnr]

    else:
        suggested = _similar_peers(asset_df, target_regnr, min(5, max(1, len(asset_df) - 1)))
        available_peers = [x for x in company_ids if x != target_regnr]
        saved_peers = [
            str(x)
            for x in st.session_state.get("bank_peer_regnrs", [])
            if str(x) in available_peers
        ]
        defaults = saved_peers if saved_peers else suggested
        peer_regnrs = st.multiselect(
            "Vælg peers",
            available_peers,
            default=defaults,
            format_func=lambda x: company_names.get(x, x),
            key="peer_manual",
        )

    peer_regnrs = list(dict.fromkeys(str(x) for x in peer_regnrs if str(x) != str(target_regnr)))
    selected_regnrs = [str(target_regnr)] + peer_regnrs

    selected = asset_df[asset_df["regnr"].isin(selected_regnrs)].copy()
    selected["Role"] = selected["regnr"].apply(
        lambda x: "Målbank" if x == str(target_regnr) else "Peer"
    )
    selected["SizeDiffPct"] = (
        selected["TotalAssets"] / target_assets - 1
    ) * 100
    selected.loc[selected["regnr"] == str(target_regnr), "SizeDiffPct"] = 0.0

    c1, c2, c3 = st.columns(3)
    c1.metric("Målbank", target_name)
    c2.metric("Aktiver i alt", f"DKK {target_assets / 1_000_000:.1f} mia.")
    c3.metric("Antal peers", len(peer_regnrs))

    if len(peer_regnrs) == 0:
        st.info("Den valgte metode har ikke produceret nogen peers endnu.")
        return

    st.subheader("Peer group efter størrelse")
    chart = selected.sort_values("TotalAssets", ascending=True)
    fig = px.bar(
        chart,
        x="TotalAssets",
        y="navn",
        orientation="h",
        color="Role",
        color_discrete_map={"Målbank": DARK_RED, "Peer": PURPLE},
        hover_data={"SizeDiffPct": ":+.1f", "TotalAssets": ":,.0f"},
        labels={
            "TotalAssets": "Aktiver i alt",
            "navn": "Bank",
            "SizeDiffPct": "Forskel vs. målbank (%)",
        },
    )
    fig.update_xaxes(tickformat=".3s")
    fig.update_layout(
        height=max(420, 36 * len(chart)),
        yaxis_title=None,
        legend_title_text=None,
        paper_bgcolor=WHITE,
        plot_bgcolor=WHITE,
        margin=dict(l=20, r=20, t=20, b=20),
        font=dict(color=BLACK),
    )
    st.plotly_chart(fig, use_container_width=True)

    display = selected[["Role", "navn", "TotalAssets", "SizeDiffPct"]].copy()
    display["Aktiver i alt"] = display["TotalAssets"].apply(
        lambda x: f"DKK {x / 1_000_000:.1f} mia."
    )
    display["Forskel vs. målbank"] = display["SizeDiffPct"].apply(
        lambda x: f"{x:+.1f}%"
    )
    display = display[["Role", "navn", "Aktiver i alt", "Forskel vs. målbank"]]
    display = display.rename(columns={"Role": "Rolle", "navn": "Bank"})
    st.dataframe(display, use_container_width=True, hide_index=True)

    bank_kpis = _bank_kpis()
    if bank_kpis:
        st.subheader("KPI-preview")
        preview_kpis = st.multiselect(
            "KPI'er",
            bank_kpis,
            default=bank_kpis[: min(3, len(bank_kpis))],
            key="peer_preview_kpis",
        )

        if preview_kpis:
            comparison = selected[["regnr", "navn", "Role"]].copy()

            for kpi_name in preview_kpis:
                meta = KPI_REGISTRY[kpi_name]
                kpi = calculate_kpi(raw, kpi_name).copy()
                if kpi.empty or "KPI_Value" not in kpi.columns:
                    comparison[kpi_name] = "–"
                    continue

                kpi["regnr"] = kpi["regnr"].astype(str)
                kpi["ÅR"] = pd.to_numeric(kpi["ÅR"], errors="coerce")
                yr = kpi[
                    (kpi["ÅR"] == year)
                    & (kpi["regnr"].isin(selected_regnrs))
                ][["regnr", "KPI_Value"]].drop_duplicates("regnr", keep="last")

                comparison = comparison.merge(
                    yr.rename(columns={"KPI_Value": f"__{kpi_name}"}),
                    on="regnr",
                    how="left",
                )
                comparison[kpi_name] = comparison[f"__{kpi_name}"].apply(
                    lambda x: _format_kpi_value(x, meta)
                )
                comparison = comparison.drop(columns=[f"__{kpi_name}"])

            comparison = comparison.rename(columns={"navn": "Bank", "Role": "Rolle"})
            comparison = comparison[["Rolle", "Bank"] + preview_kpis]
            st.dataframe(comparison, use_container_width=True, hide_index=True)

    if st.button("Brug denne peer group", type="primary", key="save_peer_group"):
        st.session_state["bank_peer_target_regnr"] = str(target_regnr)
        st.session_state["bank_peer_regnrs"] = peer_regnrs
        st.session_state["bank_peer_year"] = year
        st.success(
            f"Peer group gemt: {target_name} + {len(peer_regnrs)} peers. "
            "Den kan nu bruges i Company fingerprint."
        )

    saved_target_now = str(st.session_state.get("bank_peer_target_regnr", ""))
    saved_peers_now = st.session_state.get("bank_peer_regnrs", [])
    saved_year_now = st.session_state.get("bank_peer_year")
    if saved_target_now and saved_peers_now:
        saved_name = company_names.get(saved_target_now, saved_target_now)
        st.caption(
            f"Aktiv gemt peer group: {saved_name}, {len(saved_peers_now)} peers, år {saved_year_now}."
        )

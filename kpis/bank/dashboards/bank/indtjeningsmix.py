import pandas as pd
import plotly.express as px
import streamlit as st


DASHBOARD_META = {
    "name": "Indtjeningsmix",
    "industry": "Bank",
    "slug": "indtjeningsmix",
    "description": "Sammensætningen af bankernes indtægter på tværs af rente, gebyrer, udbytter, kursreguleringer og øvrige indtægter.",
}

# Thursday palette
PURPLE = "#412B48"
DARK_RED = "#842044"
COGNAC = "#B25F4D"
BLUE_GREY = "#B8CACE"
PURPLE_LIGHT = "#8C8AF8"
ROSE = "#DCB9CA"
PEACH = "#F5C1AE"
OLIVE = "#877470"
STONE = "#A9A69F"

COMPONENTS = {
    "Netto renteindtægter": {
        "positive": ["Res_Rind_RY"],
        "negative": ["Res_Rudg_RY"],
    },
    "Udbytte af aktier mv.": {
        "positive": ["Res_UdAk_RY"],
        "negative": [],
    },
    "Netto gebyr- og provisionsindtægter": {
        "positive": ["Res_GPi_RY"],
        "negative": ["Res_GPu_RY"],
    },
    "Kursreguleringer": {
        "positive": ["Res_Kreg_RY"],
        "negative": [],
    },
    "Andre driftsindtægter": {
        "positive": ["Res_Xdi_RY"],
        "negative": [],
    },
    "Resultat af kapitalandele": {
        "positive": ["Res_Rat_RY"],
        "negative": [],
    },
}

SOURCE_ATTRIBUTES = sorted(
    {
        attr
        for definition in COMPONENTS.values()
        for side in ("positive", "negative")
        for attr in definition[side]
    }
)

COLOR_MAP = {
    "Netto renteindtægter": PURPLE,
    "Netto gebyr- og provisionsindtægter": DARK_RED,
    "Udbytte af aktier mv.": COGNAC,
    "Kursreguleringer": PURPLE_LIGHT,
    "Andre driftsindtægter": BLUE_GREY,
    "Resultat af kapitalandele": ROSE,
}


def build_income_mix(raw: pd.DataFrame) -> pd.DataFrame:
    """Build a company-year income-mix table for Bank.

    Missing source attributes are not treated as zero. A component is only
    calculated when all of the attributes required for that component exist.
    Total income is only calculated when every component is available.
    """
    sector = raw[
        (raw["Branche"] == "Bank")
        & (raw["Attribute"].isin(SOURCE_ATTRIBUTES))
    ].copy()

    index_cols = ["Branche", "ÅR", "Måned", "regnr", "navn"]
    pivot = (
        sector.pivot_table(
            index=index_cols,
            columns="Attribute",
            values="Value",
            aggfunc="first",
        )
        .reset_index()
    )

    for attr in SOURCE_ATTRIBUTES:
        if attr not in pivot.columns:
            pivot[attr] = pd.NA

    component_cols = []

    for component, definition in COMPONENTS.items():
        required = definition["positive"] + definition["negative"]
        complete = pivot[required].notna().all(axis=1)

        value = pd.Series(pd.NA, index=pivot.index, dtype="Float64")
        positive_sum = pivot[definition["positive"]].sum(
            axis=1, min_count=len(definition["positive"])
        )

        if definition["negative"]:
            negative_sum = pivot[definition["negative"]].sum(
                axis=1, min_count=len(definition["negative"])
            )
        else:
            negative_sum = pd.Series(0.0, index=pivot.index)

        value.loc[complete] = (
            positive_sum.loc[complete] - negative_sum.loc[complete]
        )

        pivot[component] = pd.to_numeric(value, errors="coerce")
        component_cols.append(component)

    pivot["CompleteInputs"] = pivot[component_cols].notna().all(axis=1)
    pivot["TotalIncome"] = pivot[component_cols].sum(
        axis=1, min_count=len(component_cols)
    )

    for component in component_cols:
        share_col = f"Share__{component}"
        pivot[share_col] = pd.NA
        valid = pivot["CompleteInputs"] & pivot["TotalIncome"].ne(0)
        pivot.loc[valid, share_col] = (
            pivot.loc[valid, component] / pivot.loc[valid, "TotalIncome"]
        )
        pivot[share_col] = pd.to_numeric(pivot[share_col], errors="coerce")

    return pivot


def _to_long(mix: pd.DataFrame, year: int, banks: list[str]) -> pd.DataFrame:
    components = list(COMPONENTS.keys())
    filtered = mix[(mix["ÅR"] == year) & (mix["navn"].isin(banks))].copy()
    long_df = filtered.melt(
        id_vars=["regnr", "navn", "ÅR", "TotalIncome", "CompleteInputs"],
        value_vars=components,
        var_name="Indtægtskomponent",
        value_name="Beløb",
    )
    return long_df


def render(raw: pd.DataFrame):
    st.header("Bankernes indtjeningsmix")
    st.caption(
        "Indtjeningsmixet dekomponerer netto rente- og gebyrindtægter og supplerer med "
        "kursreguleringer, andre driftsindtægter og resultat af kapitalandele. "
        "Manglende input behandles ikke som nul."
    )

    mix = build_income_mix(raw)
    complete = mix[mix["CompleteInputs"]].copy()

    if complete.empty:
        st.warning("Ingen komplette bank-år kan beregnes med de nødvendige resultatposter.")
        return

    years = sorted(int(x) for x in complete["ÅR"].dropna().unique())
    year = st.selectbox("År", years, index=len(years) - 1, key="income_mix_year")

    year_df = complete[complete["ÅR"] == year].copy()
    available_banks = sorted(year_df["navn"].unique())

    # Default to the 15 largest banks by total income for readability.
    default_banks = (
        year_df.sort_values("TotalIncome", ascending=False)["navn"]
        .drop_duplicates()
        .head(15)
        .tolist()
    )

    banks = st.multiselect(
        "Banker",
        available_banks,
        default=default_banks,
        key="income_mix_banks",
    )

    if not banks:
        st.info("Vælg mindst én bank.")
        return

    long_df = _to_long(complete, year, banks)

    st.subheader("Indtægter fordelt på komponenter")
    fig = px.bar(
        long_df,
        x="navn",
        y="Beløb",
        color="Indtægtskomponent",
        barmode="relative",
        color_discrete_map=COLOR_MAP,
        labels={"navn": "Bank", "Beløb": "Rapporteret beløb"},
        hover_data={"ÅR": True},
    )
    fig.update_layout(
        template="plotly_white",
        xaxis_title=None,
        legend_title_text="Indtægtskomponent",
        margin=dict(l=20, r=20, t=20, b=20),
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Indtjeningsmix som andel af samlet indtjening")
    selected = year_df[year_df["navn"].isin(banks)].copy()
    share_cols = [f"Share__{c}" for c in COMPONENTS]
    share_table = selected.set_index("navn")[share_cols].copy()
    share_table.columns = list(COMPONENTS.keys())
    share_table["Samlet indtjening"] = selected.set_index("navn")["TotalIncome"]

    st.dataframe(
        share_table.style.format(
            {**{c: "{:.1%}" for c in COMPONENTS}, "Samlet indtjening": "{:,.0f}"},
            na_rep="–",
        ),
        use_container_width=True,
    )

    with st.expander("Datagrundlag og definition"):
        st.markdown(
            "- Netto renteindtægter = `Res_Rind_RY - Res_Rudg_RY`\n"
            "- Udbytte af aktier mv. = `Res_UdAk_RY`\n"
            "- Netto gebyr- og provisionsindtægter = `Res_GPi_RY - Res_GPu_RY`\n"
            "- Kursreguleringer = `Res_Kreg_RY`\n"
            "- Andre driftsindtægter = `Res_Xdi_RY`\n"
            "- Resultat af kapitalandele = `Res_Rat_RY`"
        )

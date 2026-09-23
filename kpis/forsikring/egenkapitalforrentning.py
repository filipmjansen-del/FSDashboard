from kpis.forsikring.source import calculate_reported_kpi


KPI_META = {
    "name": "Egenkapitalforrentning i procent",
    "industry": "Forsikring",
    "source_type": "reported",
    "slug": "egenkapitalforrentning",
    "display_format": "percentage",
    "decimals": 1,
    "direction": "higher_is_better",
    "formula_label": "Årets resultat / tidsvægtet gennemsnitlig egenkapital",
    "description": "Årets afkast til ejerne i forhold til den gennemsnitlige egenkapital.",
    "interpretation": "Viser selskabets samlede lønsomhed efter skat.",
    "direction_explanation": "Højere er som udgangspunkt bedre, når risiko og kapitalisering er sammenlignelige.",
    "caveat": "Den officielle definition bruger tidsvægtet gennemsnitlig egenkapital. Værdien er rapporteret i kildedatasættet og genberegnes ikke fra ultimo-balancer.",
}


def calculate(raw):
    return calculate_reported_kpi(raw, KPI_META["name"], "Egenkapitalforrentning i pct. (Return on equity)")

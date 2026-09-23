from kpis.forsikring.source import calculate_reported_kpi


KPI_META = {
    "name": "Operating ratio",
    "industry": "Forsikring",
    "source_type": "reported",
    "slug": "operating_ratio",
    "display_format": "percentage",
    "decimals": 1,
    "direction": "lower_is_better",
    "reading_guide": "95 % betyder 95 kr. i de samlede combined-ratio-komponenter pr. 100 kr. præmier inklusive allokeret forsikringsteknisk rente. Under 100 % er normalt gunstigt; tallet kan afvige fra combined ratio, fordi nævneren er anderledes.",
    "formula_label": "Combined-ratio-komponenter / (præmieindtægter efter bonus og præmierabatter + forsikringsteknisk rente)",
    "description": "Combined ratio genberegnet med allokeret investeringsafkast i præmiegrundlaget.",
    "interpretation": "Viser forsikringsdriftens samlede omkostningsandel inklusive forsikringsteknisk rente.",
    "direction_explanation": "Lavere er som udgangspunkt bedre.",
    "caveat": "Kan afvige fra combined ratio, når forsikringsteknisk rente påvirker nævneren. Værdien er rapporteret i kildedatasættet.",
}


def calculate(raw):
    return calculate_reported_kpi(raw, KPI_META["name"], "Operating ratio")

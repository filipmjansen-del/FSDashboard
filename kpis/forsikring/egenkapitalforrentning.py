from kpis.forsikring.source import calculate_reported_kpi


KPI_META = {
    "name": "Egenkapitalforrentning i procent",
    "industry": "Forsikring",
    "source_type": "reported",
    "source_code": "SA2808",
    "official_definition": "Forholdet mellem årets resultat og årets gennemsnitlige egenkapital opgjort i procent.",
    "slug": "egenkapitalforrentning",
    "display_format": "percentage",
    "decimals": 1,
    "direction": "higher_is_better",
    "reading_guide": "10 % betyder 10 kr. resultat efter skat pr. 100 kr. årets gennemsnitlige egenkapital. Negativ værdi betyder underskud. Højere er normalt gunstigt, men skal ses sammen med risiko og kapitalstyrke.",
    "formula_label": "Årets resultat / årets gennemsnitlige egenkapital",
    "description": "Årets resultat i forhold til årets gennemsnitlige egenkapital.",
    "interpretation": "Viser selskabets samlede lønsomhed efter skat.",
    "direction_explanation": "Højere er som udgangspunkt bedre, når risiko og kapitalisering er sammenlignelige.",
    "caveat": "Værdien er rapporteret i Finanstilsynets kildedatasæt og genberegnes ikke fra råregnskabets balancer.",
}


def calculate(raw):
    return calculate_reported_kpi(raw, KPI_META["name"], "Egenkapitalforrentning i pct. (Return on equity)")

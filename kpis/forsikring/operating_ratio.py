from kpis.forsikring.source import calculate_reported_kpi


KPI_META = {
    "name": "Operating ratio",
    "industry": "Forsikring",
    "source_type": "reported",
    "source_code": "SA2806",
    "official_definition": "Combined ratio baseret på erstatnings-, omkostnings- og nettogenforsikringsprocenter, hvor allokeret investeringsafkast er lagt til præmieindtægter i nævneren.",
    "slug": "operating_ratio",
    "display_format": "percentage",
    "decimals": 1,
    "direction": "lower_is_better",
    "reading_guide": "95 % betyder 95 kr. i de samlede combined-ratio-komponenter pr. 100 kr. præmier, når allokeret investeringsafkast er lagt til præmieindtægterne i nævneren. Under 100 % er normalt gunstigt; tallet kan afvige fra combined ratio.",
    "formula_label": "Combined ratio med allokeret investeringsafkast lagt til præmieindtægterne i nævneren",
    "description": "Rapporteret operating ratio med allokeret investeringsafkast i nævneren.",
    "interpretation": "Viser combined ratio på et præmiegrundlag, der inkluderer allokeret investeringsafkast.",
    "direction_explanation": "Lavere er som udgangspunkt bedre.",
    "caveat": "Kan afvige fra combined ratio, fordi allokeret investeringsafkast indgår i nævneren. Værdien er rapporteret i Finanstilsynets kildedatasæt.",
}


def calculate(raw):
    return calculate_reported_kpi(raw, KPI_META["name"], "Operating ratio")

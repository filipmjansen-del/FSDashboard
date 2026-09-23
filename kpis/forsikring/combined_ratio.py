from kpis.forsikring.source import calculate_reported_kpi


KPI_META = {
    "name": "Combined ratio",
    "industry": "Forsikring",
    "source_type": "reported",
    "slug": "combined_ratio",
    "display_format": "percentage",
    "decimals": 1,
    "direction": "lower_is_better",
    "reading_guide": "95 % betyder, at erstatninger, drift og nettogenforsikring tilsammen svarer til 95 kr. pr. 100 kr. præmier. Under 100 % peger på overskud fra forsikringsdriften før investeringsafkast; over 100 % peger på underskud. Lavere er normalt gunstigt.",
    "formula_label": "Bruttoerstatningsprocent + bruttoomkostningsprocent + nettogenforsikringsprocent",
    "description": "Samlet forsikringsteknisk omkostningsforhold inklusive genforsikring.",
    "interpretation": "Under 100 % peger som udgangspunkt på overskud i den underliggende forsikringsdrift før investeringsafkast.",
    "direction_explanation": "Lavere er som udgangspunkt bedre.",
    "caveat": "Genforsikringsprocenten indgår særskilt; tallet er ikke blot summen af bruttoerstatnings- og bruttoomkostningsprocent. Værdien er rapporteret i kildedatasættet.",
}


def calculate(raw):
    return calculate_reported_kpi(raw, KPI_META["name"], "Combined ratio")

from kpis.forsikring.source import calculate_reported_kpi


KPI_META = {
    "name": "Bruttoomkostningsprocent",
    "industry": "Forsikring",
    "source_type": "reported",
    "source_code": "SA2804",
    "official_definition": "Forholdet mellem forsikringsmæssige driftsomkostninger og bruttopræmieindtægter efter bonus og præmierabatter.",
    "slug": "bruttoomkostningsprocent",
    "display_format": "percentage",
    "decimals": 1,
    "direction": "lower_is_better",
    "reading_guide": "17 % betyder 17 kr. forsikringsmæssige driftsomkostninger pr. 100 kr. bruttopræmier efter bonus og præmierabatter. Lavere er normalt gunstigt, men selskabernes salgskanaler og produktmix kan være forskellige.",
    "formula_label": "Forsikringsmæssige driftsomkostninger / bruttopræmieindtægter efter bonus og præmierabatter",
    "description": "Andelen af bruttopræmier, som går til forsikringsmæssig drift.",
    "interpretation": "17 % betyder, at driftsomkostningerne svarer til 17 % af præmieindtægterne efter bonus og præmierabatter.",
    "direction_explanation": "Lavere er som udgangspunkt bedre for omkostningseffektiviteten.",
    "caveat": "Værdien er rapporteret i Finanstilsynets kildedatasæt og genberegnes ikke fra råregnskabets kontokoder.",
}


def calculate(raw):
    return calculate_reported_kpi(raw, KPI_META["name"], "Bruttoomkostningsprocent (Expense ratio)")

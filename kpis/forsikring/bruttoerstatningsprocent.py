from kpis.forsikring.source import calculate_reported_kpi


KPI_META = {
    "name": "Bruttoerstatningsprocent",
    "industry": "Forsikring",
    "source_type": "reported",
    "slug": "bruttoerstatningsprocent",
    "display_format": "percentage",
    "decimals": 1,
    "direction": "lower_is_better",
    "reading_guide": "70 % betyder 70 kr. bruttoerstatninger pr. 100 kr. bruttopræmier efter bonus og præmierabatter. Lavere er normalt gunstigt; over 100 % overstiger erstatningerne alene præmierne, før drift og genforsikring.",
    "formula_label": "Bruttoerstatningsudgifter / bruttopræmieindtægter efter bonus og præmierabatter",
    "description": "Andelen af bruttopræmier, som går til erstatninger før genforsikring.",
    "interpretation": "70 % betyder, at bruttoerstatninger svarer til 70 % af præmieindtægterne efter bonus og præmierabatter.",
    "direction_explanation": "Lavere er som udgangspunkt bedre for forsikringsdriften.",
    "caveat": "Skadesår, reserveændringer og produktmix påvirker tallet. Værdien er rapporteret i kildedatasættet og genberegnes ikke fra råregnskabets kontokoder.",
}


def calculate(raw):
    return calculate_reported_kpi(raw, KPI_META["name"], "Bruttoerstatningsprocent (Loss ratio)")

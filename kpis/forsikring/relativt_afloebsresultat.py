from kpis.forsikring.source import calculate_reported_kpi


KPI_META = {
    "name": "Relativt afløbsresultat",
    "industry": "Forsikring",
    "source_type": "reported",
    "slug": "relativt_afloebsresultat",
    "display_format": "percentage",
    "decimals": 1,
    "direction": "neutral",
    "formula_label": "Afløbsresultat / relevante primohensættelser",
    "description": "Resultatet af afvikling af tidligere års skader i forhold til de tilhørende primohensættelser.",
    "interpretation": "Viser hvor meget de tidligere skadehensættelser har afveget fra det senere afløb.",
    "direction_explanation": "Fortegnet skal fortolkes i sammenhæng med reservemetoden og den konkrete skadebestand.",
    "caveat": "Påvirkes af valuta, diskontering og indirekte forsikring. Værdien er rapporteret i kildedatasættet.",
}


def calculate(raw):
    return calculate_reported_kpi(raw, KPI_META["name"], "Relativt afløbsresultat")

from kpis.common import calculate_ratio_kpi


KPI_META = {
    "name": "Indtjening pr. omkostningskrone",
    "industry": "Bank",
    "slug": "indtjening_pr_omkostningskrone",
    "display_format": "multiple",
    "decimals": 2,
    "direction": "higher_is_better",
    "formula_label": (
        "(Res_RGTot_RY + Res_Kreg_RY + Res_Xdi_RY + Res_Rat_RY) / "
        "(Res_UPa_RY + Res_ImMa_RY + Res_Xdu_RY + Res_UGn_RY)"
    ),
    "description": (
        "Måler hvor meget indtjening banken genererer for hver krone "
        "i omkostninger."
    ),
    "interpretation": (
        "Nøgletallet giver et samlet billede af bankens omkostningseffektivitet. "
        "En værdi på eksempelvis 1,50x betyder, at banken genererer 1,50 kr. "
        "i indtjening for hver 1,00 kr. i de omkostninger, der indgår i "
        "beregningen."
    ),
    "direction_explanation": (
        "Højere er som udgangspunkt bedre, fordi banken genererer mere "
        "indtjening pr. omkostningskrone."
    ),
    "caveat": (
        "Nøgletallet kan forbedres både gennem højere indtægter og lavere "
        "omkostninger. Midlertidige indtægter, eksempelvis kursreguleringer, "
        "kan derfor påvirke nøgletallet betydeligt. Det bør ses sammen med "
        "indtægtsmix og udviklingen i de underliggende omkostninger."
    ),
}


NUMERATOR = [
    "Res_RGTot_RY",
    "Res_Kreg_RY",
    "Res_Xdi_RY",
    "Res_Rat_RY",
]

DENOMINATOR = [
    "Res_UPa_RY",
    "Res_ImMa_RY",
    "Res_Xdu_RY",
    "Res_UGn_RY",
]


def calculate(raw):
    return calculate_ratio_kpi(
        raw=raw,
        industry=KPI_META["industry"],
        numerator_attributes=NUMERATOR,
        denominator_attributes=DENOMINATOR,
        kpi_name=KPI_META["name"],
    )

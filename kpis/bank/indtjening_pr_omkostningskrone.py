from kpis.common import calculate_ratio_kpi


KPI_META = {
    "name": "Indtjening pr. omkostningskrone",
    "industry": "Bank",
    "slug": "indtjening_pr_omkostningskrone",
    "display_format": "multiple",
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

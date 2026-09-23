import importlib
import pkgutil


INDUSTRY_PACKAGES = {
    "Bank": "bank",
    "Realkredit": "realkredit",
    "Forsikring": "forsikring",
    "Pension": "pension",
    "Tværgående pensionskasser": "tvaergaaende_pensionskasser",
}


KPI_REGISTRY = {}
METRIC_REGISTRY = {}
INDUSTRY_KPI_CATALOG = {
    industry: []
    for industry in INDUSTRY_PACKAGES
}
INDUSTRY_METRIC_CATALOG = {
    industry: []
    for industry in INDUSTRY_PACKAGES
}

METRIC_METADATA = {
    "Bank": {
        "Indtjening pr. omkostningskrone": ("bank.income_per_cost", "efficiency", "ratio", "multiple", "calculated", "baseline_tested"),
        "Egenkapitalforrentning før skat": ("bank.roe_pre_tax", "profitability", "ratio", "percentage", "calculated", "baseline_tested"),
        "Egenkapitalforrentning efter skat": ("bank.roe_after_tax", "profitability", "ratio", "percentage", "calculated", "baseline_tested"),
        "Udlån i forhold til egenkapital": ("bank.loans_to_equity", "balance_sheet", "ratio", "multiple", "calculated", "baseline_tested"),
    },
    "Forsikring": {
        "Bruttoerstatningsprocent": ("insurance.gross_claims_ratio", "risk", "ratio", "percentage", "reported", "baseline_tested"),
        "Bruttoomkostningsprocent": ("insurance.gross_expense_ratio", "efficiency", "ratio", "percentage", "reported", "baseline_tested"),
        "Combined ratio": ("insurance.combined_ratio", "profitability", "ratio", "percentage", "reported", "baseline_tested"),
        "Operating ratio": ("insurance.operating_ratio", "profitability", "ratio", "percentage", "reported", "baseline_tested"),
        "Relativt afløbsresultat": ("insurance.relative_runoff_result", "risk", "ratio", "percentage", "reported", "baseline_tested"),
        "Egenkapitalforrentning i procent": ("insurance.roe", "profitability", "ratio", "percentage", "reported", "baseline_tested"),
    },
}


def _build_formula_label(module):
    """
    Creates a readable formula label automatically for ratio KPIs
    if NUMERATOR and DENOMINATOR are defined in the KPI module.
    """
    numerator = getattr(module, "NUMERATOR", None)
    denominator = getattr(module, "DENOMINATOR", None)

    if numerator and denominator:
        numerator_text = " + ".join(numerator)
        denominator_text = " + ".join(denominator)

        return (
            f"({numerator_text})\n"
            f"/\n"
            f"({denominator_text})"
        )

    return "Formula definition not provided."


def _discover_kpis():
    for industry, package_name in INDUSTRY_PACKAGES.items():

        package = importlib.import_module(
            f"kpis.{package_name}"
        )

        for module_info in pkgutil.iter_modules(
            package.__path__
        ):
            if module_info.name.startswith("_"):
                continue

            module = importlib.import_module(
                f"kpis.{package_name}.{module_info.name}"
            )

            if not hasattr(module, "KPI_META"):
                continue

            if not hasattr(module, "calculate"):
                continue

            meta = dict(module.KPI_META)

            kpi_name = meta["name"]
            try:
                metric_id, category, metric_type, unit, calculation_type, validation_status = (
                    METRIC_METADATA[industry][kpi_name]
                )
            except KeyError as error:
                raise ValueError(f"Missing metric metadata for {industry}: {kpi_name}") from error

            if metric_id in METRIC_REGISTRY:
                raise ValueError(f"Duplicate metric ID: {metric_id}")

            meta.update(
                {
                    "metric_id": metric_id,
                    "market": industry,
                    "display_name": kpi_name,
                    "category": category,
                    "metric_type": metric_type,
                    "unit": unit,
                    "source_type": meta.get("source_type", "financial_services_long"),
                    "calculation_type": calculation_type,
                    "validation_status": validation_status,
                }
            )

            if "formula_label" not in meta:
                meta["formula_label"] = _build_formula_label(
                    module
                )

            meta["calculate"] = module.calculate

            KPI_REGISTRY[kpi_name] = meta
            METRIC_REGISTRY[metric_id] = meta

            INDUSTRY_KPI_CATALOG[industry].append(
                kpi_name
            )
            INDUSTRY_METRIC_CATALOG[industry].append(metric_id)

    for industry in INDUSTRY_KPI_CATALOG:
        INDUSTRY_KPI_CATALOG[industry] = sorted(
            INDUSTRY_KPI_CATALOG[industry]
        )
        INDUSTRY_METRIC_CATALOG[industry] = sorted(INDUSTRY_METRIC_CATALOG[industry])


_discover_kpis()


def calculate_kpi(raw_data, kpi_identifier):
    """Calculate by stable metric ID or legacy display name."""
    registry = METRIC_REGISTRY if kpi_identifier in METRIC_REGISTRY else KPI_REGISTRY
    if kpi_identifier not in registry:
        raise KeyError(
            f"KPI '{kpi_identifier}' was not found."
        )

    return registry[kpi_identifier]["calculate"](
        raw_data
    )

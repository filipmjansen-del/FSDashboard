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
INDUSTRY_KPI_CATALOG = {
    industry: []
    for industry in INDUSTRY_PACKAGES
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

            if "formula_label" not in meta:
                meta["formula_label"] = _build_formula_label(
                    module
                )

            meta["calculate"] = module.calculate

            KPI_REGISTRY[kpi_name] = meta

            INDUSTRY_KPI_CATALOG[industry].append(
                kpi_name
            )

    for industry in INDUSTRY_KPI_CATALOG:
        INDUSTRY_KPI_CATALOG[industry] = sorted(
            INDUSTRY_KPI_CATALOG[industry]
        )


_discover_kpis()


def calculate_kpi(raw_data, kpi_name):
    if kpi_name not in KPI_REGISTRY:
        raise KeyError(
            f"KPI '{kpi_name}' was not found."
        )

    return KPI_REGISTRY[kpi_name]["calculate"](
        raw_data
    )

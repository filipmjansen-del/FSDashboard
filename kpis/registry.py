import importlib
import pkgutil

import kpis


INDUSTRIES = [
    "Bank",
    "Realkredit",
    "Forsikring",
    "Pension",
    "Tværgående pensionskasser",
]

PACKAGE_TO_INDUSTRY = {
    "bank": "Bank",
    "realkredit": "Realkredit",
    "forsikring": "Forsikring",
    "pension": "Pension",
    "tvaergaaende_pensionskasser": "Tværgående pensionskasser",
}


def discover_kpis():
    discovered = []

    for package_name, industry in PACKAGE_TO_INDUSTRY.items():
        package = importlib.import_module(f"kpis.{package_name}")

        for module_info in pkgutil.iter_modules(package.__path__):
            if module_info.name.startswith("_"):
                continue

            module = importlib.import_module(
                f"kpis.{package_name}.{module_info.name}"
            )

            if not hasattr(module, "KPI_META"):
                continue

            if not hasattr(module, "calculate"):
                continue

            discovered.append(
                {
                    **module.KPI_META,
                    "calculate": module.calculate,
                }
            )

    return discovered


def get_kpis_by_industry():
    result = {industry: [] for industry in INDUSTRIES}

    for kpi in discover_kpis():
        result[kpi["industry"]].append(kpi)

    for industry in result:
        result[industry] = sorted(
            result[industry],
            key=lambda x: x["name"],
        )

    return result

import importlib
import pkgutil


INDUSTRY_PACKAGES = {
    "Bank": "bank",
    "Realkredit": "realkredit",
    "Forsikring": "forsikring",
    "Pension": "pension",
    "Tværgående pensionskasser": "tvaergaaende_pensionskasser",
}

CROSS_CUTTING_DASHBOARD_PACKAGES = {
    "Client Intelligence": "client_intelligence",
}


DASHBOARD_REGISTRY = {}

INDUSTRY_DASHBOARD_CATALOG = {
    industry: []
    for industry in INDUSTRY_PACKAGES
}

CROSS_CUTTING_DASHBOARD_CATALOG = {
    section: []
    for section in CROSS_CUTTING_DASHBOARD_PACKAGES
}


def _discover_dashboards():
    catalogs = (
        (INDUSTRY_PACKAGES, INDUSTRY_DASHBOARD_CATALOG),
        (CROSS_CUTTING_DASHBOARD_PACKAGES, CROSS_CUTTING_DASHBOARD_CATALOG),
    )
    for packages, catalog in catalogs:
        for section, package_name in packages.items():
            try:
                package = importlib.import_module(
                    f"dashboards.{package_name}"
                )
            except ModuleNotFoundError:
                continue

            for module_info in pkgutil.iter_modules(
                package.__path__
            ):
                if module_info.name.startswith("_"):
                    continue

                module = importlib.import_module(
                    f"dashboards.{package_name}.{module_info.name}"
                )

                if not hasattr(module, "DASHBOARD_META"):
                    continue

                if not hasattr(module, "render"):
                    continue

                meta = dict(module.DASHBOARD_META)

                dashboard_name = meta["name"]

                meta["render"] = module.render

                DASHBOARD_REGISTRY[dashboard_name] = meta

                catalog[section].append(
                    dashboard_name
                )

    for section in INDUSTRY_DASHBOARD_CATALOG:
        INDUSTRY_DASHBOARD_CATALOG[section] = sorted(INDUSTRY_DASHBOARD_CATALOG[section])
    for section in CROSS_CUTTING_DASHBOARD_CATALOG:
        CROSS_CUTTING_DASHBOARD_CATALOG[section] = sorted(
            CROSS_CUTTING_DASHBOARD_CATALOG[section],
            key=lambda name: DASHBOARD_REGISTRY[name].get("order", 999),
        )


_discover_dashboards()


def render_dashboard(raw_data, dashboard_name):
    if dashboard_name not in DASHBOARD_REGISTRY:
        raise KeyError(
            f"Dashboard '{dashboard_name}' was not found."
        )

    DASHBOARD_REGISTRY[dashboard_name]["render"](
        raw_data
    )

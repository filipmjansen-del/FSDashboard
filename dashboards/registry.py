import importlib
import pkgutil


INDUSTRY_PACKAGES = {
    "Bank": "bank",
    "Realkredit": "realkredit",
    "Forsikring": "forsikring",
    "Pension": "pension",
    "Tværgående pensionskasser": "tvaergaaende_pensionskasser",
}


DASHBOARD_REGISTRY = {}

INDUSTRY_DASHBOARD_CATALOG = {
    industry: []
    for industry in INDUSTRY_PACKAGES
}


def _discover_dashboards():
    for industry, package_name in INDUSTRY_PACKAGES.items():
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

            INDUSTRY_DASHBOARD_CATALOG[industry].append(
                dashboard_name
            )

    for industry in INDUSTRY_DASHBOARD_CATALOG:
        INDUSTRY_DASHBOARD_CATALOG[industry] = sorted(
            INDUSTRY_DASHBOARD_CATALOG[industry]
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

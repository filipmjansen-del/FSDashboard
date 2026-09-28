"""Dashboard workspace rendering."""

from dashboards.registry import DASHBOARD_REGISTRY, render_dashboard


def render_dashboard_workspace(industry: str, dashboard_name: str, get_raw_data):
    if dashboard_name not in DASHBOARD_REGISTRY:
        raise KeyError(f"Dashboard '{dashboard_name}' was not found.")
    render_dashboard(get_raw_data(), dashboard_name)

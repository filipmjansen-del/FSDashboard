"""Client Intelligence opportunities shell."""

from dashboards.client_intelligence._shared import render_shell


DASHBOARD_META = {"name": "Opportunities", "description": "Mock opportunities workspace."}


def render(_raw_data):
    render_shell("Opportunities", "Mock/placeholder workspace for AL Sydbank commercial hypotheses.")

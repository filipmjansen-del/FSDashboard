"""Client Intelligence strategy and signals shell."""

from dashboards.client_intelligence._shared import render_shell


DASHBOARD_META = {"name": "Strategy & Signals", "description": "Mock strategy and signals workspace."}


def render(_raw_data):
    render_shell("Strategy & Signals", "Mock/placeholder workspace for AL Sydbank strategy and signals.")

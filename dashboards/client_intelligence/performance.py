"""Client Intelligence performance shell."""

from dashboards.client_intelligence._shared import render_shell


DASHBOARD_META = {"name": "Performance", "description": "Mock performance workspace."}


def render(_raw_data):
    render_shell("Performance", "Mock/placeholder workspace for AL Sydbank performance context.")

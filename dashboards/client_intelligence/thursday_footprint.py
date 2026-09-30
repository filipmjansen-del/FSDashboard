"""Client Intelligence Thursday footprint shell."""

from dashboards.client_intelligence._shared import render_shell


DASHBOARD_META = {"name": "Thursday Footprint", "description": "Mock Thursday footprint workspace."}


def render(_raw_data):
    render_shell("Thursday Footprint", "Mock/placeholder workspace for AL Sydbank Thursday knowledge.")

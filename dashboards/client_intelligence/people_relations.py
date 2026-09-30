"""Client Intelligence people and relations shell."""

from dashboards.client_intelligence._shared import render_shell


DASHBOARD_META = {"name": "People & Relations", "description": "Mock people and relations workspace."}


def render(_raw_data):
    render_shell("People & Relations", "Mock/placeholder workspace for AL Sydbank people and relations.")

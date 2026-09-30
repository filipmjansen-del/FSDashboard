"""Client Intelligence strategy and signals shell."""

from dashboards.client_intelligence._shared import render_items, render_not_connected, render_shell
from dashboards.client_intelligence.content import MERGER_FACTS


DASHBOARD_META = {"name": "Strategy & Signals", "description": "Mock strategy and signals workspace."}


def render(_raw_data):
    render_shell("Strategy & Signals", "Documented merger and integration signals for the AL Sydbank MVP.")
    render_items(MERGER_FACTS)
    render_not_connected("Documented AL Sydbank strategic priorities")

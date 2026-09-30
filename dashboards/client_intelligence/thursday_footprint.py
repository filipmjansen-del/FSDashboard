"""Client Intelligence Thursday footprint shell."""

from dashboards.client_intelligence._shared import render_items, render_shell
from dashboards.client_intelligence.content import THURSDAY_PERSPECTIVES


DASHBOARD_META = {"name": "Thursday Footprint", "description": "Mock Thursday footprint workspace."}


def render(_raw_data):
    render_shell("Thursday Footprint", "Thursday perspectives from the AL Sydbank benchmarking material.")
    render_items(THURSDAY_PERSPECTIVES)

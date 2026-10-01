"""Client Intelligence chat shell."""

from dashboards.client_intelligence._shared import render_not_connected, render_shell


DASHBOARD_META = {"name": "Chat", "description": "Future chat workspace.", "order": 70}


def render(_raw_data):
    render_shell("Chat", "Chat workspace boundary for the AL Sydbank MVP.")
    render_not_connected("AI or chat functionality")

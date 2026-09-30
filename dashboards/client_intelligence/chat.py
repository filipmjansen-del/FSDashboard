"""Client Intelligence chat shell."""

from dashboards.client_intelligence._shared import render_shell


DASHBOARD_META = {"name": "Chat", "description": "Mock chat workspace."}


def render(_raw_data):
    render_shell("Chat", "Mock/placeholder chat workspace. No AI or chat functionality is implemented.")

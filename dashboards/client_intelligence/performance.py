"""Client Intelligence performance shell."""

from dashboards.client_intelligence._shared import render_not_connected, render_shell


DASHBOARD_META = {"name": "Performance", "description": "Existing Databank performance analysis entry point.", "order": 20}


def render(_raw_data):
    render_shell("Performance", "Performance context for AL Sydbank, reusing the existing Databank analysis.")
    render_not_connected(
        "A Client Intelligence performance view. Use Bank → Bank Analyst View for the existing AL Sydbank financial analysis."
    )

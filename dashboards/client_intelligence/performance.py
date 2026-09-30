"""Client Intelligence performance shell."""

from dashboards.client_intelligence._shared import (
    render_compact_card,
    render_shell,
    render_status_label,
)


DASHBOARD_META = {"name": "Performance", "description": "Existing Databank performance analysis entry point.", "order": 20}


def render(_raw_data):
    render_shell("Performance", "Existing Databank financial analysis for AL Sydbank.")
    render_compact_card(
        "Bank Analyst View",
        "Inspect validated financial KPIs, peer benchmarking, and historical development in Bank → Bank Analyst View.",
        label="Existing Databank analysis",
    )
    render_status_label("No Client Intelligence financial calculation is duplicated here.")

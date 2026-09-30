"""Client Intelligence opportunities shell."""

from dashboards.client_intelligence._shared import render_hypothesis, render_shell
from dashboards.client_intelligence.content import COMMERCIAL_HYPOTHESES


DASHBOARD_META = {"name": "Opportunities", "description": "Qualified AL Sydbank commercial hypotheses.", "order": 60}


def render(_raw_data):
    render_shell("Opportunities", "Three hypotheses for validation; none is a confirmed client need.")
    for hypothesis in COMMERCIAL_HYPOTHESES:
        render_hypothesis(hypothesis)

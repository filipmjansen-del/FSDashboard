import unittest
from types import SimpleNamespace
from unittest.mock import patch

from dashboards.client_intelligence import overview
from dashboards.client_intelligence import (
    chat,
    opportunities,
    people_relations,
    performance,
    strategy_signals,
    thursday_footprint,
)
from dashboards.registry import (
    CROSS_CUTTING_DASHBOARD_CATALOG,
    DASHBOARD_REGISTRY,
    INDUSTRY_DASHBOARD_CATALOG,
)
from navigation import sidebar


VIEW_NAMES = {
    "Overview",
    "Performance",
    "Strategy & Signals",
    "People & Relations",
    "Thursday Footprint",
    "Opportunities",
    "Chat",
}


class ClientIntelligenceDashboardTests(unittest.TestCase):
    def test_seven_views_are_discovered_as_a_cross_cutting_section(self):
        self.assertEqual(set(CROSS_CUTTING_DASHBOARD_CATALOG["Client Intelligence"]), VIEW_NAMES)
        self.assertTrue(VIEW_NAMES.isdisjoint(INDUSTRY_DASHBOARD_CATALOG))
        for name in VIEW_NAMES:
            self.assertTrue(callable(DASHBOARD_REGISTRY[name]["render"]))

    def test_cross_cutting_navigation_does_not_create_an_industry(self):
        self.assertNotIn("Client Intelligence", sidebar.all_industries())

    def test_cross_cutting_view_navigation_has_no_industry(self):
        streamlit_stub = SimpleNamespace(session_state=SimpleNamespace(), rerun=lambda: None)
        with patch("navigation.sidebar.st", streamlit_stub):
            sidebar.navigate_to(None, "dashboard", "Overview")
        self.assertIsNone(streamlit_stub.session_state.selected_industry)
        self.assertEqual(streamlit_stub.session_state.selected_view_type, "dashboard")
        self.assertEqual(streamlit_stub.session_state.selected_view_name, "Overview")

    def test_each_view_renderer_runs_with_presentation_components(self):
        renderers = [
            overview.render,
            performance.render,
            strategy_signals.render,
            people_relations.render,
            thursday_footprint.render,
            opportunities.render,
            chat.render,
        ]
        with (
            patch("dashboards.client_intelligence.overview.render_page_intro"),
            patch("dashboards.client_intelligence.overview.render_pilot_notice"),
            patch("dashboards.client_intelligence.overview.render_section_intro"),
            patch("dashboards.client_intelligence.overview.render_kpi_cards"),
            patch("dashboards.client_intelligence.overview.render_orientation_card"),
            patch("dashboards.client_intelligence._shared.render_page_intro"),
            patch("dashboards.client_intelligence._shared.render_pilot_notice"),
            patch("dashboards.client_intelligence._shared.render_orientation_card"),
        ):
            for renderer in renderers:
                renderer(None)

    def test_overview_contains_the_required_sections(self):
        with (
            patch("dashboards.client_intelligence.overview.render_page_intro"),
            patch("dashboards.client_intelligence.overview.render_pilot_notice"),
            patch("dashboards.client_intelligence.overview.render_kpi_cards"),
            patch("dashboards.client_intelligence.overview.render_orientation_card"),
            patch("dashboards.client_intelligence.overview.render_section_intro") as section_intro,
        ):
            overview.render(None)
        self.assertEqual(
            [call.args[0] for call in section_intro.call_args_list],
            [
                "Company snapshot",
                "What changed?",
                "Performance snapshot",
                "Strategic priorities",
                "Key people & relations",
                "Thursday footprint",
                "Commercial hypotheses",
            ],
        )


if __name__ == "__main__":
    unittest.main()

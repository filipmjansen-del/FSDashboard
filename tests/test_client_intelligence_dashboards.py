import unittest
from types import SimpleNamespace
from unittest.mock import patch

from dashboards.client_intelligence import overview
from dashboards.client_intelligence import _shared
from dashboards.client_intelligence import (
    chat,
    opportunities,
    people_relations,
    performance,
    strategy_signals,
    thursday_footprint,
)
from dashboards.client_intelligence.content import (
    COMMERCIAL_HYPOTHESES,
    CUSTOMER_PROPOSITION_SIGNAL,
    H1_2026_SOURCE_URL,
    INTERNAL_ACCOUNT_MAPPING,
    PILOT_CONTEXT,
    PUBLIC_EXECUTIVES,
    STRATEGIC_POSITIONING_SIGNAL,
    MERGER_FACTS,
    THURSDAY_PERSPECTIVES,
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
        self.assertEqual(
            CROSS_CUTTING_DASHBOARD_CATALOG["Client Intelligence"],
            ["Overview", "Performance", "Strategy & Signals", "People & Relations", "Thursday Footprint", "Opportunities", "Chat"],
        )
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
            patch("dashboards.client_intelligence.overview.render_items"),
            patch("dashboards.client_intelligence.overview.render_item"),
            patch("dashboards.client_intelligence.overview.render_hypothesis"),
            patch("dashboards.client_intelligence.overview.st"),
            patch("dashboards.client_intelligence._shared.render_page_intro"),
            patch("dashboards.client_intelligence._shared.render_pilot_notice"),
            patch("dashboards.client_intelligence._shared.render_orientation_card"),
            patch("dashboards.client_intelligence._shared.st"),
            patch("dashboards.client_intelligence.people_relations.st"),
        ):
            for renderer in renderers:
                renderer(None)

    def test_overview_contains_the_required_sections(self):
        with (
            patch("dashboards.client_intelligence.overview.render_page_intro"),
            patch("dashboards.client_intelligence.overview.render_pilot_notice"),
            patch("dashboards.client_intelligence.overview.render_kpi_cards"),
            patch("dashboards.client_intelligence.overview.render_items"),
            patch("dashboards.client_intelligence.overview.render_item"),
            patch("dashboards.client_intelligence.overview.st"),
            patch("dashboards.client_intelligence.overview.render_section_intro") as section_intro,
        ):
            overview.render(None)
        self.assertEqual(
            [call.args[0] for call in section_intro.call_args_list],
            [
                "Company snapshot",
                "Performance snapshot",
                "Key signals",
                "People & relations",
                "Thursday footprint",
                "Opportunities",
            ],
        )

    def test_manual_content_keeps_facts_perspectives_and_hypotheses_distinct(self):
        self.assertTrue(MERGER_FACTS)
        self.assertTrue(THURSDAY_PERSPECTIVES)
        self.assertTrue(COMMERCIAL_HYPOTHESES)
        for fact in MERGER_FACTS:
            self.assertEqual(fact.information_type, "Fact")
            self.assertEqual(fact.source.publisher, "AL Sydbank A/S")
            self.assertEqual(fact.source.title, "Delårsrapport - 1. halvår 2026")
            self.assertEqual(fact.source.publication_date, "26 August 2026")
            self.assertEqual(fact.source.source_type, "Official company reporting")
            self.assertIn(fact.source.page_reference, {"Page 30", "Page 46"})
            self.assertEqual(fact.source.url, H1_2026_SOURCE_URL)
            self.assertTrue(fact.period)
        for perspective in THURSDAY_PERSPECTIVES:
            self.assertEqual(perspective.information_type, "Thursday perspective")
            self.assertTrue(perspective.source.title)
            self.assertTrue(perspective.period)
        for hypothesis in COMMERCIAL_HYPOTHESES:
            self.assertTrue(hypothesis.evidence)
            self.assertTrue(hypothesis.observation)
            self.assertTrue(hypothesis.potential_need)
            self.assertTrue(hypothesis.thursday_relevance)
            self.assertTrue(hypothesis.period)
            self.assertTrue(hypothesis.sources)
            self.assertTrue(all(source.title for source in hypothesis.sources))

    def test_pilot_context_uses_the_existing_validated_bank_identity(self):
        self.assertEqual(PILOT_CONTEXT.display_name, "AL Sydbank")
        self.assertEqual(PILOT_CONTEXT.latest_reporting_label, "H1 2026")
        self.assertEqual(PILOT_CONTEXT.legal_entity_reference, "bank:8079")
        self.assertEqual(PILOT_CONTEXT.regnr, "8079")

    def test_evidence_renderer_exposes_official_source_metadata(self):
        with patch("dashboards.client_intelligence._shared.st") as streamlit_stub:
            _shared.render_item(MERGER_FACTS[0])
        captions = [call.args[0] for call in streamlit_stub.caption.call_args_list]
        self.assertIn("Fact · H1 2026", captions)
        self.assertIn("Source title: Delårsrapport - 1. halvår 2026", captions)
        self.assertIn("Publisher: AL Sydbank A/S · Publication date: 26 August 2026", captions)
        self.assertIn("Page reference: Page 30 · Source type: Official company reporting", captions)
        streamlit_stub.markdown.assert_any_call(f"[Open source]({H1_2026_SOURCE_URL})")

    def test_hypothesis_renderer_shows_observation_and_structured_sources(self):
        with patch("dashboards.client_intelligence._shared.st") as streamlit_stub:
            _shared.render_hypothesis(COMMERCIAL_HYPOTHESES[0])
        writes = [call.args[0] for call in streamlit_stub.write.call_args_list]
        self.assertIn(f"**Observation:** {COMMERCIAL_HYPOTHESES[0].observation}", writes)
        captions = [call.args[0] for call in streamlit_stub.caption.call_args_list]
        self.assertIn("Hypothesis - requires client validation", captions)
        streamlit_stub.markdown.assert_any_call(f"[Open source]({H1_2026_SOURCE_URL})")

    def test_overview_renders_manual_evidence_and_thursday_content(self):
        with (
            patch("dashboards.client_intelligence.overview.render_page_intro"),
            patch("dashboards.client_intelligence.overview.render_pilot_notice"),
            patch("dashboards.client_intelligence.overview.render_kpi_cards"),
            patch("dashboards.client_intelligence.overview.render_section_intro"),
            patch("dashboards.client_intelligence.overview.render_item"),
            patch("dashboards.client_intelligence.overview.render_hypothesis"),
            patch("dashboards.client_intelligence.overview.st"),
            patch("dashboards.client_intelligence.overview.render_items") as render_items,
        ):
            overview.render(None)
        self.assertEqual(
            [call.args[0] for call in render_items.call_args_list],
            [THURSDAY_PERSPECTIVES],
        )

    def test_demo_content_uses_public_sources_and_safe_internal_labels(self):
        self.assertEqual(
            CUSTOMER_PROPOSITION_SIGNAL.source.url,
            "https://www.al-sydbank.dk/nyt/farvel-til-gebyr",
        )
        self.assertEqual(
            STRATEGIC_POSITIONING_SIGNAL.source.url,
            "https://www.al-sydbank.dk/nyt/fusionen-til-al-sydbank-er-nu-en-realitet",
        )
        self.assertEqual(len(PUBLIC_EXECUTIVES), 5)
        self.assertTrue(all("Account mapping available" in item for item in INTERNAL_ACCOUNT_MAPPING))
        self.assertEqual(
            [hypothesis.title for hypothesis in COMMERCIAL_HYPOTHESES],
            [
                "Merger integration and synergy realisation",
                "Customer and service model",
                "Digital & platform enablement",
            ],
        )
        self.assertTrue(all(hypothesis.sources for hypothesis in COMMERCIAL_HYPOTHESES))


if __name__ == "__main__":
    unittest.main()

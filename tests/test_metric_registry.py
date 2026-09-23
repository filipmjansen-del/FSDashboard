import unittest

from kpis.registry import INDUSTRY_METRIC_CATALOG, KPI_REGISTRY, METRIC_REGISTRY, get_metric_metadata


class MetricRegistryTests(unittest.TestCase):
    def test_active_metrics_have_complete_stable_metadata(self):
        required = {
            "metric_id", "market", "display_name", "display_format", "category", "metric_type", "unit",
            "direction", "source_type", "calculation_type", "validation_status",
            "description", "interpretation", "caveat",
        }

        self.assertEqual(len(METRIC_REGISTRY), len(KPI_REGISTRY))
        self.assertEqual(len(METRIC_REGISTRY), len(set(METRIC_REGISTRY)))
        for metric_id, metadata in METRIC_REGISTRY.items():
            with self.subTest(metric_id=metric_id):
                self.assertTrue(metric_id.startswith(("bank.", "insurance.")))
                self.assertTrue(required.issubset(metadata))
        self.assertIn("bank.roe_pre_tax", INDUSTRY_METRIC_CATALOG["Bank"])
        self.assertIn("insurance.combined_ratio", INDUSTRY_METRIC_CATALOG["Forsikring"])

    def test_stable_id_resolves_to_the_legacy_workspace_metadata(self):
        self.assertEqual(
            get_metric_metadata("bank.roe_pre_tax"),
            get_metric_metadata("Egenkapitalforrentning før skat"),
        )

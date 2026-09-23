from pathlib import Path
import unittest

from dashboards.bank.peerheatmap import _relative_percentile, build_heatmap_data
from data_loader import load_raw_data
from kpis.registry import KPI_REGISTRY, calculate_kpi


class PeerHeatmapRegressionTests(unittest.TestCase):
    def test_directional_values_are_preserved_and_neutral_has_no_performance_percentile(self):
        raw = load_raw_data(Path(__file__).parents[1] / "financial_services_long.xlsx")
        actual, percentiles = build_heatmap_data(
            raw, KPI_REGISTRY, calculate_kpi, 2025,
            ["Egenkapitalforrentning før skat", "Udlån i forhold til egenkapital"],
        )

        self.assertEqual(actual.shape[0], 44)
        self.assertAlmostEqual(actual["Egenkapitalforrentning før skat"].sum(), 3.7202399124)
        self.assertTrue(percentiles["Egenkapitalforrentning før skat"].notna().any())
        self.assertTrue(percentiles["Udlån i forhold til egenkapital"].isna().all())

    def test_neutral_direction_has_no_percentile(self):
        self.assertTrue(_relative_percentile([1, 2, 3], "neutral").isna().all())

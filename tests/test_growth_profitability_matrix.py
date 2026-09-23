from pathlib import Path
import unittest

from dashboards.bank.vækstvsprofitabillitet import build_matrix_data
from data_loader import load_raw_data
from kpis.registry import KPI_REGISTRY, calculate_kpi


class GrowthProfitabilityRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = load_raw_data(Path(__file__).parents[1] / "financial_services_long.xlsx")

    def test_baseline_matrix_output_is_preserved_when_joining_on_regnr(self):
        matrix = build_matrix_data(
            self.raw, calculate_kpi, "Egenkapitalforrentning før skat", "Aktivvækst", 2025
        )

        self.assertEqual(len(matrix), 44)
        self.assertAlmostEqual(matrix["Growth"].sum(), 4.4000761172)
        self.assertAlmostEqual(matrix["Profitability"].sum(), 3.7202399124)
        self.assertAlmostEqual(matrix["Assets"].sum(), 3_972_555_885.0)

    def test_only_profitability_metrics_are_eligible_for_profitability_selection(self):
        eligible = {
            name for name, meta in KPI_REGISTRY.items()
            if meta.get("industry") == "Bank" and meta.get("category") == "profitability"
        }

        self.assertEqual(eligible, {"Egenkapitalforrentning før skat", "Egenkapitalforrentning efter skat"})

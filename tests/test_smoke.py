from pathlib import Path
import unittest

from data_loader import load_raw_data
from dashboards.registry import DASHBOARD_REGISTRY
from kpis.registry import KPI_REGISTRY


class BaselineSmokeTests(unittest.TestCase):
    def test_data_loader_and_registries_load(self):
        raw = load_raw_data(Path(__file__).parents[1] / "financial_services_long.xlsx")

        self.assertFalse(raw.empty)
        self.assertTrue(KPI_REGISTRY)
        self.assertTrue(DASHBOARD_REGISTRY)

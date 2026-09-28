import unittest

from dashboards.registry import DASHBOARD_REGISTRY, INDUSTRY_DASHBOARD_CATALOG


class InsuranceMarketStructureDashboardTests(unittest.TestCase):
    def test_market_structure_dashboard_is_registered_under_insurance(self):
        name = "Forsikringsmarkedets struktur"

        self.assertIn(name, INDUSTRY_DASHBOARD_CATALOG["Forsikring"])
        self.assertIn(name, DASHBOARD_REGISTRY)
        self.assertTrue(callable(DASHBOARD_REGISTRY[name]["render"]))


if __name__ == "__main__":
    unittest.main()

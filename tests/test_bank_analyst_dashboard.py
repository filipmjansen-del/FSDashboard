import unittest

from dashboards.registry import DASHBOARD_REGISTRY, INDUSTRY_DASHBOARD_CATALOG


class BankAnalystDashboardTests(unittest.TestCase):
    def test_bank_analyst_view_is_registered(self):
        self.assertIn("Bank Analyst View", INDUSTRY_DASHBOARD_CATALOG["Bank"])
        self.assertTrue(callable(DASHBOARD_REGISTRY["Bank Analyst View"]["render"]))


if __name__ == "__main__":
    unittest.main()

import unittest

import pandas as pd

from kpis.forsikring.source import SOURCE
from kpis.registry import INDUSTRY_KPI_CATALOG, calculate_kpi


class InsuranceKpiTests(unittest.TestCase):
    def test_official_catalog_uses_reported_company_values(self):
        names = INDUSTRY_KPI_CATALOG["Forsikring"]
        self.assertEqual(len(names), 6)
        source = pd.read_csv(SOURCE)
        self.assertEqual(len(source), 3279)
        self.assertFalse(source["navn"].str.startswith("XX -").any())
        self.assertFalse(source.duplicated(["ÅR", "regnr", "Attribute"]).any())

        for name in names:
            with self.subTest(name=name):
                result = calculate_kpi(pd.DataFrame(), name)
                self.assertFalse(result.empty)
                self.assertTrue(result["ÅR"].between(2016, 2025).all())
                self.assertTrue(result["regnr"].notna().all())
                self.assertEqual(result["KPI"].nunique(), 1)
                self.assertTrue(result["KPI_Value"].notna().any())

    def test_reported_percentages_are_stored_as_decimal_ratios(self):
        result = calculate_kpi(pd.DataFrame(), "Bruttoerstatningsprocent")
        row = result.loc[(result["ÅR"] == 2016) & (result["regnr"] == 50018)].iloc[0]
        self.assertEqual(row["Value"], 194.0)
        self.assertAlmostEqual(row["KPI_Value"], 1.94)

    def test_combined_ratio_keeps_reported_reinsurance_component(self):
        claims = calculate_kpi(pd.DataFrame(), "Bruttoerstatningsprocent")
        expenses = calculate_kpi(pd.DataFrame(), "Bruttoomkostningsprocent")
        combined = calculate_kpi(pd.DataFrame(), "Combined ratio")
        key = ["ÅR", "regnr"]
        joined = claims[key + ["KPI_Value"]].merge(
            expenses[key + ["KPI_Value"]], on=key, suffixes=("_claims", "_expenses")
        ).merge(combined[key + ["KPI_Value"]], on=key)
        difference = (
            joined["KPI_Value"]
            - joined["KPI_Value_claims"]
            - joined["KPI_Value_expenses"]
        ).abs()
        self.assertTrue((difference > 0.01).any())


if __name__ == "__main__":
    unittest.main()

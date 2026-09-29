import unittest

import pandas as pd

from kpis.forsikring.source import SOURCE
from kpis.registry import INDUSTRY_KPI_CATALOG, calculate_kpi, get_metric_metadata


class InsuranceKpiTests(unittest.TestCase):
    EXPECTED_ATTRIBUTES = {
        "Bruttoerstatningsprocent (Loss ratio)",
        "Bruttoomkostningsprocent (Expense ratio)",
        "Combined ratio",
        "Operating ratio",
        "Relativt afløbsresultat",
        "Egenkapitalforrentning i pct. (Return on equity)",
    }

    def test_official_catalog_uses_reported_company_values(self):
        names = INDUSTRY_KPI_CATALOG["Forsikring"]
        self.assertEqual(len(names), 6)
        source = pd.read_csv(SOURCE)
        self.assertEqual(len(source), 3279)
        self.assertFalse(source["navn"].str.startswith("XX -").any())
        self.assertFalse((source["regnr"] < 0).any())
        self.assertEqual(set(source["Attribute"]), self.EXPECTED_ATTRIBUTES)
        self.assertTrue(source["ÅR"].between(2016, 2025).all())
        self.assertEqual(set(source["ÅR"]), set(range(2016, 2026)))
        self.assertFalse(source.duplicated(["ÅR", "Måned", "regnr", "Attribute"]).any())
        self.assertEqual(source["Value"].isna().sum(), 20)

        for name in names:
            with self.subTest(name=name):
                result = calculate_kpi(pd.DataFrame(), name)
                self.assertFalse(result.empty)
                self.assertTrue(result["ÅR"].between(2016, 2025).all())
                self.assertTrue(result["regnr"].notna().all())
                self.assertEqual(result["KPI"].nunique(), 1)
                self.assertTrue(result["KPI_Value"].notna().any())

    def test_corrected_source_regression_observations_and_metadata(self):
        source = pd.read_csv(SOURCE)
        expected = {
            (2016, 50018, "Combined ratio"): 225.0,
            (2020, 53070, "Operating ratio"): 85.0,
            (2025, 50167, "Combined ratio"): 95.0,
            (2025, 53070, "Egenkapitalforrentning i pct. (Return on equity)"): 14.1,
        }
        for (year, regnr, attribute), value in expected.items():
            with self.subTest(year=year, regnr=regnr, attribute=attribute):
                actual = source.loc[
                    (source["ÅR"] == year)
                    & (source["regnr"] == regnr)
                    & (source["Attribute"] == attribute),
                    "Value",
                ].iloc[0]
                self.assertEqual(actual, value)

        missing = source.loc[
            (source["ÅR"] == 2025)
            & (source["regnr"] == 53103)
            & (source["Attribute"] == "Relativt afløbsresultat"),
            "Value",
        ].iloc[0]
        self.assertTrue(pd.isna(missing))

        source_codes = {
            "Bruttoerstatningsprocent": "SA2803",
            "Bruttoomkostningsprocent": "SA2804",
            "Combined ratio": "SA2805",
            "Operating ratio": "SA2806",
            "Relativt afløbsresultat": "SA2807",
            "Egenkapitalforrentning i procent": "SA2808",
        }
        for name, source_code in source_codes.items():
            with self.subTest(kpi=name):
                self.assertEqual(calculate_kpi(pd.DataFrame(), name)["KPI"].iloc[0], name)
                metadata = get_metric_metadata(name)
                self.assertEqual(metadata["source_type"], "reported")
                self.assertEqual(metadata["source_code"], source_code)
                self.assertIn("official_definition", metadata)

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

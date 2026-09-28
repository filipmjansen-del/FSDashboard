from pathlib import Path
import unittest

import pandas as pd

from analytics.bank_analyst import bank_entities_for_year, build_bank_analyst_view
from data_loader import load_raw_data


class BankAnalystTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = load_raw_data(Path(__file__).parents[1] / "financial_services_long.xlsx")
        cls.entities = bank_entities_for_year(cls.raw, 2025)
        cls.benchmark_ids = cls.entities["entity_id"].tolist()

    def test_validated_banks_resolve_by_canonical_entity_id(self):
        expected = {
            "bank:3000": "Danske Bank",
            "bank:8079": "AL Sydbank",
            "bank:7858": "Jyske Bank",
        }
        for entity_id, display_name in expected.items():
            comparison, history, overview = build_bank_analyst_view(
                self.raw, entity_id, 2025, self.benchmark_ids
            )
            self.assertEqual(overview["display_name"], display_name)
            self.assertEqual(len(comparison), 8)
            self.assertFalse(history.empty)

    def test_current_yoy_and_peer_median_reconcile_to_reported_profit_before_tax(self):
        comparison, _, _ = build_bank_analyst_view(
            self.raw, "bank:3000", 2025, self.benchmark_ids
        )
        profit = comparison.loc[comparison["metric_id"].eq("bank.profit_before_tax")].iloc[0]
        source = self.raw.loc[
            (self.raw["Branche"] == "Bank")
            & (self.raw["Attribute"] == "Res_RfS_RY")
            & self.raw["ÅR"].isin([2024, 2025]),
            ["ÅR", "regnr", "Value"],
        ].copy()
        source["Value"] = pd.to_numeric(source["Value"], errors="coerce")
        current = source.loc[(source["ÅR"] == 2025) & (source["regnr"] == 3000), "Value"].iloc[0]
        previous = source.loc[(source["ÅR"] == 2024) & (source["regnr"] == 3000), "Value"].iloc[0]
        peer_median = source.loc[source["ÅR"] == 2025, "Value"].median()
        self.assertAlmostEqual(profit["current_value"], current)
        self.assertAlmostEqual(profit["previous_value"], previous)
        self.assertAlmostEqual(profit["yoy_change"], current - previous)
        self.assertAlmostEqual(profit["peer_median"], peer_median)

    def test_missing_loans_remain_missing_not_zero(self):
        comparison, _, _ = build_bank_analyst_view(
            self.raw, "bank:13290", 2025, self.benchmark_ids
        )
        loans = comparison.loc[comparison["metric_id"].eq("bank.loans")].iloc[0]
        self.assertTrue(pd.isna(loans["current_value"]))
        self.assertTrue(pd.isna(loans["yoy_change"]))


if __name__ == "__main__":
    unittest.main()

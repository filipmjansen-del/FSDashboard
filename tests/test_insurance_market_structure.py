import unittest

import pandas as pd

from analytics.insurance_market_structure import (
    build_market_structure_table, latest_available_period, same_quarter_history, summarize_market_structure,
)
from data.access import load_insurance_market_structure_fp


class InsuranceMarketStructureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.table = build_market_structure_table(load_insurance_market_structure_fp())
        cls.summary = summarize_market_structure(cls.table)

    def test_2025_q2_regression_values(self):
        tryg = self.table.loc[(self.table.year == 2025) & (self.table.quarter == 2) & (self.table.entity_name == "Tryg"), "market_share"].item()
        result = self.summary.loc[(self.summary.year == 2025) & (self.summary.quarter == 2)].iloc[0]
        self.assertAlmostEqual(tryg, 0.2337, places=3)
        self.assertAlmostEqual(result.cr5, 0.6684, places=3)
        self.assertAlmostEqual(result.hhi, 1199.3, places=0)
        self.assertEqual(result.entity_count, 35)
        self.assertEqual(result.market_size, 39_782_867)

    def test_2024_q4_regression_values(self):
        tryg = self.table.loc[(self.table.year == 2024) & (self.table.quarter == 4) & (self.table.entity_name == "Tryg"), "market_share"].item()
        result = self.summary.loc[(self.summary.year == 2024) & (self.summary.quarter == 4)].iloc[0]
        self.assertAlmostEqual(tryg, 0.2399, places=3)
        self.assertAlmostEqual(result.cr5, 0.6889, places=3)
        self.assertAlmostEqual(result.hhi, 1255.4, places=0)
        self.assertEqual(result.entity_count, 39)
        self.assertEqual(result.market_size, 75_895_673)

    def test_reported_share_is_not_recalculated_from_gross_premiums(self):
        source = load_insurance_market_structure_fp()
        source.loc[(source.year == 2025) & (source.quarter == 2) & (source.entity_name == "Tryg"), "market_value_t_dkk"] = 1.0
        table = build_market_structure_table(source)
        share = table.loc[(table.year == 2025) & (table.quarter == 2) & (table.entity_name == "Tryg"), "market_share"].item()
        self.assertAlmostEqual(share, 0.2337, places=3)

    def test_latest_period_and_same_quarter_history(self):
        self.assertEqual(latest_available_period(self.summary), (2025, 2))
        history = same_quarter_history(self.summary, 2)
        self.assertTrue(history.quarter.eq(2).all())
        self.assertEqual(history.year.max(), 2025)

    def test_duplicate_period_actor_rows_fail_explicitly(self):
        duplicate = pd.concat([load_insurance_market_structure_fp(), load_insurance_market_structure_fp().head(1)], ignore_index=True)
        with self.assertRaisesRegex(ValueError, "Duplicate F&P"):
            build_market_structure_table(duplicate)


if __name__ == "__main__":
    unittest.main()

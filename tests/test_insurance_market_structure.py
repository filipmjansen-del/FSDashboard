import unittest

import pandas as pd

from analytics.insurance_market_structure import (
    GROSS_PREMIUM_ATTRIBUTE,
    build_market_structure_table,
    summarize_market_structure,
)
from data.canonical import to_canonical_observations


class InsuranceMarketStructureTests(unittest.TestCase):
    def setUp(self):
        self.raw = pd.DataFrame(
            {
                "Branche": ["Forsikring"] * 5 + ["Bank"],
                "ÅR": [2020] * 6,
                "Måned": [12] * 6,
                "regnr": [1, 2, 3, 4, 5, 99],
                "navn": ["A", "B", "C", "Missing", "Negative", "Bank"],
                "Attribute": [GROSS_PREMIUM_ATTRIBUTE] * 5 + ["Bal_BO_ATot"],
                "Value": [50.0, 30.0, 20.0, None, -5.0, 100.0],
            }
        )

    def test_source_table_keeps_missing_and_non_positive_observations_explicit(self):
        table = build_market_structure_table(to_canonical_observations(self.raw))
        self.assertEqual(table.columns.tolist(), [
            "year", "entity_id", "display_name", "market_value", "market_share",
            "rank", "included_flag", "exclusion_reason",
        ])
        self.assertEqual(table["included_flag"].sum(), 3)
        self.assertEqual(table.loc[table["entity_id"] == "forsikring:4", "exclusion_reason"].item(), "missing_gross_premiums")
        self.assertEqual(table.loc[table["entity_id"] == "forsikring:5", "exclusion_reason"].item(), "non_positive_gross_premiums")

    def test_market_shares_and_concentration_use_the_same_population(self):
        table = build_market_structure_table(to_canonical_observations(self.raw))
        summary = summarize_market_structure(table).iloc[0]
        shares = table.loc[table["included_flag"], "market_share"]
        self.assertAlmostEqual(shares.sum(), 1.0)
        self.assertEqual(table.loc[table["included_flag"], "rank"].tolist(), [1, 2, 3])
        self.assertEqual(summary["entity_count"], 3)
        self.assertAlmostEqual(summary["market_size"], 100.0)
        self.assertAlmostEqual(summary["cr1"], 0.5)
        self.assertAlmostEqual(summary["cr3"], 1.0)
        self.assertAlmostEqual(summary["cr5"], 1.0)
        self.assertAlmostEqual(summary["hhi"], 3800.0)

    def test_only_fy_observations_are_used_when_multiple_periods_are_present(self):
        canonical = to_canonical_observations(self.raw)
        interim = canonical.loc[canonical["entity_id"] == "forsikring:1"].copy()
        interim["period_type"] = "H1"
        interim["period_end_month"] = 6
        interim["value"] = 999.0

        table = build_market_structure_table(pd.concat([canonical, interim], ignore_index=True))

        self.assertAlmostEqual(table.loc[table["included_flag"], "market_value"].sum(), 100.0)


if __name__ == "__main__":
    unittest.main()

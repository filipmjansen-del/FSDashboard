from pathlib import Path
import unittest

from dashboards.bank.indtjeningsmix import DASHBOARD_META, _calculate_income_mix
from data_loader import load_raw_data


class IncomeMixRegressionTests(unittest.TestCase):
    def test_accounting_income_mix_outputs_are_preserved(self):
        mix = _calculate_income_mix(load_raw_data(Path(__file__).parents[1] / "financial_services_long.xlsx"))

        self.assertEqual(len(mix), 2_400)
        self.assertEqual(mix[["ÅR", "regnr"]].drop_duplicates().shape[0], 400)
        self.assertAlmostEqual(mix["Amount"].sum(), 868_693_785.0)
        self.assertAlmostEqual(mix["SharePct"].sum(), 40_000.0)

    def test_dashboard_is_named_as_accounting_income_mix(self):
        self.assertEqual(DASHBOARD_META["name"], "Regnskabsmæssigt indtjeningsmix")

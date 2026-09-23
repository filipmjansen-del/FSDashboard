from pathlib import Path
import unittest

from data_loader import load_raw_data
from kpis.registry import calculate_kpi


class BankKpiTests(unittest.TestCase):
    def test_income_per_cost_kpi_uses_the_active_registry(self):
        raw = load_raw_data(Path(__file__).parent / "financial_services_long.xlsx")
        result = calculate_kpi(raw, "Indtjening pr. omkostningskrone")
        valid = result.dropna(subset=["KPI_Value"])

        self.assertFalse(valid.empty)
        self.assertTrue(valid["Denominator"].ne(0).all())
        self.assertTrue(valid["CompleteInputs"].all())
        self.assertTrue(valid["KPI_Value"].notna().all())

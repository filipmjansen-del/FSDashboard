from io import BytesIO
from pathlib import Path
import unittest

import pandas as pd
from openpyxl import load_workbook

from analytics.bank_analyst import bank_entities_for_year, build_bank_analyst_view
from analytics.insurance_market_structure import build_market_structure_table, summarize_market_structure
from data.canonical import to_canonical_observations
from data_loader import load_raw_data
from output.excel import (
    bank_analyst_filename,
    bank_analyst_workbook,
    insurance_market_structure_filename,
    insurance_market_structure_workbook,
)


class OutputExcelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = load_raw_data(Path(__file__).parents[1] / "financial_services_long.xlsx")

    def test_insurance_export_preserves_engine_tables_and_missing_values(self):
        source_table = build_market_structure_table(to_canonical_observations(self.raw))
        summary = summarize_market_structure(source_table)
        selected_year = int(summary["year"].iloc[0])
        source_table = source_table.loc[source_table["year"].eq(selected_year)].copy()
        source_table = pd.concat(
            [
                source_table,
                pd.DataFrame(
                    [{
                        "year": selected_year,
                        "entity_id": "forsikring:missing",
                        "display_name": "Manglende observation",
                        "market_value": pd.NA,
                        "market_share": pd.NA,
                        "rank": pd.NA,
                        "included_flag": False,
                        "exclusion_reason": "missing_gross_premiums",
                    }]
                ),
            ],
            ignore_index=True,
        )
        workbook = load_workbook(BytesIO(insurance_market_structure_workbook(summary.head(1), source_table)), data_only=True)

        self.assertEqual(workbook.sheetnames, ["Summary", "Market shares", "Methodology"])
        summary_sheet = workbook["Summary"]
        self.assertEqual([cell.value for cell in summary_sheet[1]], [
            "year", "entity_count", "market_size", "cr1", "cr3", "cr5", "hhi", "known_data_break",
        ])
        self.assertEqual(summary_sheet["C2"].value, summary.iloc[0]["market_size"])
        shares_sheet = workbook["Market shares"]
        self.assertEqual([cell.value for cell in shares_sheet[1]], [
            "year", "entity_id", "display_name", "market_value", "market_share", "rank", "included_flag", "exclusion_reason",
        ])
        row_number = source_table.index[source_table["market_value"].isna()][0] + 2
        self.assertIsNone(shares_sheet.cell(row=row_number, column=4).value)

    def test_bank_export_preserves_exact_analyst_comparison_and_history(self):
        entities = bank_entities_for_year(self.raw, 2025)
        comparison, history, overview = build_bank_analyst_view(
            self.raw, "bank:3000", 2025, entities["entity_id"].tolist()
        )
        workbook = load_workbook(
            BytesIO(bank_analyst_workbook(comparison, history, overview, 2025, "Alle banker med en observation i det valgte år")),
            data_only=True,
        )

        self.assertEqual(workbook.sheetnames, ["Overview", "Metric comparison", "History", "Methodology"])
        comparison_sheet = workbook["Metric comparison"]
        headers = [cell.value for cell in comparison_sheet[1]]
        self.assertIn("benchmark_median", headers)
        profit_row = comparison.loc[comparison["metric_id"].eq("bank.profit_before_tax")].iloc[0]
        exported_row = next(
            row for row in comparison_sheet.iter_rows(min_row=2, values_only=True)
            if row[headers.index("metric_id")] == "bank.profit_before_tax"
        )
        self.assertEqual(exported_row[headers.index("current_value")], profit_row["current_value"])
        self.assertEqual(exported_row[headers.index("peer_median") if "peer_median" in headers else headers.index("benchmark_median")], profit_row["peer_median"])
        history_sheet = workbook["History"]
        self.assertEqual(history_sheet.max_row - 1, len(history))

    def test_filenames_are_deterministic_and_safe(self):
        self.assertEqual(insurance_market_structure_filename(2016, 2024), "Databank_Insurance_Market_Structure_2016-2024.xlsx")
        self.assertEqual(bank_analyst_filename('A/B: Bank', 2025), "Databank_Bank_Analyst_A_B__Bank_2025.xlsx")


if __name__ == "__main__":
    unittest.main()

import unittest

from ui.formatting import format_kpi_value


class FormattingTests(unittest.TestCase):
    def test_percentage_and_missing_values_match_existing_display_rules(self):
        self.assertEqual(format_kpi_value(0.125, {"display_format": "percentage", "decimals": 1}), "12.5%")
        self.assertEqual(format_kpi_value(None, {"display_format": "number"}), "–")


if __name__ == "__main__":
    unittest.main()

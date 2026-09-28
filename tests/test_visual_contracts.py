import unittest

import pandas as pd

from dashboards.bank.analyst_view import _history_chart
from dashboards.forsikring.market_structure import displayed_market_shares
from ui.formatting import PLOTLY_PNG_HEIGHT, PLOTLY_PNG_WIDTH, chart_display_values, plotly_export_config


class VisualContractTests(unittest.TestCase):
    def test_plotly_png_export_uses_shared_powerpoint_ready_dimensions(self):
        config = plotly_export_config("Databank_Test")
        self.assertEqual(config["toImageButtonOptions"]["format"], "png")
        self.assertEqual(config["toImageButtonOptions"]["width"], PLOTLY_PNG_WIDTH)
        self.assertEqual(config["toImageButtonOptions"]["height"], PLOTLY_PNG_HEIGHT)
        self.assertEqual(config["toImageButtonOptions"]["filename"], "Databank_Test")

    def test_top_ten_market_share_display_does_not_change_underlying_population(self):
        included = pd.DataFrame(
            {"rank": list(range(1, 13)), "market_share": [0.12, 0.11, 0.10, 0.09, 0.08, 0.07, 0.06, 0.05, 0.04, 0.03, 0.02, 0.01]}
        )
        displayed = displayed_market_shares(included, "Top 10")

        self.assertEqual(len(displayed), 10)
        self.assertEqual(set(displayed["rank"]), set(range(1, 11)))
        self.assertEqual(len(included), 12)
        self.assertAlmostEqual(included["market_share"].sum(), 0.78)

    def test_bank_dkk_chart_scales_only_presentation_values_and_uses_concise_unit(self):
        history = pd.DataFrame({"fiscal_year": [2021, 2025], "value": [2_000_000, 4_000_000]})
        meta = {"display_format": "dkk_billion_tdk", "decimals": 1}

        displayed = chart_display_values(history, meta)
        figure = _history_chart(history, "Netto renteindtægter", meta, "AL Sydbank")

        self.assertEqual(history["value"].tolist(), [2_000_000, 4_000_000])
        self.assertEqual(displayed["chart_value"].tolist(), [2.0, 4.0])
        self.assertEqual(figure.layout.yaxis.title.text, "DKK mia.")
        self.assertIn("AL Sydbank · 2021-2025", figure.layout.title.text)
        self.assertGreaterEqual(figure.layout.margin.t, 100)

    def test_bank_multiple_chart_uses_x_axis_unit(self):
        history = pd.DataFrame({"fiscal_year": [2021, 2025], "value": [4.5, 5.0]})

        figure = _history_chart(history, "Udlån i forhold til egenkapital", {"display_format": "multiple", "decimals": 1}, "AL Sydbank")

        self.assertEqual(figure.layout.yaxis.title.text, "x")
        self.assertEqual(figure.layout.yaxis.ticksuffix, "x")


if __name__ == "__main__":
    unittest.main()

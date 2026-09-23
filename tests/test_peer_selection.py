from pathlib import Path
import unittest

from dashboards.bank.peer_selection import _asset_table, _similar_peers
from data_loader import load_raw_data


class PeerSelectionRegressionTests(unittest.TestCase):
    def test_asset_population_and_size_peers_are_preserved(self):
        assets = _asset_table(load_raw_data(Path(__file__).parents[1] / "financial_services_long.xlsx"), 2025)

        self.assertEqual(len(assets), 44)
        self.assertAlmostEqual(assets["TotalAssets"].sum(), 3_972_555_885.0)
        self.assertEqual(assets.head(5)["regnr"].tolist(), ["3000", "7858", "8079", "8117", "9380"])
        self.assertEqual(_similar_peers(assets, "400", 5), ["522", "9335", "755", "7670", "5999"])

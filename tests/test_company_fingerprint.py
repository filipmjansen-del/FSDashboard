import unittest

from dashboards.bank.company_fingerprint import _percentile


class CompanyFingerprintRegressionTests(unittest.TestCase):
    def test_directional_percentiles_preserve_existing_rank_calculation(self):
        values = [1.0, 2.0, 3.0]
        self.assertAlmostEqual(_percentile(values, 2.0, "higher_is_better"), 66.6666666667)
        self.assertAlmostEqual(_percentile(values, 2.0, "lower_is_better"), 66.6666666667)

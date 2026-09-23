import unittest

from data.access import DEFAULT_DATA_PATH, load_financial_services_data


class DataAccessTests(unittest.TestCase):
    def test_facade_loads_the_existing_canonical_source(self):
        raw = load_financial_services_data()
        self.assertEqual(DEFAULT_DATA_PATH.name, "financial_services_long.xlsx")
        self.assertIn("regnr", raw.columns)
        self.assertIn("Value", raw.columns)


if __name__ == "__main__":
    unittest.main()

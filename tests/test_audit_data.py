from pathlib import Path
import unittest

from scripts.audit_data import CANONICAL_CANDIDATE_KEY, audit_data


class DataAuditTests(unittest.TestCase):
    def test_audit_reports_current_source_grain(self):
        audit = audit_data(Path(__file__).parents[1] / "financial_services_long.xlsx")

        self.assertEqual(audit["columns"], [
            "Branche", "ÅR", "Måned", "regnr", "navn", "Attribute", "Value"
        ])
        self.assertEqual(audit["period_values"], [{"month": 12, "observations": audit["rows"]}])
        self.assertEqual(audit["missing_registration_numbers"], 0)
        self.assertFalse(audit["duplicate_canonical_candidates"])
        self.assertEqual(len(CANONICAL_CANDIDATE_KEY), 5)

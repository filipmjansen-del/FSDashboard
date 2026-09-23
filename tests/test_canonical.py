from pathlib import Path
import unittest

import pandas as pd

from data.canonical import (
    CANONICAL_OBSERVATION_KEY,
    build_entity_reference,
    load_canonical_observations,
    to_canonical_observations,
)


class CanonicalDataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.observations = load_canonical_observations(
            Path(__file__).parents[1] / "financial_services_long.xlsx"
        )

    def test_observation_key_is_unique_and_period_is_explicit(self):
        self.assertFalse(self.observations.duplicated(CANONICAL_OBSERVATION_KEY).any())
        self.assertEqual(set(self.observations["period_type"]), {"FY"})
        self.assertEqual(set(self.observations["period_end_month"]), {12})
        self.assertTrue(self.observations["regnr"].notna().all())

    def test_entity_reference_uses_regnr_identity(self):
        reference = build_entity_reference(self.observations)

        self.assertTrue(reference["entity_id"].str.contains(":").all())
        self.assertEqual(set(reference["id_type"]), {"regnr"})
        self.assertTrue(reference["valid_from"].le(reference["valid_to"]).all())

    def test_non_fy_periods_are_rejected(self):
        raw = pd.DataFrame(
            {
                "Branche": ["Bank"], "ÅR": [2025], "Måned": [6], "regnr": [1],
                "navn": ["Example"], "Attribute": ["metric"], "Value": [1],
            }
        )

        with self.assertRaisesRegex(ValueError, "FY"):
            to_canonical_observations(raw)

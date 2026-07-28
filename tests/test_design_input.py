from __future__ import annotations

import copy
import unittest
from pathlib import Path

from compiler.design_input import load_design_input, validate_design_input

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "project" / "design-inputs" / "emberforge-design-system.json"


class DesignInputTests(unittest.TestCase):
    def setUp(self) -> None:
        self.source = load_design_input(SOURCE)

    def test_source_has_stable_identity_and_complete_gap_map(self) -> None:
        self.assertEqual(
            "566f23a55f633642db46c401da81313c151993b747cad812ec51333784a0ee0b",
            self.source["archief_sha256"],
        )
        self.assertEqual(44, self.source["bestanden"])
        self.assertEqual(7, len(self.source["gebieden"]))

    def test_external_input_is_never_normative_or_runtime_dependent(self) -> None:
        contract = self.source["broncontract"]
        self.assertFalse(contract["normatief"])
        self.assertFalse(contract["externe_afhankelijkheden_toegestaan"])

    def test_typography_conflict_remains_explicit(self) -> None:
        typography = next(
            area for area in self.source["gebieden"] if area["id"] == "typography"
        )
        self.assertEqual("besluit-nodig", typography["status"])

    def test_world_language_has_auditable_native_migration(self) -> None:
        world_language = next(
            area
            for area in self.source["gebieden"]
            if area["id"] == "world-language"
        )
        self.assertEqual("gemigreerd", world_language["status"])
        self.assertIn("M11.1e", world_language["bewijs"])
        self.assertIn("emberforge", world_language["bewijs"])

    def test_palette_has_auditable_native_migration(self) -> None:
        palette = next(
            area
            for area in self.source["gebieden"]
            if area["id"] == "palette"
        )
        self.assertEqual("gemigreerd", palette["status"])
        self.assertIn("M11.3b", palette["bewijs"])
        self.assertIn("tokens", palette["bewijs"])

    def test_primitives_have_auditable_native_migration(self) -> None:
        primitives = next(
            area
            for area in self.source["gebieden"]
            if area["id"] == "spacing-radius-shadow-motion"
        )
        self.assertEqual("gemigreerd", primitives["status"])
        self.assertIn("M11.3c", primitives["bewijs"])
        self.assertIn("border", primitives["bewijs"])
        self.assertIn("appearance", primitives["bewijs"])

    def test_normative_external_source_fails_hard(self) -> None:
        invalid = copy.deepcopy(self.source)
        invalid["broncontract"]["normatief"] = True
        with self.assertRaisesRegex(ValueError, "mag niet normatief"):
            validate_design_input(invalid)

    def test_duplicate_gap_area_fails_hard(self) -> None:
        invalid = copy.deepcopy(self.source)
        invalid["gebieden"].append(copy.deepcopy(invalid["gebieden"][0]))
        with self.assertRaisesRegex(ValueError, "dubbel gebied"):
            validate_design_input(invalid)


if __name__ == "__main__":
    unittest.main()

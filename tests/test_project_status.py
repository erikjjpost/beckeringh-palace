from __future__ import annotations

import copy
import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "tools" / "render_status.py"
SPEC = importlib.util.spec_from_file_location("render_status", MODULE_PATH)
assert SPEC and SPEC.loader
render_status = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(render_status)


class ProjectStatusTests(unittest.TestCase):
    def setUp(self) -> None:
        self.status = render_status.load_status()

    def test_committed_status_is_generated_from_normative_source(self) -> None:
        expected = render_status.render_status(self.status)
        actual = render_status.OUTPUT.read_text(encoding="utf-8")
        self.assertEqual(actual, expected)

    def test_every_area_has_progress_evidence_and_remaining_work(self) -> None:
        self.assertEqual(len(self.status["areas"]), 10)
        for area in self.status["areas"]:
            self.assertIn(area["progress"], range(101))
            self.assertTrue(area["evidence"])
            self.assertTrue(area["remaining"])

    def test_invalid_percentage_fails_hard(self) -> None:
        invalid = copy.deepcopy(self.status)
        invalid["areas"][0]["progress"] = 101

        with self.assertRaisesRegex(ValueError, "geheel percentage"):
            render_status.validate_status(invalid)

    def test_duplicate_area_fails_hard(self) -> None:
        invalid = copy.deepcopy(self.status)
        invalid["areas"].append(copy.deepcopy(invalid["areas"][0]))

        with self.assertRaisesRegex(ValueError, "dubbel productgebied"):
            render_status.validate_status(invalid)


if __name__ == "__main__":
    unittest.main()

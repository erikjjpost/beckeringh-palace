from __future__ import annotations

import copy
import importlib.util
import unittest
from pathlib import Path

from compiler.backend import Backend, BackendRegistry
from compiler.parser import parseer
from compiler.product_compiler import compileer_producten
from compiler.project_status import calculate_overall_progress, load_project_status

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
            self.assertEqual(10, area["weight"])
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

    def test_total_progress_is_deterministically_calculated(self) -> None:
        self.assertNotIn("overall_progress", self.status)
        self.assertEqual(93, calculate_overall_progress(self.status))

    def test_schema_version_must_be_two(self) -> None:
        invalid = copy.deepcopy(self.status)
        invalid["schema_version"] = 1

        with self.assertRaisesRegex(ValueError, "schema_version moet 2 zijn"):
            render_status.validate_status(invalid)

    def test_verification_state_must_be_known(self) -> None:
        invalid = copy.deepcopy(self.status)
        invalid["current_milestone"]["verification"]["state"] = "onbekend"

        with self.assertRaisesRegex(ValueError, "verification.state moet"):
            render_status.validate_status(invalid)

    def test_verification_geverifieerd_requires_actor_and_date(self) -> None:
        invalid = copy.deepcopy(self.status)
        invalid["current_milestone"]["verification"] = {
            "state": "geverifieerd",
            "actor": None,
            "date": None,
        }

        with self.assertRaisesRegex(ValueError, "verification.actor is verplicht"):
            render_status.validate_status(invalid)

    def test_verification_non_geverifieerd_forbids_actor_and_date(self) -> None:
        invalid = copy.deepcopy(self.status)
        invalid["current_milestone"]["verification"] = {
            "state": "wacht-op-menselijke-verificatie",
            "actor": "Erik Post",
            "date": "2026-08-15",
        }

        with self.assertRaisesRegex(
            ValueError, "moeten leeg zijn zolang state niet"
        ):
            render_status.validate_status(invalid)

    def test_verification_geverifieerd_with_actor_and_date_is_valid(self) -> None:
        valid = copy.deepcopy(self.status)
        valid["current_milestone"]["verification"] = {
            "state": "geverifieerd",
            "actor": "Erik Post",
            "date": "2026-08-15",
        }

        render_status.validate_status(valid)

    def test_area_weights_must_total_one_hundred(self) -> None:
        invalid = copy.deepcopy(self.status)
        invalid["areas"][0]["weight"] = 9

        with self.assertRaisesRegex(ValueError, "samen 100"):
            render_status.validate_status(invalid)

    def test_status_is_typed_product_context_for_every_backend(self) -> None:
        status = load_project_status(render_status.SOURCE)
        registry = BackendRegistry()

        def render(_objecten, product):
            self.assertIs(product.project_status, status)
            self.assertEqual(93, product.project_status.overall_progress)
            self.assertEqual(10, len(product.project_status.areas))
            self.assertEqual(
                "M11.13a", product.project_status.current_milestone.id
            )
            self.assertEqual("TBD", product.project_status.next_step.id)
            self.assertEqual(
                "M11.10a", product.project_status.last_completed_milestone.id
            )
            self.assertEqual(
                122, product.project_status.last_completed_milestone.pull_request
            )
            return product.project_status.project

        registry.registreer(Backend("capture", render))
        objecten = parseer(
            '''
product project-status-capture {
    naam: "Projectstatus"
    doel: "Bewijst backendonafhankelijke statuscontext."
    backend: "capture"
    layout: "status-layout"
    pad: "output/products/project-status.txt"
}
'''
        )

        compiled = compileer_producten(
            objecten, registry, project_status=status
        )

        self.assertEqual("Beckeringh Palace", compiled[0].inhoud)
        self.assertIs(compiled[0].definitie.project_status, status)

    def test_product_compilation_without_status_remains_explicitly_contextless(self) -> None:
        registry = BackendRegistry()
        registry.registreer(Backend(
            "capture",
            lambda _objecten, product: (
                "none" if product.project_status is None else "status"
            ),
        ))
        objecten = parseer(
            '''
product legacy-statusless {
    naam: "Statusloos product"
    doel: "Bestaand compilatiepad zonder projectstatus."
    backend: "capture"
    layout: "legacy-layout"
    pad: "output/products/legacy-statusless.txt"
}
'''
        )

        compiled = compileer_producten(objecten, registry)

        self.assertEqual("none", compiled[0].inhoud)


if __name__ == "__main__":
    unittest.main()

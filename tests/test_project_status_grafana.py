from __future__ import annotations

import json
import unittest
from pathlib import Path

from compiler.parser import parseer_bestand
from compiler.product_backends import standaard_backend_registry
from compiler.product_compiler import compileer_producten
from compiler.product_constraints import WORLD_MODEL_CONSTRAINTS
from compiler.project_status import load_project_status
from compiler.semantic import analyseer


ROOT = Path(__file__).resolve().parents[1]


class ProjectStatusGrafanaTests(unittest.TestCase):
    def test_native_grafana_product_renders_complete_typed_status_context(self):
        objecten = []
        for path in sorted((ROOT / "architectuur").glob("*.bp")):
            objecten.extend(parseer_bestand(path))
        model = analyseer(objecten, constraints=WORLD_MODEL_CONSTRAINTS)
        status = load_project_status(ROOT / "project" / "status.json")

        products = {
            product.definitie.id: product
            for product in compileer_producten(
                model.objecten,
                standaard_backend_registry(),
                project_status=status,
            )
        }
        product = products["project-status-grafana"]
        dashboard = json.loads(product.inhoud)

        self.assertEqual("project-status", product.definitie.inhoud)
        self.assertEqual("project-status-grafana", dashboard["uid"])
        self.assertFalse(dashboard["editable"])
        self.assertEqual({"hidden": True}, dashboard["timepicker"])
        self.assertNotIn("time", dashboard)
        self.assertIn(
            f"project-status-schema:{status.schema_version}", dashboard["tags"]
        )
        self.assertIn(
            f"overall-progress:{status.overall_progress}", dashboard["tags"]
        )
        rendered = json.dumps(dashboard, ensure_ascii=False)
        self.assertIn(status.current_milestone.id, rendered)
        self.assertIn(status.last_completed_milestone.id, rendered)
        self.assertIn(status.next_step.id, rendered)
        for area in status.areas:
            self.assertIn(f"project-status-area:{area.id}", rendered)
            self.assertIn(f"{area.name} · {area.progress}%", rendered)
            self.assertIn(area.evidence, rendered)
            self.assertIn(area.remaining, rendered)

        self.assertEqual(12, len(dashboard["panels"]))


if __name__ == "__main__":
    unittest.main()

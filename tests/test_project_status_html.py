from __future__ import annotations

import unittest
from pathlib import Path
import html as html_module

from compiler.parser import parseer_bestand
from compiler.product_backends import standaard_backend_registry
from compiler.product_compiler import compileer_producten
from compiler.product_constraints import WORLD_MODEL_CONSTRAINTS
from compiler.project_status import load_project_status
from compiler.semantic import analyseer


ROOT = Path(__file__).resolve().parents[1]


class ProjectStatusHtmlTests(unittest.TestCase):
    def test_native_html_product_renders_complete_typed_status_context(self):
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
        product = products["project-status-html"]
        html = product.inhoud

        self.assertEqual("project-status", product.definitie.inhoud)
        self.assertIn('data-status-schema="1"', html)
        self.assertIn(f"<strong>{status.overall_progress}%</strong>", html)
        self.assertIn(status.current_milestone.id, html)
        self.assertIn(status.last_completed_milestone.id, html)
        self.assertIn(status.next_step.id, html)
        for area in status.areas:
            self.assertIn(f'data-status-area="{area.id}"', html)
            self.assertIn(f'value="{area.progress}"', html)
            self.assertIn(html_module.escape(area.evidence), html)
            self.assertIn(html_module.escape(area.remaining), html)

    def test_contextless_compilation_omits_only_project_status_product(self):
        objecten = []
        for path in sorted((ROOT / "architectuur").glob("*.bp")):
            objecten.extend(parseer_bestand(path))
        model = analyseer(objecten, constraints=WORLD_MODEL_CONSTRAINTS)

        products = compileer_producten(
            model.objecten, standaard_backend_registry()
        )

        self.assertEqual(
            {
                "beckeringh-palace-homepage",
                "forge-dashboard-grafana",
                "forge-dashboard-html",
                "forge-design-system-reference-html",
                "emberforge-homelab-dashboard-html",
                "emberforge-homelab-dashboard-grafana",
                "emberforge-keycloak-login-html",
                "emberforge-terminal-html",
                "emberforge-svg-asset-catalog-html",
                "emberforge-vector-node-svg",
                "emberforge-light-disc-svg",
                "emberforge-icon-dashboard-svg",
                "emberforge-icon-identity-svg",
                "emberforge-icon-terminal-svg",
                "emberforge-icon-assets-svg",
                "emberforge-merkteken-svg",
                "emberforge-woordmerk-svg",
                "emberforge-desktop-wallpaper-manifest",
                "emberforge-desktop-wallpaper-png",
                "emberforge-ultrawide-wallpaper-manifest",
                "emberforge-ultrawide-wallpaper-png",
            },
            {product.definitie.id for product in products},
        )


if __name__ == "__main__":
    unittest.main()

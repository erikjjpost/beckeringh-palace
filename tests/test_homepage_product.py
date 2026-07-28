from __future__ import annotations

import unittest
from pathlib import Path

from compiler.parser import parseer, parseer_bestand
from compiler.product_backends import standaard_backend_registry
from compiler.product_compiler import compileer_producten
from compiler.product_constraints import WORLD_MODEL_CONSTRAINTS
from compiler.semantic import SemantischeFout, analyseer


ROOT = Path(__file__).resolve().parents[1]
WORLD = ROOT / "architectuur" / "world.bp"


class HomepageProductTests(unittest.TestCase):
    def setUp(self) -> None:
        self.model = analyseer(
            parseer_bestand(WORLD),
            constraints=WORLD_MODEL_CONSTRAINTS,
        )
        self.products = {
            product.definitie.id: product
            for product in compileer_producten(
                self.model.objecten,
                standaard_backend_registry(),
            )
        }

    def test_homepage_is_een_eigen_native_html_product(self) -> None:
        homepage = self.products["beckeringh-palace-homepage"]
        definition = homepage.definitie

        self.assertEqual("html", definition.backend)
        self.assertEqual("static", definition.mode)
        self.assertEqual("output/products/index.html", definition.pad)
        self.assertEqual(
            "beckeringh-palace-homepage-composition",
            definition.opgeloste_compositie.id,
        )
        self.assertEqual(
            "beckeringh-palace-homepage-grid",
            definition.opgeloste_layout.id,
        )
        self.assertEqual(
            (
                "homepage-intro",
                "homepage-world",
                "homepage-design-system",
                "homepage-project-status",
            ),
            tuple(
                instance.id
                for instance in definition.opgeloste_compositie.instances
            ),
        )
        self.assertEqual(
            (
                "homepage-entrance",
                "homepage-world-area",
                "homepage-design-system-area",
                "homepage-project-status-area",
            ),
            tuple(
                instance.homepage_area_id
                for instance in definition.opgeloste_compositie.instances
            ),
        )
        self.assertEqual(
            (3, 2),
            (
                definition.opgeloste_layout.columns,
                definition.opgeloste_layout.rows,
            ),
        )
        self.assertEqual(64, len(definition.snapshot_id))

    def test_homepage_rendert_de_drie_native_productroutes(self) -> None:
        html = self.products["beckeringh-palace-homepage"].inhoud

        self.assertIn("<h1>Beckeringh Palace</h1>", html)
        self.assertIn("<h2>Design is data</h2>", html)
        self.assertIn(
            'data-homepage-area="homepage-entrance" '
            'data-homepage-role="entree" data-reading-order="1"',
            html,
        )
        self.assertIn(
            '<p class="bp-core-message">Design is data.</p>',
            html,
        )
        self.assertIn(
            "grid-template-columns:repeat(3,minmax(0,1fr))",
            html,
        )
        self.assertIn(
            'href="forge-dashboard.html" '
            'data-navigation-target="forge-dashboard-html"',
            html,
        )
        self.assertIn(
            'href="components.html" '
            'data-navigation-target="html-components"',
            html,
        )
        self.assertIn(
            'href="project-status.html" '
            'data-navigation-target="project-status-html"',
            html,
        )
        self.assertEqual(3, html.count('data-navigation-target="'))
        self.assertIn('data-product-mode="static"', html)
        self.assertIn('data-time-context="none"', html)

    def test_componentnavigatie_weigert_ongeldige_doelen(self) -> None:
        source = WORLD.read_text(encoding="utf-8")
        valid = '    navigatie: "forge-dashboard-html"'
        variants = (
            (
                source.replace(
                    valid,
                    '    navigatie: "missing-product"',
                    1,
                ),
                "BP4107",
            ),
            (
                source.replace(
                    valid,
                    '    navigatie: "beckeringh-palace"',
                    1,
                ),
                "BP4108",
            ),
        )
        for invalid_source, code in variants:
            with self.subTest(code=code):
                with self.assertRaises(SemantischeFout) as context:
                    analyseer(
                        parseer(invalid_source),
                        constraints=WORLD_MODEL_CONSTRAINTS,
                    )
                self.assertIn(
                    code,
                    {item.code for item in context.exception.diagnostics},
                )


if __name__ == "__main__":
    unittest.main()

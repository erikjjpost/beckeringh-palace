from __future__ import annotations

import unittest
from pathlib import Path

from compiler.brand_identity import resolveer_merkidentiteiten
from compiler.homepage_information_architecture import resolveer_homepagegebieden
from compiler.parser import parseer, parseer_bestand
from compiler.product_backends import standaard_backend_registry
from compiler.product_compiler import compileer_producten
from compiler.product_constraints import WORLD_MODEL_CONSTRAINTS
from compiler.semantic import SemantischeFout, analyseer


ROOT = Path(__file__).resolve().parents[1]
WORLD = ROOT / "architectuur" / "world.bp"


class EmberForgeProductNavigationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.model = analyseer(
            parseer_bestand(WORLD),
            constraints=WORLD_MODEL_CONSTRAINTS,
        )
        cls.homepage_areas = {
            area.id: area
            for area in resolveer_homepagegebieden(cls.model.objecten)
        }
        cls.homepage = next(
            product
            for product in compileer_producten(
                cls.model.objecten,
                standaard_backend_registry(),
            )
            if product.definitie.id == "beckeringh-palace-homepage"
        )

    def test_productfamilie_noemt_keycloak_en_terminal(self) -> None:
        brand = resolveer_merkidentiteiten(self.model.objecten)[0]

        self.assertIn("Keycloak login", brand.products)
        self.assertIn("Terminal", brand.products)
        self.assertLess(
            brand.products.index("Keycloak login"),
            brand.products.index("Terminal"),
        )

    def test_homepage_resolveert_directe_productroutes(self) -> None:
        expected = {
            "homepage-keycloak-area": (
                "emberforge-keycloak-login-html",
                "output/products/emberforge-keycloak-login.html",
            ),
            "homepage-terminal-area": (
                "emberforge-terminal-html",
                "output/products/emberforge-terminal.html",
            ),
        }

        for area_id, (target_id, artifact_path) in expected.items():
            with self.subTest(area=area_id):
                area = self.homepage_areas[area_id]
                self.assertEqual("route", area.role)
                self.assertEqual("routekaart", area.component_role)
                self.assertEqual("volledige-kaart", area.navigation_behavior)
                self.assertEqual(1, len(area.navigation_targets))
                self.assertEqual(target_id, area.navigation_targets[0].id)
                self.assertEqual(
                    artifact_path,
                    area.navigation_targets[0].artifact_path,
                )

    def test_homepage_publiceert_beide_relatieve_routes_eenmaal(self) -> None:
        html = self.homepage.inhoud

        self.assertEqual(
            1,
            html.count(
                'href="emberforge-keycloak-login.html" '
                'data-navigation-target="emberforge-keycloak-login-html"'
            ),
        )
        self.assertEqual(
            1,
            html.count(
                'href="emberforge-terminal.html" '
                'data-navigation-target="emberforge-terminal-html"'
            ),
        )
        self.assertNotIn("href=\"http", html)

    def test_weigert_dubbel_productdoel(self) -> None:
        source = WORLD.read_text(encoding="utf-8")
        invalid = source.replace(
            '    navigatie: "emberforge-terminal-html"',
            '    navigatie: "emberforge-keycloak-login-html"',
            1,
        )

        with self.assertRaises(SemantischeFout) as context:
            analyseer(
                parseer(invalid),
                constraints=WORLD_MODEL_CONSTRAINTS,
            )

        self.assertIn(
            "BP4109",
            {diagnostic.code for diagnostic in context.exception.diagnostics},
        )


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import json
import unittest
from html.parser import HTMLParser
from pathlib import Path

from compiler.parser import parseer, parseer_bestand
from compiler.product_backends import standaard_backend_registry
from compiler.product_compiler import compileer_producten
from compiler.product_constraints import WORLD_MODEL_CONSTRAINTS
from compiler.semantic import SemantischeFout, analyseer


ROOT = Path(__file__).resolve().parents[1]
WORLD = ROOT / "architectuur" / "world.bp"
DESIGN_INPUT = ROOT / "project" / "design-inputs" / "emberforge-design-system.json"


class _IdCollector(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: list[str] = []

    def handle_starttag(self, _tag, attrs) -> None:
        self.ids.extend(value for name, value in attrs if name == "id")


class EmberForgeKeycloakLoginProductTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.model = analyseer(
            parseer_bestand(WORLD),
            constraints=WORLD_MODEL_CONSTRAINTS,
        )
        cls.products = {
            product.definitie.id: product
            for product in compileer_producten(
                cls.model.objecten,
                standaard_backend_registry(),
            )
        }

    def test_modelleert_login_als_native_bat_formulier(self) -> None:
        product = self.products["emberforge-keycloak-login-html"].definitie
        composition = product.opgeloste_compositie
        layout = product.opgeloste_layout

        self.assertIsNotNone(composition)
        self.assertIsNotNone(layout)
        assert composition is not None
        assert layout is not None
        self.assertEqual("login-formulier", composition.role)
        self.assertEqual(
            (
                "keycloak-login-identity",
                "keycloak-login-password",
                "keycloak-login-submit",
            ),
            tuple(instance.id for instance in composition.instances),
        )
        self.assertEqual((1, 3), (layout.columns, layout.rows))
        self.assertEqual(640, layout.responsive_breakpoint)
        self.assertEqual(1, layout.compact_columns)

    def test_rendert_native_email_password_en_submit_semantiek(self) -> None:
        html = self.products["emberforge-keycloak-login-html"].inhoud

        self.assertIn("<h1>EmberForge Sign In</h1>", html)
        self.assertIn('<form class="bp-layout ', html)
        self.assertIn('data-composition-role="login-formulier"', html)
        self.assertIn('type="email"', html)
        self.assertIn('type="password"', html)
        self.assertIn('type="submit"', html)
        self.assertIn(">Username or email</label>", html)
        self.assertIn(">Password</label>", html)
        self.assertIn(">Sign In</button>", html)
        self.assertNotIn("client_id", html)
        self.assertNotIn("realm", html)
        self.assertNotIn("action=", html)

        parser = _IdCollector()
        parser.feed(html)
        self.assertEqual(len(parser.ids), len(set(parser.ids)))

    def test_registreert_de_login_surface_zonder_authenticatieclaim(self) -> None:
        source = json.loads(DESIGN_INPUT.read_text(encoding="utf-8"))
        area = next(
            area for area in source["gebieden"] if area["id"] == "product-surfaces"
        )

        self.assertEqual("gedeeltelijk-mapbaar", area["status"])
        self.assertIn("M11.4c", area["bewijs"])
        self.assertIn("geen Keycloak configuratie", area["bewijs"])

    def test_weigert_onbekende_formulier_en_controlsemantiek(self) -> None:
        source = WORLD.read_text(encoding="utf-8")
        mutations = (
            ('    rol: "login-formulier"', '    rol: "login-dialoog"', "BP3705"),
            ('    invoertype: "password"', '    invoertype: "secret"', "BP3827"),
            ('    actietype: "submit"', '    actietype: "authenticate"', "BP3828"),
        )
        for old, new, code in mutations:
            with self.subTest(code=code):
                with self.assertRaises(SemantischeFout) as context:
                    analyseer(
                        parseer(source.replace(old, new, 1)),
                        constraints=WORLD_MODEL_CONSTRAINTS,
                    )
                self.assertIn(
                    code,
                    {item.code for item in context.exception.diagnostics},
                )


if __name__ == "__main__":
    unittest.main()

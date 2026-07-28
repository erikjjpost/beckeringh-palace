from __future__ import annotations

import unittest
from pathlib import Path

from compiler.parser import parseer_bestand
from compiler.product_backends import standaard_backend_registry
from compiler.product_compiler import compileer_producten
from compiler.product_constraints import WORLD_MODEL_CONSTRAINTS
from compiler.semantic import analyseer
from compiler.theme_resolution import resolveer_thema


ROOT = Path(__file__).resolve().parents[1]
WORLD = ROOT / "architectuur" / "world.bp"


class EmberForgePrimitivesMigrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.model = analyseer(
            parseer_bestand(WORLD),
            constraints=WORLD_MODEL_CONSTRAINTS,
        )
        cls.theme = resolveer_thema(cls.model.objecten, "beckeringh-palace")
        cls.products = {
            product.definitie.id: product
            for product in compileer_producten(
                cls.model.objecten,
                standaard_backend_registry(),
            )
        }

    def test_resolveert_de_geverifieerde_semantische_primitieven(self) -> None:
        self.assertEqual(
            ("1px", "1px", "1px", "solid"),
            (
                self.theme.border.hairline,
                self.theme.border.regular,
                self.theme.border.strong,
                self.theme.border.style,
            ),
        )
        self.assertEqual(
            ("4px", "12px", "16px", "999px"),
            (
                self.theme.radius.small,
                self.theme.radius.medium,
                self.theme.radius.large,
                self.theme.radius.pill,
            ),
        )
        self.assertEqual(
            (
                "0 1px 2px rgba(0,0,0,0.25)",
                "0 6px 18px rgba(0,0,0,0.35)",
                "0 18px 44px rgba(0,0,0,0.45)",
            ),
            (
                self.theme.shadow.low,
                self.theme.shadow.medium,
                self.theme.shadow.high,
            ),
        )
        self.assertEqual(
            ("120ms", "220ms", "420ms", "cubic-bezier(0.2, 0.7, 0.2, 1)"),
            (
                self.theme.motion.fast,
                self.theme.motion.normal,
                self.theme.motion.slow,
                self.theme.motion.easing,
            ),
        )
        self.assertEqual(
            ("0", "4px", "8px", "16px", "32px", "64px"),
            (
                self.theme.spacing.none,
                self.theme.spacing.xs,
                self.theme.spacing.small,
                self.theme.spacing.medium,
                self.theme.spacing.large,
                self.theme.spacing.xl,
            ),
        )

    def test_html_activeert_dezelfde_opgeloste_primitieven(self) -> None:
        html = self.products["beckeringh-palace-homepage"].inhoud

        self.assertIn("--bp-border-regular: 1px;", html)
        self.assertIn("--bp-radius-medium: 12px;", html)
        self.assertIn(
            "--bp-shadow-high: 0 18px 44px rgba(0,0,0,0.45);",
            html,
        )
        self.assertIn("--bp-motion-normal: 220ms;", html)
        self.assertIn(
            "--bp-motion-easing: cubic-bezier(0.2, 0.7, 0.2, 1);",
            html,
        )
        self.assertIn("--bp-spacing-large: 32px;", html)
        self.assertIn("--bp-spacing-xl: 64px;", html)


if __name__ == "__main__":
    unittest.main()

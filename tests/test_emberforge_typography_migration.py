from __future__ import annotations

import unittest
from pathlib import Path

from compiler.parser import parseer, parseer_bestand
from compiler.product_backends import standaard_backend_registry
from compiler.product_compiler import compileer_producten
from compiler.product_constraints import WORLD_MODEL_CONSTRAINTS
from compiler.semantic import SemantischeFout, analyseer
from compiler.theme_resolution import resolveer_thema


ROOT = Path(__file__).resolve().parents[1]
WORLD = ROOT / "architectuur" / "world.bp"


class EmberForgeTypographyMigrationTests(unittest.TestCase):
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

    def test_resolveert_geverifieerde_lokale_fontstacks(self) -> None:
        typography = self.theme.typografie

        self.assertEqual(
            ("Orbitron", "Iceland", "Bank Gothic", "system-ui", "sans-serif"),
            typography.heading,
        )
        self.assertEqual(
            (
                "Inter",
                "IBM Plex Sans",
                "system-ui",
                "-apple-system",
                "sans-serif",
            ),
            typography.body,
        )
        self.assertEqual(
            ("JetBrains Mono", "Fira Code", "SF Mono", "Menlo", "monospace"),
            typography.mono,
        )
        self.assertEqual("local-only", typography.levering)

    def test_resolveert_productgedragen_emberforge_typeschaal(self) -> None:
        self.assertEqual(
            ("80px", "56px", "32px", "16px", "12px", "12px"),
            (
                self.theme.typeschaal.display,
                self.theme.typeschaal.title,
                self.theme.typeschaal.heading,
                self.theme.typeschaal.body,
                self.theme.typeschaal.label,
                self.theme.typeschaal.caption,
            ),
        )
        self.assertEqual(
            (
                ("heading", "500", "1", "0.08em"),
                ("heading", "600", "1.15", "-0.01em"),
                ("heading", "700", "1.3", "normal"),
                ("body", "400", "1.55", "normal"),
                ("body", "500", "normal", "0.18em"),
                ("body", "400", "normal", "normal"),
            ),
            tuple(
                (
                    getattr(self.theme.typeschaal, f"{rol}_font"),
                    getattr(self.theme.typeschaal, f"{rol}_weight"),
                    getattr(self.theme.typeschaal, f"{rol}_line_height"),
                    getattr(self.theme.typeschaal, f"{rol}_letter_spacing"),
                )
                for rol in ("display", "title", "heading", "body", "label", "caption")
            ),
        )

    def test_html_activeert_stacks_zonder_externe_runtimebron(self) -> None:
        html = self.products["beckeringh-palace-homepage"].inhoud

        self.assertIn(
            '--bp-font-heading: "Orbitron", "Iceland", "Bank Gothic", '
            "system-ui, sans-serif;",
            html,
        )
        self.assertIn(
            '--bp-font-body: "Inter", "IBM Plex Sans", system-ui, '
            "-apple-system, sans-serif;",
            html,
        )
        self.assertIn(
            '--bp-font-mono: "JetBrains Mono", "Fira Code", "SF Mono", '
            '"Menlo", monospace;',
            html,
        )
        self.assertIn('data-typography="forge-interface"', html)
        self.assertIn('data-font-delivery="local-only"', html)
        self.assertNotIn("@import", html)
        self.assertNotIn("fonts.googleapis.com", html)

    def test_weigert_externe_fontbron_in_stack(self) -> None:
        bron = WORLD.read_text(encoding="utf-8").replace(
            'heading: ["Orbitron", "Iceland", "Bank Gothic", "system-ui", "sans-serif"]',
            'heading: ["Orbitron", "https://fonts.example/orbitron", "sans-serif"]',
        )
        with self.assertRaises(SemantischeFout) as context:
            analyseer(parseer(bron), constraints=WORLD_MODEL_CONSTRAINTS)

        self.assertIn("BP3642", {item.code for item in context.exception.diagnostics})

    def test_weigert_scalar_in_plaats_van_fontstack(self) -> None:
        bron = WORLD.read_text(encoding="utf-8").replace(
            'mono: ["JetBrains Mono", "Fira Code", "SF Mono", "Menlo", "monospace"]',
            'mono: "JetBrains Mono"',
        )
        with self.assertRaises(SemantischeFout) as context:
            analyseer(parseer(bron), constraints=WORLD_MODEL_CONSTRAINTS)

        self.assertIn("BP3641", {item.code for item in context.exception.diagnostics})

    def test_weigert_stack_zonder_generieke_fallback(self) -> None:
        bron = WORLD.read_text(encoding="utf-8").replace(
            'body: ["Inter", "IBM Plex Sans", "system-ui", "-apple-system", "sans-serif"]',
            'body: ["Inter", "IBM Plex Sans"]',
        )
        with self.assertRaises(SemantischeFout) as context:
            analyseer(parseer(bron), constraints=WORLD_MODEL_CONSTRAINTS)

        self.assertIn("BP3643", {item.code for item in context.exception.diagnostics})

    def test_weigert_fontlevering_buiten_lokale_runtime(self) -> None:
        bron = WORLD.read_text(encoding="utf-8").replace(
            'levering: "local-only"',
            'levering: "remote"',
        )
        with self.assertRaises(SemantischeFout) as context:
            analyseer(parseer(bron), constraints=WORLD_MODEL_CONSTRAINTS)

        self.assertIn("BP3640", {item.code for item in context.exception.diagnostics})


if __name__ == "__main__":
    unittest.main()

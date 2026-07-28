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


class EmberForgePaletteMigrationTests(unittest.TestCase):
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

    def test_resolveert_de_geverifieerde_semantische_paletrollen(self) -> None:
        expected = {
            "primary": "#7DD3FC",
            "background": "#0F1724",
            "surface": "#1F2937",
            "foreground": "#E6EDF5",
            "accent": "#C9895B",
            "success": "#4ADE80",
            "warning": "#E0B341",
            "error": "#F87171",
        }

        self.assertEqual(
            expected,
            {
                role: color.waarde
                for role, color in self.theme.palet.kleuren
            },
        )

    def test_resolveert_de_geverifieerde_materiaalrollen(self) -> None:
        expected = {
            "canvas": "#0F1724",
            "surface": "#1F2937",
            "raised": "#243447",
            "foreground": "#E6EDF5",
            "muted": "#B8C5D6",
            "accent": "#C9895B",
            "outline": "#2F4259",
            "interaction": "#7DD3FC",
            "interaction-pressed": "#38BDF8",
            "disabled": "#3E5573",
        }

        self.assertEqual(
            expected,
            {
                role: color.waarde
                for role, color in self.theme.materiaal.kleuren
            },
        )

    def test_html_activeert_sky_primary_en_spaarzaam_ember_accent(self) -> None:
        html = self.products["beckeringh-palace-homepage"].inhoud

        self.assertIn("--bp-theme-primary: #7DD3FC;", html)
        self.assertIn("--bp-theme-background: #0F1724;", html)
        self.assertIn("--bp-theme-accent: #C9895B;", html)
        self.assertIn("--bp-material-raised: #243447;", html)

    def test_grafana_activeert_hetzelfde_opgeloste_materiaal(self) -> None:
        grafana = self.products["forge-dashboard-grafana"].inhoud

        self.assertIn('"fixed": "#1F2937"', grafana)
        self.assertIn('"fixed": "#243447"', grafana)
        self.assertIn('"fixed": "#C9895B"', grafana)


if __name__ == "__main__":
    unittest.main()

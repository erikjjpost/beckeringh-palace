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


class EmberForgeArtDirectionTests(unittest.TestCase):
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

    def test_resolveert_native_visuele_balans(self) -> None:
        art = self.theme.artdirection
        self.assertIsNotNone(art)
        assert art is not None

        self.assertEqual("#0F1724", art.canvas.waarde)
        self.assertEqual("#7DD3FC", art.interaction.waarde)
        self.assertEqual("#C9895B", art.warm_accent.waarde)
        self.assertEqual(2, art.warm_accent_limit)
        self.assertEqual("controlled", art.glow)
        self.assertEqual("technical-linework", art.ornament)
        self.assertEqual("spacious", art.density)
        self.assertEqual("isometric-line-art", art.imagery)

    def test_html_activeert_uitsluitend_opgeloste_art_direction(self) -> None:
        html = self.products["beckeringh-palace-homepage"].inhoud

        self.assertIn('data-art-direction="emberforge-art-direction"', html)
        self.assertIn('data-art-glow="controlled"', html)
        self.assertIn('data-art-ornament="technical-linework"', html)
        self.assertIn('data-art-warm-accent-limit="2"', html)
        self.assertIn("--bp-art-canvas: #0F1724;", html)
        self.assertIn("--bp-art-interaction: #7DD3FC;", html)
        self.assertIn("--bp-art-warm-accent: #C9895B;", html)
        self.assertIn("radial-gradient(circle at 12% 0%", html)
        self.assertIn("linear-gradient(90deg, var(--bp-material-outline)", html)

    def test_weigert_onbegrensde_warme_accenten(self) -> None:
        bron = WORLD.read_text(encoding="utf-8").replace(
            'warm-accent-limit: "2"',
            'warm-accent-limit: "unlimited"',
        )
        with self.assertRaises(SemantischeFout) as context:
            analyseer(parseer(bron), constraints=WORLD_MODEL_CONSTRAINTS)

        self.assertIn("BP3631", {item.code for item in context.exception.diagnostics})

    def test_art_direction_vereist_explicit_materiaal(self) -> None:
        bron = WORLD.read_text(encoding="utf-8").replace(
            '    materiaal: "forge-materials"\n',
            "",
        )
        with self.assertRaises(SemantischeFout) as context:
            analyseer(parseer(bron), constraints=WORLD_MODEL_CONSTRAINTS)

        self.assertIn("BP3634", {item.code for item in context.exception.diagnostics})


if __name__ == "__main__":
    unittest.main()

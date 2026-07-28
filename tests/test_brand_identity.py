from __future__ import annotations

import unittest
from pathlib import Path

from compiler.brand_identity import resolveer_merkidentiteiten
from compiler.parser import parseer, parseer_bestand
from compiler.product_constraints import WORLD_MODEL_CONSTRAINTS
from compiler.semantic import SemantischeFout, analyseer


ROOT = Path(__file__).resolve().parents[1]
WORLD = ROOT / "architectuur" / "world.bp"


class BrandIdentityTests(unittest.TestCase):
    def test_emberforge_identiteit_is_native_en_opgelost(self) -> None:
        model = analyseer(
            parseer_bestand(WORLD),
            constraints=WORLD_MODEL_CONSTRAINTS,
        )

        merken = resolveer_merkidentiteiten(model.objecten)

        self.assertEqual(("emberforge",), tuple(merk.id for merk in merken))
        emberforge = merken[0]
        self.assertEqual("Sovereign Infrastructure.", emberforge.tagline)
        self.assertEqual("Sovereignty over your own stack.", emberforge.promise)
        self.assertEqual(
            ("Own your data.", "Own your nodes.", "Own your forge."),
            emberforge.principles,
        )
        self.assertEqual(
            (
                "Homelab Dashboard",
                "Keycloak login",
                "CV Database",
                "ISMS Challenger",
                "Roadmap",
                "Marketing en merkoppervlakken",
            ),
            emberforge.products,
        )
        self.assertEqual(
            "Nederlands met technische termen in het Engels",
            emberforge.language,
        )
        self.assertEqual("Zelfverzekerd, technisch en rustig", emberforge.voice)

    def test_merkcontract_weigert_onvolledige_of_impliciete_semantiek(self) -> None:
        source = WORLD.read_text(encoding="utf-8")
        variants = (
            (
                source.replace(
                    '    tagline: "Sovereign Infrastructure."',
                    '    tagline: ""',
                    1,
                ),
                "BP4202",
            ),
            (
                source.replace(
                    '    principes: ["Own your data.", "Own your nodes.", '
                    '"Own your forge."]',
                    '    principes: ["Own your data.", "Own your nodes."]',
                    1,
                ),
                "BP4203",
            ),
            (
                source.replace(
                    '    producten: ["Homelab Dashboard", "Keycloak login", '
                    '"CV Database", "ISMS Challenger", "Roadmap", '
                    '"Marketing en merkoppervlakken"]',
                    '    producten: []',
                    1,
                ),
                "BP4204",
            ),
            (
                source.replace(
                    '    merk: "emberforge"',
                    '    merk: "missing-brand"',
                    1,
                ),
                "BP4117",
            ),
            (
                source.replace(
                    '    navigatie: "forge-dashboard-html"',
                    '    merk: "emberforge"\n'
                    '    navigatie: "forge-dashboard-html"',
                    1,
                ),
                "BP4118",
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

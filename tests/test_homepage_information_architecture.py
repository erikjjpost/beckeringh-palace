from __future__ import annotations

import unittest
from pathlib import Path

from compiler.homepage_information_architecture import (
    resolveer_homepagegebieden,
)
from compiler.parser import parseer, parseer_bestand
from compiler.product_constraints import WORLD_MODEL_CONSTRAINTS
from compiler.semantic import SemantischeFout, analyseer


ROOT = Path(__file__).resolve().parents[1]
WORLD = ROOT / "architectuur" / "world.bp"


class HomepageInformationArchitectureTests(unittest.TestCase):
    def test_homepagegebieden_resolveren_in_expliciete_leesvolgorde(self) -> None:
        model = analyseer(
            parseer_bestand(WORLD),
            constraints=WORLD_MODEL_CONSTRAINTS,
        )

        gebieden = resolveer_homepagegebieden(model.objecten)

        self.assertEqual(
            (
                "homepage-entrance",
                "homepage-world-area",
                "homepage-design-system-area",
                "homepage-project-status-area",
            ),
            tuple(gebied.id for gebied in gebieden),
        )
        self.assertEqual(
            ("entree", "route", "route", "route"),
            tuple(gebied.role for gebied in gebieden),
        )
        self.assertEqual(
            (
                "forge-dashboard-html",
                "html-components",
                "project-status-html",
            ),
            tuple(
                gebied.navigation_targets[0].id
                for gebied in gebieden
                if gebied.navigation_targets
            ),
        )

    def test_homepagegebied_contract_weigert_ongeldige_semantiek(self) -> None:
        source = WORLD.read_text(encoding="utf-8")
        variants = (
            (
                source.replace('    rol: "entree"', '    rol: "hero"', 1),
                "BP4102",
            ),
            (
                source.replace(
                    '    kernboodschap: "Design is data."',
                    '    kernboodschap: ""',
                    1,
                ),
                "BP4103",
            ),
            (
                source.replace(
                    'homepagegebied homepage-entrance {\n'
                    '    naam: "Design is data"\n'
                    '    doel: "Introduceert de ontwerpregel achter alle '
                    'Beckeringh Palace producten."\n'
                    '    rol: "entree"\n'
                    '    leesvolgorde: "1"',
                    'homepagegebied homepage-entrance {\n'
                    '    naam: "Design is data"\n'
                    '    doel: "Introduceert de ontwerpregel achter alle '
                    'Beckeringh Palace producten."\n'
                    '    rol: "entree"\n'
                    '    leesvolgorde: "0"',
                    1,
                ),
                "BP4104",
            ),
            (
                source.replace(
                    'homepagegebied homepage-world-area {\n'
                    '    naam: "Digitale wereld"\n'
                    '    doel: "Verken de samenhang tussen wereld, identiteit '
                    'en productfamilie."\n'
                    '    rol: "route"\n'
                    '    leesvolgorde: "2"',
                    'homepagegebied homepage-world-area {\n'
                    '    naam: "Digitale wereld"\n'
                    '    doel: "Verken de samenhang tussen wereld, identiteit '
                    'en productfamilie."\n'
                    '    rol: "route"\n'
                    '    leesvolgorde: "1"',
                    1,
                ),
                "BP4105",
            ),
            (
                source.replace(
                    '    navigatie: "forge-dashboard-html"',
                    '    navigatie: "missing-product"',
                    1,
                ),
                "BP4107",
            ),
            (
                source.replace(
                    '    navigatie: "forge-dashboard-html"',
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

    def test_componentinstantie_verwijst_alleen_naar_het_gebied(self) -> None:
        source = WORLD.read_text(encoding="utf-8")
        variants = (
            (
                source.replace(
                    '    homepagegebied: "homepage-entrance"',
                    '    homepagegebied: "missing-area"',
                    1,
                ),
                "BP3722",
            ),
            (
                source.replace(
                    '    homepagegebied: "homepage-entrance"',
                    '    homepagegebied: "homepage-entrance"\n'
                    '    naam: "Dubbele inhoud"',
                    1,
                ),
                "BP3723",
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

from __future__ import annotations

import unittest

from compiler.parser import parseer
from compiler.product_constraints import WORLD_MODEL_CONSTRAINTS
from compiler.semantic import SemantischeFout, analyseer


GELDIGE_BRON = '''
kleur ember-orange {
    naam: "Ember Orange"
    doel: "Forge-accent."
    waarde: "#D86A35"
}
palet ember-forge {
    naam: "Ember Forge"
    doel: "Forge-palet."
    primary: "ember-orange"
}
typografie forge-interface {
    naam: "Forge Interface"
    doel: "Forge-typografie."
    heading: "Aptos Display"
    body: "Aptos"
    mono: "JetBrains Mono"
}
thema forge {
    naam: "Forge"
    doel: "Forge-thema."
    palet: "ember-forge"
    typografie: "forge-interface"
}
wereld beckeringh-palace {
    naam: "Beckeringh Palace"
    doel: "Digitale ontwerpwereld."
    thema: "forge"
}
'''


class ThemeFoundationTests(unittest.TestCase):
    def test_accepteert_explicit_theme_chain(self):
        model = analyseer(parseer(GELDIGE_BRON), constraints=WORLD_MODEL_CONSTRAINTS)
        soorten = {obj.soort for obj in model.objecten}
        self.assertTrue({"kleur", "palet", "typografie", "thema", "wereld"} <= soorten)

    def test_weigert_onbekende_kleur_in_palet(self):
        bron = GELDIGE_BRON.replace('primary: "ember-orange"', 'primary: "verdwenen-ember"')
        with self.assertRaises(SemantischeFout) as context:
            analyseer(parseer(bron), constraints=WORLD_MODEL_CONSTRAINTS)
        self.assertIn("BP3603", {item.code for item in context.exception.diagnostics})

    def test_weigert_onbekend_palet_in_thema(self):
        bron = GELDIGE_BRON.replace('palet: "ember-forge"', 'palet: "verdwenen-palet"')
        with self.assertRaises(SemantischeFout) as context:
            analyseer(parseer(bron), constraints=WORLD_MODEL_CONSTRAINTS)
        self.assertIn("BP3604", {item.code for item in context.exception.diagnostics})

    def test_weigert_onbekende_typografie_in_thema(self):
        bron = GELDIGE_BRON.replace('typografie: "forge-interface"', 'typografie: "verdwenen-typografie"')
        with self.assertRaises(SemantischeFout) as context:
            analyseer(parseer(bron), constraints=WORLD_MODEL_CONSTRAINTS)
        self.assertIn("BP3605", {item.code for item in context.exception.diagnostics})

    def test_wereld_moet_explicit_thema_kiezen(self):
        bron = GELDIGE_BRON.replace('    thema: "forge"\n', '')
        with self.assertRaises(SemantischeFout) as context:
            analyseer(parseer(bron), constraints=WORLD_MODEL_CONSTRAINTS)
        self.assertIn("BP3606", {item.code for item in context.exception.diagnostics})

    def test_weigert_onbekende_theme_eigenschap(self):
        bron = GELDIGE_BRON.replace('    typografie: "forge-interface"', '    typografie: "forge-interface"\n    default: "verboden"')
        with self.assertRaises(SemantischeFout) as context:
            analyseer(parseer(bron), constraints=WORLD_MODEL_CONSTRAINTS)
        self.assertIn("BP3601", {item.code for item in context.exception.diagnostics})


if __name__ == "__main__":
    unittest.main()

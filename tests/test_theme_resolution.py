from __future__ import annotations

import unittest

from compiler.parser import parseer
from compiler.product_constraints import WORLD_MODEL_CONSTRAINTS
from compiler.semantic import analyseer
from compiler.theme_resolution import (
    ThemeResolutionError,
    resolveer_alle_themas,
    resolveer_thema,
)


BRON = '''
kleur ember-orange {
    naam: "Ember Orange"
    doel: "Primaire accentkleur."
    waarde: "#D86A35"
}
kleur iron-black {
    naam: "Iron Black"
    doel: "Donkere achtergrondkleur."
    waarde: "#171A1F"
}
kleur smoke-white {
    naam: "Smoke White"
    doel: "Lichte voorgrondkleur."
    waarde: "#ECECEC"
}
palet ember-forge {
    naam: "Ember Forge"
    doel: "Forge-palet."
    primary: "ember-orange"
    background: "iron-black"
    foreground: "smoke-white"
    accent: "ember-orange"
}
typografie forge-interface {
    naam: "Forge Interface"
    doel: "Forge-typografie."
    heading: ["Aptos Display", "sans-serif"]
    body: ["Aptos", "sans-serif"]
    mono: ["JetBrains Mono", "monospace"]
    levering: "local-only"
}
thema forge {
    naam: "Forge"
    doel: "Forge-ontwerpidentiteit."
    palet: "ember-forge"
    typografie: "forge-interface"
}
wereld beckeringh-palace {
    naam: "Beckeringh Palace"
    doel: "Canonieke digitale ontwerpwereld."
    thema: "forge"
}
'''


class ThemeResolutionTests(unittest.TestCase):
    def setUp(self):
        self.model = analyseer(parseer(BRON), constraints=WORLD_MODEL_CONSTRAINTS)

    def test_resolveert_volledige_expliciete_keten(self):
        resolved = resolveer_thema(self.model.objecten, "beckeringh-palace")

        self.assertEqual("beckeringh-palace", resolved.wereld_id)
        self.assertEqual("forge", resolved.thema_id)
        self.assertEqual("ember-forge", resolved.palet.id)
        self.assertEqual("forge-interface", resolved.typografie.id)
        self.assertEqual("#D86A35", resolved.palet.kleur("primary").waarde)
        self.assertEqual("#171A1F", resolved.palet.kleur("background").waarde)
        self.assertEqual(
            ("Aptos Display", "sans-serif"),
            resolved.typografie.heading,
        )
        self.assertEqual(("Aptos", "sans-serif"), resolved.typografie.body)
        self.assertEqual(
            ("JetBrains Mono", "monospace"),
            resolved.typografie.mono,
        )
        self.assertEqual("local-only", resolved.typografie.levering)

    def test_bewaart_normatieve_paletrolvolgorde(self):
        resolved = resolveer_thema(self.model.objecten, "beckeringh-palace")

        self.assertEqual(
            ("primary", "background", "foreground", "accent"),
            tuple(rol for rol, _ in resolved.palet.kleuren),
        )

    def test_resolutie_is_onafhankelijk_van_bronvolgorde(self):
        omgekeerd = tuple(reversed(self.model.objecten))

        self.assertEqual(
            resolveer_thema(self.model.objecten, "beckeringh-palace"),
            resolveer_thema(omgekeerd, "beckeringh-palace"),
        )

    def test_resolveert_werelden_in_stabiele_id_volgorde(self):
        tweede_bron = BRON + '''
wereld archive-forge {
    naam: "Archive Forge"
    doel: "Tweede expliciete ontwerpwereld."
    thema: "forge"
}
'''
        model = analyseer(parseer(tweede_bron), constraints=WORLD_MODEL_CONSTRAINTS)

        self.assertEqual(
            ("archive-forge", "beckeringh-palace"),
            tuple(theme.wereld_id for theme in resolveer_alle_themas(model.objecten)),
        )

    def test_kiest_nooit_impliciet_een_wereld(self):
        with self.assertRaisesRegex(
            ThemeResolutionError,
            "ontbrekende wereld 'default'",
        ):
            resolveer_thema(self.model.objecten, "default")


if __name__ == "__main__":
    unittest.main()

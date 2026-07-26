from __future__ import annotations

import unittest

from compiler.parser import parseer
from compiler.product_constraints import WORLD_MODEL_CONSTRAINTS
from compiler.semantic import analyseer
from compiler.theme_resolution import resolveer_thema


BRON = '''
kleur ember-orange {
    naam: "Ember Orange"
    doel: "Accentkleur."
    waarde: "#D86A35"
}
kleur iron-black {
    naam: "Iron Black"
    doel: "Canvas."
    waarde: "#171A1F"
}
kleur smoke-white {
    naam: "Smoke White"
    doel: "Voorgrond."
    waarde: "#ECECEC"
}
palet ember-forge {
    naam: "Ember Forge"
    doel: "Forge-palet."
    primary: "ember-orange"
    background: "iron-black"
    foreground: "smoke-white"
}
typografie forge-interface {
    naam: "Forge Interface"
    doel: "Interface-typografie."
    heading: "Aptos Display"
    body: "Aptos"
    mono: "JetBrains Mono"
}
typeschaal forge-type-scale {
    naam: "Forge Type Scale"
    doel: "Semantische tekstgroottes."
    display: "64px"
    title: "40px"
    heading: "28px"
    body: "16px"
    label: "14px"
    caption: "12px"
}
materiaal forged-iron {
    naam: "Forged Iron"
    doel: "Oppervlaktes van de Forge-wereld."
    canvas: "iron-black"
    surface: "iron-black"
    raised: "iron-black"
    foreground: "smoke-white"
    accent: "ember-orange"
}
border forge-lines {
    naam: "Forge Lines"
    doel: "Randhiërarchie."
    hairline: "1px"
    regular: "2px"
    strong: "4px"
    style: "solid"
}
radius forge-corners {
    naam: "Forge Corners"
    doel: "Hoekhiërarchie."
    small: "4px"
    medium: "12px"
    large: "24px"
    pill: "999px"
}
shadow forge-depth {
    naam: "Forge Depth"
    doel: "Dieptehiërarchie."
    low: "0 1px 2px #00000040"
    medium: "0 4px 12px #00000050"
    high: "0 12px 32px #00000060"
}
motion forge-motion {
    naam: "Forge Motion"
    doel: "Bewegingshiërarchie."
    fast: "120ms"
    normal: "240ms"
    slow: "480ms"
    easing: "cubic-bezier(0.2, 0, 0, 1)"
}
spacing forge-spacing {
    naam: "Forge Spacing"
    doel: "Ruimtelijke schaal."
    none: "0"
    xs: "4px"
    small: "8px"
    medium: "16px"
    large: "24px"
    xl: "40px"
}
thema forge {
    naam: "Forge"
    doel: "Forge-ontwerpidentiteit."
    palet: "ember-forge"
    typografie: "forge-interface"
    typeschaal: "forge-type-scale"
    materiaal: "forged-iron"
    border: "forge-lines"
    radius: "forge-corners"
    shadow: "forge-depth"
    motion: "forge-motion"
    spacing: "forge-spacing"
}
wereld beckeringh-palace {
    naam: "Beckeringh Palace"
    doel: "Digitale ontwerpwereld."
    thema: "forge"
}
'''


class ThemePrimitiveTests(unittest.TestCase):
    def test_resolveert_alle_expliciete_primitieven(self):
        model = analyseer(parseer(BRON), constraints=WORLD_MODEL_CONSTRAINTS)
        thema = resolveer_thema(model.objecten, "beckeringh-palace")

        self.assertEqual("forged-iron", thema.materiaal.id)
        self.assertEqual("#D86A35", thema.materiaal.kleur("accent").waarde)
        self.assertEqual("2px", thema.border.regular)
        self.assertEqual("12px", thema.radius.medium)
        self.assertEqual("0 12px 32px #00000060", thema.shadow.high)
        self.assertEqual("240ms", thema.motion.normal)
        self.assertEqual("cubic-bezier(0.2, 0, 0, 1)", thema.motion.easing)
        self.assertEqual("16px", thema.spacing.medium)
        self.assertEqual("40px", thema.spacing.xl)
        self.assertEqual("64px", thema.typeschaal.display)
        self.assertEqual("12px", thema.typeschaal.caption)

    def test_afwezige_primitieven_worden_niet_verzonnen(self):
        bron = BRON
        for regel in (
            '    materiaal: "forged-iron"\n',
            '    border: "forge-lines"\n',
            '    radius: "forge-corners"\n',
            '    shadow: "forge-depth"\n',
            '    motion: "forge-motion"\n',
            '    spacing: "forge-spacing"\n',
            '    typeschaal: "forge-type-scale"\n',
        ):
            bron = bron.replace(regel, "")
        model = analyseer(parseer(bron), constraints=WORLD_MODEL_CONSTRAINTS)
        thema = resolveer_thema(model.objecten, "beckeringh-palace")

        self.assertIsNone(thema.materiaal)
        self.assertIsNone(thema.border)
        self.assertIsNone(thema.radius)
        self.assertIsNone(thema.shadow)
        self.assertIsNone(thema.motion)
        self.assertIsNone(thema.spacing)
        self.assertIsNone(thema.typeschaal)

    def test_weigert_onbekend_spacingprofiel(self):
        bron = BRON.replace('spacing: "forge-spacing"', 'spacing: "missing-spacing"')
        with self.assertRaises(Exception) as context:
            analyseer(parseer(bron), constraints=WORLD_MODEL_CONSTRAINTS)
        self.assertEqual("BP3613", context.exception.diagnostics[0].code)

    def test_weigert_onbekende_typeschaal(self):
        bron = BRON.replace('typeschaal: "forge-type-scale"', 'typeschaal: "missing-type-scale"')
        with self.assertRaises(Exception) as context:
            analyseer(parseer(bron), constraints=WORLD_MODEL_CONSTRAINTS)
        self.assertEqual("BP3614", context.exception.diagnostics[0].code)


if __name__ == "__main__":
    unittest.main()

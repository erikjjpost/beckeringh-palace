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
thema forge {
    naam: "Forge"
    doel: "Forge-ontwerpidentiteit."
    palet: "ember-forge"
    typografie: "forge-interface"
    materiaal: "forged-iron"
    border: "forge-lines"
    radius: "forge-corners"
    shadow: "forge-depth"
    motion: "forge-motion"
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

    def test_afwezige_primitieven_worden_niet_verzonnen(self):
        bron = BRON
        for regel in (
            '    materiaal: "forged-iron"\n',
            '    border: "forge-lines"\n',
            '    radius: "forge-corners"\n',
            '    shadow: "forge-depth"\n',
            '    motion: "forge-motion"\n',
        ):
            bron = bron.replace(regel, "")
        model = analyseer(parseer(bron), constraints=WORLD_MODEL_CONSTRAINTS)
        thema = resolveer_thema(model.objecten, "beckeringh-palace")

        self.assertIsNone(thema.materiaal)
        self.assertIsNone(thema.border)
        self.assertIsNone(thema.radius)
        self.assertIsNone(thema.shadow)
        self.assertIsNone(thema.motion)


if __name__ == "__main__":
    unittest.main()

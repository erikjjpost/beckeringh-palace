from __future__ import annotations

import unittest

from compiler.backend import Backend, BackendRegistry
from compiler.parser import parseer
from compiler.product_compiler import compileer_producten


BRON = '''
kleur ember-orange {
    naam: "Ember Orange"
    doel: "Primaire accentkleur."
    waarde: "#D86A35"
}
palet ember-forge {
    naam: "Ember Forge"
    doel: "Forge-palet."
    primary: "ember-orange"
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
    doel: "Canonieke ontwerpwereld."
    thema: "forge"
}
product forge-dashboard-html {
    naam: "Forge Dashboard HTML"
    doel: "Theme-aware product."
    backend: "capture"
    layout: "forge-dashboard-ultrawide"
    pad: "output/products/forge-dashboard.html"
    wereld: "beckeringh-palace"
}
'''


class ThemedProductContextTests(unittest.TestCase):
    def test_backend_ontvangt_opgelost_thema_via_productdefinitie(self):
        registry = BackendRegistry()

        def render(objecten, product):
            self.assertIsNotNone(product.thema)
            self.assertEqual("beckeringh-palace", product.wereld)
            self.assertEqual("forge", product.thema.thema_id)
            self.assertEqual("#D86A35", product.thema.palet.kleur("accent").waarde)
            self.assertEqual(
                ("Aptos", "sans-serif"),
                product.thema.typografie.body,
            )
            return product.thema.thema_id

        registry.registreer(Backend("capture", render))
        resultaat = compileer_producten(parseer(BRON), registry)

        self.assertEqual("forge", resultaat[0].inhoud)
        self.assertEqual("forge", resultaat[0].definitie.thema.thema_id)

    def test_legacyproduct_zonder_themalaag_blijft_expliciet_themaloos(self):
        registry = BackendRegistry()
        registry.registreer(Backend(
            "capture",
            lambda objecten, product: "none" if product.thema is None else "theme",
        ))
        bron = '''
product legacy-html {
    naam: "Legacy HTML"
    doel: "Product vóór de themamigratie."
    backend: "capture"
    layout: "legacy-layout"
    pad: "output/products/legacy.html"
}
'''

        resultaat = compileer_producten(parseer(bron), registry)

        self.assertEqual("none", resultaat[0].inhoud)
        self.assertEqual("", resultaat[0].definitie.wereld)


if __name__ == "__main__":
    unittest.main()

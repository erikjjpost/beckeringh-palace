from __future__ import annotations

import unittest

from compiler.parser import parseer
from compiler.product_backends import standaard_backend_registry
from compiler.product_compiler import compileer_producten
from compiler.product_constraints import WORLD_MODEL_CONSTRAINTS
from compiler.semantic import SemantischeFout, analyseer


BRON = '''
component panel {
    naam: "Panel"
    doel: "Testcomponent."
}
compositie dashboard {
    naam: "Dashboard"
    doel: "Testcompositie."
    componenten: ["panel"]
    richting: "row"
}
layout widescreen {
    naam: "Widescreen"
    doel: "Testlayout."
    compositie: "dashboard"
    canvas-width: "1920"
    canvas-height: "1080"
}
regio content {
    naam: "Content"
    doel: "Hoofdregio."
    layout: "widescreen"
    component: "panel"
    x: "0"
    y: "0"
    width: "1920"
    height: "1080"
}
product dashboard-html {
    naam: "Dashboard HTML"
    doel: "Testproduct."
    backend: "html"
    layout: "widescreen"
    pad: "output/products/dashboard.html"
}
'''


class ProductBackendSliceTests(unittest.TestCase):
    def test_compileert_product_via_backendregistry(self):
        model = analyseer(parseer(BRON), constraints=WORLD_MODEL_CONSTRAINTS)
        producten = compileer_producten(model.objecten, standaard_backend_registry())
        self.assertEqual(1, len(producten))
        self.assertEqual("output/products/dashboard.html", producten[0].definitie.pad)
        self.assertIn("<title>Dashboard HTML</title>", producten[0].inhoud)
        self.assertIn("bp-layout-widescreen", producten[0].inhoud)

    def test_weigert_onbekende_backend(self):
        bron = BRON.replace('backend: "html"', 'backend: "figma"')
        with self.assertRaises(SemantischeFout) as context:
            analyseer(parseer(bron), constraints=WORLD_MODEL_CONSTRAINTS)
        self.assertIn("BP3502", {item.code for item in context.exception.diagnostics})

    def test_weigert_onveilig_pad(self):
        bron = BRON.replace(
            'pad: "output/products/dashboard.html"',
            'pad: "../dashboard.html"',
        )
        with self.assertRaises(SemantischeFout) as context:
            analyseer(parseer(bron), constraints=WORLD_MODEL_CONSTRAINTS)
        self.assertIn("BP3504", {item.code for item in context.exception.diagnostics})


if __name__ == "__main__":
    unittest.main()

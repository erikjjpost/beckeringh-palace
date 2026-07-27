from __future__ import annotations

import unittest

from compiler.parser import parseer
from compiler.product_backends import standaard_backend_registry
from compiler.product_compiler import compileer_producten
from compiler.product_constraints import WORLD_MODEL_CONSTRAINTS
from compiler.product_model import verzamel_producten
from compiler.semantic import SemantischeFout, analyseer


BRON = '''
component panel {
    naam: "Panel"
    doel: "Testcomponent."
}
compositie dashboard {
    naam: "Dashboard"
    doel: "Testinhoud."
    instanties: ["dashboard-panel"]
}
componentinstantie dashboard-panel {
    naam: "Dashboard panel"
    doel: "Benoemde testinhoud."
    compositie: "dashboard"
    component: "panel"
}
layout widescreen {
    naam: "Widescreen"
    doel: "Testlayout."
    type: "grid"
    regions: ["content"]
    columns: "1"
    rows: "1"
}
region content {
    naam: "Content"
    doel: "Hoofdregio."
    layout: "widescreen"
    instantie: "dashboard-panel"
    column: "1"
    row: "1"
    column-span: "1"
    row-span: "1"
}
product dashboard-html {
    naam: "Dashboard HTML"
    doel: "Testproduct."
    backend: "html"
    compositie: "dashboard"
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
        self.assertIn('data-instance="dashboard-panel"', producten[0].inhoud)

    def test_html_backend_heeft_geen_layout_fallback(self):
        model = analyseer(parseer(BRON), constraints=WORLD_MODEL_CONSTRAINTS)
        product = verzamel_producten(model.objecten)[0]
        backend = standaard_backend_registry().resolveer(product.backend)

        with self.assertRaisesRegex(
            ValueError,
            "vereist een opgeloste native layout",
        ):
            backend.render(model.objecten, product)

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

    def test_weigert_onbekende_compositie(self):
        bron = BRON.replace(
            'backend: "html"\n    compositie: "dashboard"',
            'backend: "html"\n    compositie: "missing"',
            1,
        )
        with self.assertRaises(SemantischeFout) as context:
            analyseer(parseer(bron), constraints=WORLD_MODEL_CONSTRAINTS)
        self.assertIn("BP3506", {item.code for item in context.exception.diagnostics})

    def test_weigert_verschillende_compositie_en_layoutinhoud(self):
        bron = BRON.replace(
            'instanties: ["dashboard-panel"]',
            'instanties: ["dashboard-panel", "unplaced-panel"]',
            1,
        ).replace(
            "layout widescreen {",
            '''componentinstantie unplaced-panel {
    naam: "Unplaced panel"
    doel: "Niet geplaatste testinhoud."
    compositie: "dashboard"
    component: "panel"
}
layout widescreen {''',
            1,
        )
        with self.assertRaises(SemantischeFout) as context:
            analyseer(parseer(bron), constraints=WORLD_MODEL_CONSTRAINTS)
        self.assertIn("BP3507", {item.code for item in context.exception.diagnostics})


if __name__ == "__main__":
    unittest.main()

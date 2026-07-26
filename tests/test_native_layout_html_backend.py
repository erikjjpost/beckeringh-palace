from __future__ import annotations

import unittest

from compiler.backend import Backend, BackendRegistry
from compiler.layout_model import LayoutType, ResolvedLayout
from compiler.parser import parseer
from compiler.product_backends import standaard_backend_registry
from compiler.product_compiler import compileer_producten
from compiler.product_constraints import WORLD_MODEL_CONSTRAINTS
from compiler.semantic import analyseer


BRON = '''
component panel {
    naam: "Panel"
    doel: "Testcomponent."
}
layout dashboard-grid {
    naam: "Dashboard grid"
    doel: "Plaatst dashboardpanelen."
    type: "grid"
    regions: ["grid-main"]
    columns: "12"
    rows: "4"
}
region grid-main {
    naam: "Grid main"
    doel: "Hoofdinhoud."
    layout: "dashboard-grid"
    component: "panel"
    column: "2"
    row: "1"
    column-span: "10"
    row-span: "4"
}
layout navigation-stack {
    naam: "Navigation stack"
    doel: "Ordent navigatie."
    type: "stack"
    regions: ["stack-main"]
    direction: "vertical"
}
region stack-main {
    naam: "Stack main"
    doel: "Navigatie-inhoud."
    layout: "navigation-stack"
    component: "panel"
}
layout card-flow {
    naam: "Card flow"
    doel: "Laat kaarten doorlopen."
    type: "flow"
    regions: ["flow-main"]
    direction: "horizontal"
    wrap: "true"
}
region flow-main {
    naam: "Flow main"
    doel: "Kaartinhoud."
    layout: "card-flow"
    component: "panel"
}
layout hero-layer {
    naam: "Hero layer"
    doel: "Stapelt hero-inhoud."
    type: "layer"
    regions: ["layer-main"]
}
region layer-main {
    naam: "Layer main"
    doel: "Hero-inhoud."
    layout: "hero-layer"
    component: "panel"
    layer: "3"
}
product grid-html {
    naam: "Grid HTML"
    doel: "Gridproduct."
    backend: "html"
    layout: "dashboard-grid"
    pad: "output/products/grid.html"
}
product stack-html {
    naam: "Stack HTML"
    doel: "Stackproduct."
    backend: "html"
    layout: "navigation-stack"
    pad: "output/products/stack.html"
}
product flow-html {
    naam: "Flow HTML"
    doel: "Flowproduct."
    backend: "html"
    layout: "card-flow"
    pad: "output/products/flow.html"
}
product layer-html {
    naam: "Layer HTML"
    doel: "Layerproduct."
    backend: "html"
    layout: "hero-layer"
    pad: "output/products/layer.html"
}
'''


class NativeLayoutHtmlBackendTests(unittest.TestCase):
    def setUp(self):
        self.model = analyseer(parseer(BRON), constraints=WORLD_MODEL_CONSTRAINTS)

    def test_backend_ontvangt_resolved_layout_via_productcontext(self):
        registry = BackendRegistry()

        def render(_objecten, product):
            self.assertIsInstance(product.opgeloste_layout, ResolvedLayout)
            return product.opgeloste_layout.type.value

        registry.registreer(Backend("html", render))
        producten = compileer_producten(self.model.objecten, registry)

        self.assertEqual(
            {
                "flow-html": LayoutType.FLOW.value,
                "grid-html": LayoutType.GRID.value,
                "layer-html": LayoutType.LAYER.value,
                "stack-html": LayoutType.STACK.value,
            },
            {product.definitie.id: product.inhoud for product in producten},
        )

    def test_html_backend_vertaalt_alle_native_layouttypen(self):
        producten = {
            product.definitie.id: product.inhoud
            for product in compileer_producten(
                self.model.objecten,
                standaard_backend_registry(),
            )
        }

        self.assertIn('data-layout-type="grid"', producten["grid-html"])
        self.assertIn(
            "grid-template-columns:repeat(12,minmax(0,1fr))",
            producten["grid-html"],
        )
        self.assertIn(
            'style="grid-column:2 / span 10;grid-row:1 / span 4"',
            producten["grid-html"],
        )
        self.assertIn(
            'style="display:flex;flex-direction:column"',
            producten["stack-html"],
        )
        self.assertIn(
            'style="display:flex;flex-direction:row;flex-wrap:wrap"',
            producten["flow-html"],
        )
        self.assertIn(
            'style="grid-area:1 / 1;z-index:3"',
            producten["layer-html"],
        )

    def test_normatieve_regionvolgorde_bepaalt_de_domvolgorde(self):
        bron = BRON.replace(
            'regions: ["stack-main"]',
            'regions: ["stack-second", "stack-main"]',
            1,
        ).replace(
            "region stack-main {",
            '''region stack-second {
    naam: "Stack second"
    doel: "Eerste DOM-region."
    layout: "navigation-stack"
    component: "panel"
}
region stack-main {''',
            1,
        )
        model = analyseer(parseer(bron), constraints=WORLD_MODEL_CONSTRAINTS)
        producten = {
            product.definitie.id: product.inhoud
            for product in compileer_producten(
                model.objecten,
                standaard_backend_registry(),
            )
        }

        html = producten["stack-html"]
        self.assertLess(
            html.index('data-region="stack-second"'),
            html.index('data-region="stack-main"'),
        )


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import unittest

from compiler.layout_model import LayoutDirection, LayoutType, resolveer_layouts
from compiler.parser import parseer
from compiler.product_constraints import WORLD_MODEL_CONSTRAINTS
from compiler.renderers import naar_json
from compiler.semantic import SemantischeFout, analyseer


COMPONENT = '''
component panel {
    naam: "Panel"
    doel: "Testcomponent."
}
'''

LAYOUTS = COMPONENT + '''
layout grid-layout {
    naam: "Grid"
    doel: "Plaatst inhoud in cellen."
    type: "grid"
    regions: ["grid-main"]
    columns: "12"
    rows: "4"
}
region grid-main {
    naam: "Grid main"
    doel: "Hoofdinhoud."
    layout: "grid-layout"
    component: "panel"
    column: "2"
    row: "1"
    column-span: "10"
    row-span: "4"
}
layout stack-layout {
    naam: "Stack"
    doel: "Ordent inhoud langs één as."
    type: "stack"
    regions: ["stack-main"]
    direction: "vertical"
}
region stack-main {
    naam: "Stack main"
    doel: "Eerste stackonderdeel."
    layout: "stack-layout"
    component: "panel"
}
layout flow-layout {
    naam: "Flow"
    doel: "Laat inhoud gecontroleerd doorlopen."
    type: "flow"
    regions: ["flow-main"]
    direction: "horizontal"
    wrap: "true"
}
region flow-main {
    naam: "Flow main"
    doel: "Eerste flowonderdeel."
    layout: "flow-layout"
    component: "panel"
}
layout layer-layout {
    naam: "Layer"
    doel: "Legt inhoud in expliciete lagen."
    type: "layer"
    regions: ["layer-main"]
}
region layer-main {
    naam: "Layer main"
    doel: "Onderste laag."
    layout: "layer-layout"
    component: "panel"
    layer: "0"
}
'''


class NativeLayoutModelTests(unittest.TestCase):
    def test_parseert_valideert_en_resolveert_alle_layouttypen(self):
        model = analyseer(parseer(LAYOUTS), constraints=WORLD_MODEL_CONSTRAINTS)
        layouts = resolveer_layouts(model.objecten)

        self.assertEqual(
            (LayoutType.FLOW, LayoutType.GRID, LayoutType.LAYER, LayoutType.STACK),
            tuple(layout.type for layout in layouts),
        )
        grid = next(layout for layout in layouts if layout.type is LayoutType.GRID)
        self.assertEqual((12, 4), (grid.columns, grid.rows))
        self.assertEqual((2, 10), (grid.regions[0].column, grid.regions[0].column_span))
        stack = next(layout for layout in layouts if layout.type is LayoutType.STACK)
        self.assertEqual(LayoutDirection.VERTICAL, stack.direction)
        flow = next(layout for layout in layouts if layout.type is LayoutType.FLOW)
        self.assertIs(flow.wrap, True)
        layer = next(layout for layout in layouts if layout.type is LayoutType.LAYER)
        self.assertEqual(0, layer.regions[0].layer)

    def test_cir_behoudt_layoutintentie_zonder_backendvelden(self):
        model = analyseer(parseer(LAYOUTS), constraints=WORLD_MODEL_CONSTRAINTS)
        cir = naar_json(model.objecten)
        self.assertIn('"type": "grid"', cir)
        self.assertIn('"column-span": "10"', cir)
        self.assertNotIn('"display"', cir)
        self.assertNotIn('"position"', cir)

    def test_weigert_onbekend_layouttype_met_bronlocatie(self):
        bron = LAYOUTS.replace('type: "grid"', 'type: "matrix"', 1)
        with self.assertRaises(SemantischeFout) as context:
            analyseer(parseer(bron, bron="layout.bp"), constraints=WORLD_MODEL_CONSTRAINTS)
        diagnostic = next(item for item in context.exception.diagnostics if item.code == "BP3601")
        self.assertEqual("layout.bp", diagnostic.locatie.bron)

    def test_weigert_ontbrekende_expliciete_flow_wrap(self):
        bron = LAYOUTS.replace('    wrap: "true"\n', "", 1)
        with self.assertRaises(SemantischeFout) as context:
            analyseer(parseer(bron), constraints=WORLD_MODEL_CONSTRAINTS)
        self.assertIn("BP3608", {item.code for item in context.exception.diagnostics})

    def test_weigert_region_die_niet_in_layout_staat(self):
        bron = LAYOUTS.replace('regions: ["stack-main"]', "regions: []", 1)
        with self.assertRaises(SemantischeFout) as context:
            analyseer(parseer(bron), constraints=WORLD_MODEL_CONSTRAINTS)
        self.assertIn("BP3612", {item.code for item in context.exception.diagnostics})

    def test_weigert_grid_region_buiten_layout(self):
        bron = LAYOUTS.replace('column-span: "10"', 'column-span: "12"', 1)
        with self.assertRaises(SemantischeFout) as context:
            analyseer(parseer(bron), constraints=WORLD_MODEL_CONSTRAINTS)
        self.assertIn("BP3616", {item.code for item in context.exception.diagnostics})

    def test_weigert_layout_zonder_native_type(self):
        bron = COMPONENT + '''
layout legacy-canvas {
    naam: "Legacy canvas"
    doel: "Verwijderd M6-contract."
}
'''
        with self.assertRaises(SemantischeFout) as context:
            analyseer(parseer(bron), constraints=WORLD_MODEL_CONSTRAINTS)
        self.assertIn("BP3601", {item.code for item in context.exception.diagnostics})


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import unittest

from compiler.parser import parseer
from compiler.product_constraints import WORLD_MODEL_CONSTRAINTS
from compiler.semantic import SemantischeFout, analyseer
from compiler.spatial_html_renderer import naar_spatial_html
from compiler.spatial_model import bouw_spatial_model


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
    x: "100"
    y: "100"
    width: "1720"
    height: "880"
}
'''


class SpatialSliceTests(unittest.TestCase):
    def test_bouwt_spatial_model_en_html(self):
        model = analyseer(parseer(BRON), constraints=WORLD_MODEL_CONSTRAINTS)
        layouts = bouw_spatial_model(model.objecten)
        self.assertEqual((1920, 1080), (layouts[0].canvas_width, layouts[0].canvas_height))
        self.assertEqual("content", layouts[0].regions[0].id)
        html = naar_spatial_html(model.objecten)
        self.assertIn('style="width:1920px;height:1080px"', html)
        self.assertIn('style="left:100px;top:100px;width:1720px;height:880px"', html)

    def test_weigert_onbekende_compositie(self):
        bron = BRON.replace('compositie: "dashboard"', 'compositie: "missing"')
        with self.assertRaises(SemantischeFout) as context:
            analyseer(parseer(bron), constraints=WORLD_MODEL_CONSTRAINTS)
        self.assertIn("BP3402", {item.code for item in context.exception.diagnostics})

    def test_weigert_regio_buiten_canvas(self):
        bron = BRON.replace('width: "1720"', 'width: "1900"')
        with self.assertRaises(SemantischeFout) as context:
            analyseer(parseer(bron), constraints=WORLD_MODEL_CONSTRAINTS)
        self.assertIn("BP3416", {item.code for item in context.exception.diagnostics})

    def test_spatial_model_negeert_native_layout_explicit(self):
        bron = BRON + '''
layout native-stack {
    naam: "Native stack"
    doel: "Native M9-contract."
    type: "stack"
    regions: ["native-content"]
    direction: "vertical"
}
region native-content {
    naam: "Native content"
    doel: "Native M9-region."
    layout: "native-stack"
    component: "panel"
}
'''
        model = analyseer(parseer(bron), constraints=WORLD_MODEL_CONSTRAINTS)

        self.assertEqual(
            ("widescreen",),
            tuple(layout.id for layout in bouw_spatial_model(model.objecten)),
        )


if __name__ == "__main__":
    unittest.main()

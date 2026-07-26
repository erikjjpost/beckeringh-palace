from __future__ import annotations

import unittest

from compiler.composition_css_renderer import naar_compositie_css
from compiler.composition_html_renderer import naar_compositie_html
from compiler.composition_svg_renderer import naar_compositie_svg
from compiler.parser import parseer
from compiler.product_constraints import WORLD_MODEL_CONSTRAINTS
from compiler.semantic import SemantischeFout, analyseer

BRON = '''
component forge-panel {
    naam: "Forge Panel"
    doel: "Basispaneel."
}
compositie dashboard {
    naam: "Dashboard"
    doel: "Productsamenstelling."
    componenten: ["forge-panel", "forge-panel"]
    richting: "row"
}
'''


class CompositionSliceTests(unittest.TestCase):
    def test_compileert_compositie_naar_css_html_en_svg(self):
        model = analyseer(parseer(BRON), constraints=WORLD_MODEL_CONSTRAINTS)
        self.assertIn("flex-direction: row", naar_compositie_css(model.objecten))
        html = naar_compositie_html(model.objecten)
        self.assertEqual(2, html.count('data-component="forge-panel"'))
        self.assertIn('class="bp-composition bp-dashboard"', html)
        svg = naar_compositie_svg(model.objecten)
        self.assertEqual(2, svg.count('data-component="forge-panel"'))

    def test_weigert_onbekend_component(self):
        with self.assertRaises(SemantischeFout) as context:
            analyseer(parseer(BRON.replace('"forge-panel", "forge-panel"', '"missing"')), constraints=WORLD_MODEL_CONSTRAINTS)
        self.assertEqual("BP3303", context.exception.diagnostics[0].code)

    def test_weigert_ongeldige_richting(self):
        with self.assertRaises(SemantischeFout) as context:
            analyseer(parseer(BRON.replace('richting: "row"', 'richting: "diagonal"')), constraints=WORLD_MODEL_CONSTRAINTS)
        self.assertEqual("BP3304", context.exception.diagnostics[0].code)

    def test_weigert_lege_componentlijst(self):
        with self.assertRaises(SemantischeFout) as context:
            analyseer(parseer(BRON.replace('["forge-panel", "forge-panel"]', '[]')), constraints=WORLD_MODEL_CONSTRAINTS)
        self.assertEqual("BP3302", context.exception.diagnostics[0].code)


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import unittest

from compiler.component_css_renderer import naar_component_css
from compiler.component_html_renderer import naar_component_html
from compiler.parser import parseer
from compiler.product_constraints import WORLD_MODEL_CONSTRAINTS
from compiler.semantic import SemantischeFout, analyseer


BRON = '''
token color-iron {
    naam: "Iron"
    doel: "Surface."
    type: "color"
    waarde: "#171A1F"
}

token spacing-unit {
    naam: "Spacing"
    doel: "Padding."
    type: "dimension"
    waarde: "8px"
}

component forge-panel {
    naam: "Forge Panel"
    doel: "Basispaneel."
    surface: "{color-iron}"
    padding: "{spacing-unit}"
}
'''


class ComponentSliceTests(unittest.TestCase):
    def test_compileert_component_naar_css_en_html(self):
        model = analyseer(parseer(BRON), constraints=WORLD_MODEL_CONSTRAINTS)
        self.assertEqual(
            "/* Gegenereerd door Beckeringh Palace. Niet handmatig wijzigen. */\n"
            ".bp-forge-panel {\n"
            "  background-color: var(--bp-color-iron);\n"
            "  padding: var(--bp-spacing-unit);\n"
            "}\n",
            naar_component_css(model.objecten),
        )
        html = naar_component_html(model.objecten)
        self.assertIn('class="bp-forge-panel"', html)
        self.assertIn("<h2>Forge Panel</h2>", html)

    def test_weigert_onbekende_componenteigenschap(self):
        bron = BRON.replace('    padding: "{spacing-unit}"', '    schaduw: "{spacing-unit}"')
        with self.assertRaises(SemantischeFout) as context:
            analyseer(parseer(bron), constraints=WORLD_MODEL_CONSTRAINTS)
        self.assertEqual("BP3201", context.exception.diagnostics[0].code)

    def test_weigert_letterlijke_componentwaarde(self):
        bron = BRON.replace('surface: "{color-iron}"', 'surface: "#171A1F"')
        with self.assertRaises(SemantischeFout) as context:
            analyseer(parseer(bron), constraints=WORLD_MODEL_CONSTRAINTS)
        self.assertEqual("BP3202", context.exception.diagnostics[0].code)

    def test_weigert_token_van_verkeerd_type(self):
        bron = BRON.replace('surface: "{color-iron}"', 'surface: "{spacing-unit}"')
        with self.assertRaises(SemantischeFout) as context:
            analyseer(parseer(bron), constraints=WORLD_MODEL_CONSTRAINTS)
        self.assertEqual("BP3204", context.exception.diagnostics[0].code)


if __name__ == "__main__":
    unittest.main()

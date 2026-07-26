from __future__ import annotations

import unittest

from compiler.css_renderer import naar_css
from compiler.parser import parseer
from compiler.product_constraints import WORLD_MODEL_CONSTRAINTS
from compiler.semantic import SemantischeFout, analyseer


class NativeProductSliceTests(unittest.TestCase):
    def test_compileert_tokens_deterministisch_naar_css(self):
        model = analyseer(parseer('''
token spacing-unit {
    naam: "Spacing unit"
    doel: "Basiseenheid."
    waarde: "8px"
}

token color-ember {
    naam: "Ember"
    doel: "Accentkleur."
    waarde: "#D86A35"
}
'''), constraints=WORLD_MODEL_CONSTRAINTS)

        self.assertEqual(
            "/* Gegenereerd door Beckeringh Palace. Niet handmatig wijzigen. */\n"
            ":root {\n"
            "  --bp-color-ember: #D86A35;\n"
            "  --bp-spacing-unit: 8px;\n"
            "}\n",
            naar_css(model.objecten),
        )

    def test_weigert_onbekende_objectsoort(self):
        with self.assertRaises(SemantischeFout) as context:
            analyseer(parseer('''
applicatiecomponent portal {
    naam: "Portal"
    doel: "Niet native."
}
'''), constraints=WORLD_MODEL_CONSTRAINTS)

        self.assertEqual("BP3001", context.exception.diagnostics[0].code)

    def test_native_object_vereist_naam_en_doel(self):
        with self.assertRaises(SemantischeFout) as context:
            analyseer(parseer('''
token color-ember {
    waarde: "#D86A35"
}
'''), constraints=WORLD_MODEL_CONSTRAINTS)

        self.assertEqual(
            ["BP3002", "BP3002"],
            [diagnostic.code for diagnostic in context.exception.diagnostics],
        )


if __name__ == "__main__":
    unittest.main()

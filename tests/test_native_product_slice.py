from __future__ import annotations

import unittest

from compiler.css_renderer import naar_css
from compiler.parser import parseer
from compiler.product_constraints import WORLD_MODEL_CONSTRAINTS
from compiler.semantic import SemantischeFout, analyseer
from compiler.token_json_renderer import naar_token_json


class NativeProductSliceTests(unittest.TestCase):
    def test_compileert_getypeerde_tokens_deterministisch(self):
        model = analyseer(parseer('''
token spacing-unit {
    naam: "Spacing unit"
    doel: "Basiseenheid."
    type: "dimension"
    waarde: "8px"
}

token color-accent {
    naam: "Accent"
    doel: "Semantische accentkleur."
    type: "color"
    waarde: "{color-ember}"
}

token color-ember {
    naam: "Ember"
    doel: "Accentkleur."
    type: "color"
    waarde: "#D86A35"
}
'''), constraints=WORLD_MODEL_CONSTRAINTS)

        self.assertEqual(
            "/* Gegenereerd door Beckeringh Palace. Niet handmatig wijzigen. */\n"
            ":root {\n"
            "  --bp-color-accent: var(--bp-color-ember);\n"
            "  --bp-color-ember: #D86A35;\n"
            "  --bp-spacing-unit: 8px;\n"
            "}\n",
            naar_css(model.objecten),
        )
        token_json = naar_token_json(model.objecten)
        self.assertIn('"color-accent"', token_json)
        self.assertIn('"value": "{color-ember}"', token_json)
        self.assertIn('"type": "dimension"', token_json)

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
    type: "color"
    waarde: "#D86A35"
}
'''), constraints=WORLD_MODEL_CONSTRAINTS)

        self.assertEqual(
            ["BP3002", "BP3002"],
            [diagnostic.code for diagnostic in context.exception.diagnostics],
        )

    def test_weigert_onbekend_token_type(self):
        with self.assertRaises(SemantischeFout) as context:
            analyseer(parseer('''
token color-ember {
    naam: "Ember"
    doel: "Accentkleur."
    type: "paint"
    waarde: "#D86A35"
}
'''), constraints=WORLD_MODEL_CONSTRAINTS)
        self.assertEqual("BP3101", context.exception.diagnostics[0].code)

    def test_weigert_ongeldige_waarde_voor_type(self):
        with self.assertRaises(SemantischeFout) as context:
            analyseer(parseer('''
token spacing-unit {
    naam: "Spacing"
    doel: "Basiseenheid."
    type: "dimension"
    waarde: "acht pixels"
}
'''), constraints=WORLD_MODEL_CONSTRAINTS)
        self.assertEqual("BP3105", context.exception.diagnostics[0].code)

    def test_weigert_onbekende_tokenreferentie(self):
        with self.assertRaises(SemantischeFout) as context:
            analyseer(parseer('''
token color-accent {
    naam: "Accent"
    doel: "Semantische kleur."
    type: "color"
    waarde: "{color-missing}"
}
'''), constraints=WORLD_MODEL_CONSTRAINTS)
        self.assertEqual("BP3103", context.exception.diagnostics[0].code)

    def test_weigert_referentie_naar_ander_type(self):
        with self.assertRaises(SemantischeFout) as context:
            analyseer(parseer('''
token spacing-unit {
    naam: "Spacing"
    doel: "Basiseenheid."
    type: "dimension"
    waarde: "8px"
}

token color-accent {
    naam: "Accent"
    doel: "Semantische kleur."
    type: "color"
    waarde: "{spacing-unit}"
}
'''), constraints=WORLD_MODEL_CONSTRAINTS)
        self.assertEqual("BP3104", context.exception.diagnostics[0].code)


if __name__ == "__main__":
    unittest.main()

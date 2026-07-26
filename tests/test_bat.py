from __future__ import annotations

import unittest

from compiler.parser import BATFout, parseer
from compiler.product_constraints import WORLD_MODEL_CONSTRAINTS
from compiler.renderers import naar_markdown
from compiler.semantic import SemantischeFout, analyseer


GELDIG = '''
capability informatiebeheer {
    naam: "Informatiebeheer"
    doel: "Informatie beheersen."
    levert: ["Vindbaarheid", "Betrouwbaarheid"]
}
'''


class BATTests(unittest.TestCase):
    def test_parseert_nederlandse_bron_naar_cir(self):
        objecten = parseer(GELDIG)
        self.assertEqual(1, len(objecten))
        self.assertEqual("capability", objecten[0].soort)
        self.assertEqual("informatiebeheer", objecten[0].id)
        self.assertEqual(["Vindbaarheid", "Betrouwbaarheid"], objecten[0].eigenschappen["levert"])

    def test_renderer_leest_cir(self):
        resultaat = naar_markdown(parseer(GELDIG))
        self.assertIn("# Beckeringh Architectuurmodel", resultaat)
        self.assertIn("## Informatiebeheer", resultaat)

    def test_parser_accepteert_domeinvelden_los_van_semantiek(self):
        objecten = parseer("token color-ember {\nwaarde: \"#D86A35\"\n}")
        self.assertEqual("token", objecten[0].soort)
        self.assertNotIn("naam", objecten[0].eigenschappen)

    def test_semantiek_weigert_ontbrekende_native_velden(self):
        with self.assertRaises(SemantischeFout) as context:
            analyseer(
                parseer("token color-ember {\ntype: \"color\"\nwaarde: \"#D86A35\"\n}"),
                constraints=WORLD_MODEL_CONSTRAINTS,
            )
        self.assertEqual(
            ["BP3002", "BP3002"],
            [diagnostic.code for diagnostic in context.exception.diagnostics],
        )

    def test_weigert_dubbele_ids(self):
        with self.assertRaisesRegex(BATFout, "Dubbele object-id"):
            parseer(GELDIG + GELDIG)

    def test_parser_accepteert_onbekende_soort_voor_semantische_validatie(self):
        objecten = parseer('gebouw paleis {\nnaam: "Paleis"\ndoel: "Test"\n}')
        self.assertEqual("gebouw", objecten[0].soort)

    def test_semantiek_weigert_onbekende_soort(self):
        with self.assertRaises(SemantischeFout) as context:
            analyseer(
                parseer('gebouw paleis {\nnaam: "Paleis"\ndoel: "Test"\n}'),
                constraints=WORLD_MODEL_CONSTRAINTS,
            )
        self.assertEqual("BP3001", context.exception.diagnostics[0].code)


if __name__ == "__main__":
    unittest.main()

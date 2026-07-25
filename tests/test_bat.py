from __future__ import annotations

import unittest

from compiler.parser import BATFout, parseer
from compiler.renderers import naar_markdown


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

    def test_verplicht_naam_en_doel(self):
        with self.assertRaisesRegex(BATFout, "vereist de eigenschappen"):
            parseer("capability fout {\nnaam: Fout\n}")

    def test_weigert_dubbele_ids(self):
        with self.assertRaisesRegex(BATFout, "Dubbele object-id"):
            parseer(GELDIG + GELDIG)

    def test_weigert_onbekende_soort(self):
        with self.assertRaises(BATFout):
            parseer('gebouw paleis {\nnaam: "Paleis"\ndoel: "Test"\n}')


if __name__ == "__main__":
    unittest.main()

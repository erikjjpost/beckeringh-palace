from __future__ import annotations

import unittest

from compiler.cir import Architectuurobject
from compiler.parser import parseer
from compiler.semantic import SemantischeFout, analyseer


class SemanticCoreTests(unittest.TestCase):
    def test_bouwt_symbolentabel(self):
        model = analyseer(parseer('''
capability informatiebeheer {
    naam: "Informatiebeheer"
    doel: "Informatie beheersen."
}

dienst architectuur-synchronisatie {
    naam: "Architectuur Synchronisatie"
    doel: "Architectuur representaties synchroniseren."
    ondersteunt: informatiebeheer
}
'''))

        self.assertEqual(
            ["architectuur-synchronisatie", "informatiebeheer"],
            sorted(model.symbolen),
        )
        self.assertEqual(2, len(model.objecten))

    def test_accepteert_lijst_met_referenties(self):
        model = analyseer(parseer('''
capability informatiebeheer {
    naam: "Informatiebeheer"
    doel: "Informatie beheersen."
}

capability second-brain {
    naam: "Second Brain"
    doel: "Kennis bruikbaar maken."
    afhankelijk_van: [informatiebeheer]
}
'''))

        self.assertIn("second-brain", model.symbolen)

    def test_weigert_onbekende_referentie(self):
        with self.assertRaisesRegex(
            SemantischeFout,
            "Onbekende referentie 'niet-bestaand' in second-brain.afhankelijk_van",
        ):
            analyseer(parseer('''
capability second-brain {
    naam: "Second Brain"
    doel: "Kennis bruikbaar maken."
    afhankelijk_van: niet-bestaand
}
'''))

    def test_weigert_ongeldige_relatievorm(self):
        objecten = [
            Architectuurobject(
                soort="capability",
                id="informatiebeheer",
                eigenschappen={
                    "naam": "Informatiebeheer",
                    "doel": "Informatie beheersen.",
                    "eigenaar": 42,
                },
            )
        ]
        with self.assertRaisesRegex(SemantischeFout, "Een relatie moet"):
            analyseer(objecten)

    def test_diagnostic_bevat_bronlocatie_en_code(self):
        with self.assertRaises(SemantischeFout) as context:
            analyseer(parseer('''
capability second-brain {
    naam: "Second Brain"
    doel: "Kennis bruikbaar maken."
    afhankelijk_van: niet-bestaand
}
''', bron="architectuur/second-brain.bp"))

        diagnostic = context.exception.diagnostics[0]
        self.assertEqual("BP2102", diagnostic.code)
        self.assertEqual("architectuur/second-brain.bp:5:1", str(diagnostic.locatie))

    def test_verzamelt_meerdere_semantische_fouten(self):
        objecten = [
            Architectuurobject(
                soort="capability",
                id="informatiebeheer",
                eigenschappen={
                    "naam": "Informatiebeheer",
                    "doel": "Informatie beheersen.",
                    "eigenaar": 42,
                    "gebruikt": "niet-bestaand",
                },
            )
        ]

        with self.assertRaises(SemantischeFout) as context:
            analyseer(objecten)

        self.assertEqual(
            ["BP2101", "BP2102"],
            [diagnostic.code for diagnostic in context.exception.diagnostics],
        )


if __name__ == "__main__":
    unittest.main()

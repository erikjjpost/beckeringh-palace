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


if __name__ == "__main__":
    unittest.main()

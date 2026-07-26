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

    def test_compileert_geresolveerde_relaties_naar_dependency_graph(self):
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
''', bron="architectuur/capabilities.bp"))

        self.assertEqual(
            ("informatiebeheer", "second-brain"),
            model.dependency_graph.knopen,
        )
        relatie = model.dependency_graph.relaties[0]
        self.assertEqual("second-brain", relatie.bron_id)
        self.assertEqual("afhankelijk_van", relatie.relatietype)
        self.assertEqual("informatiebeheer", relatie.doel_id)
        self.assertEqual("architectuur/capabilities.bp:10:1", str(relatie.locatie))

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

    def test_accepteert_getypeerde_eigenaarrelatie(self):
        model = analyseer(parseer('''
agent erik {
    naam: "Erik"
    doel: "Architectuur beheren."
}

capability informatiebeheer {
    naam: "Informatiebeheer"
    doel: "Informatie beheersen."
    eigenaar: erik
}
'''))

        relatie = model.dependency_graph.relaties[0]
        self.assertEqual("eigenaar", relatie.relatietype)
        self.assertEqual("erik", relatie.doel_id)

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

    def test_weigert_verkeerd_brontype(self):
        with self.assertRaises(SemantischeFout) as context:
            analyseer(parseer('''
capability informatiebeheer {
    naam: "Informatiebeheer"
    doel: "Informatie beheersen."
}

capability second-brain {
    naam: "Second Brain"
    doel: "Kennis bruikbaar maken."
    ondersteunt: informatiebeheer
}
''', bron="architectuur/types.bp"))

        diagnostic = context.exception.diagnostics[0]
        self.assertEqual("BP2301", diagnostic.code)
        self.assertEqual(
            "Relatie 'ondersteunt' verwacht als bron dienst, "
            "maar 'second-brain' is capability",
            diagnostic.boodschap,
        )
        self.assertEqual("architectuur/types.bp:10:1", str(diagnostic.locatie))

    def test_weigert_verkeerd_doeltype(self):
        with self.assertRaises(SemantischeFout) as context:
            analyseer(parseer('''
agent erik {
    naam: "Erik"
    doel: "Architectuur beheren."
}

dienst architectuur-synchronisatie {
    naam: "Architectuur Synchronisatie"
    doel: "Architectuur representaties synchroniseren."
    ondersteunt: erik
}
'''))

        diagnostic = context.exception.diagnostics[0]
        self.assertEqual("BP2302", diagnostic.code)
        self.assertEqual(
            "Relatie 'ondersteunt' verwacht als doel capability, "
            "maar 'erik' is agent",
            diagnostic.boodschap,
        )

    def test_weigert_verkeerd_eigenaartype(self):
        with self.assertRaises(SemantischeFout) as context:
            analyseer(parseer('''
capability eigenaar-capability {
    naam: "Eigenaar capability"
    doel: "Testdoel."
}

capability informatiebeheer {
    naam: "Informatiebeheer"
    doel: "Informatie beheersen."
    eigenaar: eigenaar-capability
}
'''))

        self.assertEqual("BP2302", context.exception.diagnostics[0].code)

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

    def test_weigert_cyclische_afhankelijkheid(self):
        with self.assertRaises(SemantischeFout) as context:
            analyseer(parseer('''
capability alpha {
    naam: "Alpha"
    doel: "Alpha leveren."
    afhankelijk_van: beta
}

capability beta {
    naam: "Beta"
    doel: "Beta leveren."
    afhankelijk_van: alpha
}
''', bron="architectuur/cyclus.bp"))

        diagnostic = context.exception.diagnostics[0]
        self.assertEqual("BP2201", diagnostic.code)
        self.assertEqual(
            "Cyclische relatie 'afhankelijk_van': alpha -> beta -> alpha",
            diagnostic.boodschap,
        )
        self.assertEqual("architectuur/cyclus.bp:11:1", str(diagnostic.locatie))

    def test_laat_cycli_toe_voor_niet_acyclische_relaties(self):
        model = analyseer(parseer('''
agent alpha {
    naam: "Alpha"
    doel: "Alpha vertegenwoordigen."
    gebruikt: beta
}

agent beta {
    naam: "Beta"
    doel: "Beta vertegenwoordigen."
    gebruikt: alpha
}
'''))

        self.assertEqual(2, len(model.dependency_graph.relaties))


if __name__ == "__main__":
    unittest.main()

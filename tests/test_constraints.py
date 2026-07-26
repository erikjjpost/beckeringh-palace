from __future__ import annotations

import unittest
from dataclasses import dataclass

from compiler.constraints import ConstraintContext, evalueer_constraints
from compiler.diagnostics import Diagnostic
from compiler.parser import parseer
from compiler.semantic import SemantischeFout, analyseer


@dataclass(frozen=True)
class TestConstraint:
    sleutel: str
    code: str
    boodschap: str

    def evalueer(self, context: ConstraintContext):
        locatie = context.objecten[0].bronlocatie if context.objecten else None
        return (Diagnostic(code=self.code, boodschap=self.boodschap, locatie=locatie),)


class ConstraintEngineTests(unittest.TestCase):
    def test_evalueert_constraints_in_stabiele_sleutelvolgorde(self):
        model = analyseer(parseer('''
capability informatiebeheer {
    naam: "Informatiebeheer"
    doel: "Informatie beheersen."
}
'''))
        context = ConstraintContext(
            objecten=model.objecten,
            symbolen=model.symbolen,
            dependency_graph=model.dependency_graph,
        )

        diagnostics = evalueer_constraints(
            context,
            (
                TestConstraint("z-laatste", "BP9002", "Tweede"),
                TestConstraint("a-eerste", "BP9001", "Eerste"),
            ),
        )

        self.assertEqual(
            ["BP9001", "BP9002"],
            [diagnostic.code for diagnostic in diagnostics],
        )

    def test_weigert_dubbele_constraintsleutels(self):
        model = analyseer(parseer('''
capability informatiebeheer {
    naam: "Informatiebeheer"
    doel: "Informatie beheersen."
}
'''))
        context = ConstraintContext(
            objecten=model.objecten,
            symbolen=model.symbolen,
            dependency_graph=model.dependency_graph,
        )

        with self.assertRaisesRegex(ValueError, "unieke sleutel"):
            evalueer_constraints(
                context,
                (
                    TestConstraint("zelfde", "BP9001", "Eerste"),
                    TestConstraint("zelfde", "BP9002", "Tweede"),
                ),
            )

    def test_semantische_compiler_verzamelt_constraintdiagnostics(self):
        constraints = (
            TestConstraint("b-tweede", "BP9002", "Tweede constraint"),
            TestConstraint("a-eerste", "BP9001", "Eerste constraint"),
        )

        with self.assertRaises(SemantischeFout) as context:
            analyseer(
                parseer('''
capability informatiebeheer {
    naam: "Informatiebeheer"
    doel: "Informatie beheersen."
}
''', bron="architectuur/constraints.bp"),
                constraints=constraints,
            )

        self.assertEqual(
            ["BP9001", "BP9002"],
            [diagnostic.code for diagnostic in context.exception.diagnostics],
        )
        self.assertEqual(
            "architectuur/constraints.bp:2:1",
            str(context.exception.diagnostics[0].locatie),
        )

    def test_constraints_draaien_niet_op_semantisch_ongeldig_model(self):
        aangeroepen = []

        @dataclass(frozen=True)
        class TrackingConstraint:
            sleutel: str = "tracking"

            def evalueer(self, context: ConstraintContext):
                aangeroepen.append(context)
                return ()

        with self.assertRaises(SemantischeFout) as context:
            analyseer(
                parseer('''
capability second-brain {
    naam: "Second Brain"
    doel: "Kennis bruikbaar maken."
    afhankelijk_van: ontbreekt
}
'''),
                constraints=(TrackingConstraint(),),
            )

        self.assertEqual("BP2102", context.exception.diagnostics[0].code)
        self.assertEqual([], aangeroepen)


if __name__ == "__main__":
    unittest.main()

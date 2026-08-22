from __future__ import annotations

import unittest

from compiler.data_sources import resolveer_databronnen
from compiler.parser import parseer
from compiler.product_constraints import WORLD_MODEL_CONSTRAINTS
from compiler.semantic import SemantischeFout, analyseer


AANTAL_DATABRON = '''
databron cluster-nodes {
    naam: "Node count"
    doel: "Aantal actieve clusternodes."
    expr: "count(kube_node_info)"
    eenheid: "aantal"
}
'''

TEKST_DATABRON_MET_MAPPING = '''
databron cluster-health {
    naam: "Cluster readiness"
    doel: "Of alle clusternodes gereed zijn."
    expr: "count(kube_node_info) == bool count(kube_node_info)"
    eenheid: "tekst"
    mapping: ["1:Healthy", "0:Degraded"]
}
'''


class DataSourceResolutionTests(unittest.TestCase):
    def test_resolveert_aantal_databron(self) -> None:
        model = analyseer(
            parseer(AANTAL_DATABRON), constraints=WORLD_MODEL_CONSTRAINTS
        )
        databronnen = resolveer_databronnen(model.objecten)

        self.assertEqual(1, len(databronnen))
        databron = databronnen[0]
        self.assertEqual("cluster-nodes", databron.id)
        self.assertEqual("count(kube_node_info)", databron.expr)
        self.assertEqual("aantal", databron.eenheid)
        self.assertEqual((), databron.mapping)

    def test_resolveert_tekst_databron_met_mapping(self) -> None:
        model = analyseer(
            parseer(TEKST_DATABRON_MET_MAPPING),
            constraints=WORLD_MODEL_CONSTRAINTS,
        )
        databron = resolveer_databronnen(model.objecten)[0]

        self.assertEqual("tekst", databron.eenheid)
        self.assertEqual(
            (("1", "Healthy"), ("0", "Degraded")),
            tuple((item.waarde, item.label) for item in databron.mapping),
        )


class DataSourceConstraintTests(unittest.TestCase):
    def test_weigert_onbekende_eigenschap(self) -> None:
        bron = AANTAL_DATABRON.replace(
            'eenheid: "aantal"',
            'eenheid: "aantal"\n    extra: "onbekend"',
        )
        with self.assertRaises(SemantischeFout) as context:
            analyseer(parseer(bron), constraints=WORLD_MODEL_CONSTRAINTS)

        self.assertIn("BP4410", {item.code for item in context.exception.diagnostics})

    def test_weigert_onbekende_eenheid(self) -> None:
        bron = AANTAL_DATABRON.replace('eenheid: "aantal"', 'eenheid: "kleur"')
        with self.assertRaises(SemantischeFout) as context:
            analyseer(parseer(bron), constraints=WORLD_MODEL_CONSTRAINTS)

        self.assertIn("BP4412", {item.code for item in context.exception.diagnostics})

    def test_weigert_mapping_zonder_eenheid_tekst(self) -> None:
        bron = AANTAL_DATABRON.replace(
            'eenheid: "aantal"',
            'eenheid: "aantal"\n    mapping: ["1:Ja", "0:Nee"]',
        )
        with self.assertRaises(SemantischeFout) as context:
            analyseer(parseer(bron), constraints=WORLD_MODEL_CONSTRAINTS)

        self.assertIn("BP4413", {item.code for item in context.exception.diagnostics})

    def test_weigert_tekst_databron_zonder_mapping(self) -> None:
        bron = AANTAL_DATABRON.replace('eenheid: "aantal"', 'eenheid: "tekst"')
        with self.assertRaises(SemantischeFout) as context:
            analyseer(parseer(bron), constraints=WORLD_MODEL_CONSTRAINTS)

        self.assertIn("BP4415", {item.code for item in context.exception.diagnostics})

    def test_weigert_ongeldige_mapping_invoer(self) -> None:
        bron = TEKST_DATABRON_MET_MAPPING.replace(
            'mapping: ["1:Healthy", "0:Degraded"]',
            'mapping: ["zonder-scheidingsteken"]',
        )
        with self.assertRaises(SemantischeFout) as context:
            analyseer(parseer(bron), constraints=WORLD_MODEL_CONSTRAINTS)

        self.assertIn("BP4414", {item.code for item in context.exception.diagnostics})


if __name__ == "__main__":
    unittest.main()

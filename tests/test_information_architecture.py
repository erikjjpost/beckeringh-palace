from __future__ import annotations

import unittest

from compiler.design_compositions import resolveer_composities
from compiler.information_architecture import resolveer_informatiegebieden
from compiler.parser import parseer
from compiler.product_constraints import WORLD_MODEL_CONSTRAINTS
from compiler.semantic import SemantischeFout, analyseer


BRON = '''
informatiegebied wereld {
    naam: "Wereld"
    doel: "Wereldinhoud."
    soorten: ["wereld"]
    inhoud: ["palace"]
    navigatie: ["dashboard-html"]
}

wereld palace {
    naam: "Palace"
    doel: "Digitale wereld."
    thema: "forge"
}

component panel {
    naam: "Panel"
    doel: "Informatiepaneel."
}

compositie dashboard {
    naam: "Dashboard"
    doel: "Dashboardinhoud."
    instanties: ["world-panel"]
}

componentinstantie world-panel {
    naam: "Overschreven naam"
    doel: "Overschreven doel."
    compositie: "dashboard"
    component: "panel"
    informatiegebied: "wereld"
}

product dashboard-html {
    naam: "Dashboard HTML"
    doel: "Dashboardproduct."
    backend: "html"
    compositie: "dashboard"
    layout: "dashboard-layout"
    pad: "output/products/dashboard.html"
}

layout dashboard-layout {
    naam: "Dashboardlayout"
    doel: "Testlayout."
    type: "grid"
    regions: ["world-region"]
    columns: "1"
    rows: "1"
}

region world-region {
    naam: "Wereldregio"
    doel: "Testregio."
    layout: "dashboard-layout"
    instantie: "world-panel"
    column: "1"
    row: "1"
    column-span: "1"
    row-span: "1"
}
'''


class InformationArchitectureTests(unittest.TestCase):
    def test_lost_gebied_backendonafhankelijk_op(self):
        model = analyseer(parseer(BRON), constraints=WORLD_MODEL_CONSTRAINTS)

        gebied = resolveer_informatiegebieden(model.objecten)[0]
        instantie = resolveer_composities(model.objecten)[0].instances[0]

        self.assertEqual(("wereld",), gebied.object_kinds)
        self.assertEqual(
            (("palace", "Palace", "wereld", "Digitale wereld."),),
            tuple(
                (anker.id, anker.naam, anker.object_kind, anker.doel)
                for anker in gebied.content_anchors
            ),
        )
        self.assertEqual(
            (("dashboard-html", "Dashboard HTML", "product", "output/products/dashboard.html"),),
            tuple(
                (doel.id, doel.naam, doel.target_kind, doel.artifact_path)
                for doel in gebied.navigation_targets
            ),
        )
        self.assertEqual("wereld", instantie.information_area_id)
        self.assertEqual("Wereld", instantie.naam)
        self.assertEqual("Wereldinhoud.", instantie.doel)
        self.assertEqual("informatiegebied:wereld", instantie.metric_kind)
        self.assertEqual(1, instantie.metric_value)
        self.assertEqual(
            (("wereld", 1),),
            tuple((detail.label, detail.value) for detail in instantie.metric_details),
        )
        self.assertEqual(gebied.navigation_targets, instantie.navigation_targets)
        self.assertEqual(gebied.content_anchors, instantie.content_anchors)

    def test_weigert_onbekend_gebied(self):
        with self.assertRaises(SemantischeFout) as context:
            analyseer(
                parseer(BRON.replace(
                    'informatiegebied: "wereld"',
                    'informatiegebied: "missing"',
                )),
                constraints=WORLD_MODEL_CONSTRAINTS,
            )
        self.assertIn("BP3717", {item.code for item in context.exception.diagnostics})

    def test_weigert_lege_onbekende_en_overlappende_soorten(self):
        varianten = (
            (BRON.replace('soorten: ["wereld"]', "soorten: []"), "BP4002"),
            (
                BRON.replace('soorten: ["wereld"]', 'soorten: ["missing"]'),
                "BP4003",
            ),
            (
                BRON.replace(
                    "wereld palace {",
                    '''informatiegebied dubbel {
    naam: "Dubbel"
    doel: "Overlappend gebied."
    soorten: ["wereld"]
}

wereld palace {''',
                ),
                "BP4004",
            ),
        )
        for bron, code in varianten:
            with self.subTest(code=code):
                with self.assertRaises(SemantischeFout) as context:
                    analyseer(parseer(bron), constraints=WORLD_MODEL_CONSTRAINTS)
                self.assertIn(code, {item.code for item in context.exception.diagnostics})

    def test_weigert_combinatie_met_legacy_metric(self):
        bron = BRON.replace(
            '    informatiegebied: "wereld"',
            '    informatiegebied: "wereld"\n    metric-kind: "wereld"',
        )
        with self.assertRaises(SemantischeFout) as context:
            analyseer(parseer(bron), constraints=WORLD_MODEL_CONSTRAINTS)
        self.assertIn("BP3718", {item.code for item in context.exception.diagnostics})

    def test_weigert_ongeldige_navigatie(self):
        varianten = (
            (BRON.replace('navigatie: ["dashboard-html"]', "navigatie: []"), "BP4005"),
            (
                BRON.replace(
                    'navigatie: ["dashboard-html"]',
                    'navigatie: ["missing"]',
                ),
                "BP4006",
            ),
            (
                BRON.replace(
                    'navigatie: ["dashboard-html"]',
                    'navigatie: ["palace"]',
                ),
                "BP4007",
            ),
            (
                BRON.replace(
                    "wereld palace {",
                    '''informatiegebied dubbel {
    naam: "Dubbel"
    doel: "Dubbele navigatie."
    soorten: ["merk"]
    navigatie: ["dashboard-html"]
}

wereld palace {''',
                ),
                "BP4008",
            ),
        )
        for bron, code in varianten:
            with self.subTest(code=code):
                with self.assertRaises(SemantischeFout) as context:
                    analyseer(parseer(bron), constraints=WORLD_MODEL_CONSTRAINTS)
                self.assertIn(code, {item.code for item in context.exception.diagnostics})

    def test_weigert_ongeldige_inhoudsankers(self):
        varianten = (
            (BRON.replace('inhoud: ["palace"]', "inhoud: []"), "BP4009"),
            (
                BRON.replace('inhoud: ["palace"]', 'inhoud: ["missing"]'),
                "BP4010",
            ),
            (
                BRON.replace('inhoud: ["palace"]', 'inhoud: ["dashboard-html"]'),
                "BP4011",
            ),
            (
                BRON.replace(
                    "wereld palace {",
                    '''informatiegebied dubbel {
    naam: "Dubbel"
    doel: "Dubbele inhoud."
    soorten: ["wereld"]
    inhoud: ["palace"]
    navigatie: ["missing-product"]
}

wereld palace {''',
                ),
                "BP4012",
            ),
        )
        for bron, code in varianten:
            with self.subTest(code=code):
                with self.assertRaises(SemantischeFout) as context:
                    analyseer(parseer(bron), constraints=WORLD_MODEL_CONSTRAINTS)
                self.assertIn(code, {item.code for item in context.exception.diagnostics})


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import unittest

from compiler.design_compositions import resolveer_composities
from compiler.parser import parseer
from compiler.product_constraints import WORLD_MODEL_CONSTRAINTS
from compiler.semantic import SemantischeFout, analyseer


BRON = '''
component forge-panel {
    naam: "Forge Panel"
    doel: "Basispaneel."
}

compositie dashboard {
    naam: "Dashboard"
    doel: "Productsamenstelling."
    instanties: ["dashboard-left", "dashboard-right"]
}

componentinstantie dashboard-left {
    naam: "Linkerpaneel"
    doel: "Linker dashboardinhoud."
    compositie: "dashboard"
    component: "forge-panel"
}

componentinstantie dashboard-right {
    naam: "Rechterpaneel"
    doel: "Rechter dashboardinhoud."
    compositie: "dashboard"
    component: "forge-panel"
}
'''


class NativeCompositionModelTests(unittest.TestCase):
    def test_lost_geordende_componentinstanties_op(self):
        model = analyseer(parseer(BRON), constraints=WORLD_MODEL_CONSTRAINTS)

        compositie = resolveer_composities(model.objecten)[0]

        self.assertEqual("dashboard", compositie.id)
        self.assertEqual(
            ("dashboard-left", "dashboard-right"),
            tuple(instantie.id for instantie in compositie.instances),
        )
        self.assertEqual(
            ("forge-panel", "forge-panel"),
            tuple(instantie.component_id for instantie in compositie.instances),
        )
        self.assertTrue(all(
            instantie.composition_id == "dashboard"
            for instantie in compositie.instances
        ))

    def test_weigert_legacy_layoutvelden(self):
        bron = BRON.replace(
            '    instanties: ["dashboard-left", "dashboard-right"]',
            '    componenten: ["forge-panel"]\n    richting: "row"',
        )
        with self.assertRaises(SemantischeFout) as context:
            analyseer(parseer(bron), constraints=WORLD_MODEL_CONSTRAINTS)

        self.assertEqual(
            ["BP3701", "BP3701", "BP3702", "BP3712", "BP3712"],
            [diagnostic.code for diagnostic in context.exception.diagnostics],
        )

    def test_weigert_dubbele_instantie(self):
        bron = BRON.replace(
            '["dashboard-left", "dashboard-right"]',
            '["dashboard-left", "dashboard-left"]',
        )
        with self.assertRaises(SemantischeFout) as context:
            analyseer(parseer(bron), constraints=WORLD_MODEL_CONSTRAINTS)

        self.assertIn("BP3702", {item.code for item in context.exception.diagnostics})

    def test_weigert_onbekende_instantie(self):
        bron = BRON.replace('"dashboard-right"', '"missing"', 1)
        with self.assertRaises(SemantischeFout) as context:
            analyseer(parseer(bron), constraints=WORLD_MODEL_CONSTRAINTS)

        self.assertIn("BP3703", {item.code for item in context.exception.diagnostics})

    def test_weigert_ontbrekende_wederkerige_referentie(self):
        bron = BRON.replace(
            '    instanties: ["dashboard-left", "dashboard-right"]',
            '    instanties: ["dashboard-left"]',
        )
        with self.assertRaises(SemantischeFout) as context:
            analyseer(parseer(bron), constraints=WORLD_MODEL_CONSTRAINTS)

        self.assertIn("BP3712", {item.code for item in context.exception.diagnostics})

    def test_weigert_instantie_met_verkeerde_compositie(self):
        bron = BRON.replace(
            '    compositie: "dashboard"',
            '    compositie: "missing"',
            1,
        )
        with self.assertRaises(SemantischeFout) as context:
            analyseer(parseer(bron), constraints=WORLD_MODEL_CONSTRAINTS)

        self.assertTrue(
            {"BP3704", "BP3711"}.issubset(
                {item.code for item in context.exception.diagnostics}
            )
        )

    def test_weigert_onbekend_component(self):
        bron = BRON.replace('    component: "forge-panel"', '    component: "missing"', 1)
        with self.assertRaises(SemantischeFout) as context:
            analyseer(parseer(bron), constraints=WORLD_MODEL_CONSTRAINTS)

        self.assertIn("BP3713", {item.code for item in context.exception.diagnostics})

    def test_weigert_onbekend_instantieveld(self):
        bron = BRON.replace(
            '    component: "forge-panel"',
            '    component: "forge-panel"\n    variant: "compact"',
            1,
        )
        with self.assertRaises(SemantischeFout) as context:
            analyseer(parseer(bron), constraints=WORLD_MODEL_CONSTRAINTS)

        self.assertIn("BP3710", {item.code for item in context.exception.diagnostics})


if __name__ == "__main__":
    unittest.main()

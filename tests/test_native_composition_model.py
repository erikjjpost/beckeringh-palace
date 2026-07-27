from __future__ import annotations

import unittest

from compiler.design_compositions import resolveer_composities
from compiler.parser import parseer
from compiler.product_constraints import WORLD_MODEL_CONSTRAINTS
from compiler.semantic import SemantischeFout, analyseer


BRON = '''
appearance panel-default {
    naam: "Default panel"
    doel: "Standaard paneelappearance."
    material: "raised"
    foreground: "foreground"
    accent: "accent"
    border: "regular"
    radius: "medium"
    shadow: "medium"
    motion: "normal"
    spacing: "small"
    heading-style: "heading"
    body-style: "body"
    label-style: "label"
    caption-style: "caption"
}

appearance panel-compact {
    naam: "Compact panel"
    doel: "Compacte paneelappearance."
    material: "raised"
    foreground: "foreground"
    accent: "accent"
    border: "regular"
    radius: "medium"
    shadow: "low"
    motion: "normal"
    spacing: "xs"
    heading-style: "heading"
    body-style: "body"
    label-style: "label"
    caption-style: "caption"
}

component forge-panel {
    naam: "Forge Panel"
    doel: "Basispaneel."
    appearance: "panel-default"
}

variant forge-panel-compact {
    naam: "Compact Forge Panel"
    doel: "Gecontroleerde compacte paneelafwijking."
    component: "forge-panel"
    appearance: "panel-compact"
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
    variant: "forge-panel-compact"
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
        self.assertEqual("forge-panel-compact", compositie.instances[0].variant_id)
        self.assertEqual("panel-compact", compositie.instances[0].appearance_id)
        self.assertIsNone(compositie.instances[1].variant_id)
        self.assertEqual("panel-default", compositie.instances[1].appearance_id)
        self.assertIsNone(compositie.instances[1].metric_kind)
        self.assertIsNone(compositie.instances[1].metric_value)

    def test_resolveert_en_valideert_optionele_modeltelling(self):
        bron = BRON.replace(
            '    component: "forge-panel"\n}',
            '    component: "forge-panel"\n    metric-kind: "component"\n}',
            1,
        )
        model = analyseer(parseer(bron), constraints=WORLD_MODEL_CONSTRAINTS)

        compositie = resolveer_composities(model.objecten)[0]

        self.assertEqual("component", compositie.instances[1].metric_kind)
        self.assertEqual(1, compositie.instances[1].metric_value)

        ongeldig = bron.replace('metric-kind: "component"', 'metric-kind: ""')
        with self.assertRaises(SemantischeFout) as context:
            analyseer(parseer(ongeldig), constraints=WORLD_MODEL_CONSTRAINTS)

        self.assertIn("BP3714", {item.code for item in context.exception.diagnostics})

        onbekend = bron.replace(
            'metric-kind: "component"',
            'metric-kind: "onbekende-soort"',
        )
        with self.assertRaises(SemantischeFout) as context:
            analyseer(parseer(onbekend), constraints=WORLD_MODEL_CONSTRAINTS)

        self.assertIn("BP3715", {item.code for item in context.exception.diagnostics})

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
        bron = BRON.replace(
            '''componentinstantie dashboard-right {
    naam: "Rechterpaneel"
    doel: "Rechter dashboardinhoud."
    compositie: "dashboard"
    component: "forge-panel"''',
            '''componentinstantie dashboard-right {
    naam: "Rechterpaneel"
    doel: "Rechter dashboardinhoud."
    compositie: "dashboard"
    component: "missing"''',
            1,
        )
        with self.assertRaises(SemantischeFout) as context:
            analyseer(parseer(bron), constraints=WORLD_MODEL_CONSTRAINTS)

        self.assertIn("BP3713", {item.code for item in context.exception.diagnostics})

    def test_weigert_onbekende_variant(self):
        bron = BRON.replace(
            '    variant: "forge-panel-compact"',
            '    variant: "missing"',
            1,
        )
        with self.assertRaises(SemantischeFout) as context:
            analyseer(parseer(bron), constraints=WORLD_MODEL_CONSTRAINTS)

        self.assertIn("BP3804", {item.code for item in context.exception.diagnostics})

    def test_weigert_variant_van_ander_component(self):
        bron = BRON.replace(
            '    component: "forge-panel"\n    appearance: "panel-compact"',
            '    component: "other-panel"\n    appearance: "panel-compact"',
            1,
        ).replace(
            'component forge-panel {',
            '''component other-panel {
    naam: "Other Panel"
    doel: "Ander paneel."
    appearance: "panel-default"
}

component forge-panel {''',
            1,
        )
        with self.assertRaises(SemantischeFout) as context:
            analyseer(parseer(bron), constraints=WORLD_MODEL_CONSTRAINTS)

        self.assertIn("BP3805", {item.code for item in context.exception.diagnostics})

    def test_weigert_variant_met_onbekende_appearance(self):
        bron = BRON.replace(
            '    appearance: "panel-compact"',
            '    appearance: "missing"',
            1,
        )
        with self.assertRaises(SemantischeFout) as context:
            analyseer(parseer(bron), constraints=WORLD_MODEL_CONSTRAINTS)

        self.assertIn("BP3803", {item.code for item in context.exception.diagnostics})

    def test_weigert_onbekend_variantveld(self):
        bron = BRON.replace(
            '    appearance: "panel-compact"',
            '    appearance: "panel-compact"\n    padding: "small"',
            1,
        )
        with self.assertRaises(SemantischeFout) as context:
            analyseer(parseer(bron), constraints=WORLD_MODEL_CONSTRAINTS)

        self.assertIn("BP3801", {item.code for item in context.exception.diagnostics})


if __name__ == "__main__":
    unittest.main()

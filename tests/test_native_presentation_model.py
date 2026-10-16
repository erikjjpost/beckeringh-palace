from __future__ import annotations

import unittest

from compiler.parser import parseer
from compiler.presentations import DiaFormaat, resolveer_presentaties
from compiler.product_constraints import WORLD_MODEL_CONSTRAINTS
from compiler.semantic import SemantischeFout, analyseer


BRON = '''
component panel {
    naam: "Panel"
    doel: "Testcomponent."
}
compositie intro-content {
    naam: "Intro inhoud"
    doel: "Testinhoud voor de introdia."
    instanties: ["intro-panel"]
}
componentinstantie intro-panel {
    naam: "Intro paneel"
    doel: "Benoemde introinhoud."
    compositie: "intro-content"
    component: "panel"
}
layout intro-layout {
    naam: "Intro layout"
    doel: "Testlayout voor de introdia."
    type: "grid"
    regions: ["intro-region"]
    columns: "1"
    rows: "1"
}
region intro-region {
    naam: "Introregio"
    doel: "Hoofdregio van de introdia."
    layout: "intro-layout"
    instantie: "intro-panel"
    column: "1"
    row: "1"
    column-span: "1"
    row-span: "1"
}
compositie closing-content {
    naam: "Afsluitende inhoud"
    doel: "Testinhoud voor de slotdia."
    instanties: ["closing-panel"]
}
componentinstantie closing-panel {
    naam: "Slotpaneel"
    doel: "Benoemde slotinhoud."
    compositie: "closing-content"
    component: "panel"
}
layout closing-layout {
    naam: "Slotlayout"
    doel: "Testlayout voor de slotdia."
    type: "grid"
    regions: ["closing-region"]
    columns: "1"
    rows: "1"
}
region closing-region {
    naam: "Slotregio"
    doel: "Hoofdregio van de slotdia."
    layout: "closing-layout"
    instantie: "closing-panel"
    column: "1"
    row: "1"
    column-span: "1"
    row-span: "1"
}
presentatie keynote {
    naam: "Keynote"
    doel: "Ordent de intro- en slotdia."
    dias: ["dia-slot", "dia-intro"]
}
dia dia-slot {
    naam: "Slot"
    doel: "Sluit de presentatie af."
    presentatie: "keynote"
    compositie: "closing-content"
    layout: "closing-layout"
    formaat: "afsluiting"
}
dia dia-intro {
    naam: "Intro"
    doel: "Opent de presentatie."
    presentatie: "keynote"
    compositie: "intro-content"
    layout: "intro-layout"
    formaat: "cover"
}
'''


class NativePresentationModelTests(unittest.TestCase):
    def _diagnostic_codes(self, bron: str) -> set[str]:
        with self.assertRaises(SemantischeFout) as context:
            analyseer(parseer(bron), constraints=WORLD_MODEL_CONSTRAINTS)
        return {
            diagnostic.code
            for diagnostic in context.exception.diagnostics
        }

    def test_parseert_en_valideert_geldige_presentatie(self) -> None:
        model = analyseer(parseer(BRON), constraints=WORLD_MODEL_CONSTRAINTS)

        self.assertIn("presentatie", {obj.soort for obj in model.objecten})
        self.assertIn("dia", {obj.soort for obj in model.objecten})

    def test_resolveert_dias_in_declaratievolgorde_niet_in_id_volgorde(self) -> None:
        model = analyseer(parseer(BRON), constraints=WORLD_MODEL_CONSTRAINTS)

        presentatie = resolveer_presentaties(model.objecten)[0]

        self.assertEqual("keynote", presentatie.id)
        self.assertEqual(
            ("dia-slot", "dia-intro"),
            tuple(dia.id for dia in presentatie.dias),
        )

    def test_elke_dia_hergebruikt_de_gedeelde_compositie_en_layoutresolver(self) -> None:
        model = analyseer(parseer(BRON), constraints=WORLD_MODEL_CONSTRAINTS)

        presentatie = resolveer_presentaties(model.objecten)[0]
        dia_slot, dia_intro = presentatie.dias

        self.assertEqual("closing-content", dia_slot.opgeloste_compositie.id)
        self.assertEqual("closing-layout", dia_slot.opgeloste_layout.id)
        self.assertEqual("Slot", dia_slot.naam)
        self.assertEqual(DiaFormaat.AFSLUITING, dia_slot.formaat)
        self.assertEqual("intro-content", dia_intro.opgeloste_compositie.id)
        self.assertEqual("intro-layout", dia_intro.opgeloste_layout.id)
        self.assertEqual("Intro", dia_intro.naam)
        self.assertEqual(DiaFormaat.COVER, dia_intro.formaat)

    def test_weigert_onbekende_eigenschap_op_presentatie_en_dia(self) -> None:
        self.assertIn(
            "BP4420",
            self._diagnostic_codes(
                BRON.replace(
                    'doel: "Ordent de intro- en slotdia."',
                    'doel: "Ordent de intro- en slotdia."\n    thema: "palace"',
                )
            ),
        )
        self.assertIn(
            "BP4430",
            self._diagnostic_codes(
                BRON.replace(
                    'doel: "Opent de presentatie."',
                    'doel: "Opent de presentatie."\n    merk: "forge"',
                )
            ),
        )

    def test_weigert_ongeldige_of_onvolledige_dialijst(self) -> None:
        self.assertIn(
            "BP4421",
            self._diagnostic_codes(
                BRON.replace(
                    'dias: ["dia-slot", "dia-intro"]',
                    'dias: ["dia-slot", "dia-slot"]',
                )
            ),
        )
        self.assertIn(
            "BP4421",
            self._diagnostic_codes(
                BRON.replace('dias: ["dia-slot", "dia-intro"]', 'dias: []')
            ),
        )

    def test_weigert_onbekende_dia_in_presentatie(self) -> None:
        self.assertIn(
            "BP4422",
            self._diagnostic_codes(
                BRON.replace(
                    'dias: ["dia-slot", "dia-intro"]',
                    'dias: ["dia-slot", "dia-missing"]',
                )
            ),
        )

    def test_weigert_niet_wederkerige_dialijst(self) -> None:
        self.assertIn(
            "BP4423",
            self._diagnostic_codes(
                BRON.replace(
                    'presentatie: "keynote"\n    compositie: "intro-content"',
                    'presentatie: "andere-presentatie"\n    compositie: "intro-content"',
                )
            ),
        )

    def test_weigert_dia_naar_onbekende_presentatie(self) -> None:
        self.assertIn(
            "BP4431",
            self._diagnostic_codes(
                BRON.replace(
                    'dias: ["dia-slot", "dia-intro"]\n}\ndia dia-slot {\n    naam: "Slot"\n    doel: "Sluit de presentatie af."\n    presentatie: "keynote"',
                    'dias: ["dia-intro"]\n}\ndia dia-slot {\n    naam: "Slot"\n    doel: "Sluit de presentatie af."\n    presentatie: "missing"',
                )
            ),
        )

    def test_weigert_onbekende_compositie_en_layout_op_dia(self) -> None:
        self.assertIn(
            "BP4432",
            self._diagnostic_codes(
                BRON.replace(
                    'compositie: "intro-content"\n    layout: "intro-layout"',
                    'compositie: "missing"\n    layout: "intro-layout"',
                )
            ),
        )
        self.assertIn(
            "BP4433",
            self._diagnostic_codes(
                BRON.replace(
                    'compositie: "intro-content"\n    layout: "intro-layout"',
                    'compositie: "intro-content"\n    layout: "missing"',
                )
            ),
        )

    def test_weigert_verschillende_compositie_en_layoutinhoud_op_dia(self) -> None:
        bron = BRON.replace(
            'instanties: ["intro-panel"]',
            'instanties: ["intro-panel", "unplaced-panel"]',
            1,
        ).replace(
            "layout intro-layout {",
            '''componentinstantie unplaced-panel {
    naam: "Ongeplaatst paneel"
    doel: "Niet geplaatste testinhoud."
    compositie: "intro-content"
    component: "panel"
}
layout intro-layout {''',
            1,
        )

        self.assertIn("BP4434", self._diagnostic_codes(bron))

    def test_weigert_onbekend_formaat_op_dia(self) -> None:
        self.assertIn(
            "BP4435",
            self._diagnostic_codes(
                BRON.replace('formaat: "cover"', 'formaat: "diavoorstelling"')
            ),
        )

    def test_weigert_ontbrekend_formaat_op_dia(self) -> None:
        self.assertIn(
            "BP4435",
            self._diagnostic_codes(
                BRON.replace('\n    formaat: "cover"', "")
            ),
        )

    def test_accepteert_ieder_toegestaan_diaformaat(self) -> None:
        for formaat in DiaFormaat:
            bron = BRON.replace('formaat: "cover"', f'formaat: "{formaat.value}"')
            model = analyseer(parseer(bron), constraints=WORLD_MODEL_CONSTRAINTS)
            presentatie = resolveer_presentaties(model.objecten)[0]
            dia_intro = next(
                dia for dia in presentatie.dias if dia.id == "dia-intro"
            )
            self.assertEqual(formaat, dia_intro.formaat)


if __name__ == "__main__":
    unittest.main()

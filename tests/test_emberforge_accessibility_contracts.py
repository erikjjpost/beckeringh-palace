from __future__ import annotations

import json
import unittest
from pathlib import Path

from compiler.component_accessibility import (
    resolveer_componenttoegankelijkheid,
)
from compiler.component_examples import resolveer_componentvoorbeelden
from compiler.component_html_renderer import naar_component_html
from compiler.design_compositions import resolveer_composities
from compiler.parser import parseer, parseer_bestand
from compiler.product_backends import standaard_backend_registry
from compiler.product_compiler import compileer_producten
from compiler.product_constraints import WORLD_MODEL_CONSTRAINTS
from compiler.semantic import SemantischeFout, analyseer


ROOT = Path(__file__).resolve().parents[1]
WORLD = ROOT / "architectuur" / "world.bp"
DESIGN_INPUT = (
    ROOT / "project" / "design-inputs" / "emberforge-design-system.json"
)


class EmberForgeAccessibilityContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.source = WORLD.read_text(encoding="utf-8")
        cls.model = analyseer(
            parseer_bestand(WORLD),
            constraints=WORLD_MODEL_CONSTRAINTS,
        )
        cls.contracts = {
            contract.component_id: contract
            for contract in resolveer_componenttoegankelijkheid(
                cls.model.objecten
            )
        }
        cls.examples = {
            example.id: example
            for example in resolveer_componentvoorbeelden(cls.model.objecten)
        }
        cls.compositions = {
            composition.id: composition
            for composition in resolveer_composities(cls.model.objecten)
        }
        cls.products = {
            product.definitie.id: product
            for product in compileer_producten(
                cls.model.objecten,
                standaard_backend_registry(),
            )
        }

    def test_modelleert_naam_rol_waarde_fout_disabled_en_toetsenbord(self) -> None:
        expected = {
            "forge-panel": (
                "groep",
                "titel",
                None,
                None,
                "niet-van-toepassing",
                "geen",
                "geen",
                (),
            ),
            "forge-button": (
                "actie",
                "label",
                None,
                None,
                "native",
                "tabvolgorde",
                "activeren",
                ("Enter", "Space"),
            ),
            "forge-input": (
                "tekstinvoer",
                "label",
                "waarde",
                "melding",
                "native",
                "tabvolgorde",
                "tekstinvoer",
                (),
            ),
            "forge-status": (
                "status",
                "label",
                "waarde",
                None,
                "niet-van-toepassing",
                "geen",
                "geen",
                (),
            ),
            "forge-app-tile": (
                "actie",
                "label",
                "status",
                None,
                "native",
                "tabvolgorde",
                "activeren",
                ("Enter", "Space"),
            ),
            "forge-stat-card": (
                "groep",
                "label",
                "waarde",
                None,
                "niet-van-toepassing",
                "geen",
                "geen",
                (),
            ),
        }

        self.assertEqual(
            expected,
            {
                component_id: (
                    self.contracts[component_id].rol,
                    self.contracts[component_id].naambron,
                    self.contracts[component_id].waardebron,
                    self.contracts[component_id].foutbron,
                    self.contracts[component_id].disabled_gedrag,
                    self.contracts[component_id].focusgedrag,
                    self.contracts[component_id].toetsenbordgedrag,
                    self.contracts[component_id].toetsen,
                )
                for component_id in expected
            },
        )

    def test_componentvoorbeelden_ontvangen_het_opgeloste_contract(self) -> None:
        expected = {
            "forge-button-primary-example": (
                "forge-button-accessibility",
                "actie",
                "label",
            ),
            "forge-input-error-example": (
                "forge-input-accessibility",
                "tekstinvoer",
                "label",
            ),
            "forge-status-running-example": (
                "forge-status-accessibility",
                "status",
                "label",
            ),
            "forge-app-tile-isms-example": (
                "forge-app-tile-accessibility",
                "actie",
                "label",
            ),
            "forge-stat-card-nodes-example": (
                "forge-stat-card-accessibility",
                "groep",
                "label",
            ),
        }

        self.assertEqual(
            expected,
            {
                example_id: (
                    self.examples[example_id].accessibility.contract_id,
                    self.examples[example_id].accessibility.rol,
                    self.examples[example_id].accessibility.naambron,
                )
                for example_id in expected
            },
        )

    def test_catalogus_gebruikt_native_semantiek_en_expliciete_koppelingen(
        self,
    ) -> None:
        catalog = naar_component_html(self.model.objecten)

        self.assertIn(
            'data-accessibility-contract="forge-button-accessibility"',
            catalog,
        )
        self.assertIn('data-accessibility-role="actie"', catalog)
        self.assertIn('data-accessibility-keyboard="activeren"', catalog)
        self.assertIn('data-accessibility-keys="Enter Space"', catalog)
        self.assertIn('<button type="button"', catalog)
        self.assertIn(">Sign In</button>", catalog)

        self.assertIn(
            '<label id="bp-example-forge-input-error-example-rest-label" '
            'for="bp-example-forge-input-error-example-rest-control" '
            'class="bp-example-label">Hostname</label>',
            catalog,
        )
        self.assertIn(
            'id="bp-example-forge-input-error-example-rest-control"',
            catalog,
        )
        self.assertIn('aria-invalid="true"', catalog)
        self.assertIn(
            'aria-describedby="'
            'bp-example-forge-input-error-example-rest-message"',
            catalog,
        )
        self.assertIn(
            'id="bp-example-forge-input-error-example-rest-message" '
            'class="bp-example-message">Hostname is ongeldig.</small>',
            catalog,
        )

        self.assertIn(
            'data-accessibility-contract="forge-app-tile-accessibility"',
            catalog,
        )
        self.assertIn(
            'aria-labelledby="'
            'bp-example-forge-app-tile-isms-example-rest-label"',
            catalog,
        )
        self.assertIn(
            'aria-describedby="'
            'bp-example-forge-app-tile-isms-example-rest-description '
            'bp-example-forge-app-tile-isms-example-rest-status"',
            catalog,
        )
        self.assertNotIn('role="button"', catalog)
        self.assertNotIn('tabindex="0"', catalog)

    def test_disabled_is_native_en_niet_interactief_blijft_uit_tabvolgorde(
        self,
    ) -> None:
        catalog = naar_component_html(self.model.objecten)

        self.assertIn(
            'data-example="forge-button-primary-example" '
            'data-component="forge-button"',
            catalog,
        )
        self.assertIn(
            'data-component-state="disabled" '
            'data-component-states="rest hover focus pressed disabled"',
            catalog,
        )
        self.assertIn(
            'data-accessibility-disabled="native"',
            catalog,
        )
        self.assertIn(
            'data-accessibility-keys="Enter Space" disabled>',
            catalog,
        )
        self.assertIn(
            'data-accessibility-focus="geen" '
            'data-accessibility-keyboard="geen"',
            catalog,
        )
        self.assertNotIn('aria-disabled="true"', catalog)

    def test_compositie_en_beide_backends_dragen_hetzelfde_contract(
        self,
    ) -> None:
        dashboard = self.compositions["forge-dashboard"]
        center = next(
            instance
            for instance in dashboard.instances
            if instance.id == "forge-dashboard-center-panel"
        )
        homepage = self.products["beckeringh-palace-homepage"].inhoud
        grafana = json.loads(
            self.products["forge-dashboard-grafana"].inhoud
        )

        self.assertEqual(
            "forge-panel-accessibility",
            center.accessibility.contract_id,
        )
        self.assertEqual("groep", center.accessibility.rol)
        self.assertIn(
            'data-accessibility-contract="forge-panel-accessibility"',
            homepage,
        )
        self.assertIn(
            'data-accessibility-role="groep"',
            homepage,
        )
        self.assertIn(
            "BAT toegankelijkheid: forge-panel-accessibility",
            grafana["panels"][2]["description"],
        )
        self.assertIn(
            "Toegankelijkheidsrol: groep",
            grafana["panels"][2]["description"],
        )

    def test_weigert_impliciete_of_incompatibele_toegankelijkheid(self) -> None:
        missing = self.source.replace(
            '    toegankelijkheid: "forge-button-accessibility"\n',
            "",
            1,
        )
        with self.assertRaises(SemantischeFout) as context:
            analyseer(parseer(missing), constraints=WORLD_MODEL_CONSTRAINTS)
        self.assertIn(
            "BP3832",
            {item.code for item in context.exception.diagnostics},
        )

        unknown = self.source.replace(
            '    toegankelijkheid: "forge-button-accessibility"\n',
            '    toegankelijkheid: "missing-accessibility"\n',
            1,
        )
        with self.assertRaises(SemantischeFout) as context:
            analyseer(parseer(unknown), constraints=WORLD_MODEL_CONSTRAINTS)
        self.assertIn(
            "BP3832",
            {item.code for item in context.exception.diagnostics},
        )

        wrong_source = self.source.replace(
            '    naambron: "label"\n',
            '    naambron: "waarde"\n',
            1,
        )
        with self.assertRaises(SemantischeFout) as context:
            analyseer(
                parseer(wrong_source),
                constraints=WORLD_MODEL_CONSTRAINTS,
            )
        self.assertIn(
            "BP3834",
            {item.code for item in context.exception.diagnostics},
        )

        wrong_keyboard = self.source.replace(
            '    toetsenbord: "activeren"\n',
            '    toetsenbord: "geen"\n',
            1,
        )
        with self.assertRaises(SemantischeFout) as context:
            analyseer(
                parseer(wrong_keyboard),
                constraints=WORLD_MODEL_CONSTRAINTS,
            )
        self.assertIn(
            "BP3837",
            {item.code for item in context.exception.diagnostics},
        )

    def test_bat_bevat_geen_html_of_aria_implementatievelden(self) -> None:
        for contract in self.contracts.values():
            with self.subTest(contract=contract.contract_id):
                self.assertNotIn("html", contract.bron.eigenschappen)
                self.assertFalse(
                    any(
                        veld.startswith("aria")
                        for veld in contract.bron.eigenschappen
                    )
                )

    def test_designbron_registreert_het_toegankelijkheidscontract(self) -> None:
        source = json.loads(DESIGN_INPUT.read_text(encoding="utf-8"))
        components = next(
            area for area in source["gebieden"] if area["id"] == "components"
        )

        self.assertIn("M11.3h", components["bewijs"])
        for begrip in (
            "naam",
            "rol",
            "waarde",
            "fout",
            "disabled",
            "toetsenbord",
        ):
            self.assertIn(begrip, components["bewijs"].lower())


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

from compiler.component_css_renderer import naar_component_css
from compiler.component_examples import resolveer_componentvoorbeelden
from compiler.design_components import verzamel_componenten
from compiler.design_variants import resolveer_varianten
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


class EmberForgeComponentFamilyMigrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.source = WORLD.read_text(encoding="utf-8")
        cls.model = analyseer(
            parseer_bestand(WORLD),
            constraints=WORLD_MODEL_CONSTRAINTS,
        )
        cls.components = {
            component.id: component
            for component in verzamel_componenten(cls.model.objecten)
        }
        cls.variants = {
            variant.id: variant
            for variant in resolveer_varianten(cls.model.objecten)
        }
        cls.examples = {
            example.id: example
            for example in resolveer_componentvoorbeelden(cls.model.objecten)
        }
        cls.products = {
            product.definitie.id: product
            for product in compileer_producten(
                cls.model.objecten,
                standaard_backend_registry(),
            )
        }

    def test_modelleert_de_vijf_productgedragen_componentrollen(self) -> None:
        expected = {
            "forge-button": ("actie", ("label",)),
            "forge-input": (
                "invoer",
                ("label", "waarde", "melding"),
            ),
            "forge-status": ("status", ("label", "waarde")),
            "forge-app-tile": (
                "app-tegel",
                ("label", "beschrijving", "status"),
            ),
            "forge-stat-card": (
                "statistiek",
                ("label", "waarde", "beschrijving"),
            ),
        }

        self.assertEqual(
            expected,
            {
                component_id: (
                    self.components[component_id].rol,
                    self.components[component_id].anatomie,
                )
                for component_id in expected
            },
        )

    def test_modelleert_de_geverifieerde_componentvarianten(self) -> None:
        expected = {
            "forge-button": {
                "forge-button-primary",
                "forge-button-secondary",
                "forge-button-ghost",
                "forge-button-ember",
            },
            "forge-input": {
                "forge-input-default",
                "forge-input-error",
            },
            "forge-status": {
                "forge-status-running",
                "forge-status-pending",
                "forge-status-failed",
                "forge-status-info",
            },
            "forge-app-tile": {
                "forge-app-tile-default",
                "forge-app-tile-ember",
            },
            "forge-stat-card": {
                "forge-stat-card-value",
                "forge-stat-card-health",
                "forge-stat-card-progress",
                "forge-stat-card-progress-ember",
            },
        }

        self.assertEqual(
            expected,
            {
                component_id: {
                    variant.id
                    for variant in self.variants.values()
                    if variant.component_id == component_id
                }
                for component_id in expected
            },
        )
        self.assertEqual(
            ("rest", "hover", "focus", "pressed", "disabled"),
            tuple(
                state
                for state, _ in self.variants[
                    "forge-button-primary"
                ].state_appearances
            ),
        )
        self.assertEqual(
            ("rest", "hover", "focus", "pressed", "disabled"),
            tuple(
                state
                for state, _ in self.variants[
                    "forge-app-tile-default"
                ].state_appearances
            ),
        )

    def test_resolveert_productinhoud_als_componentvoorbeelden(self) -> None:
        expected = {
            "forge-button-primary-example": (
                "forge-button",
                "forge-button-primary",
                "Sign In",
                None,
                None,
                None,
                None,
            ),
            "forge-input-error-example": (
                "forge-input",
                "forge-input-error",
                "Hostname",
                "lab..local",
                None,
                "Hostname is ongeldig.",
                None,
            ),
            "forge-status-running-example": (
                "forge-status",
                "forge-status-running",
                "Running",
                "62",
                None,
                None,
                None,
            ),
            "forge-app-tile-isms-example": (
                "forge-app-tile",
                "forge-app-tile-default",
                "ISMS Challenger",
                None,
                "Information Security Management",
                None,
                "running",
            ),
            "forge-stat-card-nodes-example": (
                "forge-stat-card",
                "forge-stat-card-value",
                "Nodes",
                "12",
                "All Running",
                None,
                None,
            ),
        }

        self.assertEqual(
            expected,
            {
                example_id: (
                    self.examples[example_id].component_id,
                    self.examples[example_id].variant_id,
                    self.examples[example_id].label,
                    self.examples[example_id].waarde,
                    self.examples[example_id].beschrijving,
                    self.examples[example_id].melding,
                    self.examples[example_id].status,
                )
                for example_id in expected
            },
        )

    def test_catalogus_rendert_semantische_voorbeelden_uit_bat(self) -> None:
        catalog = self.products["forge-design-system-reference-html"].inhoud

        self.assertIn(
            'data-example="forge-button-primary-example"',
            catalog,
        )
        self.assertIn('<button type="button"', catalog)
        self.assertIn(">Sign In</button>", catalog)
        self.assertIn(
            'data-example="forge-input-error-example"',
            catalog,
        )
        self.assertIn(
            'class="bp-example-label">Hostname</label>',
            catalog,
        )
        self.assertIn('value="lab..local"', catalog)
        self.assertIn(
            'class="bp-example-message">Hostname is ongeldig.</small>',
            catalog,
        )
        self.assertIn(
            'data-example="forge-status-running-example"',
            catalog,
        )
        self.assertIn(">Running</span> · <span>62</span>", catalog)
        self.assertIn(
            'data-example="forge-app-tile-isms-example"',
            catalog,
        )
        self.assertIn(">ISMS Challenger</strong>", catalog)
        self.assertIn(
            'class="bp-example-description">'
            "Information Security Management</span>",
            catalog,
        )
        self.assertIn(
            'data-example="forge-stat-card-nodes-example"',
            catalog,
        )
        self.assertIn("<strong>12</strong>", catalog)
        self.assertIn("<p>All Running</p>", catalog)

    def test_css_draagt_structuur_en_bronbewezen_tonen(self) -> None:
        css = naar_component_css(self.model.objecten)
        catalog = self.products["forge-design-system-reference-html"].inhoud

        self.assertIn(".bp-forge-button {", css)
        self.assertIn("display: inline-flex;", css)
        self.assertIn(".bp-forge-input {", css)
        self.assertIn(".bp-forge-status {", css)
        self.assertIn(".bp-forge-app-tile {", css)
        self.assertIn(".bp-forge-stat-card {", css)
        self.assertIn(
            "background-color: var(--bp-material-success-surface);",
            css,
        )
        self.assertIn(
            "color: var(--bp-material-success-foreground);",
            css,
        )
        self.assertIn(
            "border-radius: var(--bp-radius-control);",
            css,
        )
        self.assertIn(
            "box-shadow: var(--bp-shadow-glow-accent);",
            css,
        )
        references = set(re.findall(r"var\(--(?P<name>bp-[^)]+)\)", css))
        definitions = set(
            re.findall(
                r"--(?P<name>bp-[a-z0-9-]+):",
                catalog + css,
            )
        )
        self.assertLessEqual(references, definitions)

    def test_weigert_onjuiste_anatomie_en_voorbeeldreferenties(self) -> None:
        wrong_anatomy = self.source.replace(
            '    anatomie: ["label"]',
            '    anatomie: ["label", "waarde"]',
            1,
        )
        with self.assertRaises(SemantischeFout) as context:
            analyseer(
                parseer(wrong_anatomy),
                constraints=WORLD_MODEL_CONSTRAINTS,
            )
        self.assertIn(
            "BP3222",
            {item.code for item in context.exception.diagnostics},
        )

        unknown_variant = self.source.replace(
            '    variant: "forge-button-primary"',
            '    variant: "missing-variant"',
            1,
        )
        with self.assertRaises(SemantischeFout) as context:
            analyseer(
                parseer(unknown_variant),
                constraints=WORLD_MODEL_CONSTRAINTS,
            )
        self.assertIn(
            "BP3822",
            {item.code for item in context.exception.diagnostics},
        )

    def test_designbron_registreert_de_volledige_componentfamilie(self) -> None:
        source = json.loads(DESIGN_INPUT.read_text(encoding="utf-8"))
        components = next(
            area for area in source["gebieden"] if area["id"] == "components"
        )

        self.assertEqual("gemigreerd", components["status"])
        self.assertIn("M11.3g", components["bewijs"])
        for component in (
            "button",
            "input",
            "status",
            "app tile",
            "stat card",
        ):
            self.assertIn(component, components["bewijs"].lower())
        verified = {
            item["pad"]: item["sha256"]
            for item in source["geverifieerde_bronnen"]
        }
        self.assertEqual(
            "3bbd80152f39cba6ac3106b9bb86aefc756ec150bd910e8c6be7651e473a090c",
            verified[
                "EmberForge-Design-System/ui_kits/homelab-dashboard/"
                "AppTile.jsx"
            ],
        )
        self.assertEqual(
            "63fd6c9a1d2742ccea72cb8ff9aaf452cef34fbaf4053de95d69dd6206390d6d",
            verified[
                "EmberForge-Design-System/ui_kits/homelab-dashboard/"
                "styles.css"
            ],
        )


if __name__ == "__main__":
    unittest.main()

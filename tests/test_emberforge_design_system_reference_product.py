from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

from compiler.design_system_reference import (
    REFERENCE_SECTION_ROLES,
    resolveer_designsystemreferentie,
)
from compiler.design_render_targets import resolveer_renderdoelen
from compiler.parser import parseer, parseer_bestand
from compiler.product_backends import standaard_backend_registry
from compiler.product_compiler import compileer_producten
from compiler.product_constraints import WORLD_MODEL_CONSTRAINTS
from compiler.product_model import verzamel_producten
from compiler.semantic import SemantischeFout, analyseer


ROOT = Path(__file__).resolve().parents[1]
WORLD = ROOT / "architectuur" / "world.bp"
DESIGN_INPUT = (
    ROOT / "project" / "design-inputs" / "emberforge-design-system.json"
)
PRODUCT_ID = "forge-design-system-reference-html"


class EmberForgeDesignSystemReferenceProductTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.source = WORLD.read_text(encoding="utf-8")
        cls.model = analyseer(
            parseer_bestand(WORLD),
            constraints=WORLD_MODEL_CONSTRAINTS,
        )
        cls.product_definitions = {
            product.id: product
            for product in verzamel_producten(cls.model.objecten)
        }
        cls.products = {
            product.definitie.id: product
            for product in compileer_producten(
                cls.model.objecten,
                standaard_backend_registry(),
            )
        }
        cls.product = cls.products[PRODUCT_ID]
        cls.reference = resolveer_designsystemreferentie(
            cls.model.objecten,
            cls.product.definitie.reference_section_ids,
        )

    def test_modelleert_vijf_geordende_referentiesecties(self) -> None:
        self.assertEqual(
            REFERENCE_SECTION_ROLES,
            tuple(section.role for section in self.reference.sections),
        )
        self.assertEqual(
            (
                "forge-reference-primitives",
                "forge-reference-tokens",
                "forge-reference-states",
                "forge-reference-examples",
                "forge-reference-accessibility",
            ),
            tuple(section.id for section in self.reference.sections),
        )

    def test_is_een_statisch_native_product_en_geen_html_renderdoel(self) -> None:
        definition = self.product.definitie

        self.assertEqual("design-system", definition.inhoud)
        self.assertEqual("static", definition.mode)
        self.assertEqual(
            "forge-design-system-reference-composition",
            definition.compositie,
        )
        self.assertEqual(
            "forge-design-system-reference-stack",
            definition.layout,
        )
        self.assertEqual("output/products/components.html", definition.pad)
        self.assertEqual(64, len(definition.snapshot_id))
        self.assertEqual(
            f"sha256:{definition.snapshot_id}",
            definition.snapshot_ref,
        )
        self.assertNotIn(
            "html-components",
            {target.id for target in resolveer_renderdoelen(self.model.objecten)},
        )

    def test_rendert_navigeerbare_secties_in_normatieve_volgorde(self) -> None:
        html = self.product.inhoud

        self.assertIn(
            'data-product-content="design-system"',
            html,
        )
        self.assertIn(
            'data-product-mode="static"',
            html,
        )
        self.assertIn(
            'aria-label="EmberForge designsystem referentiesecties"',
            html,
        )
        positions = [
            html.index(f'href="#{section.id}"')
            for section in self.reference.sections
        ]
        self.assertEqual(sorted(positions), positions)
        for section in self.reference.sections:
            self.assertIn(
                f'id="{section.id}" data-reference-role="{section.role}"',
                html,
            )

    def test_publiceert_primitieven_en_tokens_met_feitelijke_waarden(self) -> None:
        html = self.product.inhoud

        for primitive_kind in (
            "palette",
            "typography",
            "type-scale",
            "material",
            "border",
            "radius",
            "shadow",
            "motion",
            "spacing",
            "art-direction",
        ):
            self.assertIn(
                f'data-primitive-kind="{primitive_kind}"',
                html,
            )
        self.assertIn("#0F1724", html)
        self.assertIn("Orbitron", html)
        self.assertIn("cubic-bezier(0.2, 0.7, 0.2, 1)", html)
        self.assertEqual(
            len(self.reference.tokens),
            html.count('data-token="'),
        )
        self.assertIn(
            'data-token="color-primary"',
            html,
        )
        self.assertIn("{color-sky}", html)

    def test_publiceert_states_voorbeelden_en_toegankelijkheid_eenmaal(self) -> None:
        html = self.product.inhoud
        expected_states = sum(
            len(variant.state_appearances)
            for variant in self.reference.variants
        )

        self.assertEqual(
            expected_states,
            html.count('data-state-reference="'),
        )
        self.assertEqual(
            len(self.reference.examples),
            html.count('data-reference-example="'),
        )
        self.assertEqual(
            len(self.reference.accessibility),
            html.count('data-accessibility-reference="'),
        )
        self.assertIn(">Sign In</button>", html)
        self.assertIn('aria-invalid="true"', html)
        self.assertIn(
            'data-accessibility-keys="Enter Space"',
            html,
        )
        self.assertIn('data-component-state="hover"', html)

    def test_gebruikt_unieke_html_identifiers(self) -> None:
        identifiers = re.findall(r'\bid="([^"]+)"', self.product.inhoud)

        self.assertTrue(identifiers)
        self.assertEqual(len(identifiers), len(set(identifiers)))

    def test_verbindt_dezelfde_technische_artifacts_zonder_externe_runtime(self) -> None:
        html = self.product.inhoud

        self.assertIn('href="tokens.css"', html)
        self.assertIn('href="components.css"', html)
        for target in ("css-components", "css-tokens", "json-tokens"):
            self.assertIn(
                f'data-navigation-target="{target}"',
                html,
            )
        self.assertIsNone(re.search(r"https?://|@import", html))

    def test_weigert_onvolledige_of_niet_statische_referentie(self) -> None:
        missing = self.source.replace(
            ', "forge-reference-accessibility"]',
            "]",
            1,
        )
        with self.assertRaises(SemantischeFout) as context:
            analyseer(
                parseer(missing),
                constraints=WORLD_MODEL_CONSTRAINTS,
            )
        self.assertIn(
            "BP3843",
            {item.code for item in context.exception.diagnostics},
        )

        interactive = self.source.replace(
            'product forge-design-system-reference-html {\n'
            '    naam: "EmberForge Design System Referentie"\n'
            '    doel: "Tokens, primitives, componenttoestanden, voorbeelden '
            'en toegankelijkheidscontracten als één navigeerbaar product."\n'
            '    backend: "html"\n'
            '    mode: "static"',
            'product forge-design-system-reference-html {\n'
            '    naam: "EmberForge Design System Referentie"\n'
            '    doel: "Tokens, primitives, componenttoestanden, voorbeelden '
            'en toegankelijkheidscontracten als één navigeerbaar product."\n'
            '    backend: "html"\n'
            '    mode: "interactive"',
            1,
        )
        with self.assertRaises(SemantischeFout) as context:
            analyseer(
                parseer(interactive),
                constraints=WORLD_MODEL_CONSTRAINTS,
            )
        self.assertIn(
            "BP3844",
            {item.code for item in context.exception.diagnostics},
        )

    def test_designbron_registreert_het_native_referentieproduct(self) -> None:
        source = json.loads(DESIGN_INPUT.read_text(encoding="utf-8"))
        components = next(
            area for area in source["gebieden"] if area["id"] == "components"
        )

        self.assertIn("M11.3i", components["bewijs"])
        self.assertIn("referentieproduct", components["bewijs"])


if __name__ == "__main__":
    unittest.main()

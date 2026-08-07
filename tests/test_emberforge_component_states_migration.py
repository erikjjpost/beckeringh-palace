from __future__ import annotations

import json
import unittest
from pathlib import Path

from compiler.component_css_renderer import naar_component_css
from compiler.design_compositions import resolveer_composities
from compiler.design_variants import resolveer_varianten
from compiler.parser import parseer, parseer_bestand
from compiler.product_backends import standaard_backend_registry
from compiler.product_compiler import compileer_producten
from compiler.product_constraints import WORLD_MODEL_CONSTRAINTS
from compiler.semantic import SemantischeFout, analyseer
from compiler.theme_resolution import resolveer_thema


ROOT = Path(__file__).resolve().parents[1]
WORLD = ROOT / "architectuur" / "world.bp"
DESIGN_INPUT = (
    ROOT / "project" / "design-inputs" / "emberforge-design-system.json"
)


class EmberForgeComponentStatesMigrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.source = WORLD.read_text(encoding="utf-8")
        cls.model = analyseer(
            parseer_bestand(WORLD),
            constraints=WORLD_MODEL_CONSTRAINTS,
        )
        cls.theme = resolveer_thema(cls.model.objecten, "beckeringh-palace")
        cls.variants = {
            variant.id: variant
            for variant in resolveer_varianten(cls.model.objecten)
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

    def test_resolveert_bronbewezen_stateprimitieven(self) -> None:
        self.assertEqual(
            {
                "interaction": "#7DD3FC",
                "interaction-pressed": "#38BDF8",
                "disabled": "#3E5573",
            },
            {
                role: self.theme.materiaal.kleur(role).waarde
                for role in (
                    "interaction",
                    "interaction-pressed",
                    "disabled",
                )
            },
        )
        self.assertEqual("none", self.theme.shadow.none)
        self.assertEqual(
            (
                "0 0 0 1px rgba(125,211,252,0.18), "
                "0 6px 24px rgba(125,211,252,0.10)"
            ),
            self.theme.shadow.glow,
        )
        self.assertEqual("0px", self.theme.motion.rest_offset)
        self.assertEqual("-1px", self.theme.motion.hover_offset)

    def test_variant_draagt_alle_vijf_toestanden(self) -> None:
        expected = (
            ("rest", "forge-panel-card-rest-appearance"),
            ("hover", "forge-panel-card-hover-appearance"),
            ("focus", "forge-panel-card-focus-appearance"),
            ("pressed", "forge-panel-card-pressed-appearance"),
            ("disabled", "forge-panel-card-disabled-appearance"),
        )

        self.assertEqual(
            expected,
            self.variants["forge-panel-route"].state_appearances,
        )
        self.assertEqual(
            expected,
            self.variants["forge-panel-compact"].state_appearances,
        )

    def test_compositie_ontvangt_opgeloste_statecontracten(self) -> None:
        homepage = self.compositions[
            "beckeringh-palace-homepage-composition"
        ]
        route = next(
            instance
            for instance in homepage.instances
            if instance.id == "homepage-world"
        )
        dashboard = self.compositions["forge-dashboard"]
        compact = next(
            instance
            for instance in dashboard.instances
            if instance.id == "forge-dashboard-center-panel"
        )

        self.assertEqual(
            self.variants["forge-panel-route"].state_appearances,
            route.state_appearances,
        )
        self.assertEqual(
            self.variants["forge-panel-compact"].state_appearances,
            compact.state_appearances,
        )

    def test_css_vertaalt_states_zonder_schaalanimatie(self) -> None:
        css = naar_component_css(self.model.objecten)
        selector = ".bp-forge-panel.bp-variant-forge-panel-route"

        self.assertIn(
            f'{selector}:hover:not([aria-disabled="true"]), '
            f"{selector}.bp-state-hover {{",
            css,
        )
        self.assertIn(
            f"{selector}:focus-visible, {selector}:focus-within, "
            f"{selector}.bp-state-focus {{",
            css,
        )
        self.assertIn(
            f'{selector}:active:not([aria-disabled="true"]), '
            f"{selector}.bp-state-pressed {{",
            css,
        )
        self.assertIn(
            f'{selector}:disabled, {selector}[aria-disabled="true"], '
            f"{selector}.bp-state-disabled {{",
            css,
        )
        self.assertIn(
            "border: var(--bp-border-regular) var(--bp-border-style) "
            "var(--bp-material-interaction-pressed);",
            css,
        )
        self.assertIn(
            "transform: translateY(var(--bp-motion-hover-offset));",
            css,
        )
        self.assertIn("cursor: not-allowed;", css)
        self.assertNotIn("scale(", css)

    def test_catalogus_toont_iedere_opgeloste_state(self) -> None:
        catalog = self.products["forge-design-system-reference-html"].inhoud

        self.assertIn("--bp-material-interaction: var(--bp-color-sky-400);", catalog)
        self.assertIn(
            "--bp-material-interaction-pressed: var(--bp-color-sky-500);",
            catalog,
        )
        self.assertIn("--bp-shadow-glow:", catalog)
        self.assertIn("--bp-motion-hover-offset: -1px;", catalog)
        self.assertIn(
            '<body data-world="beckeringh-palace" data-theme="forge" ',
            catalog,
        )
        for state in ("rest", "hover", "focus", "pressed", "disabled"):
            self.assertIn(
                f'data-component-state="{state}"',
                catalog,
            )
        self.assertIn(
            'class="bp-forge-panel bp-variant-forge-panel-route '
            'bp-state-disabled"',
            catalog,
        )
        self.assertIn(
            'data-accessibility-disabled="niet-van-toepassing"',
            catalog,
        )
        self.assertNotIn('aria-disabled="true"', catalog)

    def test_producten_publiceren_statecontract_als_metadata(self) -> None:
        homepage = self.products["beckeringh-palace-homepage"].inhoud
        grafana = json.loads(
            self.products["forge-dashboard-grafana"].inhoud
        )

        self.assertIn(
            'data-component-states="rest hover focus pressed disabled"',
            homepage,
        )
        self.assertIn(
            'data-state-pressed-appearance="'
            'forge-panel-card-pressed-appearance"',
            homepage,
        )
        self.assertNotIn(
            ".bp-region:focus-within, .bp-region:hover",
            homepage,
        )
        self.assertIn(
            "BAT states: rest=forge-panel-card-rest-appearance, "
            "hover=forge-panel-card-hover-appearance, "
            "focus=forge-panel-card-focus-appearance, "
            "pressed=forge-panel-card-pressed-appearance, "
            "disabled=forge-panel-card-disabled-appearance",
            grafana["panels"][2]["description"],
        )

    def test_weigert_onvolledig_of_onbekend_statecontract(self) -> None:
        incomplete = self.source.replace(
            '    disabled: "forge-panel-card-disabled-appearance"\n',
            "",
            1,
        )
        with self.assertRaises(SemantischeFout) as context:
            analyseer(
                parseer(incomplete),
                constraints=WORLD_MODEL_CONSTRAINTS,
            )
        self.assertIn(
            "BP3806",
            {item.code for item in context.exception.diagnostics},
        )

        unknown = self.source.replace(
            '    focus: "forge-panel-card-focus-appearance"',
            '    focus: "missing-appearance"',
            1,
        )
        with self.assertRaises(SemantischeFout) as context:
            analyseer(
                parseer(unknown),
                constraints=WORLD_MODEL_CONSTRAINTS,
            )
        self.assertIn(
            "BP3807",
            {item.code for item in context.exception.diagnostics},
        )

    def test_designbron_registreert_componentmigratie(self) -> None:
        source = json.loads(DESIGN_INPUT.read_text(encoding="utf-8"))
        components = next(
            area for area in source["gebieden"] if area["id"] == "components"
        )

        self.assertEqual("gemigreerd", components["status"])
        self.assertIn("M11.3f", components["bewijs"])
        self.assertIn("M11.3g", components["bewijs"])
        self.assertIn("rust", components["bewijs"])
        self.assertIn("disabled", components["bewijs"])
        self.assertIn("button", components["bewijs"])


if __name__ == "__main__":
    unittest.main()

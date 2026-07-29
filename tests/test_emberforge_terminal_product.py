from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

from compiler.component_css_renderer import naar_component_css
from compiler.component_examples import resolveer_componentvoorbeelden
from compiler.design_components import verzamel_componenten
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


class EmberForgeTerminalProductTests(unittest.TestCase):
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

    def test_modelleert_terminalsurface_als_getypeerd_componentvoorbeeld(
        self,
    ) -> None:
        component = self.components["forge-terminal"]
        example = self.examples["forge-terminal-neofetch-example"]
        terminal = example.terminal

        self.assertEqual("terminal", component.rol)
        self.assertEqual(
            (
                "label",
                "venstertitel",
                "vensterknoppen",
                "tabs",
                "actieve-tab",
                "markering",
                "gebruiker",
                "host",
                "sleutels",
                "waarden",
                "pad",
                "prompt",
                "cursor",
            ),
            component.anatomie,
        )
        self.assertIsNotNone(terminal)
        assert terminal is not None
        self.assertEqual(
            ("sluiten", "minimaliseren", "maximaliseren"),
            terminal.vensterknoppen,
        )
        self.assertEqual(
            ("~/emberforge", "k9s", "+"),
            terminal.tabs,
        )
        self.assertEqual("~/emberforge", terminal.actieve_tab)
        self.assertEqual(("thb1", "emberforge", "~", "$", "▍"), (
            terminal.gebruiker,
            terminal.host,
            terminal.pad,
            terminal.prompt,
            terminal.cursor,
        ))
        self.assertEqual(13, len(terminal.systeemvelden))
        self.assertEqual(
            ("OS", "EmberForge OS · 6.6.12-ember"),
            terminal.systeemvelden[0],
        )
        self.assertEqual(
            ("Cluster", "homelab · 12 nodes · 98% healthy"),
            terminal.systeemvelden[-1],
        )

    def test_publiceert_een_statisch_native_terminalproduct(self) -> None:
        product = self.products["emberforge-terminal-html"].definitie
        composition = product.opgeloste_compositie
        layout = product.opgeloste_layout

        self.assertEqual("static", product.mode)
        self.assertEqual(
            "output/products/emberforge-terminal.html",
            product.pad,
        )
        self.assertEqual(64, len(product.snapshot_id))
        self.assertIsNotNone(composition)
        self.assertIsNotNone(layout)
        assert composition is not None
        assert layout is not None
        self.assertEqual("terminal-sessie", composition.role)
        self.assertEqual(
            ("emberforge-terminal-session",),
            tuple(instance.id for instance in composition.instances),
        )
        self.assertEqual(
            "forge-terminal-neofetch-example",
            composition.instances[0].example.id,
        )
        self.assertEqual("stack", layout.type.value)
        self.assertEqual(
            ("emberforge-terminal-region",),
            tuple(region.id for region in layout.regions),
        )

    def test_rendert_terminal_semantisch_zonder_shelluitvoering(self) -> None:
        html = self.products["emberforge-terminal-html"].inhoud

        self.assertIn("<h1>EmberForge Terminal</h1>", html)
        self.assertIn('data-composition-role="terminal-sessie"', html)
        self.assertIn(
            'data-component-role="terminal"',
            html,
        )
        self.assertIn('data-terminal-static="true"', html)
        self.assertEqual(3, html.count('data-terminal-control="'))
        self.assertEqual(3, html.count('data-terminal-tab="'))
        self.assertIn('data-terminal-tab-active="true"', html)
        self.assertEqual(13, html.count('class="bp-terminal-field"'))
        self.assertIn("<dt>OS:</dt>", html)
        self.assertIn("<dd>EmberForge OS · 6.6.12-ember</dd>", html)
        self.assertIn("<dt>Cluster:</dt>", html)
        self.assertIn("<dd>homelab · 12 nodes · 98% healthy</dd>", html)
        self.assertIn('class="bp-terminal-prompt"', html)
        self.assertIn('data-accessibility-role="groep"', html)
        self.assertIn('data-product-mode="static"', html)
        self.assertIn('data-time-context="none"', html)
        self.assertNotIn("<script", html)
        self.assertNotIn("contenteditable", html)
        self.assertNotIn("@keyframes", html)

        identifiers = re.findall(r'\bid="([^"]+)"', html)
        self.assertEqual(len(identifiers), len(set(identifiers)))

    def test_componentcss_gebruikt_alleen_opgeloste_themerollen(self) -> None:
        css = naar_component_css(self.model.objecten)

        self.assertIn(".bp-forge-terminal {", css)
        self.assertIn("font-family: var(--bp-font-mono);", css)
        self.assertIn(
            "background: var(--bp-material-field);",
            css,
        )
        self.assertIn(
            'data-terminal-control="sluiten"',
            css,
        )
        self.assertIn(
            'data-terminal-tab-active="true"',
            css,
        )
        self.assertNotIn("#0A111C", css)
        self.assertNotIn("#7DD3FC", css)
        self.assertNotIn("#C9895B", css)

    def test_weigert_onvolledige_of_inconsistente_terminalinhoud(self) -> None:
        mutations = (
            (
                '    actieve-tab: "~/emberforge"',
                '    actieve-tab: "missing"',
            ),
            (
                '    vensterknoppen: ["sluiten", "minimaliseren", "maximaliseren"]',
                '    vensterknoppen: ["sluiten", "maximaliseren"]',
            ),
            (
                '"Disk", "Cluster"]',
                '"Disk"]',
            ),
        )
        for old, new in mutations:
            with self.subTest(replacement=new):
                with self.assertRaises(SemantischeFout) as context:
                    analyseer(
                        parseer(self.source.replace(old, new, 1)),
                        constraints=WORLD_MODEL_CONSTRAINTS,
                    )
                self.assertIn(
                    "BP3829",
                    {item.code for item in context.exception.diagnostics},
                )

    def test_registreert_de_bytegelijke_terminalbronnen_en_migratie(
        self,
    ) -> None:
        source = json.loads(DESIGN_INPUT.read_text(encoding="utf-8"))
        verified = {
            item["pad"]: item["sha256"]
            for item in source["geverifieerde_bronnen"]
        }
        self.assertEqual(
            "769d8bf62725d9141391e7a5b3b05adc890b8bbfc2e5584c68971f3b9f2d32a8",
            verified[
                "EmberForge-Design-System/ui_kits/terminal/README.md"
            ],
        )
        self.assertEqual(
            "c9a15f5d4766cc9739665be3061af9fb027c98d5963961ef705a5b20dc1e3414",
            verified[
                "EmberForge-Design-System/ui_kits/terminal/index.html"
            ],
        )
        self.assertEqual(
            "5da0796962af0317672b58c1e29ab3abc851acbfccf8849379690d666456188b",
            verified[
                "EmberForge-Design-System/preview/"
                "brand-terminal-identity.html"
            ],
        )
        area = next(
            area
            for area in source["gebieden"]
            if area["id"] == "product-surfaces"
        )
        self.assertEqual("gemigreerd", area["status"])
        self.assertIn("M11.4d", area["bewijs"])
        self.assertIn("geen werkende shell", area["bewijs"])
        self.assertIn("actuele telemetrie", area["bewijs"])


if __name__ == "__main__":
    unittest.main()

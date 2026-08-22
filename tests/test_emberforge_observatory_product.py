from __future__ import annotations

import unittest
import json
from html.parser import HTMLParser
from pathlib import Path

from compiler.parser import parseer_bestand
from compiler.product_backends import standaard_backend_registry
from compiler.product_compiler import compileer_producten
from compiler.product_constraints import WORLD_MODEL_CONSTRAINTS
from compiler.semantic import analyseer


ROOT = Path(__file__).resolve().parents[1]
WORLD = ROOT / "architectuur" / "world.bp"
DESIGN_INPUT = (
    ROOT / "project" / "design-inputs" / "emberforge-design-system.json"
)


class _IdCollector(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: list[str] = []

    def handle_starttag(self, _tag, attrs) -> None:
        self.ids.extend(value for name, value in attrs if name == "id")


class EmberForgeObservatoryProductTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.model = analyseer(
            parseer_bestand(WORLD),
            constraints=WORLD_MODEL_CONSTRAINTS,
        )
        cls.products = {
            product.definitie.id: product
            for product in compileer_producten(
                cls.model.objecten,
                standaard_backend_registry(),
            )
        }

    def test_componeert_tien_bat_voorbeelden_als_observatory(self) -> None:
        product = self.products["emberforge-observatory-html"]
        composition = product.definitie.opgeloste_compositie

        self.assertIsNotNone(composition)
        assert composition is not None
        self.assertEqual(10, len(composition.instances))
        self.assertEqual(
            (
                "forge-stat-card-nodes-example",
                "forge-stat-card-health-example",
                "forge-stat-card-cpu-example",
                "forge-stat-card-memory-example",
                "forge-status-running-example",
                "forge-status-pending-example",
                "forge-status-failed-example",
                "forge-status-info-example",
                "forge-app-tile-isms-example",
                "forge-app-tile-cv-example",
            ),
            tuple(
                instance.example.id
                for instance in composition.instances
                if instance.example is not None
            ),
        )

    def test_gebruikt_responsief_vier_naar_twee_kolomscontract(self) -> None:
        layout = self.products[
            "emberforge-observatory-html"
        ].definitie.opgeloste_layout

        self.assertIsNotNone(layout)
        assert layout is not None
        self.assertEqual((4, 3), (layout.columns, layout.rows))
        self.assertEqual(960, layout.responsive_breakpoint)
        self.assertEqual(2, layout.compact_columns)
        self.assertEqual(
            tuple(range(1, 11)),
            tuple(region.compact_order for region in layout.regions),
        )

    def test_rendert_productinhoud_semantisch_uit_de_voorbeelden(self) -> None:
        html = self.products["emberforge-observatory-html"].inhoud

        self.assertIn("<h1>The Observatory</h1>", html)
        self.assertIn('data-responsive-breakpoint="960"', html)
        self.assertIn('data-compact-columns="2"', html)
        self.assertEqual(10, html.count('data-example="'))
        self.assertEqual(4, html.count('data-component-role="statistiek"'))
        self.assertEqual(4, html.count('data-component-role="status"'))
        self.assertEqual(2, html.count('data-component-role="app-tegel"'))
        self.assertIn(
            'class="bp-region" data-region="homelab-app-isms-region"',
            html,
        )
        self.assertIn(">ISMS Challenger</strong>", html)
        self.assertIn(">CV Tool</strong>", html)
        self.assertIn(">Running</span> · <span>62</span>", html)
        self.assertNotIn("fonts.googleapis.com", html)

        parser = _IdCollector()
        parser.feed(html)
        self.assertEqual(len(parser.ids), len(set(parser.ids)))

    def test_rendert_dezelfde_compositie_als_native_grafana_dashboard(self) -> None:
        html_product = self.products["emberforge-observatory-html"].definitie
        grafana_product = self.products[
            "emberforge-observatory-grafana"
        ].definitie
        dashboard = json.loads(
            self.products["emberforge-observatory-grafana"].inhoud
        )

        self.assertEqual(
            html_product.opgeloste_compositie,
            grafana_product.opgeloste_compositie,
        )
        self.assertEqual(
            html_product.opgeloste_layout,
            grafana_product.opgeloste_layout,
        )
        self.assertEqual("The Observatory Grafana", dashboard["title"])
        self.assertEqual(
            "emberforge-observatory-grafana",
            dashboard["uid"],
        )
        self.assertTrue(dashboard["editable"])
        self.assertEqual({"hidden": False}, dashboard["timepicker"])
        self.assertEqual(11, len(dashboard["panels"]))
        self.assertEqual(
            [
                "The Observatory",
                "Nodes",
                "Cluster Health",
                "CPU Usage",
                "Memory",
                "Running",
                "Pending",
                "Failed",
                "Healthy",
                "ISMS Challenger",
                "CV Tool",
            ],
            [panel["title"] for panel in dashboard["panels"]],
        )
        self.assertEqual(
            [
                {"h": 4, "w": 24, "x": 0, "y": 0},
                {"h": 16, "w": 6, "x": 0, "y": 4},
                {"h": 16, "w": 6, "x": 6, "y": 4},
                {"h": 16, "w": 6, "x": 12, "y": 4},
                {"h": 16, "w": 6, "x": 18, "y": 4},
                {"h": 16, "w": 6, "x": 0, "y": 20},
                {"h": 16, "w": 6, "x": 6, "y": 20},
                {"h": 16, "w": 6, "x": 12, "y": 20},
                {"h": 16, "w": 6, "x": 18, "y": 20},
                {"h": 16, "w": 12, "x": 0, "y": 36},
                {"h": 16, "w": 12, "x": 12, "y": 36},
            ],
            [panel["gridPos"] for panel in dashboard["panels"]],
        )
        descriptions = "\n".join(
            panel["description"] for panel in dashboard["panels"][1:]
        )
        self.assertIn("BAT variant: forge-stat-card-value", descriptions)
        self.assertIn("BAT states: rest=forge-status-running-appearance", descriptions)
        self.assertIn("BAT variant: forge-app-tile-default", descriptions)
        self.assertIn("Toegankelijkheidsrol: status", descriptions)
        self.assertIn("Toetsenbordgedrag: activeren", descriptions)

    def test_registreert_de_productsurface_als_gecontroleerde_migratie(self) -> None:
        source = json.loads(DESIGN_INPUT.read_text(encoding="utf-8"))
        area = next(
            area
            for area in source["gebieden"]
            if area["id"] == "product-surfaces"
        )

        self.assertEqual("gemigreerd", area["status"])
        self.assertIn("M11.4b", area["bewijs"])
        self.assertIn("tien BAT componentvoorbeelden", area["bewijs"])


if __name__ == "__main__":
    unittest.main()

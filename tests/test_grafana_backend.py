from __future__ import annotations

import json
import unittest
from dataclasses import replace
from pathlib import Path

from compiler.backends.grafana import backend
from compiler.parser import parseer, parseer_bestand
from compiler.product_backends import standaard_backend_registry
from compiler.product_compiler import compileer_producten
from compiler.product_constraints import WORLD_MODEL_CONSTRAINTS
from compiler.semantic import analyseer


ROOT = Path(__file__).resolve().parents[1]
WORLD = ROOT / "architectuur" / "world.bp"


class GrafanaBackendTests(unittest.TestCase):
    def test_compileert_forge_dashboard_naar_importeerbaar_json(self):
        model = analyseer(
            parseer_bestand(WORLD),
            constraints=WORLD_MODEL_CONSTRAINTS,
        )
        producten = {
            product.definitie.id: product
            for product in compileer_producten(
                model.objecten,
                standaard_backend_registry(),
            )
        }

        product = producten["forge-dashboard-grafana"]
        dashboard = json.loads(product.inhoud)

        self.assertEqual("Forge Dashboard Grafana", dashboard["title"])
        self.assertEqual("forge-dashboard-grafana", dashboard["uid"])
        self.assertEqual(41, dashboard["schemaVersion"])
        self.assertEqual("dark", dashboard["style"])
        self.assertEqual(
            [
                {"h": 8, "w": 8, "x": 0, "y": 0},
                {"h": 8, "w": 8, "x": 8, "y": 0},
                {"h": 8, "w": 8, "x": 16, "y": 0},
            ],
            [panel["gridPos"] for panel in dashboard["panels"]],
        )
        self.assertEqual(
            [
                "Linker Forge-paneel",
                "Centraal Forge-paneel",
                "Rechter Forge-paneel",
            ],
            [panel["title"] for panel in dashboard["panels"]],
        )
        self.assertTrue(all(panel["type"] == "text" for panel in dashboard["panels"]))
        self.assertEqual(
            "Benoemd paneel voor de centrale dashboardinhoud.",
            dashboard["panels"][1]["options"]["content"],
        )
        self.assertEqual(
            "Benoemd paneel voor de centrale dashboardinhoud.\n\n"
            "BAT component: forge-panel\n"
            "BAT variant: forge-panel-compact\n"
            "BAT appearance: forge-panel-compact-appearance",
            dashboard["panels"][1]["description"],
        )
        self.assertEqual(
            "output/products/forge-dashboard.grafana.json",
            product.definitie.pad,
        )

    def test_weigert_niet_grid_layout_expliciet(self):
        bron = '''
component panel {
    naam: "Panel"
    doel: "Testcomponent."
}
compositie dashboard {
    naam: "Dashboard"
    doel: "Testinhoud."
    instanties: ["dashboard-panel"]
}
componentinstantie dashboard-panel {
    naam: "Dashboard panel"
    doel: "Testinhoud."
    compositie: "dashboard"
    component: "panel"
}
layout dashboard-stack {
    naam: "Dashboard stack"
    doel: "Testlayout."
    type: "stack"
    regions: ["content"]
    direction: "vertical"
}
region content {
    naam: "Content"
    doel: "Testregio."
    layout: "dashboard-stack"
    instantie: "dashboard-panel"
}
product dashboard-grafana {
    naam: "Dashboard Grafana"
    doel: "Testproduct."
    backend: "grafana"
    compositie: "dashboard"
    layout: "dashboard-stack"
    pad: "output/products/dashboard.grafana.json"
}
'''
        model = analyseer(parseer(bron), constraints=WORLD_MODEL_CONSTRAINTS)

        with self.assertRaisesRegex(
            ValueError,
            "ondersteunt alleen native grid-layouts",
        ):
            compileer_producten(model.objecten, standaard_backend_registry())

    def test_weigert_product_zonder_native_thema(self):
        model = analyseer(
            parseer_bestand(WORLD),
            constraints=WORLD_MODEL_CONSTRAINTS,
        )
        product = next(
            product
            for product in compileer_producten(
                model.objecten,
                standaard_backend_registry(),
            )
            if product.definitie.id == "forge-dashboard-grafana"
        )

        with self.assertRaisesRegex(
            ValueError,
            "vereist een opgelost native thema",
        ):
            backend.render(
                model.objecten,
                replace(product.definitie, thema=None),
            )


if __name__ == "__main__":
    unittest.main()

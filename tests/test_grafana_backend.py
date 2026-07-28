from __future__ import annotations

import json
import unittest
from dataclasses import replace
from pathlib import Path

from compiler.backends.grafana import backend
from compiler.parser import parseer, parseer_bestand
from compiler.product_backends import standaard_backend_registry
from compiler.product_compiler import compileer_producten
from compiler.product_model import SNAPSHOT_ID_LENGTH
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
        self.assertFalse(dashboard["editable"])
        self.assertEqual({"hidden": True}, dashboard["timepicker"])
        self.assertNotIn("refresh", dashboard)
        self.assertNotIn("time", dashboard)
        self.assertNotIn("timezone", dashboard)
        self.assertEqual(
            [
                {"h": 4, "w": 24, "x": 0, "y": 0},
                {"h": 16, "w": 8, "x": 0, "y": 4},
                {"h": 16, "w": 8, "x": 8, "y": 4},
                {"h": 16, "w": 8, "x": 16, "y": 4},
            ],
            [panel["gridPos"] for panel in dashboard["panels"]],
        )
        self.assertEqual(
            [
                "Forge Dashboard",
                (
                    "Wereld en identiteit, overzicht van wereld, merk en "
                    "bronassets"
                ),
                (
                    "Forge ontwerpsysteem, overzicht van ontwerpprimitieven "
                    "en componenten"
                ),
                (
                    "Productfamilie, overzicht van composities, layouts en "
                    "uitvoerproducten"
                ),
            ],
            [panel["title"] for panel in dashboard["panels"]],
        )
        self.assertTrue(all(panel["type"] == "canvas" for panel in dashboard["panels"]))
        self.assertEqual(
            "#282E36",
            dashboard["panels"][2]["options"]["root"]["background"]["color"]["fixed"],
        )
        self.assertEqual(
            "#20252C",
            dashboard["panels"][0]["options"]["root"]["background"]["color"]["fixed"],
        )
        self.assertEqual(
            {"color": {"fixed": "#46505C"}, "width": 2},
            dashboard["panels"][2]["options"]["root"]["border"],
        )
        middennamen = [
            element["name"]
            for element in dashboard["panels"][2]["options"]["root"]["elements"]
        ]
        self.assertIn("forge-dashboard-center-panel-metric-detail-labels", middennamen)
        self.assertIn("forge-dashboard-center-panel-metric-detail-values", middennamen)
        self.assertIn("forge-dashboard-center-panel-metric-detail-rule-15", middennamen)
        self.assertIn("forge-dashboard-center-panel-product-navigation", middennamen)
        self.assertIn("forge-dashboard-center-panel-content-anchors", middennamen)
        self.assertEqual(
            "Forge ontwerpsysteem, overzicht van ontwerpprimitieven en componenten",
            dashboard["panels"][2]["title"],
        )
        self.assertIn(
            "Leesvolgorde: 2",
            dashboard["panels"][2]["description"],
        )
        navigatie = next(
            element
            for element in dashboard["panels"][2]["options"]["root"]["elements"]
            if element["name"] == "forge-dashboard-center-panel-product-navigation"
        )
        self.assertEqual(
            ["components.html", "components.css", "tokens.css", "tokens.json"],
            [link["url"] for link in navigatie["links"]],
        )
        self.assertEqual(
            {"height": 528, "left": 4, "top": 4, "width": 4},
            dashboard["panels"][2]["options"]["root"]["elements"][0]["placement"],
        )
        inhoud = next(
            element
            for element in dashboard["panels"][2]["options"]["root"]["elements"]
            if element["name"] == "forge-dashboard-center-panel-content-anchors"
        )
        self.assertEqual(
            "Forge · thema\nNordic forge-ontwerpidentiteit voor Beckeringh Palace.\n"
            "Forge Materials · materiaal\nMateriële kleurrollen voor "
            "Forge-oppervlakken en accenten.\n"
            "Forge Panel · component\nBasispaneel voor dashboards en "
            "productdocumentatie.",
            inhoud["config"]["text"]["fixed"],
        )
        self.assertEqual(
            {
                "align": "left",
                "color": {"fixed": "#ECECEC"},
                "size": 28,
                "text": {"fixed": "Forge ontwerpsysteem", "mode": "fixed"},
                "valign": "top",
            },
            dashboard["panels"][2]["options"]["root"]["elements"][1]["config"],
        )
        self.assertEqual(
            {
                "height": 192,
                "left": 16,
                "top": 112,
                "width": 280,
            },
            dashboard["panels"][2]["options"]["root"]["elements"][3]["placement"],
        )
        self.assertEqual(
            "appearance\nborder\ncomponent\nkleur\nmateriaal\nmotion\npalet\nradius\n"
            "shadow\nspacing\nthema\ntoken\ntypeschaal\ntypografie\nvariant",
            dashboard["panels"][2]["options"]["root"]["elements"][3]["config"][
                "text"
            ]["fixed"],
        )
        self.assertEqual(
            {"fixed": "#AEB4BD"},
            dashboard["panels"][2]["options"]["root"]["elements"][3]["config"][
                "color"
            ],
        )
        self.assertEqual(
            {"fixed": "#AEB4BD"},
            dashboard["panels"][2]["options"]["root"]["elements"][-1]["config"][
                "color"
            ],
        )
        self.assertEqual(
            {"color": {"fixed": "#46505C"}, "width": 0},
            next(
                element
                for element in dashboard["panels"][2]["options"]["root"]["elements"]
                if element["name"] == "forge-dashboard-center-panel-metric-detail-rule-1"
            )["border"],
        )
        linker_elementen = {
            element["name"]: element
            for element in dashboard["panels"][1]["options"]["root"]["elements"]
        }
        self.assertEqual(
            {"fixed": "#AEB4BD"},
            linker_elementen[
                "forge-dashboard-left-panel-metric-detail-labels"
            ]["config"]["color"],
        )
        self.assertEqual(
            {"fixed": "#ECECEC"},
            linker_elementen[
                "forge-dashboard-left-panel-metric-detail-values"
            ]["config"]["color"],
        )
        self.assertEqual(
            {"color": {"fixed": "#46505C"}, "width": 0},
            linker_elementen[
                "forge-dashboard-left-panel-metric-detail-rule-1"
            ]["border"],
        )
        self.assertEqual(
            "30",
            dashboard["panels"][2]["options"]["root"]["elements"][2]["config"][
                "text"
            ]["fixed"],
        )
        self.assertEqual(
            ["2", "30", "31"],
            [
                panel["options"]["root"]["elements"][2]["config"]["text"][
                    "fixed"
                ]
                for panel in dashboard["panels"][1:]
            ],
        )
        self.assertEqual(
            "De ontwerpprimitieven, tokens en componentcontracten van de "
            "Forge-identiteit.\n\n"
            "BAT component: forge-panel\n"
            "BAT variant: forge-panel-compact\n"
            "BAT appearance: forge-panel-compact-appearance\n"
            "BAT informatiegebied: forge-design-system\n"
            "Toegankelijkheidslabel: Forge ontwerpsysteem, overzicht van "
            "ontwerpprimitieven en componenten\n"
            "Leesvolgorde: 2",
            dashboard["panels"][2]["description"],
        )
        self.assertEqual(
            "Beckeringh Palace · Forge · Gegenereerd uit BAT · "
            "Statische architectuursnapshot · Snapshot "
            f"{product.definitie.snapshot_id[:SNAPSHOT_ID_LENGTH]}",
            dashboard["panels"][0]["options"]["root"]["elements"][0]["config"][
                "text"
            ]["fixed"],
        )
        self.assertEqual(
            "Informatiearchitectuur van de Beckeringh Palace wereld, het Forge "
            "ontwerpsysteem en de productfamilie.",
            dashboard["panels"][0]["description"],
        )
        self.assertEqual(
            {"fixed": "#ECECEC"},
            dashboard["panels"][0]["options"]["root"]["elements"][1]["config"][
                "color"
            ],
        )
        self.assertEqual(
            {"fixed": "#AEB4BD"},
            dashboard["panels"][0]["options"]["root"]["elements"][2]["config"][
                "color"
            ],
        )
        self.assertEqual(
            "output/products/forge-dashboard.grafana.json",
            product.definitie.pad,
        )
        self.assertIn(product.definitie.snapshot_ref, dashboard["tags"])

    def test_interactief_product_behoudt_tijdcontext(self):
        model = analyseer(
            parseer_bestand(WORLD),
            constraints=WORLD_MODEL_CONSTRAINTS,
        )
        product = {
            product.definitie.id: product
            for product in compileer_producten(
                model.objecten,
                standaard_backend_registry(),
            )
        }["forge-dashboard-grafana"]
        interactief = replace(
            product.definitie,
            mode="interactive",
            has_time_context=True,
        )

        dashboard = json.loads(backend.render(model.objecten, interactief))

        self.assertEqual("", dashboard["refresh"])
        self.assertEqual(
            {"from": "now-6h", "to": "now"},
            dashboard["time"],
        )
        self.assertEqual("browser", dashboard["timezone"])

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

    def test_weigert_niet_pixelgebaseerde_canvas_spacing(self):
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
        thema = product.definitie.thema
        assert thema is not None
        assert thema.spacing is not None
        ongeldige_spacing = replace(thema.spacing, xs="0.25rem")

        with self.assertRaisesRegex(
            ValueError,
            "vereist een px-waarde voor spacing.xs",
        ):
            backend.render(
                model.objecten,
                replace(
                    product.definitie,
                    thema=replace(thema, spacing=ongeldige_spacing),
                ),
            )


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import unittest
from pathlib import Path

from compiler.layout_model import LayoutType
from compiler.parser import parseer_bestand
from compiler.product_backends import standaard_backend_registry
from compiler.product_compiler import compileer_producten
from compiler.product_constraints import WORLD_MODEL_CONSTRAINTS
from compiler.semantic import analyseer
from compiler.spatial_model import bouw_spatial_model


ROOT = Path(__file__).resolve().parents[1]
WORLD = ROOT / "architectuur" / "world.bp"


class ForgeNativeLayoutMigrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.model = analyseer(
            parseer_bestand(WORLD),
            constraints=WORLD_MODEL_CONSTRAINTS,
        )

    def test_forge_dashboard_gebruikt_native_gridcontract(self) -> None:
        producten = {
            product.definitie.id: product
            for product in compileer_producten(
                self.model.objecten,
                standaard_backend_registry(),
            )
        }
        product = producten["forge-dashboard-html"]
        layout = product.definitie.opgeloste_layout

        self.assertIsNotNone(layout)
        assert layout is not None
        self.assertEqual(LayoutType.GRID, layout.type)
        self.assertEqual((3, 1), (layout.columns, layout.rows))
        self.assertEqual(
            (
                "forge-dashboard-left",
                "forge-dashboard-center",
                "forge-dashboard-right",
            ),
            tuple(region.id for region in layout.regions),
        )
        self.assertIn('data-layout-type="grid"', product.inhoud)
        self.assertIn(
            "grid-template-columns:repeat(3,minmax(0,1fr))",
            product.inhoud,
        )

    def test_forge_dashboard_is_geen_spatial_layout_meer(self) -> None:
        self.assertNotIn(
            "forge-dashboard-ultrawide",
            {layout.id for layout in bouw_spatial_model(self.model.objecten)},
        )


if __name__ == "__main__":
    unittest.main()

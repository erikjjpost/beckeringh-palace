from __future__ import annotations

import unittest
from pathlib import Path

from compiler.layout_model import LayoutType
from compiler.parser import parseer_bestand
from compiler.product_backends import standaard_backend_registry
from compiler.product_compiler import compileer_producten
from compiler.product_model import SNAPSHOT_ID_LENGTH
from compiler.product_constraints import WORLD_MODEL_CONSTRAINTS
from compiler.semantic import analyseer


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
        compositie = product.definitie.opgeloste_compositie
        layout = product.definitie.opgeloste_layout

        self.assertIsNotNone(compositie)
        self.assertIsNotNone(layout)
        assert compositie is not None
        assert layout is not None
        self.assertEqual(
            (
                "forge-dashboard-left-panel",
                "forge-dashboard-center-panel",
                "forge-dashboard-right-panel",
            ),
            tuple(instantie.id for instantie in compositie.instances),
        )
        self.assertIsNone(compositie.instances[0].variant_id)
        self.assertEqual(
            "forge-panel-compact",
            compositie.instances[1].variant_id,
        )
        self.assertEqual(
            "forge-panel-card-rest-appearance",
            compositie.instances[1].appearance_id,
        )
        self.assertIsNone(compositie.instances[2].variant_id)
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
        self.assertEqual(
            tuple(instantie.id for instantie in compositie.instances),
            tuple(region.instance_id for region in layout.regions),
        )
        self.assertIn('data-layout-type="grid"', product.inhoud)
        self.assertIn(
            "Beckeringh Palace · Forge · Gegenereerd uit BAT",
            product.inhoud,
        )
        self.assertIn("<h1>Forge Dashboard</h1>", product.inhoud)
        self.assertIn(
            "<p class=\"bp-product-purpose\">Informatiearchitectuur van de "
            "Beckeringh Palace wereld, het Forge ontwerpsysteem en de "
            "productfamilie.</p>",
            product.inhoud,
        )
        self.assertIn("@media (max-width: 960px)", product.inhoud)
        self.assertIn(
            "grid-template-columns:repeat(3,minmax(0,1fr))",
            product.inhoud,
        )
        self.assertIn(
            'data-variant="forge-panel-compact" '
            'data-appearance="forge-panel-card-rest-appearance"',
            product.inhoud,
        )
        self.assertIn(
            'class="bp-region bp-forge-panel bp-variant-forge-panel-compact"',
            product.inhoud,
        )
        self.assertEqual(1, product.inhoud.count('data-variant="'))
        self.assertEqual(
            ("2", "145", "79"),
            tuple(
                str(instantie.metric_value)
                for instantie in compositie.instances
            ),
        )
        self.assertIn(
            '<p class="bp-metric" data-metric-kind="informatiegebied:palace-world">2</p>',
            product.inhoud,
        )
        self.assertIn(
            '<p class="bp-metric" data-metric-kind="informatiegebied:forge-design-system">145</p>',
            product.inhoud,
        )
        self.assertIn(
            '<p class="bp-metric" data-metric-kind="informatiegebied:palace-product-family">79</p>',
            product.inhoud,
        )
        self.assertIn(
            'data-information-area="palace-world" data-reading-order="1" '
            'data-accessibility-contract="forge-panel-accessibility"',
            product.inhoud,
        )
        self.assertIn(
            'aria-label="Wereld en identiteit, overzicht van wereld, merk en '
            'bronassets"',
            product.inhoud,
        )
        self.assertLess(
            product.inhoud.index('data-reading-order="1"'),
            product.inhoud.index('data-reading-order="2"'),
        )
        self.assertLess(
            product.inhoud.index('data-reading-order="2"'),
            product.inhoud.index('data-reading-order="3"'),
        )
        self.assertIn(
            '<a href="components.html" '
            'data-navigation-target="forge-design-system-reference-html" '
            'data-navigation-kind="product">'
            'EmberForge Design System Referentie</a>',
            product.inhoud,
        )
        self.assertIn(
            '<a href="project-status.html" data-navigation-target="project-status-html" '
            'data-navigation-kind="product">Beckeringh Palace Projectstatus</a>',
            product.inhoud,
        )
        self.assertIn(
            '<li data-content-anchor="forge" data-object-kind="thema">'
            "<strong>Forge</strong><span>Nordic forge-ontwerpidentiteit voor "
            "Beckeringh Palace.</span></li>",
            product.inhoud,
        )
        self.assertEqual(24, product.inhoud.count('data-content-anchor="'))
        self.assertIn('<ul class="bp-metric-details">', product.inhoud)
        self.assertIn('data-product-mode="static"', product.inhoud)
        self.assertIn('data-time-context="none"', product.inhoud)
        self.assertEqual(64, len(product.definitie.snapshot_id))
        self.assertIn(
            f'data-snapshot-id="{product.definitie.snapshot_id}"',
            product.inhoud,
        )
        self.assertIn(
            f'data-snapshot-ref="{product.definitie.snapshot_ref}"',
            product.inhoud,
        )
        self.assertIn(
            "Beckeringh Palace · Forge · Gegenereerd uit BAT · "
            "Statische architectuursnapshot · Snapshot "
            f"{product.definitie.snapshot_id[:SNAPSHOT_ID_LENGTH]}",
            product.inhoud,
        )
        self.assertIn(
            'data-information-area="forge-design-system"',
            product.inhoud,
        )
        self.assertIn(
            '<li><span>token</span><span class="bp-metric-detail-value">10</span></li>',
            product.inhoud,
        )
        self.assertIn(
            '<p class="bp-description">De digitale wereld, haar merk en haar '
            "reproduceerbare bronassets.</p>",
            product.inhoud,
        )


if __name__ == "__main__":
    unittest.main()

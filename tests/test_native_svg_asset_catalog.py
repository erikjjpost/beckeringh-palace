from __future__ import annotations

import json
import unittest
from pathlib import Path

from compiler.parser import parseer, parseer_bestand
from compiler.product_backends import standaard_backend_registry
from compiler.product_compiler import compileer_producten
from compiler.product_constraints import WORLD_MODEL_CONSTRAINTS
from compiler.semantic import SemantischeFout, analyseer
from compiler.svg_asset_catalog import resolveer_svg_assetcatalogus


ROOT = Path(__file__).resolve().parents[1]
WORLD = ROOT / "architectuur" / "world.bp"
DESIGN_INPUT = (
    ROOT / "project" / "design-inputs" / "emberforge-design-system.json"
)


BRON = '''
asset forge-node {
    naam: "Forge Node"
    doel: "Decoratief technisch lijnmotief."
    formaat: "svg"
    rol: "ornament"
    viewbox: "0 0 64 64"
    paden: ["M32 6 L56 32 L32 58 L8 32 Z"]
    vulling: "none"
    lijn: "currentColor"
    lijndikte: "2"
    lijneinde: "round"
    lijnverbinding: "round"
    toegankelijkheid: "decoratief"
}
asset forge-mark {
    naam: "Forge Mark"
    doel: "Informatief gevuld merkteken."
    formaat: "svg"
    rol: "icoon"
    viewbox: "0 0 32 32"
    paden: ["M4 4 L28 4 L28 28 L4 28 Z"]
    vulling: "currentColor"
    lijn: "none"
    toegankelijkheid: "informatief"
    label: "Forge merkteken"
}
component panel {
    naam: "Panel"
    doel: "Cataloguspaneel."
}
compositie asset-catalog-content {
    naam: "Assetcatalogus"
    doel: "Testinhoud voor alle native assets."
    instanties: ["catalog-content"]
}
componentinstantie catalog-content {
    naam: "Native assets"
    doel: "Alle getypeerde SVG assets."
    compositie: "asset-catalog-content"
    component: "panel"
}
layout asset-catalog-stack {
    naam: "Assetcatalogus stack"
    doel: "Plaatst de catalogusinhoud."
    type: "stack"
    regions: ["asset-catalog-region"]
    direction: "vertical"
}
region asset-catalog-region {
    naam: "Assetcatalogusregio"
    doel: "Enige catalogusregio."
    layout: "asset-catalog-stack"
    instantie: "catalog-content"
}
product forge-node-svg {
    naam: "Forge Node SVG"
    doel: "Genereert het decoratieve lijnmotief."
    backend: "svg"
    mode: "static"
    inhoud: "asset"
    asset: "forge-node"
    pad: "output/products/forge-node.svg"
}
product forge-mark-svg {
    naam: "Forge Mark SVG"
    doel: "Genereert het informatieve merkteken."
    backend: "svg"
    mode: "static"
    inhoud: "asset"
    asset: "forge-mark"
    pad: "output/products/forge-mark.svg"
}
product forge-assets-html {
    naam: "Forge SVG Asset Catalog"
    doel: "Ontsluit alle native SVG assets."
    backend: "html"
    mode: "static"
    inhoud: "asset-catalog"
    compositie: "asset-catalog-content"
    layout: "asset-catalog-stack"
    assets: ["forge-node", "forge-mark"]
    pad: "output/products/assets.html"
}
'''


class NativeSvgAssetCatalogTests(unittest.TestCase):
    def _diagnostic_codes(self, bron: str) -> set[str]:
        with self.assertRaises(SemantischeFout) as context:
            analyseer(parseer(bron), constraints=WORLD_MODEL_CONSTRAINTS)
        return {
            diagnostic.code
            for diagnostic in context.exception.diagnostics
        }

    def test_resolveert_expliciete_catalogusvolgorde_en_artifacts(self) -> None:
        model = analyseer(parseer(BRON), constraints=WORLD_MODEL_CONSTRAINTS)

        catalog = resolveer_svg_assetcatalogus(
            model.objecten,
            ("forge-node", "forge-mark"),
        )

        self.assertEqual(
            ("forge-node", "forge-mark"),
            tuple(entry.asset.id for entry in catalog.entries),
        )
        self.assertEqual(
            ("forge-node-svg", "forge-mark-svg"),
            tuple(entry.artifact_product_id for entry in catalog.entries),
        )
        self.assertEqual(
            (
                "output/products/forge-node.svg",
                "output/products/forge-mark.svg",
            ),
            tuple(entry.artifact_path for entry in catalog.entries),
        )

    def test_compileert_navigeerbare_catalogus_uit_opgeloste_assets(self) -> None:
        model = analyseer(parseer(BRON), constraints=WORLD_MODEL_CONSTRAINTS)
        products = {
            product.definitie.id: product
            for product in compileer_producten(
                model.objecten,
                standaard_backend_registry(),
            )
        }

        product = products["forge-assets-html"]
        html = product.inhoud

        self.assertEqual(
            ("forge-node", "forge-mark"),
            product.definitie.asset_ids,
        )
        self.assertEqual(
            2,
            len(product.definitie.asset_catalog.entries),
        )
        self.assertIn('data-asset-count="2"', html)
        self.assertEqual(2, html.count('class="bp-asset-card"'))
        self.assertEqual(2, html.count('data-bp-preview="true"'))
        self.assertIn('href="forge-node.svg"', html)
        self.assertIn('href="forge-mark.svg"', html)
        self.assertIn("Forge merkteken", html)
        self.assertIn(
            f'data-bp-snapshot="{product.definitie.snapshot_ref}"',
            html,
        )
        self.assertNotIn("<script", html)
        self.assertNotIn("url(", html)

    def test_catalogus_is_onafhankelijk_van_bronvolgorde(self) -> None:
        model = analyseer(parseer(BRON), constraints=WORLD_MODEL_CONSTRAINTS)

        eerste = next(
            product.inhoud
            for product in compileer_producten(
                model.objecten,
                standaard_backend_registry(),
            )
            if product.definitie.id == "forge-assets-html"
        )
        tweede = next(
            product.inhoud
            for product in compileer_producten(
                tuple(reversed(model.objecten)),
                standaard_backend_registry(),
            )
            if product.definitie.id == "forge-assets-html"
        )

        self.assertEqual(eerste, tweede)

    def test_weigert_impliciete_onbekende_of_onvolledige_dekking(self) -> None:
        self.assertIn(
            "BP4321",
            self._diagnostic_codes(
                BRON.replace(
                    '    asset: "forge-node"',
                    '    asset: "forge-node"\n'
                    '    assets: ["forge-node", "forge-mark"]',
                    1,
                )
            ),
        )
        self.assertIn(
            "BP4322",
            self._diagnostic_codes(
                BRON.replace(
                    'assets: ["forge-node", "forge-mark"]',
                    'assets: ["forge-node", "forge-node"]',
                )
            ),
        )
        self.assertIn(
            "BP4323",
            self._diagnostic_codes(
                BRON.replace(
                    'assets: ["forge-node", "forge-mark"]',
                    'assets: ["forge-node", "missing"]',
                )
            ),
        )
        self.assertIn(
            "BP4324",
            self._diagnostic_codes(
                BRON.replace(
                    'assets: ["forge-node", "forge-mark"]',
                    'assets: ["forge-node"]',
                )
            ),
        )

    def test_weigert_ontbrekend_of_ambigu_artifactproduct(self) -> None:
        invalid = BRON.replace(
            '    asset: "forge-mark"\n'
            '    pad: "output/products/forge-mark.svg"',
            '    asset: "forge-node"\n'
            '    pad: "output/products/forge-mark.svg"',
        )

        self.assertIn("BP4325", self._diagnostic_codes(invalid))

    def test_weigert_verkeerde_backend_mode_pad_en_compositie(self) -> None:
        self.assertIn(
            "BP4326",
            self._diagnostic_codes(
                BRON.replace(
                    'product forge-assets-html {\n'
                    '    naam: "Forge SVG Asset Catalog"\n'
                    '    doel: "Ontsluit alle native SVG assets."\n'
                    '    backend: "html"',
                    'product forge-assets-html {\n'
                    '    naam: "Forge SVG Asset Catalog"\n'
                    '    doel: "Ontsluit alle native SVG assets."\n'
                    '    backend: "grafana"',
                )
            ),
        )
        self.assertIn(
            "BP4327",
            self._diagnostic_codes(
                BRON.replace(
                    'product forge-assets-html {\n'
                    '    naam: "Forge SVG Asset Catalog"\n'
                    '    doel: "Ontsluit alle native SVG assets."\n'
                    '    backend: "html"\n'
                    '    mode: "static"',
                    'product forge-assets-html {\n'
                    '    naam: "Forge SVG Asset Catalog"\n'
                    '    doel: "Ontsluit alle native SVG assets."\n'
                    '    backend: "html"\n'
                    '    mode: "interactive"',
                )
            ),
        )
        self.assertIn(
            "BP4328",
            self._diagnostic_codes(
                BRON.replace(
                    'pad: "output/products/assets.html"',
                    'pad: "output/products/assets.json"',
                )
            ),
        )
        self.assertIn(
            "BP4329",
            self._diagnostic_codes(
                BRON.replace(
                    'instanties: ["catalog-content"]',
                    'instanties: ["catalog-content", "catalog-content"]',
                )
            ),
        )

    def test_world_publiceert_catalogus_en_homepageroute(self) -> None:
        model = analyseer(
            parseer_bestand(WORLD),
            constraints=WORLD_MODEL_CONSTRAINTS,
        )
        products = {
            product.definitie.id: product
            for product in compileer_producten(
                model.objecten,
                standaard_backend_registry(),
            )
        }

        catalog = products["emberforge-svg-asset-catalog-html"]
        homepage = products["beckeringh-palace-homepage"].inhoud

        self.assertEqual("asset-catalog", catalog.definitie.inhoud)
        self.assertIn(
            'data-product-content="asset-catalog"',
            catalog.inhoud,
        )
        self.assertEqual(
            (
                "emberforge-vector-node",
                "emberforge-icon-dashboard",
                "emberforge-icon-identity",
                "emberforge-icon-terminal",
                "emberforge-icon-assets",
                "emberforge-merkteken",
                "emberforge-woordmerk",
            ),
            catalog.definitie.asset_ids,
        )
        self.assertIn(
            'data-asset="emberforge-vector-node"',
            catalog.inhoud,
        )
        self.assertIn(
            'href="emberforge-vector-node.svg" '
            'data-asset-product="emberforge-vector-node-svg"',
            catalog.inhoud,
        )
        for asset_id in (
            "emberforge-icon-dashboard",
            "emberforge-icon-identity",
            "emberforge-icon-terminal",
            "emberforge-icon-assets",
            "emberforge-merkteken",
            "emberforge-woordmerk",
        ):
            self.assertIn(f'data-asset="{asset_id}"', catalog.inhoud)
            self.assertIn(
                f'href="{asset_id}.svg" '
                f'data-asset-product="{asset_id}-svg"',
                catalog.inhoud,
            )
        self.assertIn(
            'data-asset-family="emberforge-merkassets" '
            'data-asset-variant="merkteken"',
            catalog.inhoud,
        )
        self.assertIn(
            "<dd>EmberForge merkassets (merk)</dd>",
            catalog.inhoud,
        )
        self.assertEqual(
            1,
            homepage.count(
                'href="assets.html" '
                'data-navigation-target="'
                'emberforge-svg-asset-catalog-html"'
            ),
        )

    def test_designbron_registreert_catalogus_zonder_placeholderactivering(
        self,
    ) -> None:
        source = json.loads(DESIGN_INPUT.read_text(encoding="utf-8"))
        vector_assets = next(
            area
            for area in source["gebieden"]
            if area["id"] == "vector-assets"
        )

        self.assertEqual("geblokkeerd", vector_assets["status"])
        self.assertIn("M11.5a", vector_assets["bewijs"])
        self.assertIn("M11.5b", vector_assets["bewijs"])
        self.assertIn("catalogus", vector_assets["bewijs"])
        self.assertIn("placeholders", vector_assets["bewijs"])


if __name__ == "__main__":
    unittest.main()

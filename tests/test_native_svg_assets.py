from __future__ import annotations

import unittest
from pathlib import Path

from compiler.parser import parseer, parseer_bestand
from compiler.product_backends import standaard_backend_registry
from compiler.product_compiler import compileer_producten
from compiler.product_constraints import WORLD_MODEL_CONSTRAINTS
from compiler.semantic import SemantischeFout, analyseer
from compiler.svg_assets import resolveer_svg_assets


ROOT = Path(__file__).resolve().parents[1]
WORLD = ROOT / "architectuur" / "world.bp"


BRON = '''
asset forge-vector-node {
    naam: "Forge Vector Node"
    doel: "Herbruikbaar technisch lijnmotief voor EmberForge vectorproducten."
    formaat: "svg"
    rol: "icoon"
    viewbox: "0 0 64 64"
    paden: ["M32 6 L38 24 L56 32 L38 40 L32 58 L26 40 L8 32 L26 24 Z", "M32 22 L42 32 L32 42 L22 32 Z"]
    vulling: "none"
    lijn: "currentColor"
    lijndikte: "2"
    lijneinde: "round"
    lijnverbinding: "round"
    toegankelijkheid: "informatief"
    label: "Technisch Forge lijnmotief"
}

product forge-vector-node-svg {
    naam: "Forge Vector Node SVG"
    doel: "Genereert het native lijnmotief als veilig SVG product."
    backend: "svg"
    mode: "static"
    inhoud: "asset"
    asset: "forge-vector-node"
    pad: "output/products/forge-vector-node.svg"
}
'''


class NativeSvgAssetTests(unittest.TestCase):
    def _diagnostic_codes(self, bron: str) -> set[str]:
        with self.assertRaises(SemantischeFout) as context:
            analyseer(parseer(bron), constraints=WORLD_MODEL_CONSTRAINTS)
        return {
            diagnostic.code
            for diagnostic in context.exception.diagnostics
        }

    def test_resolveert_getypeerde_svg_geometrie(self):
        model = analyseer(parseer(BRON), constraints=WORLD_MODEL_CONSTRAINTS)

        asset = resolveer_svg_assets(model.objecten)[0]

        self.assertEqual("forge-vector-node", asset.id)
        self.assertEqual("icoon", asset.rol)
        self.assertEqual((0.0, 0.0, 64.0, 64.0), asset.viewbox)
        self.assertEqual(2, len(asset.paden))
        self.assertEqual("currentColor", asset.lijn)
        self.assertEqual(2.0, asset.lijndikte)
        self.assertEqual("informatief", asset.toegankelijkheid)
        self.assertEqual("Technisch Forge lijnmotief", asset.label)

    def test_world_model_publiceert_het_native_emberforge_ornament(self):
        model = analyseer(
            parseer_bestand(WORLD),
            constraints=WORLD_MODEL_CONSTRAINTS,
        )
        asset = next(
            asset
            for asset in resolveer_svg_assets(model.objecten)
            if asset.id == "emberforge-vector-node"
        )
        product = next(
            product
            for product in compileer_producten(
                model.objecten,
                standaard_backend_registry(),
            )
            if product.definitie.id == "emberforge-vector-node-svg"
        )

        self.assertEqual("ornament", asset.rol)
        self.assertEqual("decoratief", asset.toegankelijkheid)
        self.assertEqual(
            "output/products/emberforge-vector-node.svg",
            product.definitie.pad,
        )
        self.assertIn(
            'data-bp-asset="emberforge-vector-node"',
            product.inhoud,
        )
        self.assertIn('aria-hidden="true"', product.inhoud)

    def test_world_model_publiceert_een_samenhangende_iconenfamilie(self):
        model = analyseer(
            parseer_bestand(WORLD),
            constraints=WORLD_MODEL_CONSTRAINTS,
        )
        assets = {
            asset.id: asset
            for asset in resolveer_svg_assets(model.objecten)
        }
        icon_ids = (
            "emberforge-icon-dashboard",
            "emberforge-icon-identity",
            "emberforge-icon-terminal",
            "emberforge-icon-assets",
        )

        self.assertEqual(set(icon_ids), {
            asset_id for asset_id in assets if asset_id.startswith("emberforge-icon-")
        })
        self.assertEqual(
            {"icoon"},
            {assets[asset_id].rol for asset_id in icon_ids},
        )
        self.assertEqual(
            {(0.0, 0.0, 24.0, 24.0)},
            {assets[asset_id].viewbox for asset_id in icon_ids},
        )
        self.assertEqual(
            {"none"},
            {assets[asset_id].vulling for asset_id in icon_ids},
        )
        self.assertEqual(
            {"currentColor"},
            {assets[asset_id].lijn for asset_id in icon_ids},
        )
        self.assertEqual(
            {1.5},
            {assets[asset_id].lijndikte for asset_id in icon_ids},
        )
        self.assertEqual(
            {"round"},
            {assets[asset_id].lijneinde for asset_id in icon_ids},
        )
        self.assertEqual(
            {"round"},
            {assets[asset_id].lijnverbinding for asset_id in icon_ids},
        )
        self.assertEqual(
            {"informatief"},
            {assets[asset_id].toegankelijkheid for asset_id in icon_ids},
        )
        self.assertEqual(
            {"Dashboard", "Identity", "Terminal", "Assets"},
            {assets[asset_id].label for asset_id in icon_ids},
        )

    def test_compileert_een_veilig_statisch_svg_product(self):
        model = analyseer(parseer(BRON), constraints=WORLD_MODEL_CONSTRAINTS)

        product = compileer_producten(
            model.objecten,
            standaard_backend_registry(),
        )[0]

        self.assertEqual("forge-vector-node", product.definitie.asset)
        self.assertEqual(
            "forge-vector-node",
            product.definitie.opgelost_asset.id,
        )
        self.assertIn(
            '<svg xmlns="http://www.w3.org/2000/svg" '
            'viewBox="0 0 64 64"',
            product.inhoud,
        )
        self.assertIn('role="img"', product.inhoud)
        self.assertIn(
            'aria-labelledby="forge-vector-node-title"',
            product.inhoud,
        )
        self.assertIn(
            "<title id=\"forge-vector-node-title\">"
            "Technisch Forge lijnmotief</title>",
            product.inhoud,
        )
        self.assertIn('stroke="currentColor"', product.inhoud)
        self.assertIn('stroke-width="2"', product.inhoud)
        self.assertIn('data-bp-snapshot="sha256:', product.inhoud)
        self.assertNotIn("<script", product.inhoud)
        self.assertNotIn("href=", product.inhoud)

    def test_svg_product_is_onafhankelijk_van_bronvolgorde(self):
        model = analyseer(parseer(BRON), constraints=WORLD_MODEL_CONSTRAINTS)

        eerste = compileer_producten(
            model.objecten,
            standaard_backend_registry(),
        )[0].inhoud
        tweede = compileer_producten(
            tuple(reversed(model.objecten)),
            standaard_backend_registry(),
        )[0].inhoud

        self.assertEqual(eerste, tweede)

    def test_decoratief_asset_krijgt_geen_toegankelijke_naam(self):
        bron = BRON.replace(
            'toegankelijkheid: "informatief"\n'
            '    label: "Technisch Forge lijnmotief"',
            'toegankelijkheid: "decoratief"',
        )
        model = analyseer(parseer(bron), constraints=WORLD_MODEL_CONSTRAINTS)

        inhoud = compileer_producten(
            model.objecten,
            standaard_backend_registry(),
        )[0].inhoud

        self.assertIn('aria-hidden="true"', inhoud)
        self.assertNotIn("<title", inhoud)
        self.assertNotIn('role="img"', inhoud)

    def test_weigert_onbekende_assetvelden_en_assettypen(self):
        self.assertIn(
            "BP4301",
            self._diagnostic_codes(
                BRON.replace(
                    '    formaat: "svg"',
                    '    formaat: "svg"\n    bron: "unsafe.svg"',
                )
            ),
        )
        self.assertIn(
            "BP4302",
            self._diagnostic_codes(
                BRON.replace('formaat: "svg"', 'formaat: "png"')
            ),
        )
        self.assertIn(
            "BP4303",
            self._diagnostic_codes(
                BRON.replace('rol: "icoon"', 'rol: "widget"')
            ),
        )

    def test_weigert_ongeldige_viewbox_en_padgeometrie(self):
        self.assertIn(
            "BP4304",
            self._diagnostic_codes(
                BRON.replace('viewbox: "0 0 64 64"', 'viewbox: "0 0 64 0"')
            ),
        )
        self.assertIn(
            "BP4305",
            self._diagnostic_codes(
                BRON.replace(
                    'paden: ["M32 6 L38 24 L56 32 L38 40 L32 58 L26 40 L8 32 L26 24 Z", "M32 22 L42 32 L32 42 L22 32 Z"]',
                    'paden: ["M0 0 L1 1", "M0 0 L1 1"]',
                )
            ),
        )
        self.assertIn(
            "BP4306",
            self._diagnostic_codes(
                BRON.replace(
                    '"M32 22 L42 32 L32 42 L22 32 Z"',
                    '"M0 0 <script> Z"',
                )
            ),
        )

    def test_weigert_actieve_svg_inhoud_en_inconsistent_lijncontract(self):
        self.assertIn(
            "BP4307",
            self._diagnostic_codes(
                BRON.replace(
                    'lijn: "currentColor"',
                    'lijn: "url(https://example.invalid/paint)"',
                )
            ),
        )
        self.assertIn(
            "BP4308",
            self._diagnostic_codes(
                BRON.replace('    lijndikte: "2"\n', "")
            ),
        )

    def test_weigert_impliciete_toegankelijkheid(self):
        self.assertIn(
            "BP4309",
            self._diagnostic_codes(
                BRON.replace(
                    'toegankelijkheid: "informatief"',
                    'toegankelijkheid: "auto"',
                )
            ),
        )
        self.assertIn(
            "BP4310",
            self._diagnostic_codes(
                BRON.replace(
                    '    label: "Technisch Forge lijnmotief"\n',
                    "",
                )
            ),
        )
        self.assertIn(
            "BP4310",
            self._diagnostic_codes(
                BRON.replace(
                    'toegankelijkheid: "informatief"',
                    'toegankelijkheid: "decoratief"',
                )
            ),
        )

    def test_weigert_onvolledig_of_verkeerd_svg_productcontract(self):
        self.assertIn(
            "BP3510",
            self._diagnostic_codes(
                BRON.replace(
                    'asset: "forge-vector-node"',
                    'asset: "missing"',
                )
            ),
        )
        self.assertIn(
            "BP3511",
            self._diagnostic_codes(
                BRON.replace('backend: "svg"', 'backend: "html"')
            ),
        )
        self.assertIn(
            "BP3512",
            self._diagnostic_codes(
                BRON.replace('mode: "static"', 'mode: "interactive"')
            ),
        )
        self.assertIn(
            "BP3513",
            self._diagnostic_codes(
                BRON.replace(
                    '    asset: "forge-vector-node"',
                    '    asset: "forge-vector-node"\n    layout: "missing"',
                )
            ),
        )
        self.assertIn(
            "BP3514",
            self._diagnostic_codes(
                BRON.replace(
                    "output/products/forge-vector-node.svg",
                    "output/products/forge-vector-node.html",
                )
            ),
        )


if __name__ == "__main__":
    unittest.main()

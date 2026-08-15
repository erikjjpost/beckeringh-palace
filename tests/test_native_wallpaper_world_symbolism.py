"""Regressiecontracten voor native EmberForge wallpaperwereldsymboliek."""
from __future__ import annotations

import unittest
from pathlib import Path

from compiler.parser import parseer_bestand
from compiler.product_backends import standaard_backend_registry
from compiler.product_compiler import compileer_producten
from compiler.product_constraints import WORLD_MODEL_CONSTRAINTS
from compiler.semantic import analyseer
from compiler.svg_assets import resolveer_svg_assets
from compiler.wallpaper_products import resolveer_wallpapers


ROOT = Path(__file__).resolve().parents[1]
WORLD = ROOT / "architectuur" / "world.bp"


class NativeWallpaperWorldSymbolismTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.model = analyseer(
            parseer_bestand(WORLD),
            constraints=WORLD_MODEL_CONSTRAINTS,
        )
        cls.assets = {
            asset.id: asset
            for asset in resolveer_svg_assets(cls.model.objecten)
        }
        cls.wallpapers = {
            wallpaper.id: wallpaper
            for wallpaper in resolveer_wallpapers(cls.model.objecten)
        }

    def test_symboliek_is_veilige_native_lijngeometrie(self) -> None:
        expected_roles = {
            "emberforge-palace": "illustratie",
            "emberforge-beaver": "illustratie",
            "emberforge-nordic-weave": "ornament",
        }
        for asset_id, role in expected_roles.items():
            with self.subTest(asset=asset_id):
                asset = self.assets[asset_id]
                self.assertEqual(role, asset.rol)
                self.assertEqual("none", asset.vulling)
                self.assertEqual("currentColor", asset.lijn)
                self.assertEqual("decoratief", asset.toegankelijkheid)
                self.assertIsNone(asset.label)

    def test_beide_formaten_hebben_een_eigen_wereldlaag_onder_muziek(self) -> None:
        for wallpaper in self.wallpapers.values():
            with self.subTest(wallpaper=wallpaper.id):
                world_index = next(
                    index
                    for index, layer in enumerate(wallpaper.lagen)
                    if "wereldlaag" in layer.id
                )
                music_index = next(
                    index
                    for index, layer in enumerate(wallpaper.lagen)
                    if "muzieklaag" in layer.id
                )
                world_layer = wallpaper.lagen[world_index]
                self.assertEqual("illustratie", world_layer.rol)
                self.assertLess(world_index, music_index)
                self.assertEqual(
                    (
                        "emberforge-palace",
                        "emberforge-beaver",
                        "emberforge-beaver",
                    ),
                    tuple(item.asset.id for item in world_layer.plaatsingen),
                )
                self.assertEqual(
                    ("muted", "muted", "muted"),
                    tuple(item.color_role for item in world_layer.plaatsingen),
                )
                self.assertTrue(
                    all(item.dekking <= 0.16 for item in world_layer.plaatsingen)
                )

    def test_noorse_vlecht_blijft_ornament_en_voegt_geen_warmte_toe(self) -> None:
        for wallpaper in self.wallpapers.values():
            with self.subTest(wallpaper=wallpaper.id):
                ornament = next(
                    layer for layer in wallpaper.lagen
                    if "ornamentlaag" in layer.id
                )
                weave = [
                    item
                    for item in ornament.plaatsingen
                    if item.asset.id == "emberforge-nordic-weave"
                ]
                self.assertEqual(4, len(weave))
                self.assertEqual(4, len(ornament.plaatsingen))
                self.assertTrue(
                    all(item.color_role == "interaction" for item in weave)
                )
                self.assertTrue(all(item.dekking <= 0.10 for item in weave))

    def test_circle_of_fifths_geometrie_blijft_ongewijzigd(self) -> None:
        expected = {
            "emberforge-ultrawide-wallpaper": (1410, 30, 1020, 1020),
            "emberforge-desktop-wallpaper": (350, 50, 1200, 1100),
        }
        for wallpaper_id, geometry in expected.items():
            wallpaper = self.wallpapers[wallpaper_id]
            music = next(
                layer for layer in wallpaper.lagen if "muzieklaag" in layer.id
            )
            self.assertEqual(1, len(music.plaatsingen))
            placement = music.plaatsingen[0]
            self.assertEqual("emberforge-circle-of-fifths", placement.asset.id)
            self.assertEqual(
                geometry,
                (
                    placement.x,
                    placement.y,
                    placement.breedte,
                    placement.hoogte,
                ),
            )

    def test_symboliek_wordt_als_herbruikbare_svg_producten_gepubliceerd(self) -> None:
        products = {
            product.definitie.id: product
            for product in compileer_producten(
                self.model.objecten,
                standaard_backend_registry(),
            )
        }
        for asset_id in (
            "emberforge-palace",
            "emberforge-beaver",
            "emberforge-nordic-weave",
        ):
            with self.subTest(asset=asset_id):
                product = products[f"{asset_id}-svg"]
                self.assertIn(f'data-bp-asset="{asset_id}"', product.inhoud)

        catalog = products["emberforge-svg-asset-catalog-html"]
        for asset_id in (
            "emberforge-palace",
            "emberforge-beaver",
            "emberforge-nordic-weave",
        ):
            self.assertIn(f'data-asset="{asset_id}"', catalog.inhoud)


if __name__ == "__main__":
    unittest.main()

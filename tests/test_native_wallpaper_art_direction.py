"""Regressiecontracten voor de native EmberForge wallpaperlichtwerking."""
from __future__ import annotations

import unittest
from pathlib import Path

from compiler.parser import parseer_bestand
from compiler.product_constraints import WORLD_MODEL_CONSTRAINTS
from compiler.semantic import analyseer
from compiler.wallpaper_products import resolveer_wallpapers


ROOT = Path(__file__).resolve().parents[1]
WORLD = ROOT / "architectuur" / "world.bp"


class NativeWallpaperArtDirectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        model = analyseer(
            parseer_bestand(WORLD),
            constraints=WORLD_MODEL_CONSTRAINTS,
        )
        cls.wallpapers = {
            wallpaper.id: wallpaper
            for wallpaper in resolveer_wallpapers(model.objecten)
        }

    def test_lichtwerking_staat_achter_de_functionele_informatie(self) -> None:
        for wallpaper in self.wallpapers.values():
            with self.subTest(wallpaper=wallpaper.id):
                self.assertIn("lichtlaag", wallpaper.lagen[0].id)
                music_index = next(
                    index
                    for index, layer in enumerate(wallpaper.lagen)
                    if "muzieklaag" in layer.id
                )
                self.assertGreater(music_index, 0)
                self.assertEqual(
                    "emberforge-circle-of-fifths",
                    wallpaper.lagen[music_index].plaatsingen[0].asset.id,
                )

    def test_koel_hoofdlicht_en_twee_warme_accenten_zijn_expliciet(self) -> None:
        for wallpaper in self.wallpapers.values():
            with self.subTest(wallpaper=wallpaper.id):
                light_placements = wallpaper.lagen[0].plaatsingen
                self.assertEqual(4, len(light_placements))
                self.assertEqual(
                    ("interaction", "interaction", "accent", "accent"),
                    tuple(item.color_role for item in light_placements),
                )
                self.assertTrue(
                    all(item.asset.id == "emberforge-light-disc" for item in light_placements)
                )
                self.assertTrue(
                    all(item.effect == "radial-glow" for item in light_placements)
                )
                warm = [item for item in light_placements if item.color_role == "accent"]
                self.assertEqual(2, len(warm))
                self.assertTrue(all(item.dekking <= 0.14 for item in warm))

    def test_beide_formaten_behouden_eigen_lichtgeometrie(self) -> None:
        ultrawide = self.wallpapers["emberforge-ultrawide-wallpaper"].lagen[0]
        desktop = self.wallpapers["emberforge-desktop-wallpaper"].lagen[0]

        self.assertNotEqual(
            tuple((item.x, item.y, item.breedte, item.hoogte) for item in ultrawide.plaatsingen),
            tuple((item.x, item.y, item.breedte, item.hoogte) for item in desktop.plaatsingen),
        )


if __name__ == "__main__":
    unittest.main()

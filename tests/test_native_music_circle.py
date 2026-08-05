from __future__ import annotations

import unittest
from pathlib import Path

from compiler.music_circle import (
    EXPECTED_MAJOR,
    EXPECTED_MINOR,
    EXPECTED_SIGNATURES,
    resolveer_muziekcirkels,
)
from compiler.parser import parseer, parseer_bestand
from compiler.product_constraints import WORLD_MODEL_CONSTRAINTS
from compiler.semantic import analyseer
from compiler.wallpaper_products import resolveer_wallpapers


ROOT = Path(__file__).resolve().parents[1]
WORLD = ROOT / "architectuur" / "world.bp"

BRON = '''
muziekcirkel fifths {
    naam: "Circle of Fifths"
    doel: "Functionele muziekreferentie."
    majeur: ["C", "G", "D", "A", "E", "B", "F#/Gb", "Db", "Ab", "Eb", "Bb", "F"]
    mineur: ["Am", "Em", "Bm", "F#m", "C#m", "G#m", "D#m/Ebm", "Bbm", "Fm", "Cm", "Gm", "Dm"]
    voortekens: ["0", "1#", "2#", "3#", "4#", "5#", "6#/6b", "5b", "4b", "3b", "2b", "1b"]
}
'''


class NativeMusicCircleTests(unittest.TestCase):
    def test_resolveert_exacte_muziekinformatie_en_vectorgeometrie(self) -> None:
        model = analyseer(parseer(BRON), constraints=WORLD_MODEL_CONSTRAINTS)
        circle = resolveer_muziekcirkels(model.objecten)[0]

        self.assertEqual(EXPECTED_MAJOR, circle.majeur)
        self.assertEqual(EXPECTED_MINOR, circle.mineur)
        self.assertEqual(EXPECTED_SIGNATURES, circle.voortekens)
        self.assertEqual("illustratie", circle.asset.rol)
        self.assertEqual((0.0, 0.0, 1000.0, 1000.0), circle.asset.viewbox)
        self.assertGreater(len(circle.asset.paden), 100)
        self.assertFalse(any("<" in path or ">" in path for path in circle.asset.paden))

    def test_weigert_afwijkende_volgorde_of_onbekende_velden(self) -> None:
        source = BRON.replace('"C", "G"', '"G", "C"').replace(
            '    voortekens:', '    renderer: "mag-niet"\n    voortekens:'
        )
        with self.assertRaises(ValueError) as caught:
            analyseer(parseer(source), constraints=WORLD_MODEL_CONSTRAINTS)
        message = str(caught.exception)
        self.assertIn("BP4401", message)
        self.assertIn("BP4402", message)

    def test_world_plaatst_dezelfde_functionele_cirkel_op_beide_formaten(self) -> None:
        model = analyseer(parseer_bestand(WORLD), constraints=WORLD_MODEL_CONSTRAINTS)
        circles = resolveer_muziekcirkels(model.objecten)
        wallpapers = {item.id: item for item in resolveer_wallpapers(model.objecten)}

        self.assertEqual(("emberforge-circle-of-fifths",), tuple(item.id for item in circles))
        for wallpaper_id in ("emberforge-ultrawide-wallpaper", "emberforge-desktop-wallpaper"):
            placements = [
                placement
                for layer in wallpapers[wallpaper_id].lagen
                for placement in layer.plaatsingen
                if placement.asset.id == "emberforge-circle-of-fifths"
            ]
            self.assertEqual(1, len(placements))
            self.assertEqual("contain", placements[0].fit)
            self.assertEqual(1.0, placements[0].dekking)


if __name__ == "__main__":
    unittest.main()

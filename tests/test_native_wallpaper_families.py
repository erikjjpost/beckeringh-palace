from __future__ import annotations

import json
import struct
import unittest
from pathlib import Path

from compiler.parser import parseer, parseer_bestand
from compiler.product_backends import standaard_backend_registry
from compiler.product_compiler import compileer_producten
from compiler.product_constraints import WORLD_MODEL_CONSTRAINTS
from compiler.semantic import SemantischeFout, analyseer
from compiler.wallpaper_families import resolveer_wallpaperfamilies


ROOT = Path(__file__).resolve().parents[1]
WORLD = ROOT / "architectuur" / "world.bp"


BRON = '''
kleur ink {
    naam: "Ink"
    doel: "Donkere canvaswaarde."
    waarde: "#0F1724"
}
kleur bone {
    naam: "Bone"
    doel: "Lichte voorgrond."
    waarde: "#E6EDF5"
}
palet forge-palette {
    naam: "Forge palette"
    doel: "Minimaal testpalet."
    background: "ink"
    foreground: "bone"
}
typografie forge-type {
    naam: "Forge type"
    doel: "Lokale testtypografie."
    heading: ["Aptos Display", "sans-serif"]
    body: ["Aptos", "sans-serif"]
    mono: ["JetBrains Mono", "monospace"]
    levering: "local-only"
}
materiaal forge-material {
    naam: "Forge material"
    doel: "Semantisch wallpapermateriaal."
    canvas: "ink"
    foreground: "bone"
}
thema forge {
    naam: "Forge"
    doel: "Wallpaper familiethema."
    palet: "forge-palette"
    typografie: "forge-type"
    materiaal: "forge-material"
}
wereld palace {
    naam: "Palace"
    doel: "Wallpaper familiewereld."
    thema: "forge"
}
merk emberforge {
    naam: "EmberForge"
    doel: "Wallpaper familiemerk."
    tagline: "Sovereign Infrastructure."
    belofte: "Sovereignty over your own stack."
    principes: ["Own your data.", "Own your nodes.", "Own your forge."]
    producten: ["Wallpaper"]
    taal: "Nederlands"
    stem: "Technisch en rustig"
}
merk ander-merk {
    naam: "Ander merk"
    doel: "Bewijst de merkgrens."
    tagline: "Other."
    belofte: "Other promise."
    principes: ["Other one.", "Other two.", "Other three."]
    producten: ["Wallpaper"]
    taal: "Nederlands"
    stem: "Rustig"
}
asset forge-node {
    naam: "Forge Node"
    doel: "Herbruikbaar lijnornament."
    formaat: "svg"
    rol: "ornament"
    viewbox: "0 0 10 10"
    paden: ["M0 0 H10 V10 H0 Z"]
    vulling: "none"
    lijn: "currentColor"
    lijndikte: "1"
    lijneinde: "round"
    lijnverbinding: "round"
    toegankelijkheid: "decoratief"
}
wallpaperfamilie forge-wallpapers {
    naam: "Forge Wallpapers"
    doel: "Ordent twee expliciete canvasformaten."
    merk: "emberforge"
    wallpapers: ["forge-ultrawide", "forge-desktop"]
}
wallpaper forge-ultrawide {
    naam: "Forge Ultrawide"
    doel: "Expliciet breed testcanvas."
    wereld: "palace"
    merk: "emberforge"
    familie: "forge-wallpapers"
    variant: "ultrawide-64x32"
    formaat: "png"
    breedte: "64"
    hoogte: "32"
    canvas: "canvas"
    lagen: ["forge-ultrawide-layer"]
}
wallpaperlaag forge-ultrawide-layer {
    naam: "Ultrawide ornamentlaag"
    doel: "Eigen laag voor het brede canvas."
    wallpaper: "forge-ultrawide"
    rol: "ornament"
    plaatsingen: ["forge-ultrawide-node"]
}
assetplaatsing forge-ultrawide-node {
    naam: "Ultrawide node"
    doel: "Expliciete plaatsing voor het brede canvas."
    laag: "forge-ultrawide-layer"
    asset: "forge-node"
    x: "8"
    y: "8"
    breedte: "16"
    hoogte: "16"
    fit: "contain"
    dekking: "1"
    kleur: "foreground"
}
wallpaper forge-desktop {
    naam: "Forge Desktop"
    doel: "Expliciet standaard testcanvas."
    wereld: "palace"
    merk: "emberforge"
    familie: "forge-wallpapers"
    variant: "desktop-40x30"
    formaat: "png"
    breedte: "40"
    hoogte: "30"
    canvas: "canvas"
    lagen: ["forge-desktop-layer"]
}
wallpaperlaag forge-desktop-layer {
    naam: "Desktop ornamentlaag"
    doel: "Eigen laag voor het standaard canvas."
    wallpaper: "forge-desktop"
    rol: "ornament"
    plaatsingen: ["forge-desktop-node"]
}
assetplaatsing forge-desktop-node {
    naam: "Desktop node"
    doel: "Expliciete plaatsing voor het standaard canvas."
    laag: "forge-desktop-layer"
    asset: "forge-node"
    x: "12"
    y: "7"
    breedte: "16"
    hoogte: "16"
    fit: "contain"
    dekking: "1"
    kleur: "foreground"
}
product forge-ultrawide-manifest {
    naam: "Forge Ultrawide Manifest"
    doel: "Publiceert de brede familievariant."
    backend: "wallpaper-manifest"
    mode: "static"
    inhoud: "wallpaper"
    wereld: "palace"
    wallpaper: "forge-ultrawide"
    pad: "output/products/forge-ultrawide.wallpaper.json"
}
product forge-ultrawide-png {
    naam: "Forge Ultrawide PNG"
    doel: "Rendert de brede familievariant."
    backend: "wallpaper-png"
    mode: "static"
    inhoud: "wallpaper"
    wereld: "palace"
    wallpaper: "forge-ultrawide"
    pad: "output/products/forge-ultrawide.png"
}
product forge-desktop-manifest {
    naam: "Forge Desktop Manifest"
    doel: "Publiceert de standaard familievariant."
    backend: "wallpaper-manifest"
    mode: "static"
    inhoud: "wallpaper"
    wereld: "palace"
    wallpaper: "forge-desktop"
    pad: "output/products/forge-desktop.wallpaper.json"
}
product forge-desktop-png {
    naam: "Forge Desktop PNG"
    doel: "Rendert de standaard familievariant."
    backend: "wallpaper-png"
    mode: "static"
    inhoud: "wallpaper"
    wereld: "palace"
    wallpaper: "forge-desktop"
    pad: "output/products/forge-desktop.png"
}
'''


def _png_metadata(payload: bytes) -> dict[str, str]:
    metadata = {}
    offset = 8
    while offset < len(payload):
        length = struct.unpack(">I", payload[offset:offset + 4])[0]
        name = payload[offset + 4:offset + 8]
        data = payload[offset + 8:offset + 8 + length]
        if name == b"tEXt":
            key, value = data.split(b"\x00", 1)
            metadata[key.decode("latin-1")] = value.decode("latin-1")
        offset += length + 12
    return metadata


class NativeWallpaperFamilyTests(unittest.TestCase):
    def _diagnostic_codes(self, bron: str) -> set[str]:
        with self.assertRaises(SemantischeFout) as context:
            analyseer(parseer(bron), constraints=WORLD_MODEL_CONSTRAINTS)
        return {
            diagnostic.code
            for diagnostic in context.exception.diagnostics
        }

    def test_resolveert_geordende_merkgebonden_formaten(self) -> None:
        model = analyseer(parseer(BRON), constraints=WORLD_MODEL_CONSTRAINTS)

        familie = resolveer_wallpaperfamilies(model.objecten)[0]

        self.assertEqual("forge-wallpapers", familie.id)
        self.assertEqual("emberforge", familie.merk)
        self.assertEqual(
            ("forge-ultrawide", "forge-desktop"),
            tuple(wallpaper.id for wallpaper in familie.wallpapers),
        )
        self.assertEqual(
            ("ultrawide-64x32", "desktop-40x30"),
            tuple(wallpaper.variant for wallpaper in familie.wallpapers),
        )
        self.assertEqual(
            ((64, 32), (40, 30)),
            tuple(
                (wallpaper.breedte, wallpaper.hoogte)
                for wallpaper in familie.wallpapers
            ),
        )
        self.assertEqual(
            ("forge-ultrawide-node", "forge-desktop-node"),
            tuple(
                wallpaper.lagen[0].plaatsingen[0].id
                for wallpaper in familie.wallpapers
            ),
        )

    def test_hergebruikt_backend_en_asset_met_expliciete_geometrie(self) -> None:
        model = analyseer(parseer(BRON), constraints=WORLD_MODEL_CONSTRAINTS)
        products = {
            product.definitie.id: product
            for product in compileer_producten(
                model.objecten,
                standaard_backend_registry(),
            )
        }

        for variant, size in (
            ("ultrawide", (64, 32)),
            ("desktop", (40, 30)),
        ):
            manifest = json.loads(
                products[f"forge-{variant}-manifest"].inhoud
            )
            png = products[f"forge-{variant}-png"].inhoud
            metadata = _png_metadata(png)

            self.assertEqual(3, manifest["schema_version"])
            self.assertEqual(
                "forge-wallpapers",
                manifest["wallpaper"]["familie"]["id"],
            )
            self.assertEqual(
                size,
                struct.unpack(">II", png[16:24]),
            )
            self.assertEqual(
                "forge-wallpapers",
                metadata["bp-wallpaper-family"],
            )
            self.assertEqual(
                manifest["wallpaper"]["familie"]["variant"],
                metadata["bp-wallpaper-variant"],
            )
            self.assertEqual(
                "forge-node",
                manifest["wallpaper"]["lagen"][0]["plaatsingen"][0]["asset"],
            )

    def test_world_publiceert_ultrawide_en_1900_bij_1200(self) -> None:
        model = analyseer(
            parseer_bestand(WORLD),
            constraints=WORLD_MODEL_CONSTRAINTS,
        )
        families = {
            familie.id: familie
            for familie in resolveer_wallpaperfamilies(model.objecten)
        }
        products = {
            product.definitie.id: product
            for product in compileer_producten(
                model.objecten,
                standaard_backend_registry(),
            )
        }

        familie = families["emberforge-wallpapers"]
        self.assertEqual(
            ((3840, 1080), (1900, 1200)),
            tuple(
                (wallpaper.breedte, wallpaper.hoogte)
                for wallpaper in familie.wallpapers
            ),
        )
        self.assertEqual(
            {
                "emberforge-ultrawide-wallpaper-manifest",
                "emberforge-ultrawide-wallpaper-png",
                "emberforge-desktop-wallpaper-manifest",
                "emberforge-desktop-wallpaper-png",
            },
            {
                product_id
                for product_id in products
                if "wallpaper" in product_id
            },
        )

    def test_weigert_onbekende_velden_en_merk(self) -> None:
        self.assertIn(
            "BP4390",
            self._diagnostic_codes(
                BRON.replace(
                    '    merk: "emberforge"\n'
                    '    wallpapers: ["forge-ultrawide", "forge-desktop"]',
                    '    merk: "emberforge"\n'
                    '    schaal: "auto"\n'
                    '    wallpapers: ["forge-ultrawide", "forge-desktop"]',
                )
            ),
        )
        self.assertIn(
            "BP4391",
            self._diagnostic_codes(
                BRON.replace(
                    '    merk: "emberforge"\n'
                    '    wallpapers: ["forge-ultrawide", "forge-desktop"]',
                    '    merk: "missing"\n'
                    '    wallpapers: ["forge-ultrawide", "forge-desktop"]',
                )
            ),
        )

    def test_weigert_onvolledige_lijst_en_onbekend_lid(self) -> None:
        self.assertIn(
            "BP4392",
            self._diagnostic_codes(
                BRON.replace(
                    'wallpapers: ["forge-ultrawide", "forge-desktop"]',
                    'wallpapers: ["forge-ultrawide"]',
                )
            ),
        )
        self.assertIn(
            "BP4393",
            self._diagnostic_codes(
                BRON.replace(
                    'wallpapers: ["forge-ultrawide", "forge-desktop"]',
                    'wallpapers: ["forge-ultrawide", "missing"]',
                )
            ),
        )

    def test_weigert_niet_wederkerige_leden_en_dubbele_varianten(self) -> None:
        self.assertIn(
            "BP4394",
            self._diagnostic_codes(
                BRON.replace(
                    'familie: "forge-wallpapers"\n'
                    '    variant: "desktop-40x30"',
                    'familie: "missing"\n'
                    '    variant: "desktop-40x30"',
                )
            ),
        )
        self.assertIn(
            "BP4395",
            self._diagnostic_codes(
                BRON.replace(
                    'variant: "desktop-40x30"',
                    'variant: "ultrawide-64x32"',
                )
            ),
        )

    def test_weigert_merkverschil_en_dubbel_canvasformaat(self) -> None:
        self.assertIn(
            "BP4396",
            self._diagnostic_codes(
                BRON.replace(
                    'naam: "Forge Desktop"\n'
                    '    doel: "Expliciet standaard testcanvas."\n'
                    '    wereld: "palace"\n'
                    '    merk: "emberforge"',
                    'naam: "Forge Desktop"\n'
                    '    doel: "Expliciet standaard testcanvas."\n'
                    '    wereld: "palace"\n'
                    '    merk: "ander-merk"',
                )
            ),
        )
        self.assertIn(
            "BP4397",
            self._diagnostic_codes(
                BRON.replace(
                    '    breedte: "40"\n'
                    '    hoogte: "30"\n'
                    '    canvas: "canvas"\n'
                    '    lagen: ["forge-desktop-layer"]',
                    '    breedte: "64"\n'
                    '    hoogte: "32"\n'
                    '    canvas: "canvas"\n'
                    '    lagen: ["forge-desktop-layer"]',
                )
            ),
        )

    def test_weigert_eenzijdig_familielidmaatschap(self) -> None:
        self.assertIn(
            "BP4398",
            self._diagnostic_codes(
                BRON.replace(
                    '    familie: "forge-wallpapers"\n'
                    '    variant: "desktop-40x30"\n',
                    '    familie: "forge-wallpapers"\n',
                )
            ),
        )


if __name__ == "__main__":
    unittest.main()

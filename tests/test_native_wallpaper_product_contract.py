from __future__ import annotations

import json
import unittest
from pathlib import Path

from compiler.parser import parseer, parseer_bestand
from compiler.product_backends import standaard_backend_registry
from compiler.product_compiler import compileer_producten
from compiler.product_constraints import WORLD_MODEL_CONSTRAINTS
from compiler.semantic import SemantischeFout, analyseer
from compiler.wallpaper_products import resolveer_wallpapers


ROOT = Path(__file__).resolve().parents[1]
WORLD = ROOT / "architectuur" / "world.bp"


BRON = '''
kleur ink {
    naam: "Ink"
    doel: "Donkere canvaswaarde."
    waarde: "#0F1724"
}
palet forge-palette {
    naam: "Forge palette"
    doel: "Minimaal testpalet."
    background: "ink"
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
    doel: "Semantisch canvasmateriaal."
    canvas: "ink"
    outline: "ink"
    foreground: "ink"
}
thema forge {
    naam: "Forge"
    doel: "Wallpaper testthema."
    palet: "forge-palette"
    typografie: "forge-type"
    materiaal: "forge-material"
}
wereld palace {
    naam: "Palace"
    doel: "Wallpaper testwereld."
    thema: "forge"
}
merk emberforge {
    naam: "EmberForge"
    doel: "Wallpaper testmerk."
    tagline: "Sovereign Infrastructure."
    belofte: "Sovereignty over your own stack."
    principes: ["Own your data.", "Own your nodes.", "Own your forge."]
    producten: ["Wallpaper"]
    taal: "Nederlands"
    stem: "Technisch en rustig"
}
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
    doel: "Informatief merkteken."
    formaat: "svg"
    rol: "logo"
    viewbox: "0 0 64 64"
    paden: ["M8 8 L56 8 L56 56 L8 56 Z"]
    vulling: "none"
    lijn: "currentColor"
    lijndikte: "2"
    lijneinde: "round"
    lijnverbinding: "round"
    toegankelijkheid: "informatief"
    label: "Forge"
}
wallpaper forge-ultrawide {
    naam: "Forge Ultrawide"
    doel: "Geordende wallpaperintentie."
    wereld: "palace"
    merk: "emberforge"
    formaat: "png"
    breedte: "3840"
    hoogte: "1080"
    canvas: "canvas"
    lagen: ["forge-ornament-layer", "forge-brand-layer"]
}
wallpaperlaag forge-ornament-layer {
    naam: "Ornamentlaag"
    doel: "Rustige technische achtergrondornamentiek."
    wallpaper: "forge-ultrawide"
    rol: "ornament"
    plaatsingen: ["forge-node-placement"]
}
wallpaperlaag forge-brand-layer {
    naam: "Merklaag"
    doel: "Expliciete merkplaatsing."
    wallpaper: "forge-ultrawide"
    rol: "merk"
    plaatsingen: ["forge-mark-placement"]
}
assetplaatsing forge-node-placement {
    naam: "Forge node links"
    doel: "Plaatst het lijnmotief binnen de veilige canvasgrens."
    laag: "forge-ornament-layer"
    asset: "forge-node"
    x: "120"
    y: "120"
    breedte: "840"
    hoogte: "840"
    fit: "contain"
    dekking: "0.14"
    kleur: "outline"
}
assetplaatsing forge-mark-placement {
    naam: "Forge merkteken"
    doel: "Plaatst het merkteken centraal."
    laag: "forge-brand-layer"
    asset: "forge-mark"
    x: "1680"
    y: "300"
    breedte: "480"
    hoogte: "480"
    fit: "contain"
    dekking: "1"
    kleur: "foreground"
}
product forge-ultrawide-manifest {
    naam: "Forge Ultrawide Wallpaper Manifest"
    doel: "Publiceert het opgeloste wallpapercontract."
    backend: "wallpaper-manifest"
    mode: "static"
    inhoud: "wallpaper"
    wereld: "palace"
    wallpaper: "forge-ultrawide"
    pad: "output/products/forge-ultrawide.wallpaper.json"
}
'''


class NativeWallpaperProductContractTests(unittest.TestCase):
    def _diagnostic_codes(self, bron: str) -> set[str]:
        with self.assertRaises(SemantischeFout) as context:
            analyseer(parseer(bron), constraints=WORLD_MODEL_CONSTRAINTS)
        return {
            diagnostic.code
            for diagnostic in context.exception.diagnostics
        }

    def test_resolveert_canvas_formaat_lagen_en_assetplaatsingen(self) -> None:
        model = analyseer(parseer(BRON), constraints=WORLD_MODEL_CONSTRAINTS)

        wallpaper = resolveer_wallpapers(model.objecten)[0]

        self.assertEqual("forge-ultrawide", wallpaper.id)
        self.assertEqual((3840, 1080), (wallpaper.breedte, wallpaper.hoogte))
        self.assertEqual("png", wallpaper.formaat)
        self.assertEqual("canvas", wallpaper.canvas_role)
        self.assertEqual("#0F1724", wallpaper.canvas.waarde)
        self.assertEqual(
            ("forge-ornament-layer", "forge-brand-layer"),
            tuple(laag.id for laag in wallpaper.lagen),
        )
        self.assertEqual(
            ("forge-node-placement",),
            tuple(item.id for item in wallpaper.lagen[0].plaatsingen),
        )
        self.assertEqual(
            (
                "forge-node",
                120,
                120,
                840,
                840,
                "contain",
                0.14,
                "outline",
                "#0F1724",
            ),
            (
                wallpaper.lagen[0].plaatsingen[0].asset.id,
                wallpaper.lagen[0].plaatsingen[0].x,
                wallpaper.lagen[0].plaatsingen[0].y,
                wallpaper.lagen[0].plaatsingen[0].breedte,
                wallpaper.lagen[0].plaatsingen[0].hoogte,
                wallpaper.lagen[0].plaatsingen[0].fit,
                wallpaper.lagen[0].plaatsingen[0].dekking,
                wallpaper.lagen[0].plaatsingen[0].color_role,
                wallpaper.lagen[0].plaatsingen[0].color.waarde,
            ),
        )

    def test_compileert_stabiel_machineleesbaar_contractproduct(self) -> None:
        model = analyseer(parseer(BRON), constraints=WORLD_MODEL_CONSTRAINTS)

        products = {
            product.definitie.id: product
            for product in compileer_producten(
                model.objecten,
                standaard_backend_registry(),
            )
        }
        product = products["forge-ultrawide-manifest"]
        manifest = json.loads(product.inhoud)

        self.assertEqual("wallpaper", product.definitie.inhoud)
        self.assertEqual(
            "forge-ultrawide",
            product.definitie.opgeloste_wallpaper.id,
        )
        self.assertEqual(3, manifest["schema_version"])
        self.assertEqual(
            product.definitie.snapshot_ref,
            manifest["product"]["snapshot"],
        )
        self.assertEqual(
            {
                "breedte": 3840,
                "hoogte": 1080,
                "eenheid": "px",
                "materiaalrol": "canvas",
                "kleur": "#0F1724",
            },
            manifest["wallpaper"]["canvas"],
        )
        self.assertEqual(
            ["forge-ornament-layer", "forge-brand-layer"],
            [laag["id"] for laag in manifest["wallpaper"]["lagen"]],
        )
        self.assertEqual(
            "forge-node",
            manifest["wallpaper"]["lagen"][0]["plaatsingen"][0]["asset"],
        )
        self.assertNotIn("familie", manifest["wallpaper"])
        self.assertEqual(
            {
                "materiaalrol": "outline",
                "kleur": "#0F1724",
            },
            {
                key: manifest["wallpaper"]["lagen"][0]["plaatsingen"][0][key]
                for key in ("materiaalrol", "kleur")
            },
        )
        self.assertNotIn("<script", product.inhoud)
        self.assertNotIn("://", product.inhoud)

    def test_contract_is_onafhankelijk_van_bronvolgorde(self) -> None:
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

    def test_weigert_onbekende_referenties_en_velden(self) -> None:
        self.assertIn(
            "BP4351",
            self._diagnostic_codes(
                BRON.replace(
                    '    canvas: "canvas"',
                    '    canvas: "canvas"\n    bron: "wallpaper.png"',
                )
            ),
        )
        self.assertIn(
            "BP4352",
            self._diagnostic_codes(
                BRON.replace('    wereld: "palace"', '    wereld: "missing"', 1)
            ),
        )
        self.assertIn(
            "BP4353",
            self._diagnostic_codes(
                BRON.replace(
                    '    merk: "emberforge"',
                    '    merk: "missing"',
                    1,
                )
            ),
        )
        self.assertIn(
            "BP4358",
            self._diagnostic_codes(
                BRON.replace(
                    'lagen: ["forge-ornament-layer", "forge-brand-layer"]',
                    'lagen: ["forge-ornament-layer", "missing"]',
                )
            ),
        )

    def test_weigert_impliciet_formaat_canvas_en_lagenrelaties(self) -> None:
        self.assertIn(
            "BP4354",
            self._diagnostic_codes(
                BRON.replace('    formaat: "png"', '    formaat: "jpeg"')
            ),
        )
        self.assertIn(
            "BP4355",
            self._diagnostic_codes(
                BRON.replace('    breedte: "3840"', '    breedte: "03840"')
            ),
        )
        self.assertIn(
            "BP4356",
            self._diagnostic_codes(
                BRON.replace('    canvas: "canvas"', '    canvas: "surface"')
            ),
        )
        self.assertIn(
            "BP4359",
            self._diagnostic_codes(
                BRON.replace(
                    '    wallpaper: "forge-ultrawide"',
                    '    wallpaper: "missing"',
                    1,
                )
            ),
        )
        self.assertIn(
            "BP4365",
            self._diagnostic_codes(
                BRON.replace(
                    '    laag: "forge-ornament-layer"',
                    '    laag: "forge-brand-layer"',
                    1,
                )
            ),
        )

    def test_weigert_ongeldige_assetplaatsing(self) -> None:
        self.assertIn(
            "BP4368",
            self._diagnostic_codes(
                BRON.replace('    asset: "forge-node"', '    asset: "missing"')
            ),
        )
        self.assertIn(
            "BP4369",
            self._diagnostic_codes(
                BRON.replace('    x: "120"', '    x: "-1"')
            ),
        )
        self.assertIn(
            "BP4370",
            self._diagnostic_codes(
                BRON.replace('    breedte: "840"', '    breedte: "3800"')
            ),
        )
        self.assertIn(
            "BP4371",
            self._diagnostic_codes(
                BRON.replace('    fit: "contain"', '    fit: "auto"', 1)
            ),
        )
        self.assertIn(
            "BP4372",
            self._diagnostic_codes(
                BRON.replace('    dekking: "0.14"', '    dekking: "1.1"')
            ),
        )
        self.assertIn(
            "BP4373",
            self._diagnostic_codes(
                BRON.replace('    asset: "forge-node"', '    asset: "forge-mark"')
            ),
        )
        self.assertIn(
            "BP4374",
            self._diagnostic_codes(
                BRON.replace('    kleur: "outline"', '    kleur: "missing"')
            ),
        )

    def test_weigert_impliciet_of_inconsistent_productcontract(self) -> None:
        self.assertIn(
            "BP4380",
            self._diagnostic_codes(
                BRON.replace(
                    '    inhoud: "wallpaper"',
                    '    inhoud: "composition"',
                )
            ),
        )
        self.assertIn(
            "BP4380",
            self._diagnostic_codes(
                BRON.replace(
                    '    inhoud: "wallpaper"\n',
                    "",
                ).replace(
                    '    wallpaper: "forge-ultrawide"\n'
                    '    pad: "output/products/forge-ultrawide.wallpaper.json"',
                    '    pad: "output/products/forge-ultrawide.wallpaper.json"',
                    1,
                )
            ),
        )
        self.assertIn(
            "BP4381",
            self._diagnostic_codes(
                BRON.replace(
                    '    wallpaper: "forge-ultrawide"\n'
                    '    pad: "output/products/forge-ultrawide.wallpaper.json"',
                    '    wallpaper: "missing"\n'
                    '    pad: "output/products/forge-ultrawide.wallpaper.json"',
                    1,
                )
            ),
        )
        self.assertIn(
            "BP4382",
            self._diagnostic_codes(
                BRON.replace(
                    '    backend: "wallpaper-manifest"',
                    '    backend: "html"',
                )
            ),
        )
        self.assertIn(
            "BP4383",
            self._diagnostic_codes(
                BRON.replace('    mode: "static"', '    mode: "interactive"')
            ),
        )
        self.assertIn(
            "BP4385",
            self._diagnostic_codes(
                BRON.replace(
                    '    wallpaper: "forge-ultrawide"\n'
                    '    pad: "output/products/forge-ultrawide.wallpaper.json"',
                    '    wallpaper: "forge-ultrawide"\n'
                    '    layout: "missing"\n'
                    '    pad: "output/products/forge-ultrawide.wallpaper.json"',
                    1,
                )
            ),
        )
        self.assertIn(
            "BP4386",
            self._diagnostic_codes(
                BRON.replace(
                    'pad: "output/products/forge-ultrawide.wallpaper.json"',
                    'pad: "output/products/forge-ultrawide.json"',
                )
            ),
        )

    def test_world_publiceert_een_native_ultrawide_contract(self) -> None:
        model = analyseer(
            parseer_bestand(WORLD),
            constraints=WORLD_MODEL_CONSTRAINTS,
        )
        wallpapers = {
            wallpaper.id: wallpaper
            for wallpaper in resolveer_wallpapers(model.objecten)
        }
        products = {
            product.definitie.id: product
            for product in compileer_producten(
                model.objecten,
                standaard_backend_registry(),
            )
        }

        wallpaper = wallpapers["emberforge-ultrawide-wallpaper"]
        product = products["emberforge-ultrawide-wallpaper-manifest"]
        manifest = json.loads(product.inhoud)

        self.assertEqual((3840, 1080), (wallpaper.breedte, wallpaper.hoogte))
        self.assertEqual("#0F1724", wallpaper.canvas.waarde)
        self.assertEqual(
            ("ornament", "illustratie", "merk"),
            tuple(laag.rol for laag in wallpaper.lagen),
        )
        self.assertEqual(
            (
                "emberforge-vector-node-left",
                "emberforge-vector-node-right",
                "emberforge-wallpaper-circle-of-fifths",
                "emberforge-wallpaper-merkteken",
            ),
            tuple(
                plaatsing.id
                for laag in wallpaper.lagen
                for plaatsing in laag.plaatsingen
            ),
        )
        self.assertEqual(
            "emberforge-ultrawide-wallpaper",
            manifest["wallpaper"]["id"],
        )
        self.assertEqual("png", manifest["wallpaper"]["formaat"])


if __name__ == "__main__":
    unittest.main()

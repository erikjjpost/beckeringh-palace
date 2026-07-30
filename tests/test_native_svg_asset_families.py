from __future__ import annotations

import json
import unittest
from pathlib import Path

from compiler.parser import parseer, parseer_bestand
from compiler.product_backends import standaard_backend_registry
from compiler.product_compiler import compileer_producten
from compiler.product_constraints import WORLD_MODEL_CONSTRAINTS
from compiler.semantic import SemantischeFout, analyseer
from compiler.svg_asset_families import resolveer_svg_assetfamilies


ROOT = Path(__file__).resolve().parents[1]
WORLD = ROOT / "architectuur" / "world.bp"
DESIGN_INPUT = (
    ROOT / "project" / "design-inputs" / "emberforge-design-system.json"
)


BRON = '''
merk forge {
    naam: "Forge"
    doel: "Merk voor een native assetfamilie."
    tagline: "Native assets."
    belofte: "Eén gecontroleerde merktaal."
    principes: ["Expliciet.", "Reproduceerbaar.", "Samenhangend."]
    producten: ["Merkproducten"]
    taal: "Nederlands"
    stem: "Technisch en rustig"
}
assetfamilie forge-merk {
    naam: "Forge merkfamilie"
    doel: "Ordent merkteken en woordmerk."
    type: "merk"
    merk: "forge"
    assets: ["forge-mark", "forge-wordmark"]
}
asset forge-mark {
    naam: "Forge merkteken"
    doel: "Compact merkteken."
    formaat: "svg"
    rol: "logo"
    familie: "forge-merk"
    variant: "merkteken"
    viewbox: "0 0 64 64"
    paden: ["M32 4 L56 20 L48 52 L16 52 L8 20 Z"]
    vulling: "none"
    lijn: "currentColor"
    lijndikte: "2"
    lijneinde: "round"
    lijnverbinding: "round"
    toegankelijkheid: "informatief"
    label: "Forge"
}
asset forge-wordmark {
    naam: "Forge woordmerk"
    doel: "Horizontaal woordmerk."
    formaat: "svg"
    rol: "logo"
    familie: "forge-merk"
    variant: "woordmerk"
    viewbox: "0 0 240 64"
    paden: ["M8 8 V56 M8 8 H40 M8 32 H34 M8 56 H40"]
    vulling: "none"
    lijn: "currentColor"
    lijndikte: "2"
    lijneinde: "round"
    lijnverbinding: "round"
    toegankelijkheid: "informatief"
    label: "Forge"
}
'''


class NativeSvgAssetFamilyTests(unittest.TestCase):
    def _diagnostic_codes(self, bron: str) -> set[str]:
        with self.assertRaises(SemantischeFout) as context:
            analyseer(parseer(bron), constraints=WORLD_MODEL_CONSTRAINTS)
        return {
            diagnostic.code
            for diagnostic in context.exception.diagnostics
        }

    def test_resolveert_geordende_getypeerde_merkfamilie(self) -> None:
        model = analyseer(parseer(BRON), constraints=WORLD_MODEL_CONSTRAINTS)

        familie = resolveer_svg_assetfamilies(model.objecten)[0]

        self.assertEqual("forge-merk", familie.id)
        self.assertEqual("merk", familie.familietype)
        self.assertEqual("forge", familie.merk)
        self.assertEqual(
            ("forge-mark", "forge-wordmark"),
            tuple(asset.id for asset in familie.assets),
        )
        self.assertEqual(
            ("merkteken", "woordmerk"),
            tuple(asset.variant for asset in familie.assets),
        )

    def test_weigert_onbekende_velden_type_merk_en_assets(self) -> None:
        self.assertIn(
            "BP4331",
            self._diagnostic_codes(
                BRON.replace(
                    '    type: "merk"',
                    '    type: "merk"\n    bron: "logo.svg"',
                )
            ),
        )
        self.assertIn(
            "BP4332",
            self._diagnostic_codes(
                BRON.replace('type: "merk"', 'type: "collectie"')
            ),
        )
        self.assertIn(
            "BP4333",
            self._diagnostic_codes(
                BRON.replace('merk: "forge"', 'merk: "missing"')
            ),
        )
        self.assertIn(
            "BP4334",
            self._diagnostic_codes(
                BRON.replace(
                    'assets: ["forge-mark", "forge-wordmark"]',
                    'assets: ["forge-mark", "forge-mark"]',
                )
            ),
        )
        self.assertIn(
            "BP4335",
            self._diagnostic_codes(
                BRON.replace(
                    'assets: ["forge-mark", "forge-wordmark"]',
                    'assets: ["forge-mark", "missing"]',
                )
            ),
        )

    def test_weigert_impliciete_of_niet_wederkerige_leden(self) -> None:
        self.assertIn(
            "BP4336",
            self._diagnostic_codes(
                BRON.replace('    variant: "merkteken"\n', "")
            ),
        )
        self.assertIn(
            "BP4336",
            self._diagnostic_codes(
                BRON.replace(
                    'familie: "forge-merk"',
                    'familie: "missing"',
                    1,
                )
            ),
        )
        self.assertIn(
            "BP4337",
            self._diagnostic_codes(
                BRON.replace('    familie: "forge-merk"\n', "", 1)
            ),
        )

    def test_weigert_dubbele_variant_verkeerde_rol_en_onvolledig_merk(self) -> None:
        self.assertIn(
            "BP4338",
            self._diagnostic_codes(
                BRON.replace(
                    'variant: "woordmerk"',
                    'variant: "merkteken"',
                )
            ),
        )
        self.assertIn(
            "BP4339",
            self._diagnostic_codes(
                BRON.replace('rol: "logo"', 'rol: "icoon"', 1)
            ),
        )
        self.assertIn(
            "BP4340",
            self._diagnostic_codes(
                BRON.replace(
                    'variant: "woordmerk"',
                    'variant: "lockup"',
                )
            ),
        )

    def test_world_model_publiceert_iconen_en_merkfamilie(self) -> None:
        model = analyseer(
            parseer_bestand(WORLD),
            constraints=WORLD_MODEL_CONSTRAINTS,
        )
        families = {
            familie.id: familie
            for familie in resolveer_svg_assetfamilies(model.objecten)
        }

        self.assertEqual(
            {"emberforge-iconen", "emberforge-merkassets"},
            set(families),
        )
        self.assertEqual(
            (
                "emberforge-icon-dashboard",
                "emberforge-icon-identity",
                "emberforge-icon-terminal",
                "emberforge-icon-assets",
            ),
            tuple(
                asset.id
                for asset in families["emberforge-iconen"].assets
            ),
        )
        self.assertEqual(
            ("emberforge-merkteken", "emberforge-woordmerk"),
            tuple(
                asset.id
                for asset in families["emberforge-merkassets"].assets
            ),
        )
        products = {
            product.definitie.id: product
            for product in compileer_producten(
                model.objecten,
                standaard_backend_registry(),
            )
        }
        merkteken = products["emberforge-merkteken-svg"].inhoud
        woordmerk = products["emberforge-woordmerk-svg"].inhoud
        self.assertIn(
            'data-bp-family="emberforge-merkassets"',
            merkteken,
        )
        self.assertIn('data-bp-variant="merkteken"', merkteken)
        self.assertIn('viewBox="0 0 96 96"', merkteken)
        self.assertIn(
            'data-bp-family="emberforge-merkassets"',
            woordmerk,
        )
        self.assertIn('data-bp-variant="woordmerk"', woordmerk)
        self.assertIn('viewBox="0 0 592 80"', woordmerk)

    def test_designbron_registreert_nieuwe_native_merkgeometrie(self) -> None:
        source = json.loads(DESIGN_INPUT.read_text(encoding="utf-8"))
        vector_assets = next(
            area
            for area in source["gebieden"]
            if area["id"] == "vector-assets"
        )

        self.assertEqual("geblokkeerd", vector_assets["status"])
        self.assertIn("M11.5d", vector_assets["bewijs"])
        self.assertIn("nieuw EmberForge merkteken", vector_assets["bewijs"])
        self.assertIn("placeholder", vector_assets["bewijs"])


if __name__ == "__main__":
    unittest.main()

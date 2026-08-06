"""Regressiecontracten voor de native Figma masterbeschrijving."""
from __future__ import annotations

import json
import unittest
from pathlib import Path

from compiler.figma_master import resolveer_figma_masters
from compiler.parser import parseer, parseer_bestand
from compiler.product_backends import standaard_backend_registry
from compiler.product_compiler import compileer_producten
from compiler.product_constraints import WORLD_MODEL_CONSTRAINTS
from compiler.semantic import SemantischeFout, analyseer


ROOT = Path(__file__).resolve().parents[1]
WORLD = ROOT / "architectuur" / "world.bp"


class NativeFigmaProductContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.model = analyseer(
            parseer_bestand(WORLD),
            constraints=WORLD_MODEL_CONSTRAINTS,
        )

    def test_master_selecteert_dezelfde_native_bouwstenen_expliciet(self) -> None:
        masters = resolveer_figma_masters(self.model.objecten)
        self.assertEqual(1, len(masters))
        master = masters[0]
        self.assertEqual("emberforge-figma-master", master.id)
        self.assertEqual("beckeringh-palace", master.wereld)
        self.assertEqual("forge", master.thema.thema_id)
        self.assertEqual(11, len(master.assets))
        self.assertEqual(7, len(master.componenten))
        self.assertEqual(20, len(master.varianten))
        self.assertEqual(7, len(master.composities))
        self.assertEqual(7, len(master.layouts))
        self.assertEqual(
            "emberforge-merkteken",
            master.assets[-2].id,
        )
        self.assertEqual(
            "beckeringh-palace-homepage-grid",
            master.layouts[-1].id,
        )

    def test_manifest_is_statisch_machineleesbaar_en_brongebonden(self) -> None:
        products = {
            product.definitie.id: product
            for product in compileer_producten(
                self.model.objecten,
                standaard_backend_registry(),
            )
        }
        product = products["emberforge-figma-master-manifest"]
        self.assertEqual("figma-manifest", product.definitie.backend)
        self.assertEqual("figma-master", product.definitie.inhoud)
        self.assertEqual("static", product.definitie.mode)
        self.assertTrue(product.definitie.snapshot_ref.startswith("sha256:"))
        payload = json.loads(product.inhoud)
        self.assertEqual(1, payload["schema_version"])
        self.assertEqual(
            product.definitie.snapshot_ref,
            payload["product"]["snapshot"],
        )
        self.assertEqual("forge", payload["theme"]["id"])
        self.assertEqual(
            "#0F1724",
            payload["theme"]["palet"]["rollen"]["background"],
        )
        self.assertEqual(11, len(payload["assets"]))
        self.assertEqual(7, len(payload["components"]))
        self.assertEqual(20, len(payload["variants"]))
        self.assertEqual(7, len(payload["compositions"]))
        self.assertEqual(7, len(payload["layouts"]))
        self.assertIn("appearances", payload)

    def test_manifest_is_deterministisch(self) -> None:
        registry = standaard_backend_registry()
        eerste = next(
            product.inhoud
            for product in compileer_producten(self.model.objecten, registry)
            if product.definitie.id == "emberforge-figma-master-manifest"
        )
        tweede = next(
            product.inhoud
            for product in compileer_producten(self.model.objecten, registry)
            if product.definitie.id == "emberforge-figma-master-manifest"
        )
        self.assertEqual(eerste, tweede)

    def test_weigert_impliciete_of_inconsistente_masterselectie(self) -> None:
        bron = """
wereld demo {
    naam: "Demo"
    doel: "Demo wereld"
}
figmamaster demo-master {
    naam: "Demo master"
    doel: "Ongeldige selectie"
    wereld: "demo"
    assets: ["mist"]
    componenten: ["mist"]
    varianten: ["mist"]
    composities: ["mist"]
    layouts: ["mist", "mist"]
}
"""
        with self.assertRaises(SemantischeFout) as fout:
            analyseer(parseer(bron), constraints=WORLD_MODEL_CONSTRAINTS)
        codes = {diagnostic.code for diagnostic in fout.exception.diagnostics}
        self.assertIn("BP4404", codes)
        self.assertIn("BP4405", codes)


if __name__ == "__main__":
    unittest.main()

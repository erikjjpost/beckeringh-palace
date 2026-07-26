from __future__ import annotations

import unittest

from compiler.world_model import (
    Domeinstatus,
    NATIVE_OBJECTSOORTEN,
    is_native_objectsoort,
    objectsoortdefinitie,
)


class WorldModelBoundaryTests(unittest.TestCase):
    def test_native_world_model_is_productgericht(self):
        self.assertEqual(
            {
                "asset",
                "border",
                "component",
                "compositie",
                "kleur",
                "layout",
                "materiaal",
                "merk",
                "motion",
                "palet",
                "product",
                "radius",
                "regio",
                "renderdoel",
                "shadow",
                "thema",
                "token",
                "typografie",
                "variant",
                "wereld",
            },
            set(NATIVE_OBJECTSOORTEN),
        )

    def test_architectuurconcepten_zijn_geen_native_bat(self):
        for soort in ("capability", "dienst", "agent"):
            with self.subTest(soort=soort):
                definitie = objectsoortdefinitie(soort)
                self.assertIsNotNone(definitie)
                self.assertEqual(Domeinstatus.MIGRATIE, definitie.status)
                self.assertFalse(is_native_objectsoort(soort))

    def test_archimate_is_extern(self):
        definitie = objectsoortdefinitie("archimate")
        self.assertIsNotNone(definitie)
        self.assertEqual(Domeinstatus.EXTERN, definitie.status)
        self.assertFalse(is_native_objectsoort("archimate"))

    def test_onbekende_objectsoort_heeft_geen_impliciete_semantiek(self):
        self.assertIsNone(objectsoortdefinitie("applicatiecomponent"))
        self.assertFalse(is_native_objectsoort("applicatiecomponent"))


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import unittest

from compiler.design_render_targets import resolveer_renderdoelen
from compiler.parser import parseer
from compiler.product_constraints import WORLD_MODEL_CONSTRAINTS
from compiler.render_target_renderer import (
    RenderTargetRendererRegistry,
    render_renderdoelen,
)
from compiler.semantic import SemantischeFout, analyseer


BRON = '''
renderdoel html-components {
    naam: "HTML component catalogue"
    doel: "Een minimale componentcatalogus genereren."
    formaat: "html"
    pad: "output/products/components.html"
}

renderdoel css-components {
    naam: "CSS components"
    doel: "Componenten als CSS-klassen genereren."
    formaat: "css"
    pad: "output/products/components.css"
}
'''


class NativeRenderTargetTests(unittest.TestCase):
    def test_resolveert_renderdoelen_deterministisch(self):
        model = analyseer(parseer(BRON), constraints=WORLD_MODEL_CONSTRAINTS)

        renderdoelen = resolveer_renderdoelen(model.objecten)

        self.assertEqual(
            ["css-components", "html-components"],
            [renderdoel.id for renderdoel in renderdoelen],
        )
        self.assertEqual("css", renderdoelen[0].formaat)
        self.assertEqual(
            "output/products/components.css",
            renderdoelen[0].pad,
        )

    def test_rendert_doelen_via_expliciete_id_binding(self):
        model = analyseer(parseer(BRON), constraints=WORLD_MODEL_CONSTRAINTS)
        registry = RenderTargetRendererRegistry(
            {
                "css-components": lambda _objecten: "components",
                "html-components": lambda _objecten: "catalogue",
            }
        )

        artifacts = render_renderdoelen(model.objecten, registry)

        self.assertEqual(
            [
                ("css-components", "output/products/components.css", "components"),
                ("html-components", "output/products/components.html", "catalogue"),
            ],
            [
                (artifact.definitie.id, artifact.definitie.pad, artifact.inhoud)
                for artifact in artifacts
            ],
        )

    def test_leidt_renderer_niet_af_uit_formaat(self):
        model = analyseer(parseer(BRON), constraints=WORLD_MODEL_CONSTRAINTS)
        registry = RenderTargetRendererRegistry(
            {
                "css-components": lambda _objecten: "components",
            }
        )

        with self.assertRaisesRegex(
            KeyError,
            "Renderdoel 'html-components' heeft geen geregistreerde renderer",
        ):
            render_renderdoelen(model.objecten, registry)

    def test_weigert_onbekend_renderdoelveld(self):
        bron = BRON.replace(
            '    formaat: "html"',
            '    formaat: "html"\n    renderer: "component-html"',
            1,
        )
        with self.assertRaises(SemantischeFout) as context:
            analyseer(parseer(bron), constraints=WORLD_MODEL_CONSTRAINTS)

        self.assertIn(
            "BP3901",
            [diagnostic.code for diagnostic in context.exception.diagnostics],
        )

    def test_weigert_ontbrekend_formaat(self):
        bron = BRON.replace('    formaat: "html"\n', "", 1)
        with self.assertRaises(SemantischeFout) as context:
            analyseer(parseer(bron), constraints=WORLD_MODEL_CONSTRAINTS)

        self.assertIn(
            "BP3902",
            [diagnostic.code for diagnostic in context.exception.diagnostics],
        )

    def test_weigert_onveilig_artifactpad(self):
        bron = BRON.replace(
            "output/products/components.html",
            "../components.html",
            1,
        )
        with self.assertRaises(SemantischeFout) as context:
            analyseer(parseer(bron), constraints=WORLD_MODEL_CONSTRAINTS)

        self.assertIn(
            "BP3903",
            [diagnostic.code for diagnostic in context.exception.diagnostics],
        )

    def test_weigert_dubbel_artifactpad(self):
        bron = BRON.replace(
            "output/products/components.css",
            "output/products/components.html",
            1,
        )
        with self.assertRaises(SemantischeFout) as context:
            analyseer(parseer(bron), constraints=WORLD_MODEL_CONSTRAINTS)

        self.assertIn(
            "BP3904",
            [diagnostic.code for diagnostic in context.exception.diagnostics],
        )


if __name__ == "__main__":
    unittest.main()

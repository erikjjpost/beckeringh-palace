from __future__ import annotations

import unittest
from compiler.component_css_renderer import naar_component_css
from compiler.component_html_renderer import naar_component_html
from compiler.parser import parseer
from compiler.product_constraints import WORLD_MODEL_CONSTRAINTS
from compiler.semantic import SemantischeFout, analyseer


BRON = '''
appearance forge-panel-appearance {
    naam: "Forge Panel Appearance"
    doel: "Verhoogd paneelprofiel."
    material: "raised"
    foreground: "foreground"
    accent: "accent"
    border: "regular"
    radius: "medium"
    shadow: "medium"
    motion: "normal"
    spacing: "small"
    heading-style: "heading"
    body-style: "body"
    label-style: "label"
    caption-style: "caption"
}

component forge-panel {
    naam: "Forge Panel"
    doel: "Basispaneel."
    appearance: "forge-panel-appearance"
}
'''


class ComponentSliceTests(unittest.TestCase):
    def test_compileert_component_via_semantisch_appearance_contract(self):
        model = analyseer(parseer(BRON), constraints=WORLD_MODEL_CONSTRAINTS)
        css = naar_component_css(model.objecten)
        self.assertIn("background-color: var(--bp-material-raised);", css)
        self.assertIn("color: var(--bp-material-foreground);", css)
        self.assertIn(
            "border: var(--bp-border-regular) var(--bp-border-style) var(--bp-material-accent);",
            css,
        )
        self.assertIn("border-radius: var(--bp-radius-medium);", css)
        self.assertIn("box-shadow: var(--bp-shadow-medium);", css)
        self.assertIn("transition-duration: var(--bp-motion-normal);", css)
        self.assertIn("padding: var(--bp-spacing-small);", css)
        self.assertIn("font-family: var(--bp-font-heading);", css)
        self.assertIn("font-size: var(--bp-type-heading);", css)
        self.assertIn("font-size: var(--bp-type-body);", css)
        self.assertIn("font-size: var(--bp-type-label);", css)
        self.assertIn("font-size: var(--bp-type-caption);", css)
        html = naar_component_html(model.objecten)
        self.assertIn('class="bp-forge-panel"', html)

    def test_weigert_direct_visueel_componentveld(self):
        bron = BRON.replace(
            '    appearance: "forge-panel-appearance"',
            '    appearance: "forge-panel-appearance"\n    surface: "raised"',
        )
        with self.assertRaises(SemantischeFout) as context:
            analyseer(parseer(bron), constraints=WORLD_MODEL_CONSTRAINTS)
        self.assertIn("BP3201", {item.code for item in context.exception.diagnostics})

    def test_weigert_onvolledig_appearance_contract(self):
        bron = BRON.replace('    caption-style: "caption"\n', '')
        with self.assertRaises(SemantischeFout) as context:
            analyseer(parseer(bron), constraints=WORLD_MODEL_CONSTRAINTS)
        self.assertIn("BP3212", {item.code for item in context.exception.diagnostics})

    def test_weigert_onbekende_semantische_rol(self):
        bron = BRON.replace('    heading-style: "heading"', '    heading-style: "enorm"')
        with self.assertRaises(SemantischeFout) as context:
            analyseer(parseer(bron), constraints=WORLD_MODEL_CONSTRAINTS)
        self.assertIn("BP3211", {item.code for item in context.exception.diagnostics})

    def test_component_vereist_bestaande_appearance(self):
        bron = BRON.replace('appearance: "forge-panel-appearance"', 'appearance: "missing"')
        with self.assertRaises(SemantischeFout) as context:
            analyseer(parseer(bron), constraints=WORLD_MODEL_CONSTRAINTS)
        self.assertIn("BP3205", {item.code for item in context.exception.diagnostics})


if __name__ == "__main__":
    unittest.main()

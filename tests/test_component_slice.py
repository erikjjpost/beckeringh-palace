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

VARIANT = BRON + '''
appearance forge-panel-compact-appearance {
    naam: "Compact Forge Panel Appearance"
    doel: "Compact paneelprofiel."
    material: "surface"
    foreground: "foreground"
    accent: "accent"
    border: "hairline"
    radius: "small"
    shadow: "low"
    motion: "fast"
    spacing: "xs"
    heading-style: "title"
    body-style: "body"
    label-style: "label"
    caption-style: "caption"
}

variant forge-panel-compact {
    naam: "Compact Forge Panel"
    doel: "Past het compacte profiel toe."
    component: "forge-panel"
    appearance: "forge-panel-compact-appearance"
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

    def test_genereert_variantappearance_onder_explicitiete_selector(self):
        model = analyseer(parseer(VARIANT), constraints=WORLD_MODEL_CONSTRAINTS)
        css = naar_component_css(model.objecten)
        selector = ".bp-forge-panel.bp-variant-forge-panel-compact"

        self.assertIn(f"{selector} {{", css)
        self.assertIn("background-color: var(--bp-material-surface);", css)
        self.assertIn("padding: var(--bp-spacing-xs);", css)
        self.assertIn(f"{selector} h1, {selector} h2", css)
        self.assertLess(css.index(".bp-forge-panel {"), css.index(selector))

    def test_toont_basiscomponent_en_variant_in_componentcatalogus(self):
        model = analyseer(parseer(VARIANT), constraints=WORLD_MODEL_CONSTRAINTS)
        html = naar_component_html(model.objecten)

        self.assertEqual(2, html.count('data-component="forge-panel"'))
        self.assertIn(
            'class="bp-forge-panel bp-variant-forge-panel-compact" '
            'data-component="forge-panel" '
            'data-variant="forge-panel-compact" '
            'data-appearance="forge-panel-compact-appearance"',
            html,
        )
        self.assertIn("<h2>Compact Forge Panel</h2>", html)
        self.assertIn("<p>Past het compacte profiel toe.</p>", html)

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

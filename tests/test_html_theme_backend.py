from __future__ import annotations

import unittest

from compiler.parser import parseer
from compiler.product_backends import standaard_backend_registry
from compiler.product_compiler import compileer_producten
from compiler.product_constraints import WORLD_MODEL_CONSTRAINTS
from compiler.semantic import analyseer


BRON = '''
kleur ember-orange {
    naam: "Ember Orange"
    doel: "Accentkleur."
    waarde: "#D86A35"
}
kleur iron-black {
    naam: "Iron Black"
    doel: "Achtergrondkleur."
    waarde: "#171A1F"
}
kleur smoke-white {
    naam: "Smoke White"
    doel: "Voorgrondkleur."
    waarde: "#ECECEC"
}
palet ember-forge {
    naam: "Ember Forge"
    doel: "Forge-palet."
    primary: "ember-orange"
    background: "iron-black"
    surface: "iron-black"
    foreground: "smoke-white"
    accent: "ember-orange"
}
typografie forge-interface {
    naam: "Forge Interface"
    doel: "Forge-typografie."
    heading: "Aptos Display"
    body: "Aptos"
    mono: "JetBrains Mono"
}
materiaal forge-materials {
    naam: "Forge Materials"
    doel: "Forge-materialen."
    canvas: "iron-black"
    surface: "iron-black"
    raised: "iron-black"
    foreground: "smoke-white"
    accent: "ember-orange"
}
border forge-borders {
    naam: "Forge Borders"
    doel: "Forge-borders."
    hairline: "1px"
    regular: "2px"
    strong: "3px"
    style: "solid"
}
radius forge-radius {
    naam: "Forge Radius"
    doel: "Forge-radius."
    small: "4px"
    medium: "12px"
    large: "24px"
    pill: "999px"
}
shadow forge-shadows {
    naam: "Forge Shadows"
    doel: "Forge-schaduwen."
    low: "0 2px 8px #00000040"
    medium: "0 8px 24px #00000059"
    high: "0 20px 48px #00000073"
}
motion forge-motion {
    naam: "Forge Motion"
    doel: "Forge-motion."
    fast: "120ms"
    normal: "220ms"
    slow: "420ms"
    easing: "cubic-bezier(0.2, 0.8, 0.2, 1)"
}
thema forge {
    naam: "Forge"
    doel: "Forge-identiteit."
    palet: "ember-forge"
    typografie: "forge-interface"
    materiaal: "forge-materials"
    border: "forge-borders"
    radius: "forge-radius"
    shadow: "forge-shadows"
    motion: "forge-motion"
}
wereld beckeringh-palace {
    naam: "Beckeringh Palace"
    doel: "Ontwerpwereld."
    thema: "forge"
}
token color-iron {
    naam: "Iron"
    doel: "Oppervlak."
    type: "color"
    waarde: "#171A1F"
}
token color-smoke {
    naam: "Smoke"
    doel: "Voorgrond."
    type: "color"
    waarde: "#ECECEC"
}
token color-ember {
    naam: "Ember"
    doel: "Accent."
    type: "color"
    waarde: "#D86A35"
}
token spacing-unit {
    naam: "Spacing"
    doel: "Spacing."
    type: "dimension"
    waarde: "8px"
}
token radius-medium {
    naam: "Radius"
    doel: "Radius."
    type: "dimension"
    waarde: "12px"
}
component forge-panel {
    naam: "Forge Panel"
    doel: "Paneel."
    surface: "{color-iron}"
    foreground: "{color-smoke}"
    accent: "{color-ember}"
    padding: "{spacing-unit}"
    radius: "{radius-medium}"
}
compositie forge-dashboard {
    naam: "Forge Dashboard"
    doel: "Dashboard."
    instanties: ["forge-dashboard-panel"]
}
componentinstantie forge-dashboard-panel {
    naam: "Forge Dashboard Panel"
    doel: "Benoemd paneel."
    compositie: "forge-dashboard"
    component: "forge-panel"
}
layout forge-dashboard-ultrawide {
    naam: "Forge Dashboard Ultrawide"
    doel: "Canvas."
    type: "grid"
    regions: ["forge-dashboard-left"]
    columns: "1"
    rows: "1"
}
region forge-dashboard-left {
    naam: "Linkerpaneel"
    doel: "Regio."
    layout: "forge-dashboard-ultrawide"
    component: "forge-panel"
    column: "1"
    row: "1"
    column-span: "1"
    row-span: "1"
}
product forge-dashboard-html {
    naam: "Forge Dashboard HTML"
    doel: "HTML-product."
    backend: "html"
    wereld: "beckeringh-palace"
    layout: "forge-dashboard-ultrawide"
    pad: "output/products/forge-dashboard.html"
}
'''


class HtmlThemeBackendTests(unittest.TestCase):
    def test_render_resolved_theme_als_css_en_metadata(self):
        model = analyseer(parseer(BRON), constraints=WORLD_MODEL_CONSTRAINTS)
        product = compileer_producten(model.objecten, standaard_backend_registry())[0]

        self.assertIn('--bp-theme-primary: #D86A35;', product.inhoud)
        self.assertIn('--bp-theme-background: #171A1F;', product.inhoud)
        self.assertIn('--bp-theme-foreground: #ECECEC;', product.inhoud)
        self.assertIn('--bp-font-heading: "Aptos Display";', product.inhoud)
        self.assertIn('--bp-font-body: "Aptos";', product.inhoud)
        self.assertIn('--bp-font-mono: "JetBrains Mono";', product.inhoud)
        self.assertIn('--bp-material-canvas: #171A1F;', product.inhoud)
        self.assertIn('--bp-material-accent: #D86A35;', product.inhoud)
        self.assertIn('--bp-border-hairline: 1px;', product.inhoud)
        self.assertIn('--bp-border-style: solid;', product.inhoud)
        self.assertIn('--bp-radius-medium: 12px;', product.inhoud)
        self.assertIn('--bp-shadow-low: 0 2px 8px #00000040;', product.inhoud)
        self.assertIn('--bp-motion-normal: 220ms;', product.inhoud)
        self.assertIn('--bp-motion-easing: cubic-bezier(0.2, 0.8, 0.2, 1);', product.inhoud)
        self.assertIn('background: var(--bp-material-raised);', product.inhoud)
        self.assertIn('border-radius: var(--bp-radius-medium);', product.inhoud)
        self.assertIn('data-world="beckeringh-palace"', product.inhoud)
        self.assertIn('data-theme="forge"', product.inhoud)


if __name__ == "__main__":
    unittest.main()

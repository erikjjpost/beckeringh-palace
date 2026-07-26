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
thema forge {
    naam: "Forge"
    doel: "Forge-identiteit."
    palet: "ember-forge"
    typografie: "forge-interface"
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
    componenten: ["forge-panel"]
    richting: "row"
}
layout forge-dashboard-ultrawide {
    naam: "Forge Dashboard Ultrawide"
    doel: "Canvas."
    compositie: "forge-dashboard"
    canvas-width: "3840"
    canvas-height: "1080"
}
regio forge-dashboard-left {
    naam: "Linkerpaneel"
    doel: "Regio."
    layout: "forge-dashboard-ultrawide"
    component: "forge-panel"
    x: "80"
    y: "120"
    width: "1120"
    height: "840"
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
        self.assertIn('data-world="beckeringh-palace"', product.inhoud)
        self.assertIn('data-theme="forge"', product.inhoud)


if __name__ == "__main__":
    unittest.main()

"""HTML-backendplugin voor ruimtelijke, theme-driven producten."""
from __future__ import annotations

from collections.abc import Iterable

from compiler.backend import Backend
from compiler.cir import Architectuurobject
from compiler.product_model import ProductDefinition
from compiler.spatial_html_renderer import naar_spatial_html


def _css_string(waarde: str) -> str:
    return '"' + waarde.replace('\\', '\\\\').replace('"', '\\"') + '"'


def _theme_css(product: ProductDefinition) -> str:
    thema = product.thema
    if thema is None:
        return ""

    regels = ["    :root {"]
    for rol, kleur in thema.palet.kleuren:
        regels.append(f"      --bp-theme-{rol}: {kleur.waarde};")
    regels.extend([
        f"      --bp-font-heading: {_css_string(thema.typografie.heading)};",
        f"      --bp-font-body: {_css_string(thema.typografie.body)};",
        f"      --bp-font-mono: {_css_string(thema.typografie.mono)};",
        "    }",
        "    body {",
        "      margin: 0;",
        "      background: var(--bp-theme-background);",
        "      color: var(--bp-theme-foreground);",
        "      font-family: var(--bp-font-body);",
        "    }",
        "    h1, h2, h3, h4, h5, h6 { font-family: var(--bp-font-heading); }",
        "    code, pre, kbd, samp { font-family: var(--bp-font-mono); }",
    ])
    return "\n".join(regels) + "\n"


def _render(
    objecten: Iterable[Architectuurobject],
    product: ProductDefinition,
) -> str:
    inhoud = naar_spatial_html(objecten, layout_id=product.layout, titel=product.naam)
    if product.thema is None:
        return inhoud

    thema = product.thema
    inhoud = inhoud.replace("  <style>\n", "  <style>\n" + _theme_css(product), 1)
    inhoud = inhoud.replace(
        "<body>",
        f'<body data-world="{thema.wereld_id}" data-theme="{thema.thema_id}">',
        1,
    )
    return inhoud


backend = Backend("html", _render)

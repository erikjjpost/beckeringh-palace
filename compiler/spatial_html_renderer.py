"""HTML-backend die uitsluitend het Spatial Model consumeert."""
from __future__ import annotations

import html
import re
from collections.abc import Iterable

from compiler.cir import Architectuurobject
from compiler.spatial_model import bouw_spatial_model


def _css_naam(identifier: str) -> str:
    naam = re.sub(r"[^a-zA-Z0-9_-]+", "-", identifier).strip("-").lower()
    return naam or "object"


def naar_spatial_html(objecten: Iterable[Architectuurobject]) -> str:
    regels = [
        "<!doctype html>",
        '<html lang="nl">',
        "<head>",
        '  <meta charset="utf-8">',
        "  <title>Beckeringh Palace spatial products</title>",
        '  <link rel="stylesheet" href="tokens.css">',
        '  <link rel="stylesheet" href="components.css">',
        "  <style>",
        "    .bp-canvas { position: relative; overflow: hidden; }",
        "    .bp-region { position: absolute; box-sizing: border-box; }",
        "  </style>",
        "</head>",
        "<body>",
    ]
    for layout in bouw_spatial_model(objecten):
        regels.append(
            f'  <main class="bp-canvas bp-layout-{_css_naam(layout.id)}" '
            f'style="width:{layout.canvas_width}px;height:{layout.canvas_height}px" '
            f'data-composition="{html.escape(layout.compositie)}">'
        )
        regels.append(f"    <h1>{html.escape(layout.naam)}</h1>")
        for region in layout.regions:
            regels.append(
                f'    <section class="bp-region bp-{_css_naam(region.component)}" '
                f'data-region="{html.escape(region.id)}" '
                f'style="left:{region.x}px;top:{region.y}px;width:{region.width}px;height:{region.height}px">'
            )
            regels.append(f"      <h2>{html.escape(region.naam)}</h2>")
            regels.append("    </section>")
        regels.append("  </main>")
    regels.extend(["</body>", "</html>", ""])
    return "\n".join(regels)

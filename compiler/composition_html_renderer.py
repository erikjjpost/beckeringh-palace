"""HTML-renderer voor Beckeringh Palace-composities."""
from __future__ import annotations

import html
import re
from collections.abc import Iterable

from compiler.cir import Architectuurobject
from compiler.design_compositions import verzamel_composities


def _css_naam(identifier: str) -> str:
    naam = re.sub(r"[^a-zA-Z0-9_-]+", "-", identifier).strip("-").lower()
    return naam or "composition"


def naar_compositie_html(objecten: Iterable[Architectuurobject]) -> str:
    regels = [
        "<!doctype html>",
        '<html lang="nl">',
        "<head>",
        '  <meta charset="utf-8">',
        "  <title>Beckeringh Palace composities</title>",
        '  <link rel="stylesheet" href="tokens.css">',
        '  <link rel="stylesheet" href="components.css">',
        '  <link rel="stylesheet" href="compositions.css">',
        "</head>",
        "<body>",
    ]
    for compositie in verzamel_composities(objecten):
        regels.append(
            f'  <main class="bp-composition bp-{_css_naam(compositie.id)}" '
            f'data-direction="{html.escape(compositie.richting)}">'
        )
        regels.append(f"    <h1>{html.escape(compositie.naam)}</h1>")
        regels.append(f"    <p>{html.escape(compositie.doel)}</p>")
        for component_id in compositie.componenten:
            regels.append(
                f'    <section class="bp-{_css_naam(component_id)}" '
                f'data-component="{html.escape(component_id)}"></section>'
            )
        regels.append("  </main>")
    regels.extend(["</body>", "</html>", ""])
    return "\n".join(regels)
